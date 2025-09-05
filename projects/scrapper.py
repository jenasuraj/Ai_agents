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
from langchain.prompts import PromptTemplate
memory = InMemorySaver()



llm = ChatOpenAI(
  api_key=os.getenv("OPENROUTER_API_KEY"),
  base_url=os.getenv("OPENROUTER_BASE_URL"),
  model="google/gemini-2.5-flash",
  temperature=0.5,
  top_p= 0.4,)

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
def weather(input:str)->str:
    """use this tool to fetch weather or temperature related information,provide city name only as input"""
    print("weather tool called...")
    try:
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={input}&units=metric&appid={os.getenv("OPENWEATHER_API_KEY")}').json()
        if str(response["cod"]) != '200':
            return f"server error"
        extracted_response = response["main"]["temp"]
        return f"current temperature at {input} is {extracted_response}"
    except Exception as e:
          return "couldn't find information, Server error"


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



prompt = """
Your name is Suraj, a helpful assistant who can provide well detailed information and also real time data.
After gathering information, your responses will be automatically summarized for conciseness.

Tools available:  
- urlExtractor → fetch URLs and brief content for a topic.  
- contentScrapper → scrape detailed info from a specific URL.  
- Weather -> fetch current temperature for any city.
- News -> Fetch current trending news about companies/products (e.g., tesla, apple).

Usage guidelines:
1. Use urlExtractor for quick overviews and to find relevant URLs
2. Use contentScrapper for deep dives into specific pages
3. Provide detailed information - the summarizer will make it concise
4. Remember: urlExtractor often provides enough content, so only use contentScrapper if you need more details
"""

def agent_func(state:State):
    tools = [urlExtractor,weather,contentScrapper,news]
    agent = create_react_agent(tools=tools,model=llm,prompt=prompt)
    response = agent.invoke(state)
    return {"messages":[AIMessage(content=response["messages"][-1].content)]}


summarising_prompt = PromptTemplate.from_template("""
You are an experienced summariser, so your job is to summarise user's data into tiny understandable words.
You should not summarise too short but summarise the user's data in meaningfull structured way.                                          
But If user's data about greetings / hello etc , you can provide whatever response you want.
user's data:{response}
""")
def summariser(state:State):
    print("in summariser node")
    response = state["messages"][-1].content
    chain = summarising_prompt | llm
    summarised_data = chain.invoke({"response":response})
    return{
        "messages":[AIMessage(content=summarised_data.content)]
    } 


graph_builder = StateGraph(State)
graph_builder.add_node("agent_func",agent_func)
graph_builder.add_node("summariser",summariser)
graph_builder.add_edge(START,"agent_func")
graph_builder.add_edge("agent_func","summariser")
graph_builder.add_edge("summariser",END)
graph = graph_builder.compile(checkpointer=memory)    


while True:
    inputData = input("Enter : ")
    config = {"configurable": {"thread_id": "1"}}
    initial_state = {"messages":[{"role":"user","content":inputData}]}
    response = graph.invoke(initial_state, config,stream_mode="values")
    print(response["messages"][-1].content)