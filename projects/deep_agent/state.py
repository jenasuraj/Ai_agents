from dotenv import load_dotenv
load_dotenv()
import os
from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
import operator


llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    model="mistralai/mistral-small-2603",
)

class State(TypedDict):
    messages: Annotated[list, add_messages]
    plan: str
    conversations : dict #conversation object in the state to keep the content (plan) and status ...#conversation object in the state to keep the content (plan) and status ...