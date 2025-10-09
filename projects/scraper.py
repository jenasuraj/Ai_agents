from firecrawl import Firecrawl
from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient
from langchain_openai import ChatOpenAI
load_dotenv()
import os
import requests
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage, HumanMessage,ToolMessage,SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.prompts import PromptTemplate
memory = InMemorySaver()
from langchain.agents import create_agent
import json

llm = ChatOpenAI(
  api_key=os.getenv("OPENROUTER_API_KEY"),
  base_url=os.getenv("OPENROUTER_BASE_URL"),
  model="google/gemini-2.5-flash",
  temperature=0.1)

class State(TypedDict):
    messages:Annotated[list,add_messages]


@tool
def contentScrapper(input:str)->str:
    """use this tool to scrap the web content and to fetch extra information from internet,
    But in order to use this tool, you need to provide a url as input, i.e provide url as input and take structured output""" 
    print("we are in firecrawl tool and input is",input)
    firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))  
    doc = firecrawl.scrape(input, formats=["markdown", "html"]) 
    return doc


@tool
def urlExtractor(input:str)->str:
    """Use this tool to extract url from the internet"""
    print("we are in tavily tool and input is",input)
    client = TavilyClient(os.getenv("TAVILY_API_KEY"))
    response = client.search(query=input)
    return response


@tool
def news(input:str)->str:
    """use this tool to fetch news information like news regarding tesla/apple/hollywood etc so provide as a single word input for ex:tesla"""
    print("news tool called...")   
    try:
        response = requests.get(f'https://newsapi.org/v2/everything?q={input}&from=2025-09-03&to=2025-09-03&sortBy=popularity&apiKey={os.getenv("NEWS_API_KEY")}').json()
        if not response["articles"]:
            return "server error"
        else:
            return response["articles"][:5]
    except Exception as e:
        return "could not load the data error..."    


tools = [news,urlExtractor,contentScrapper]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)

def agent_func(state:State):
    system_prompt = SystemMessage(
        "You are a helpful AI assistant, please respond to the users query to the best of your ability!")
    response = llm_with_tools.invoke([system_prompt] + state["messages"], config)
    return {"messages": [response]}


def routing(state:State):
    last = state["messages"][-1]
    print("last is",last)
    if last.additional_kwargs.get("tool_calls",None):
        print("yes")
        return "yes"
    else:
        print("no")
        return "No"   


def toolCall(state: State):
    outputs = []
    last_msg = state["messages"][-1]
    for tool_call in last_msg.tool_calls:
        tool_name = tool_call["name"]
        args = tool_call["args"]["input"]
        if tool_name == "urlExtractor":
            response = urlExtractor.invoke(args)
        elif tool_name == "contentScrapper":
            response = contentScrapper.invoke(args)
        elif tool_name == "news":
            response = news.invoke(args)
        else:
            response = f"Unknown tool: {tool_name}"
        outputs.append(
            ToolMessage(
                content=str(response),
                tool_call_id=tool_call["id"]
            )
        )
    return {"messages": outputs}



graph_builder = StateGraph(State)
graph_builder.add_node("agent_func",agent_func)
graph_builder.add_node("toolCall",toolCall)
graph_builder.add_edge(START,"agent_func")
graph_builder.add_conditional_edges("agent_func",routing,{"yes":"toolCall","No":END})
graph_builder.add_edge("toolCall","agent_func")
graph = graph_builder.compile(checkpointer=memory)    


while True:
    inputData = input("Enter : ")
    config = {"configurable": {"thread_id": "1"}}
    initial_state = {"messages":HumanMessage(content=inputData)}
    response = graph.invoke(initial_state, config,stream_mode="values")
    print(response["messages"][-1].content)
    
