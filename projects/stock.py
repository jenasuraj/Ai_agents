import os
import asyncio
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI
load_dotenv()
from langchain.tools import tool
import requests

class State(TypedDict):
    messages: Annotated[list, add_messages]


llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    model="google/gemini-2.5-flash",
    temperature=0.5,
    top_p=0.4,)

client = MultiServerMCPClient(
    {
        "myserver": {
            "url": "http://127.0.0.1:8000/mcp",
            "transport": "streamable_http",
        }
    }
)

@tool
async def vintage(input:str)->str:
    """use this tool to fetch daily stock data, just put the name of the stock registered in the market"""
    print("entered vintage",input)
    try:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={input}&apikey={os.getenv("ALPHAVINTAGE_API_KEY")}'
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        return "error !"


async def main_node(state: State):
    mcptools = await client.get_tools()
    localtools = [vintage]
    tools = mcptools+localtools
    agent = create_agent(model=llm, tools=tools)
    response = await agent.ainvoke({"messages":[{"role":"user","content":state["messages"][-1].content}]})
    print("response is",response["messages"][-1].content)
    return {"messages": [AIMessage(content=response["messages"][-1].content)]}


graph_builder = StateGraph(State)
graph_builder.add_node("main_node", main_node)
graph_builder.add_edge(START,"main_node")
graph_builder.add_edge("main_node",END)
graph = graph_builder.compile()


async def main():
    while True:
        inputQuery = input("Enter stock name : ")
        initial_state = {"messages": [{"role": "user", "content": inputQuery}]}
        response = await graph.ainvoke(initial_state) 
        print(response["messages"][-1].content)
if __name__ == "__main__":
    asyncio.run(main())