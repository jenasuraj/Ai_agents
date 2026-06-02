from prompts import system_prompt
from pydantic import BaseModel, Field
from typing import Annotated, List, Dict
from typing_extensions import TypedDict
from dotenv import load_dotenv
load_dotenv()
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain.tools import tool


llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    model="mistralai/mistral-small-2603",
)

class AgentSchema(BaseModel):
    plan: str = Field(description="prepare a full plan like a paragraph written in plain english")
    routes: List[str] = Field(description="add name of the agents , as its a list put list of strings i.e [agent1,agen2 ... agentn]")
     

class State(TypedDict, total=False):
    messages: Annotated[list, add_messages]
    plan: str
    final_answer: str
    agents: List[str]
    agents_response: Dict[str, str]
    active_agent: str



@tool
def weather_tool(input: str) -> str:
    """Use this tool to fetch weather related information."""
    return f"weather in {input} is 25 degree celsius"

tools = [weather_tool]
llm_with_tools = llm.bind_tools(tools)


def get_user_question(state: State) -> str:
    for message in state["messages"]:
        if isinstance(message, dict) and message.get("role") == "user":
            return message["content"]
        if isinstance(message, HumanMessage):
            return message.content

    message = state["messages"][0]
    if isinstance(message, dict):
        return message["content"]
    return message.content


def call_agent(agent_name: str, system_prompt: str, state: State) -> Dict:
    prev = dict(state.get("agents_response", {}))
    response = llm_with_tools.invoke([
        SystemMessage(
            content=(
                f"{system_prompt}\n\n"
                "You have access to tools. Use them when they are helpful or needed. "
                "If a tool result is already present in the conversation, use it to produce your answer."
            )
        ),
        *state["messages"],
        HumanMessage(
            content=(
                f"User question:\n{get_user_question(state)}\n\n"
                f"Supervisor plan:\n{state.get('plan', '')}\n\n"
                f"Previous agent responses:\n{prev}"
            )
        ),
    ])

    update = {
        "messages": [response],
        "active_agent": agent_name,
    }

    if not getattr(response, "tool_calls", None):
        prev[agent_name] = response.content
        update["agents_response"] = prev

    return update


def supervisor(state:State):
    response = llm.with_structured_output(AgentSchema).invoke([{"role":"user","content":get_user_question(state)},
    {"role":"system","content":system_prompt.format()},
    ])
    valid_agents = ["coding", "research", "weather"]
    routes = [agent for agent in response.routes if agent in valid_agents]
    return {
        "agents": routes,
        "plan": response.plan,
        "agents_response": {}
    }



def coding(state:State):
    print("coding called...")
    return call_agent(
        "coding",
        "You are a coding agent. Help with programming, debugging, architecture, and code explanations. "
        "Return practical, correct, concise technical output.",
        state,
    )


def research(state:State):
    print("research called...")
    return call_agent(
        "research",
        "You are a research agent. Gather and organize useful information for the user's question. "
        "If live/current data is required and no tool output is available, clearly say what cannot be verified.",
        state,
    )


def weather(state:State):
    print("weather called...")
    return call_agent(
        "weather",
        "You are a weather agent. Answer weather-related questions. "
        "If the user did not provide a location, ask for the location. "
        "If live weather data is needed and no weather API/tool result is available, explain that live weather data is not connected yet.",
        state,
    )


def synthesizer(state:State):
    print("synthesizer called...")
    response = llm.invoke([
        {
            "role": "system",
            "content": (
                "You are the final response synthesizer. Create one helpful final answer for the user "
                "using the supervisor plan and all available worker responses. Do not mention internal routing "
                "unless it is necessary to explain a limitation."
            ),
        },
        {
            "role": "user",
            "content": (
                f"User question:\n{get_user_question(state)}\n\n"
                f"Supervisor plan:\n{state.get('plan', '')}\n\n"
                f"Worker responses:\n{state.get('agents_response', {})}"
            ),
        },
    ])
    return {"final_answer": response.content}


def routing(state:State):
    completed_agents = set(state.get("agents_response", {}).keys())
    for agent in state.get("agents", []):
        if agent not in completed_agents:
            return agent
    return "synthesizer"


def tool_routing(state: State):
    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tool"

    return routing(state)


def route_after_tool(state: State):
    return state.get("active_agent", "synthesizer")


graph = StateGraph(State)
graph.add_node("supervisor",supervisor)
graph.add_node("coding",coding)
graph.add_node("research",research)
graph.add_node("weather",weather)
graph.add_node("synthesizer",synthesizer)
graph.add_node("tool", ToolNode(tools))

graph.add_edge(START,"supervisor")
graph.add_conditional_edges("supervisor",  routing,["coding","research","weather","synthesizer"])
graph.add_conditional_edges("coding",      tool_routing,["tool","coding","research","weather","synthesizer"])
graph.add_conditional_edges("research",    tool_routing,["tool","coding","research","weather","synthesizer"])
graph.add_conditional_edges("weather",     tool_routing,["tool","coding","research","weather","synthesizer"])
graph.add_conditional_edges("tool",        route_after_tool,["coding","research","weather","synthesizer"])
graph.add_edge("synthesizer",END)


graph_builder = graph.compile()

while True:
    question = input("ENTER :   ")
    response = graph_builder.invoke({"messages":[{"role":"user","content":question}]})
    print("RESPONSE -> ", response.get("final_answer", response))
