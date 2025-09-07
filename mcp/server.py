from mcp.server.fastmcp import FastMCP
import requests
mcp = FastMCP("myserver")
from dotenv import load_dotenv
load_dotenv()
import os
import json
from firecrawl import Firecrawl


@mcp.tool()
def news(input:str)->str:
    """use this tool to fetch news information like news regarding tesla/apple/hollywood etc so provide as a single word input for ex:tesla"""
    print("news tool called...",input)   
    try:
        response = requests.get(f'https://newsapi.org/v2/everything?q={input}&sortBy=popularity&apiKey={os.getenv("NEWS_API_KEY")}').json()
        if not response["articles"]:
            return "server error"
        else:
            return response["articles"][:5]
    except Exception as e:
        return "could not load the data error..." 



@mcp.tool()
def weather(input:str)->str:
    """use this tool to fetch weather or temperature related information,provide city name only as input"""
    print("weather tool called...",input)
    try:
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={input}&units=metric&appid={os.getenv("OPENWEATHER_API_KEY")}').json()
        if str(response["cod"]) != '200':
            return f"server error"
        extracted_response = response["main"]["temp"]
        print("temperature is ",extracted_response)
        return f"current temperature at {input} is {extracted_response}"
    except Exception as e:
          return "couldn't find information, Server error"   



@mcp.tool()
def contentScrapper(input: str) -> str:
    """Scrape web content using Firecrawl. Provide a valid URL as input (e.g., https://moneycontrol.com)."""
    print("we are in firecrawl tool and input is", input)
    firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))  
    doc = firecrawl.scrape(input, formats=["markdown", "html"]) 

    # doc looks like: {'markdown': '...', 'html': '...'}
    if "markdown" in doc:
        content = doc["markdown"][:1500]  # trim if very long
    elif "html" in doc:
        content = doc["html"][:1500]
    else:
        content = str(doc)
    print("Returning scraped content to LangGraph...")
    return content



if __name__ == "__main__":
    mcp.run(transport="streamable-http")
    