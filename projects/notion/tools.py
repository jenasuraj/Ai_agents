from tavily import TavilyClient
from firecrawl import Firecrawl
from langchain.tools import tool
import os


@tool
def tavily(input: str) -> str:
    """
    Fetch current information from the internet.
    Input: Query (e.g., current news, latest events).
    Output: Summarized result from Tavily.
    """
    print("Running tavily tool with input:", input)
    client = TavilyClient(os.getenv("TAVILY_API_KEY"))
    response = client.search(query=input)
    return response


@tool
def contentScrapper(input: str) -> str:
    """
    Scrape content from a web page using Firecrawl.
    Input: A valid URL (e.g., https://en.wikipedia.org/wiki/India).
    Output: Extracted content (up to 1500 characters) in markdown or HTML format.
    """
    print("Running contentScrapper with input:", input)
    firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))
    doc = firecrawl.scrape(input, formats=["markdown", "html"])
    if "markdown" in doc:
        content = doc["markdown"][:1500]
    elif "html" in doc:
        content = doc["html"][:1500]
    else:
        content = str(doc)
    print("Returning scraped content to LangGraph...")
    return content

