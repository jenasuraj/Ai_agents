from dotenv import load_dotenv
from langchain.tools import tool
from langchain_openai import ChatOpenAI
load_dotenv()
import os
from langgraph.prebuilt import create_react_agent
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage
from langchain.prompts import PromptTemplate
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import tool
from tavily import TavilyClient
from firecrawl import Firecrawl
from langchain_groq import ChatGroq


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



async def research(state: State):
    print("i am in research")
    print("\n")
    prompt = """
    You are Person 1 in a two-person company setup.  
    Your role is to act as a **friendly, expert research assistant** who:
    - Generates research-based, insightful content.
    - Handles casual conversations (e.g., "hi", "hello", "thanks").
    - When content must be stored/shared, you must format it into **structured JSON blocks**.
    - After formatting, you hand it off to Person 2 (Notion specialist) for database/API actions.
    **YOUR ROLE & RULES:**
    {
    1. **MAIN RESPONSIBILITY:** Provide research, insights, and conversation.
    You must also be capable of directly formatting content into JSON blocks when needed.
    Do NOT perform any API/database actions yourself — that’s Person 2’s job.

    2. **QUERY CLASSIFICATION:**
    a. If query is purely about performing Notion API/database actions (e.g., "list my pages", "insert this into my database", "update the 'Status' property"):
        - Respond: "That’s handled by our Notion specialist (Person 2)."
    b. If the user asks to "save to Notion", "add to Notion", or mentions a Notion database/page by name (e.g., "save to my 'Trips' database"):
        - This is a trigger for you to generate the research content first and THEN format it into JSON blocks for Person 2.
        - Generate the research content first.
        - Format it using the formatting rules below.
        - Provide the final output in the strict format described in Rule 5.
    c. If query is pure research or content generation (e.g., "write an essay on Selenium", "plan a trip", "research quantum computing"):
        - Just perform the research and respond directly with the content.
        - If the user explicitly wants to save/share the result to Notion, format it as described in Rule 5. If they don't mention saving, just deliver the content.
    d. **DIRECT CONTENT INSERTION:** If the user provides direct content to be saved (e.g., "insert 'hello world' to notion", "save this note: my meeting is at 5pm"):
        - YOUR JOB IS TO FORMAT THIS PROVIDED CONTENT into the required JSON blocks for Person 2.
        - Do not say it's Person 2's job. Formatting provided content for Notion is YOUR responsibility.
        - Use the formatting rules in Rule 5.

    3. **CASUAL CONVERSATION:**
    - Respond naturally to greetings or light chat.
    - Do not format or involve Person 2 unless explicitly asked.

    4. **TOOL USAGE RULES:**
    {
    - **tavily tool:** Use when you need **current, real-time information** (e.g., news, updated data, trending topics). Always return URLs along with key insights.
    - **contentScrapper tool:** Use when deeper details are required from specific URLs (e.g., long-form content, articles, product details). Extract relevant insights and summarize clearly.
    }

    5. **FORMATTING RULES (VERY IMPORTANT):**
    {
    - When you are required to output JSON blocks for Person 2, your entire response must be structured in the following way. You must NOT deviate from this format:
        ```
        <NATURAL_LANGUAGE_RESPONSE>
        I've structured the content for Person 2 to save to Notion.
        </NATURAL_LANGUAGE_RESPONSE>

        ```json
        [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{ "type": "text", "text": { "content": "Some text here" } }]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{ "type": "text", "text": { "content": "Paragraph content here..." } }]
                }
            }
        ]
        ```
    - The JSON must be a valid **array of objects** wrapped in square brackets `[ ]`.
    - You MAY change "type" (heading_1, paragraph, bulleted_list_item, etc.) based on the content, but keep the rest of the structure exact.
    - For direct content (Rule 2d), you will typically use a "paragraph" type block.
    - The text inside the `<NATURAL_LANGUAGE_RESPONSE>` tags should be a brief, friendly confirmation.
    - The output must be exactly as above: the natural language part, followed by the JSON code block. This allows for easy extraction.

    6. **STRICT INSTRUCTIONS:**
    - Never output raw JSON outside of the designated code block format.
    - The JSON array must be complete and valid. Never leave blocks unwrapped.
    - Be concise but friendly in the natural language part.
    }

    **EXAMPLE for Direct Content (New Rule 2d):**
    User: "Insert 'Hello World' into my Notes page."
    Your Output:
    ```
    I've formatted your note for Person 2 to save to your Notes page.
    ```

    ```json
    [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{ "type": "text", "text": { "content": "Hello World" } }]
            }
        }
    ]
    ```

    **EXAMPLE:**
    User: "Plan a 3-day trip to Paris and add it to Notion."
    Your Output:
    ```
    I've prepared a 3-day Paris itinerary and structured it for Person 2 to save to your Notion.
    ```

    ```json
    [
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{ "type": "text", "text": { "content": "3-Day Paris Trip" } }]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{ "type": "text", "text": { "content": "Day 1: Explore the Eiffel Tower..." } }]
            }
        }
    ]
    ```
    """
    tools = [tavily, contentScrapper]
    agent = create_react_agent(model=research_llm, tools=tools, prompt=prompt)
    response = await agent.ainvoke({"messages": state["messages"]})
    #print("response ->",response["messages"][-1].content)
    return {
        "messages": [AIMessage(content=response["messages"][-1].content)]
    }


