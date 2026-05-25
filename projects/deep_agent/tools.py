
from state import State
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
load_dotenv()



tavily_tool = TavilySearchResults(max_results=5, search_depth="advanced")


@tool
def read_plan(state:State):
    """Use this tool to read what plan has been generated for user query"""
    print("read tool is called ...conversation is",state["conversations"])
    return state["conversations"]


@tool
def write_plan(plan: str, status: str,state:State):
    """
    This tool is used to Create, update, or edit a plan.
    ARGS:
       - plan     : new plan content
       - status   : "pending" or "completed"
       - old_plan : existing plan to edit
    """
    if status == "completed":
        state["conversations"][plan] = status
        return f"modified the status of plan {plan} as {status}"
    state["conversations"][plan] = status or "pending"
    return f"added plan in the plan notebook"

