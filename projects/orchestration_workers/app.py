#  First, we create an orchestrator node whose job is to understand the user query and break it into independent subtasks.
#  The orchestrator returns an array of plan objects. Each object represents one independent task, like frontend design, backend design, database design, testing strategy, etc.
#  Then we use LangGraph's Send API. Send allows us to dynamically call the same worker node multiple times, but each call gets its own isolated state.
#  So we loop over the plan array and for every task we return:
#  Send("worker", { task: task })
#  This means LangGraph will create multiple worker executions at runtime.
#  Each worker receives only its own task, processes it independently, and returns its result.
#  All worker results are merged into the main state using a reducer like operator.add.
#  Finally, the synthesizer node takes all worker outputs and combines them into one final response.



from pydantic import BaseModel, Field
from typing import Annotated
from typing_extensions import TypedDict
import operator
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
load_dotenv()



llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    model="mistralai/mistral-small-2603",)



class TaskItem(BaseModel):
    description: str = Field(description="Clear subtask description")
    required_skills: list[str] = Field(description="Required skills")
    context: str = Field(description="Context needed for this task")


class PlanState(BaseModel):
    plan: str = Field(description="High level execution plan")
    tasks: list[TaskItem] = Field(description="Independent subtasks")


class State(TypedDict):
    query: str
    plan: dict
    worker_outputs: Annotated[list[dict], operator.add]
    final_response: str





def main_agent(state: State):
    response = llm.with_structured_output(PlanState).invoke([
        {
            "role": "system",
            "content": """
            You are an orchestrator agent.

            Your job:
            1. Understand the user query
            2. Break it into 2-5 independent subtasks
            3. Each subtask should be executable independently by a worker
            """
        },
        {
            "role": "user",
            "content": state["query"]
        }
    ])
    return {
        "plan": response.model_dump()
    }

def assign_workers(state: State):
    tasks = state["plan"]["tasks"]
    sends = []
    for i, task in enumerate(tasks):
        send_obj = Send(
            "worker",
            {
                "task": task,
                "worker_id": i + 1,
                "original_query": state["query"]
            }
        )
        sends.append(send_obj)
    return sends

def worker(state: dict):
    task = state["task"]
    worker_id = state["worker_id"]
    response = llm.invoke([
        {
            "role": "system",
            "content": f"""
            You are worker agent {worker_id}.

            Complete ONLY your assigned task.
            Do not think about other tasks.
            """
        },
        {
            "role": "user",
            "content": f"""
            Original Goal:
            {state["original_query"]}

            Your Task:
            {task["description"]}

            Context:
            {task["context"]}

            Required Skills:
            {task["required_skills"]}
            """
        }
    ])
    print(f"\n[WORKER {worker_id}] DONE")
    return {
        "worker_outputs": [
            {
                "worker_id": worker_id,
                "task": task["description"],
                "result": response.content
            }
        ]
    }

def synthesizer(state: State):
    merged_text = ""

    for item in state["worker_outputs"]:
        merged_text += f"""
        Worker {item['worker_id']}
        Task: {item['task']}
        Result:
        {item['result']}

        """
    response = llm.invoke([
        {
            "role": "system",
            "content": """
            You are a synthesizer agent.

            Combine all worker outputs into one final polished response.
            Remove redundancy.
            Keep coherence.
            """
        },
        {
            "role": "user",
            "content": merged_text
        }
    ])

    return {
        "final_response": response.content
    }





graph = StateGraph(State)

graph.add_node("main_agent", main_agent)
graph.add_node("worker", worker)
graph.add_node("synthesizer", synthesizer)
graph.add_edge(START, "main_agent")
graph.add_conditional_edges(
    "main_agent",
    assign_workers,
    ["worker"]
)
graph.add_edge("worker", "synthesizer")
graph.add_edge("synthesizer", END)
app = graph.compile()




while True:
    query = input("\nEnter query: ")
    if query.lower() == "exit":
        break
    result = app.invoke({
        "query": query,
        "plan": {},
        "worker_outputs": [],
        "final_response": ""
    })
    print("\nFINAL RESPONSE:\n")
    print(result["final_response"])