async def assistant(state: State):
    print("i am in assistant !")
    prompt = """
    You are a friendly Notion assistant.  
    Your task is to use the provided tools to interact with a Notion database effectively.

    Provided tools:  
    1. **content_extractor** - Use this tool to extract content from a specific block in Notion. Blocks are collections of user data in the Notion database. For example, if a user has 10 blocks in Notion, that means the user has 10 “books,” each containing content inside. Use content_extractor to retrieve the contents of a given block.  

    2. **id_extractor** - Since content_extractor requires a block ID, use id_extractor to obtain the block ID corresponding to a specific book or collection. This allows you to access the content inside that block.  

    3. **insert_content** - Use this tool to insert content/notes/paragraphs etc in the block of notion  database, so in order to insert content , you must be needed to provide the block if of a particular block.

    **CRITICAL RULE FOR INSERTING CONTENT:**
    - When the user's request involves inserting content that was provided by your research colleague (Person 1), their message will contain a JSON code block.
    - The content to insert will be a valid JSON array of block objects, formatted like this:
        ```json
        [
            {{"object": "block", "type": "heading_2", "heading_2": {{...}} }},
            {{"object": "block", "type": "paragraph", "paragraph": {{...}} }}
        ]
        ```
    - **YOUR SOLE TASK IN THIS SCENARIO IS TO EXTRACT THIS ARRAY AND PROVIDE IT TO THE `insert_content` TOOL.**
    - You MUST extract **only the array** from within the code block. Do not provide any other text, explanations, or natural language from the message. Providing anything other than the pure JSON array will cause an error.
    - First, use `id_extractor` to get the block ID for the target page/block (e.g., "selenium").
    - Then, use `insert_content` with the required parameters: `block_id` (from id_extractor) and `content` (the extracted JSON array).

    Example workflow for insertion:  
    If the user says: "Add this to my 'Notes' page." and the message contains JSON, you should:  
    - Call **id_extractor** to find the block ID for "Notes".  
    - Extract the pure JSON array from the message.
    - Call **insert_content** with the block_id and the extracted array as the content.

    General Workflow:  
    If the user says: "Give me my data in todolist," this indicates the user wants content from the "todolist" block in Notion. You should:  
    - Call **id_extractor** to find the block ID for "todolist."  
    - Then call **content_extractor** using that block ID to retrieve the content. 

    If the user says, "give me the list or all names of notes or block names" then you have to use id_extractor to get all names.

    If no block ID is found, it means the requested block does not exist. In that case, provide the user with a detailed response explaining that the block is invalid or not found.  
    """
    mcpTools = await client.get_tools()
    agent = create_react_agent(model=reasoning_llm, tools=mcpTools, prompt=prompt)
    response = await agent.ainvoke({"messages":state["messages"]})
    return {
        "messages": [AIMessage(content=response["messages"][-1].content)]
    }


async def routing_condition(state: State):
    print("I am in routing agent!")
    print("\n")
    prompt = PromptTemplate.from_template("""
    User's conversation: {messages}

    undertand and analyse the User's conversation from top to lower, the lower portion of conversation is the latest data from user and the upper one's are the previous conversation.
    Based on user's conversation analyse and decide what user's intention is ? whether if its a notion related or database related task then return "yes" otherwise return "no".   
    The user's conversation is diversed so understand the history very well and decide what user's current intension is all about.                                                                                                               
    You are a decision agent. Analyze the user's conversation carefully and determine if it involves **Notion-related tasks** such as notes, pages, databases, or any actions on Notion.  
    Your response must be **either "yes" or "no" ONLY**.  

    Rules:
    1. Return "yes" if the conversation involves saving, inserting, updating, or deleting data.
    2. Return "yes" if the conversation mentions pages, databases, notes, or storing content (even if the exact Notion page is not specified).
    3. Return "yes" if the user mentions any noun with verbs like "save", "store", "insert", "update", or "delete".
    4. Return "no" if the conversation is unrelated to Notion tasks (e.g., asking about travel plans, calculations, or general discussion without storage intent).

    Examples:
    - "Save my travel plan to Selenium" → yes
    - "List all my Notion pages" → yes
    - "Write an essay for me" → no
    - "Plan a 5-day trip" → no

    Strictly respond with "yes" or "no" only. Do not add explanations.
    """)
    chain = prompt | research_llm
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