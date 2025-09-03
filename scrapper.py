from firecrawl import Firecrawl
from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient
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
from langgraph.checkpoint.memory import InMemorySaver
memory = InMemorySaver()


llm = ChatOpenAI(
  api_key=os.getenv("OPENROUTER_API_KEY"),
  base_url=os.getenv("OPENROUTER_BASE_URL"),
  model="google/gemini-2.5-flash",
  temperature=0.5,
  top_p= 0.4,)

class State(TypedDict):
    messages:Annotated[list,add_messages]
    temp:str

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
def weather(input:str)->str:
    """use this tool to fetch weather or temperature related information,provide city name only as input"""
    try:
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={input}&units=metric&appid={os.getenv("OPENWEATHER_API_KEY")}').json()
        if str(response["cod"]) != '200':
            return f"server error"
        extracted_response = response["main"]["temp"]
        return f"current temperature at {input} is {extracted_response}"
    except Exception as e:
          return "couldn't find information, Server error"


prompt = """
Your name is Suraj, a helpful assistant who can provide well detailed information and also real time data,
like stock news, general news and so on.  
Tools available:  
- urlExtractor → fetch URLs for a topic.  
- contentScrapper → scrape detailed info from a URL.  
Use urlExtractor for quick/general info.  
Use contentScrapper when deeper details are needed.  
When necessary, you may call multiple tools 
(e.g., fetch a URL with urlExtractor and then use the url on contentScrapper
if the result isn't relevant or detailed enough).  
"""

def agent_func(state:State):
    tools = [urlExtractor,weather,contentScrapper]
    agent = create_react_agent(tools=tools,model=llm,prompt=prompt)
    response = agent.invoke(state)
    return {"messages":[AIMessage(content=response["messages"][-1].content)]}

graph_builder = StateGraph(State)
graph_builder.add_node("agent_func",agent_func)
graph_builder.add_edge(START,"agent_func")
graph_builder.add_edge("agent_func",END)
graph = graph_builder.compile(checkpointer=memory)    


while True:
    inputData = input("Enter : ")
    config = {"configurable": {"thread_id": "1"}}
    initial_state = {"messages":[{"role":"user","content":inputData}]}
    response = graph.invoke(initial_state, config,stream_mode="values")
    print(response["messages"][-1].content)