from firecrawl import Firecrawl
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_openai import ChatOpenAI
load_dotenv()
import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage,SystemMessage,HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
memory = InMemorySaver()
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.agents import create_agent


loader = WebBaseLoader(
    web_paths=("https://subodhjena.com/",),
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


@tool
def ragdb(input:str):
    """use this tool to interact with the rag or personal data base"""
    print("i am in ragdb")
    rag_res = retriever.invoke(input)
    updated_response = '/n/n'.join([i.page_content for i in rag_res])
    return updated_response



llm = ChatOpenAI(
  api_key=os.getenv("OPENROUTER_API_KEY"),
  base_url=os.getenv("OPENROUTER_BASE_URL"),
  model="google/gemini-2.5-flash",
  temperature=0.2,
  )

class State(TypedDict):
    messages:Annotated[list,add_messages]


def agent_func(state:State):
    prompt = """
    You are a very helpful assistant, and your job is to analyse the user query and
    decide whether its a general call or its a database call ?. 
    Basically database has all the information regarding mr subodh jena, so if user query is regarding subodh jena, use tools like ragdb.
    and if user query is not related to subodh jena, dont use any tool and answer user's demand friendly way.
    """
    agent = create_agent(model=llm,tools=[ragdb],prompt=prompt)
    response = agent.invoke({"messages":state["messages"]})
    return {
        "messages":[AIMessage(content=response["messages"][-1].content)]
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