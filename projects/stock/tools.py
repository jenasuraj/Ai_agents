from langchain.tools import tool
import requests
from dotenv import load_dotenv
load_dotenv()
import os
from tavily import TavilyClient

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
    
@tool
def Tavily(input:str)->str:
    """Use this tool to extract information from the internet"""
    client = TavilyClient(os.getenv("TAVILY_API_KEY"))
    response = client.search(query=input)
    return response    