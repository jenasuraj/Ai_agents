from pydantic import BaseModel, Field
from typing import Annotated, List, Dict, Any
from typing_extensions import TypedDict
from dotenv import load_dotenv
load_dotenv()
import json
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode
from langchain.tools import tool


@tool
def weather_tool(input: str) -> str:
    """Use this tool to fetch weather related information."""
    return f"weather in {input} is 25 degree celsius"


llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    model="mistralai/mistral-small-2603",
)

memory = InMemorySaver()

tools = [weather_tool]
llm_with_tools = llm.bind_tools(tools)


class DayPlan(BaseModel):
    day: str = Field(description="Day number or range, example: 'Day 1' or 'Day 1-2'")
    place: str = Field(description="Main place/city/location for this day")
    todo: List[str] = Field(description="Things to do on this day")
    food: List[str] = Field(description="Food or restaurant suggestions")
    estimated_cost: int = Field(description="Estimated cost for this day in INR")
    travel_tip: str = Field(description="Useful travel tip for this day")


class FinalOutput(BaseModel):
    user_query: str = Field(description="Original user query")
    destination: str = Field(description="Main travel destination")
    total_days: int = Field(description="Total number of travel days")
    budget: int = Field(description="Approx total budget in INR")
    itinerary: List[DayPlan] = Field(description="Day-wise travel plan")
    tools_used: List[str] = Field(description="List of tools used by the agent")
    warnings: List[str] = Field(description="Important warnings or things to keep in mind")
    ui_summary: str = Field(description="Short frontend-friendly summary")


class State(TypedDict):
    messages: Annotated[list, add_messages]
    plan: str
    final_answer: str
    structured_response: Dict[str, Any]


planner_prompt = """
You are a travel planning agent.

Your job:
1. Understand the user's travel request.
2. Make a short execution plan.
3. Decide whether tools are needed.
4. If weather/location info is needed, mention that weather_tool should be used.

Do not call tools.
Only return the plan.
"""
main_agent_prompt = """
You are a travel execution agent.

You already have a plan.
Follow the plan carefully.
Use tools whenever needed.
After tool results are received, create a useful travel plan.

Your final answer should include:
- destination
- total days
- day-wise itinerary
- places to visit
- food suggestions
- estimated cost
- travel tips
- warnings if any
"""


def planner_node(state: State):
    response = llm.invoke(
        [
            SystemMessage(content=planner_prompt),
            *state["messages"],
        ]
    )
    return {
        "plan": response.content
    }

def main_agent(state: State):
    response = llm_with_tools.invoke(
        [
            SystemMessage(
                content=f"""
                {main_agent_prompt}

                Current plan:
                {state["plan"]}
                """
            ),
            *state["messages"],
        ]
    )

    return {
        "messages": [response]
    }

def routing(state: State):
    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tool"

    return "final_formatter"


structured_llm = llm.with_structured_output(FinalOutput)
def final_formatter_node(state: State):
    user_query = state["messages"][0].content
    final_answer = state["messages"][-1].content

    tool_names = []

    for msg in state["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tool_call in msg.tool_calls:
                tool_names.append(tool_call["name"])

    structured = structured_llm.invoke(
        f"""
        Convert this travel planning result into a frontend-friendly JSON structure.

        Follow this schema strictly:

        {{
          "user_query": "...",
          "destination": "...",
          "total_days": 3,
          "budget": 15000,
          "itinerary": [
            {{
              "day": "Day 1",
              "place": "...",
              "todo": ["...", "..."],
              "food": ["...", "..."],
              "estimated_cost": 3000,
              "travel_tip": "..."
            }}
          ],
          "tools_used": ["..."],
          "warnings": ["...", "..."],
          "ui_summary": "..."
        }}

        Important:
        - itinerary must be an array of day-wise objects.
        - day can be "Day 1" or "Day 1-2".
        - todo must be a list of strings.
        - food must be a list of strings.
        - estimated_cost must be an integer in INR.
        - budget must be an integer in INR.
        - Do not return markdown.
        - Do not return normal text.
        - Follow the Pydantic schema strictly.

        User query:
        {user_query}

        Plan:
        {state["plan"]}

        Final answer:
        {final_answer}

        Tools used:
        {tool_names}
        """
    )
    return {
        "final_answer": final_answer,
        "structured_response": structured.model_dump()
    }


graph_builder = StateGraph(State)
graph_builder.add_node("planner_node", planner_node)
graph_builder.add_node("main_agent", main_agent)
graph_builder.add_node("tool_node", ToolNode(tools))
graph_builder.add_node("final_formatter", final_formatter_node)
graph_builder.add_edge(START, "planner_node")
graph_builder.add_edge("planner_node", "main_agent")
graph_builder.add_conditional_edges(
    "main_agent",
    routing,
    {
        "tool": "tool_node",
        "final_formatter": "final_formatter"
    }
)
graph_builder.add_edge("tool_node", "main_agent")
graph_builder.add_edge("final_formatter", END)
graph = graph_builder.compile(checkpointer=memory)


while True:
    inputData = input("Enter : ")
    config = {"configurable": {"thread_id": "1"}}
    initial_state = {
        "messages": [HumanMessage(content=inputData)]}
    response = graph.invoke(initial_state, config)
    print("\nStructured Output:")
    print(json.dumps(response["structured_response"], indent=2))