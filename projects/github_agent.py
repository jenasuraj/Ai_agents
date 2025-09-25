from firecrawl import Firecrawl
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_openai import ChatOpenAI
load_dotenv()
import os
from langgraph.prebuilt import create_react_agent
import requests
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage
from langchain.prompts import PromptTemplate
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from langgraph.checkpoint.memory import InMemorySaver



checkpointer = InMemorySaver()
client = MultiServerMCPClient(
    {
        "myserver": {
            "url": "http://127.0.0.1:8000/mcp",
            "transport": "streamable_http",
        },
        "github_server": {
            "command": "docker",
            "args": [
                "run",
                "-i",
                "--rm",
                "-e",
                "GITHUB_PERSONAL_ACCESS_TOKEN",
                "ghcr.io/github/github-mcp-server",
            ],
            "env": {
                "GITHUB_PERSONAL_ACCESS_TOKEN": f'{os.getenv("GITHUB_ACCESS_TOKEN")}'
            },
            "transport": "stdio",
        },
    }
)

class State(TypedDict):
    messages:Annotated[list,add_messages]

llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    model="google/gemini-2.5-flash",
    temperature=0.5,
    top_p=0.3,)


async def first(state:State):
    prompt = """
    You are a very helpful assistant and your name is suraj !.
    You are capable of using some superpower tools, like manipulating github, and some other tools,
    so whenever user gives you a task, do that with all your heart, and whenever the task deals with github,
    reconfirm to user that, whether you have to do that specific task regarding github because it's risky.
    """
    tools = await client.get_tools()
    agent = create_react_agent(model=llm,tools=tools,prompt=prompt)
    response =await agent.ainvoke({"messages":state["messages"]})
    return{
       "messages":[AIMessage(content=response["messages"][-1].content)]
    }


graph_builder = StateGraph(State)
graph_builder.add_node("first",first)
graph_builder.add_edge(START,"first")
graph_builder.add_edge("first",END)
graph = graph_builder.compile(checkpointer=checkpointer)


async def main():
    while True:
        inputQuery = input("ENTER : ")
        initial_state = {
        "messages":[{"role":"user","content":inputQuery}]
        }
        response =await graph.ainvoke(initial_state,{"configurable": {"thread_id": "1"}},) 
        print(response["messages"][-1].content) 

if __name__ == "__main__":
    asyncio.run(main())