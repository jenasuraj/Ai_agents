from firecrawl import Firecrawl
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_openai import ChatOpenAI
load_dotenv()
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage
from langchain.prompts import PromptTemplate
from langgraph.checkpoint.memory import InMemorySaver
import os,json
from langgraph.prebuilt import create_react_agent
from tavily import TavilyClient
from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()

class State(TypedDict):
    messages: Annotated[list,add_messages]

llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    model="google/gemini-2.5-flash",
    temperature=0.1)


@tool
def url_search(input:str)->str:
    """use this tool to extract urls from the internet, provide a proper content/tagline as input"""
    print("in url search tool...",input)
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(input)
    return f"response for url fetching from 'url_search' is {response}"


@tool
def content_scrapper(input:str)->str:
    """Use this tool to extract content from websites, provide input as proper url format ex input: https://firecrawl.dev """
    print("in content scrapper",input)
    firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))
    doc = firecrawl.scrape(input, formats=["markdown"])
    return doc


def planner(state:State):
    print("in first node...")
    prompt = PromptTemplate.from_template("""
    **User's Question**: {messages}.",                                      
    **Role and introduction** - [                                                                           
    "You are working in a company of size 3 member and you are a thought building member.",
    "Your job is one of the most important, because you will provide thought process to user's question.",                                      
    "And as per your thought writing, other 2 members will act further. So understand the user's question and provide a deepful thought."]
    
    **Rules and steps to build thought** - [
    "You have to analyse what user's intention is ?",
    "you should start your thought exactly how a real thinker does.",
    "You are not only able to provide the entire content, so member-2 has the ability to call the internet, and fetch some extra information."
    "in order to help member-2, you have to generate a list of search queries so that member-2 can see the search queries and one by one call the internet."
    "Remember": the search queries should not be urls, but should promote calling urls, ex: search_queries: ["github program in dev.to","global pollution index by bbc"] etc. ]                                                                                                                                                                                                                                

    **Process and structure** - 
    The content or thought you generate must be like the example follows below:
    User's question: "hello ! i have graduated from college and its been more than 2 months, i am in my home, so i want to go to bengaluru and for this plan a data what i can do in bengaluru and how can i get a job".
    Your response :                                                                            
    {{ 
    thought - User has requested me to plan a thoughtful plan what he/she could do in bengaluru.
    thought - User has passed out from college and its been more than 2 months, so user might be in tension whether he/she could make a job or not.
    thought - first i have to make user feel ok and give him/her confidence.
    thought - user wants to move to bengalore and bengalore is a nice place because it is full of companies and user can go visit them.
    thought - now let me generate  a plan for users query ---> Command: (You generate a plan now !)
    thought - OK now i have finally generated a plan, but hang on i am working in a company with 2 more members, and the second member's responsibility is to enhance my plan/thought via the use of internet.
    thought - But hang on the second member can only use internet only when i add some search queries  let let me make  collection of search_queries.
    thought - The search query should not be urls but collection of strong url suggesting strings for ex: ["github program in dev.to","global pollution index by bbc"].
    thought - OK now i have finally made the search query.
    thought - Wow now i have both plan and search query, so now i can deliver these entire data to second member.
    thought - But before i pass it to second member, i better have to structure the entire thought/plan very well.
    thought - Now i have structured it and let me complete the process and deliver to second member.
    }}
    **Example of output** -
    {{                                      
    At the end, always respond in the following JSON structure:
    {{
    "thoughts": [
        "thought - user wants to find a job in Bengaluru",
        "thought - I will generate a plan",
        "thought - I will also generate search queries for member-2"
    ],
    "plan": "Step-by-step plan of what user can do",
    "search_queries": [
        "LinkedIn student programs Bengaluru",
        "Naukri.com fresher jobs Bengaluru",
        "Meetup events for freshers Bengaluru"
    ]
    }}
    }}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    """)
    chain = prompt | llm
    response = chain.invoke({"messages":state["messages"]})
    #print("response from first node is",response.content)
    print("\n")
    return{
        "messages":[AIMessage(content=response.content)]
    }


