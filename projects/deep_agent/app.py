from dotenv import load_dotenv
load_dotenv()
import os
from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from rag.prompts import system_prompt


memory = InMemorySaver()
llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    model="anthropic/claude-3.5-sonnet",
)
class State(TypedDict):
    messages: Annotated[list, add_messages]
    plan: str



tavily_tool = TavilySearchResults(max_results=5, search_depth="advanced")


conversations = {}

@tool
def read_plan():
    """Use this tool to read what plan has been generated for user query"""
    print("read tool is called ...conversation is",conversations)
    return conversations


@tool
def write_plan(plan: str, status: str):
    """
    This tool is used to Create, update, or edit a plan.
    ARGS:
       - plan     : new plan content
       - status   : "pending" or "completed"
       - old_plan : existing plan to edit
    """
    print("write plan is called ...")
    print("plan is",plan ,"status is",status)
    print("conversation is", conversations)
    print("\n\n")

    if status == "completed":
        conversations[plan] = status
        return f"modified the status of plan {plan} as {status}"
    conversations[plan] = status or "pending"
    return f"added plan in the plan notebook"


        


tools = [tavily_tool, read_plan,write_plan]
llm_with_tools = llm.bind_tools(tools)




def agent_node(state: State):
    system_prompt = system_prompt
    res = llm_with_tools.invoke(
        [SystemMessage(content=system_prompt)] + state["messages"]
    )
    return {"messages": [res]}



def routing(state: State):
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tool"
    return END


graph_builder = StateGraph(State)
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("tool", ToolNode(tools))
graph_builder.add_edge(START, "agent")
graph_builder.add_conditional_edges(
    "agent",
    routing,
    {
        "tool": "tool",
        END: END
    }
)
graph_builder.add_edge("tool", "agent")
graph = graph_builder.compile(checkpointer=memory)



while True:
    user_input = input("\nEnter: ")
    config = {"configurable": {"thread_id": "1"}, "recursion_limit": 50}
    state = {
        "messages": [HumanMessage(content=user_input)]
    }
    final = None
    for event in graph.stream(state, config, stream_mode="values"):
        if "messages" in event:
            msg = event["messages"][-1]
            if isinstance(msg, AIMessage) and msg.content:
                final = msg.content
    print("\nAnswer:\n")
    print(final)