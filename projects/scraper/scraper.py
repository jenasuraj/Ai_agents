from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
load_dotenv()
import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage, HumanMessage,ToolMessage,SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from tools import news,urlExtractor,contentScrapper
from prompts import system_prompt

memory = InMemorySaver()

llm = ChatOpenAI(
  api_key=os.getenv("OPENROUTER_API_KEY"),
  base_url=os.getenv("OPENROUTER_BASE_URL"),
  model="google/gemini-2.5-flash",
  temperature=0.1)

class State(TypedDict):
    messages:Annotated[list,add_messages]

tools = [news,urlExtractor,contentScrapper]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)

def agent_func(state:State):
    response = llm_with_tools.invoke([system_prompt] + state["messages"], config)
    return {"messages": [response]}


def routing(state:State):
    last = state["messages"][-1]
    if last.additional_kwargs.get("tool_calls",None):
        print("yes")
        return "yes"
    else:
        print("no")
        return "No"   


def toolCall(state: State):
    outputs = []
    last_msg = state["messages"][-1]
    for tool_call in last_msg.tool_calls:
        tool_name = tool_call["name"]
        args = tool_call["args"]["input"]
        if tool_name == "urlExtractor":
            response = urlExtractor.invoke(args)
        elif tool_name == "contentScrapper":
            response = contentScrapper.invoke(args)
        elif tool_name == "news":
            response = news.invoke(args)
        else:
            response = f"Unknown tool: {tool_name}"
        outputs.append(
            ToolMessage(
                content=str(response),
                tool_call_id=tool_call["id"]
            )
        )
    return {"messages": outputs}


graph_builder = StateGraph(State)
graph_builder.add_node("agent_func",agent_func)
graph_builder.add_node("toolCall",toolCall)
graph_builder.add_edge(START,"agent_func")
graph_builder.add_conditional_edges("agent_func",routing,{"yes":"toolCall","No":END})
graph_builder.add_edge("toolCall","agent_func")
graph = graph_builder.compile(checkpointer=memory)    


while True:
    inputData = input("Enter : ")
    config = {"configurable": {"thread_id": "1"}}
    initial_state = {"messages":HumanMessage(content=inputData)}
    response = graph.invoke(initial_state, config,stream_mode="values")
    print(response["messages"][-1].content)