def url_extractor(state:State):
    print("in second node...")
    prompt ="""
    **Person-1 message:**  
    {messages}

    **Tools:**  
    - `url_search`: use this tool to extract a URL from the internet.  
    - Input: a single search query (string).  
    - Output: a single relevant URL.  

    **Your Role:**  
    You are Person-2, a **URL Finder** in a 3-person research company.  
    - You receive Person-1's conversation message above, which contains multiple `search_queries`.  
    - Each `search_query` is a tagline describing a topic we need to find a relevant URL for.  
    - Your job is to call `url_search` **once per query**, pass the tagline as input, and collect all results.  

    **Workflow:**  
    1. Carefully read all items in `search_queries`.  
    2. Think step by step: for each query, decide which search terms to pass to `url_search`.  
    3. Call `url_search` once per item.  
    4. Return your result as a **valid JSON object** containing all queries mapped to their URLs.  

    **Example:**  
    Input:
    ```json
    {{
    "search_queries": [
        "LinkedIn student programs Bengaluru",
        "Naukri.com fresher jobs Bengaluru",
        "Meetup events for freshers Bengaluru"
    ]
    }}
    Reasoning:

    I have 3 queries → I will call url_search 3 times.
    First call with "LinkedIn student programs Bengaluru", get URL.
    Second call with "Naukri.com fresher jobs Bengaluru", get URL.
    Third call with "Meetup events for freshers Bengaluru", get URL.

    Output:
    {{
    "search_queries_urls": [
        {{ "LinkedIn student programs Bengaluru": "https://linkedin.com/bengaluru_careers" }},
        {{ "Naukri.com fresher jobs Bengaluru": "https://naukri.com/fresher-jobs" }},
        {{ "Meetup events for freshers Bengaluru": "https://meetup.com/freshers-bengaluru-events" }}
    ]
    }}
    Important:

    Always output a single JSON object with a key search_queries_urls.
    Each query must be present exactly once with its resolved URL.
    Never invent fake URLs — use url_search results only.
    """
    agent = create_react_agent(model=llm,tools=[url_search],prompt=prompt)
    response = agent.invoke({"messages":state["messages"]})
    #print("response from second node is",response["messages"][-1].content)
    print("\n")
    #print("response is",response)
    return{
        "messages":[AIMessage(content=response["messages"][-1].content)]
    }


def final(state: State):
    print("in final node...")
    prompt = """
    **Conversation**: {message}
    **Look search_querues_urls in the conversation**
    {{
    "search_queries_urls": [
        {{ "LinkedIn student programs Bengaluru": "https://linkedin.com/bengaluru_careers" }},
        {{ "Naukri.com fresher jobs Bengaluru": "https://naukri.com/fresher-jobs" }},
        {{ "Meetup events for freshers Bengaluru": "https://meetup.com/freshers-bengaluru-events" }}
    ]
    }}

    **Your Role (Person-3):**  
    You are the final member in a 3-person research company.  
    - Member-1 has already given their thoughts and a detailed plan.  
    - Member-2 has already fetched these URLs.  
    - Now it’s your job to **call `content_scrapper` for each of these URLs**, gather all the content, and produce a **final structured response** that follows Member-1’s reasoning carefully.

    **Instructions:**  
    1. For each URL inside `search_queries_urls`, call the tool `content_scrapper` once and collect the markdown content.  
    2. Read Member-1’s thoughts carefully and use them as a guide.  
    3. Combine your scraped data with Member-1’s plan into a **final structured response** that is clear, actionable, and insightful.  
    4. Your answer must be **natural language, not JSON**.  
    5. Use headings, bullet points, and sections to make the final report easy to read.

    **Expected Output Style:**  
    - Begin by confirming you looked at the URLs.  
    - Briefly summarize the insights you found from scraping.  
    - Expand on Member-1’s plan with details from the scraped content.  
    - End with a final recommendation / action plan for the user.
    """
    agent = create_react_agent(model=llm, tools=[content_scrapper], prompt=prompt)
    response = agent.invoke({"messages": state["messages"]})
    #print("response from third node is",response["messages"][-1].content)
    print("\n")
    return {"messages": [AIMessage(content=response["messages"][-1].content)]}



graph_builder = StateGraph(State)
graph_builder.add_node("planner",planner)
graph_builder.add_node("url_extractor",url_extractor)
graph_builder.add_node("final",final)
graph_builder.add_edge(START,"planner")
graph_builder.add_edge("planner","url_extractor")
graph_builder.add_edge("url_extractor","final")
graph_builder.add_edge("final",END)
graph = graph_builder.compile(checkpointer=checkpointer)

while True:
    inputQuery = input("ENTER : ")
    initial_state = {"messages":[{"role":"user","content":inputQuery}]}
    response = graph.invoke(initial_state,{"configurable": {"thread_id": "1"}})
    print("\n")
    print(response["messages"][-1].content)

