from mcp.server.fastmcp import FastMCP
import requests
from dotenv import load_dotenv
load_dotenv()
import os
import json
from firecrawl import Firecrawl
from notion_client import Client
import requests
mcp = FastMCP("notion_server")
notion = Client(auth=os.getenv("NOTION_TOKEN_NO")) 



@mcp.tool()
def content_extractor(input: str):
    """Extract  content from a Notion block using its block ID."""
    print("in content extractor...",input)
    def retrieve_notion_block(block_id, notion_token):
        url = f"https://api.notion.com/v1/blocks/{block_id}/children"
        headers = {
            "Authorization": f"Bearer {notion_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None

    def extract_text_from_block(block):
        block_type = block.get("type")
        if block_type == "paragraph":
            return "".join([t["text"]["content"] for t in block["paragraph"]["rich_text"]])
        elif block_type in ["heading_1", "heading_2", "heading_3"]:
            return "".join([t["text"]["content"] for t in block[block_type]["rich_text"]])
        elif block_type in ["bulleted_list_item", "numbered_list_item"]:
            return "".join([t["text"]["content"] for t in block[block_type]["rich_text"]])
        return ""

    block_data = retrieve_notion_block(input, os.getenv("NOTION_TOKEN_NO"))
    if not block_data:
        return []
    contents = []
    for block in block_data.get("results", []):
        text = extract_text_from_block(block)
        if text:
            contents.append(text)
    return contents





@mcp.tool()
def id_extractor(input: str) -> str:
    """
    Extract the block IDs of Notion Blocks. 
    Input: Name of the Notion page (or partial name). 
    Output: Dictionary mapping page titles to their block IDs.
    """
    print("Running idExtractor with input:", input)
    notion = Client(auth=os.getenv("NOTION_TOKEN_NO"))
    page_dict = {}
    response = notion.search(filter={"property": "object", "value": "page"})
    for page in response["results"]:
        title = "Untitled"
        if "title" in page["properties"]:
            title_parts = page["properties"]["title"]["title"]
            if title_parts:
                title = title_parts[0]["plain_text"]
        page_dict[title] = page["id"]
    return f"Block IDs of Notion pages along with their names: {page_dict}"





@mcp.tool()
def insert_content(input: str,content):
    """Use this tool to insert content/data in your blocks/pages in notion database, so for that provide input as block_id and also provide the content you want to insert"""
    url = f'https://api.notion.com/v1/blocks/{input}/children'
    headers = {
        "Authorization": f"Bearer {os.getenv('NOTION_TOKEN_NO')}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"}
    updated_content = json.loads(content)
    data = {
    "children":updated_content
           }
    
    print("data is", json.dumps(data,indent=4))

    try:
        response = requests.patch(url, headers=headers, json=data)
        print("Status code:", response.status_code)
        print("Response text:", response.text)
        
        if response.ok:
            return "✅ Content inserted successfully."
        else:
            return f"❌ Could not insert content. Status: {response.status_code}\nResponse: {response.text}"
    except Exception as e:
        return f"🚨 Could not make a request to Notion: {e}"
         


if __name__ == "__main__":
    mcp.run(transport="streamable-http")