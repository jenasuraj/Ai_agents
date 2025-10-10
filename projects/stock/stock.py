import os
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI

load_dotenv()

from tools import Tavily
from prompts import (
    final_prompt,
    company_base_prompt,
    risk_assessment_prompt,
    finance_metrics_prompt,
    growth_prompt
)

# ---- STATE ----
class State(TypedDict):
    messages: Annotated[list, add_messages]
    company_basics: Annotated[list, add_messages]
    finance_metrics: Annotated[list, add_messages]
    growth: Annotated[list, add_messages]
    risk_assessment: Annotated[list, add_messages]


# ---- LLM ----
llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    model="x-ai/grok-4-fast",
)

tools = [Tavily]
llm_with_tools = llm.bind_tools(tools)


# ---- COMPANY BASICS ----
def company_basics(state: State):
    print("🟡 Entered company_basics node...")
    response = llm_with_tools.invoke(
        [company_base_prompt, HumanMessage(content=state["messages"][-1].content)]
    )
    print("✅ company_basics response received.")
    return {
        "company_basics": [response],
        "messages": [response]
    }


def company_basics_tool_router(state: State):
    print("🔍 Checking tool calls in company_basics...")
    last = state["company_basics"][-1]
    if last.additional_kwargs.get("tool_calls"):
        print("🧠 company_basics tool call detected → YES")
        return "yes"
    else:
        print("❌ No tool call in company_basics → NO")
        return "no"


def company_basics_tool(state: State):
    print("⚙️ Running company_basics_tool...")
    outputs = []
    last_msg = state["company_basics"][-1]
    for tool_call in last_msg.tool_calls:
        tool_name = tool_call["name"]
        args = tool_call["args"]["input"]
        print(f"🔧 Invoking tool '{tool_name}' with args: {args}")

        if tool_name == "Tavily":
            response = Tavily.invoke(args)
        else:
            response = f"Unknown tool: {tool_name}"

        outputs.append(ToolMessage(content=str(response), tool_call_id=tool_call["id"]))
    return {"company_basics": outputs, "messages": outputs}


# ---- FINANCE METRICS ----
def finance_metrics(state: State):
    print("🟡 Entered finance_metrics node...")
    response = llm_with_tools.invoke(
        [finance_metrics_prompt, HumanMessage(content=state["messages"][-1].content)]
    )
    print("✅ finance_metrics response received.")
    return {
        "finance_metrics": [response],
        "messages": [response]
    }


def finance_metrics_tool_router(state: State):
    print("🔍 Checking tool calls in finance_metrics...")
    last = state["finance_metrics"][-1]
    if last.additional_kwargs.get("tool_calls"):
        print("🧠 finance_metrics tool call detected → YES")
        return "yes"
    else:
        print("❌ No tool call in finance_metrics → NO")
        return "no"


def finance_metrics_tool(state: State):
    print("⚙️ Running finance_metrics_tool...")
    outputs = []
    last_msg = state["finance_metrics"][-1]
    for tool_call in last_msg.tool_calls:
        tool_name = tool_call["name"]
        args = tool_call["args"]["input"]
        print(f"🔧 Invoking tool '{tool_name}' with args: {args}")

        if tool_name == "Tavily":
            response = Tavily.invoke(args)
        else:
            response = f"Unknown tool: {tool_name}"

        outputs.append(ToolMessage(content=str(response), tool_call_id=tool_call["id"]))
    return {"finance_metrics": outputs, "messages": outputs}


# ---- RISK ASSESSMENT ----
def risk_assessment(state: State):
    print("🟡 Entered risk_assessment node...")
    response = llm_with_tools.invoke(
        [risk_assessment_prompt, HumanMessage(content=state["messages"][-1].content)]
    )
    print("✅ risk_assessment response received.")
    return {
        "risk_assessment": [response],
        "messages": [response]
    }


def risk_assessment_tool_router(state: State):
    print("🔍 Checking tool calls in risk_assessment...")
    last = state["risk_assessment"][-1]
    if last.additional_kwargs.get("tool_calls"):
        print("🧠 risk_assessment tool call detected → YES")
        return "yes"
    else:
        print("❌ No tool call in risk_assessment → NO")
        return "no"


