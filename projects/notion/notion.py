from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
load_dotenv()
import os
from langchain.agents import create_agent
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from langgraph.checkpoint.memory import InMemorySaver
from langchain_groq import ChatGroq
from prompts import routing_prompt,research_prompt,assistant_prompt
from tools import tavily,contentScrapper


checkpointer = InMemorySaver()
client = MultiServerMCPClient(
    {
     "notion_server": {
            "url": "http://127.0.0.1:8000/mcp",
            "transport": "streamable_http",
        }
    }
)

class State(TypedDict):
    messages:Annotated[list,add_messages]

research_llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    model="google/gemini-2.5-flash",
    temperature=0.2)
    
fast_llm = ChatGroq(model='meta-llama/llama-4-scout-17b-16e-instruct')

reasoning_llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    model='openai/gpt-4o-mini',
    max_completion_tokens=2000,
    temperature=0.1,)


async def research(state: State):
    print("i am in research")
    print("\n")
    tools = [tavily, contentScrapper]
    agent = create_agent(model=research_llm, tools=tools, prompt=research_prompt)
    response = await agent.ainvoke({"messages": state["messages"]})
    return {
        "messages": [AIMessage(content=response["messages"][-1].content)]
    }


async def assistant(state: State):
    print("i am in assistant !")
    mcpTools = await client.get_tools()
    agent = create_agent(model=reasoning_llm, tools=mcpTools, prompt=assistant_prompt)
    response = await agent.ainvoke({"messages":state["messages"]})
    return {
        "messages": [AIMessage(content=response["messages"][-1].content)]
    }


async def routing_condition(state: State):
    print("I am in routing agent!")
    print("\n")
    chain = routing_prompt | research_llm
    response = await chain.ainvoke({"messages": state["messages"]})
    print(response.content)
    if "no" in response.content.lower():
        return "no"
    elif "yes" in response.content.lower():
        return "yes"



graph_builder = StateGraph(State)
graph_builder.add_node("research",research)
graph_builder.add_node("assistant",assistant)
graph_builder.add_edge(START,"research")
graph_builder.add_conditional_edges("research",routing_condition,{"yes":"assistant","no":END})
graph_builder.add_edge("assistant",END)
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