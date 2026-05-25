from state import llm,State
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import ToolNode
from prompts import system_prompt
from tools import tavily_tool,read_plan,write_plan


memory = InMemorySaver()        
tools = [tavily_tool, read_plan,write_plan]
llm_with_tools = llm.bind_tools(tools)




def agent_node(state: State):
    print(f"state is",state)
    raw_response: AIMessage = llm_with_tools.invoke(
        [SystemMessage(content=system_prompt)] + state["messages"]
    )
    clean_message = AIMessage(
        content=raw_response.content,
        tool_calls=raw_response.tool_calls,
    )
    print("\n\n")
    return {"messages": [clean_message]}



def routing(state: State):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tool"
    return END


graph_builder = StateGraph(State)
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("tool", ToolNode(tools))
graph_builder.add_edge(START, "agent")
graph_builder.add_conditional_edges(
    "agent",
    routing,
    {
        "tool": "tool",
        END: END
    }
)
graph_builder.add_edge("tool", "agent")
graph = graph_builder.compile(checkpointer=memory)



while True:
    user_input = input("\nEnter: ")
    config = {"configurable": {"thread_id": "1"}, "recursion_limit": 50}
    state = {
        "messages": [HumanMessage(content=user_input)]
    }
    final = None
    for event in graph.stream(state, config, stream_mode="values"):
        if "messages" in event:
            msg = event["messages"][-1]
            if isinstance(msg, AIMessage) and msg.content:
                final = msg.content
    print("\nAnswer:\n")
    print(final)