def risk_assessment_tool(state: State):
    print("⚙️ Running risk_assessment_tool...")
    outputs = []
    last_msg = state["risk_assessment"][-1]
    for tool_call in last_msg.tool_calls:
        tool_name = tool_call["name"]
        args = tool_call["args"]["input"]
        print(f"🔧 Invoking tool '{tool_name}' with args: {args}")

        if tool_name == "Tavily":
            response = Tavily.invoke(args)
        else:
            response = f"Unknown tool: {tool_name}"

        outputs.append(ToolMessage(content=str(response), tool_call_id=tool_call["id"]))
    return {"risk_assessment": outputs, "messages": outputs}


# ---- GROWTH ----
def growth(state: State):
    print("🟡 Entered growth node...")
    response = llm_with_tools.invoke(
        [growth_prompt, HumanMessage(content=state["messages"][-1].content)]
    )
    print("✅ growth response received.")
    return {
        "growth": [response],
        "messages": [response]
    }


def growth_tool_router(state: State):
    print("🔍 Checking tool calls in growth...")
    last = state["growth"][-1]
    if last.additional_kwargs.get("tool_calls"):
        print("🧠 growth tool call detected → YES")
        return "yes"
    else:
        print("❌ No tool call in growth → NO")
        return "no"


def growth_tool(state: State):
    print("⚙️ Running growth_tool...")
    outputs = []
    last_msg = state["growth"][-1]
    for tool_call in last_msg.tool_calls:
        tool_name = tool_call["name"]
        args = tool_call["args"]["input"]
        print(f"🔧 Invoking tool '{tool_name}' with args: {args}")

        if tool_name == "Tavily":
            response = Tavily.invoke(args)
        else:
            response = f"Unknown tool: {tool_name}"

        outputs.append(ToolMessage(content=str(response), tool_call_id=tool_call["id"]))
    return {"growth": outputs, "messages": outputs}



def final_node(state: State):
    print("🟢 Reached final_node")
    try:
        if all(state.get(k) for k in ["company_basics", "finance_metrics", "growth", "risk_assessment"]):
            agent = final_prompt | llm
            response = agent.invoke({"messages": state["messages"]})
            print("✅ Final LLM summary generated.")
            return {"messages": [AIMessage(content=response.content)]}
        else:
            print("⚠️ Missing some node outputs. Skipping final response.")
            return {"messages": [SystemMessage(content="Incomplete data from one or more nodes.")]}
    except Exception as e:
        print(f"❌ Final node error: {e}")
        return {"messages": [SystemMessage(content=f"Error: {e}")]}


# ---- GRAPH BUILDER ----
graph_builder = StateGraph(State)

graph_builder.add_node("company_basics", company_basics)
graph_builder.add_node("finance_metrics", finance_metrics)
graph_builder.add_node("risk_assessment", risk_assessment)
graph_builder.add_node("growth", growth)
graph_builder.add_node("final_node", final_node)

graph_builder.add_node("company_basics_tool", company_basics_tool)
graph_builder.add_node("finance_metrics_tool", finance_metrics_tool)
graph_builder.add_node("risk_assessment_tool", risk_assessment_tool)
graph_builder.add_node("growth_tool", growth_tool)

graph_builder.add_conditional_edges("company_basics", company_basics_tool_router, {"yes": "company_basics_tool", "no": "final_node"})
graph_builder.add_conditional_edges("finance_metrics", finance_metrics_tool_router, {"yes": "finance_metrics_tool", "no": "final_node"})
graph_builder.add_conditional_edges("risk_assessment", risk_assessment_tool_router, {"yes": "risk_assessment_tool", "no": "final_node"})
graph_builder.add_conditional_edges("growth", growth_tool_router, {"yes": "growth_tool", "no": "final_node"})

graph_builder.add_edge("company_basics_tool", "company_basics")
graph_builder.add_edge("finance_metrics_tool", "finance_metrics")
graph_builder.add_edge("risk_assessment_tool", "risk_assessment")
graph_builder.add_edge("growth_tool", "growth")

graph_builder.add_edge(START, "company_basics")
graph_builder.add_edge(START, "finance_metrics")
graph_builder.add_edge(START, "risk_assessment")
graph_builder.add_edge(START, "growth")

graph_builder.add_edge("final_node", END)
graph = graph_builder.compile()

# ---- EXECUTION LOOP ----
while True:
    inputQuery = input("Enter stock name : ")
    print(f"🚀 Starting flow for query: {inputQuery}")
    initial_state = {"messages": [{"role": "user", "content": inputQuery}]}
    response = graph.invoke(initial_state)
    print("📊 Final Response:\n", response["messages"][-1].content)
