from firecrawl import Firecrawl
from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient
load_dotenv()
import os
import requests


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
