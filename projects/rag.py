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
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings


loader = WebBaseLoader(
    web_paths=("https://surajjena.com/",),
)
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  
    chunk_overlap=200, 
    add_start_index=True,  
)
all_splits = text_splitter.split_documents(docs)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
vector_store = InMemoryVectorStore(embeddings)
ids = vector_store.add_documents(documents=all_splits)
print("data added to v-db")
retriever = vector_store.as_retriever(search_kwargs={"k": 5})


llm = ChatOpenAI(
  api_key=os.getenv("OPENROUTER_API_KEY"),
  base_url=os.getenv("OPENROUTER_BASE_URL"),
  model="google/gemini-2.5-flash",
  temperature=0.2,
  )

class State(TypedDict):
    messages:Annotated[list,add_messages]


def agent_func(state:State):
    res = retriever.invoke(state["messages"][-1].content)
    response = '/n/n'.join([i.page_content for i in res])
    return {
        "messages":[AIMessage(content=response)]
    }

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