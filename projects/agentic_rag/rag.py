from dotenv import load_dotenv
load_dotenv()
import os
from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


memory = InMemorySaver()

llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    model="google/gemini-2.5-flash",
)


class State(TypedDict):
    messages: Annotated[list, add_messages]
    plan: str



tavily_tool = TavilySearchResults(max_results=5, search_depth="advanced")

@tool
def weather_tool(location: str) -> str:
    """This is a weather tool used to fetch weather related info like temperature, etc
    Args : 
         location - this is an arguement that takes the name of the location like (tokyo, new york etc)
    Returns : 
         It returns the weather information like temperature ."""
    print("called weather tool")
    return "35°C and a bit warm"

@tool
def coding_tool(code: str) -> str:
    """This tool is used to fetch the code from your codebase.
    Args : code - this arguement takes the name of your code file you want to access for example , authSlice.tsx 
    Returns : Returns the code file you want to take a look. """
    print("called coding tool")
    
    response =  """import React, { useState } from "react";

                type User = {
                email: string;
                password: string;
                };

                const Auth: React.FC = () => {
                const [user, setUser] = useState<User>({ email: "", password: "" });
                const [isLoggedIn, setIsLoggedIn] = useState(false);
                const [error, setError] = useState("");

                const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
                    setUser({ ...user, [e.target.name]: e.target.value });
                };

                const handleLogin = (e: React.FormEvent) => {
                    e.preventDefault();

                    if (!user.email || !user.password) {
                    setError("All fields required");
                    return;
                    }

                    if (user.email === "test@example.com" && user.password === "1234") {
                    setIsLoggedIn(true);
                    setError("");
                    } else {
                    setError("Invalid credentials");
                    }
                };

                const handleLogout = () => {
                    setIsLoggedIn(false);
                    setUser({ email: "", password: "" });
                };

                return (
                    <div style={{ maxWidth: 300, margin: "auto", paddingTop: 50 }}>
                    {isLoggedIn ? (
                        <>
                        <h3>Welcome, {user.email}</h3>
                        <button onClick={handleLogout}>Logout</button>
                        </>
                    ) : (
                        <form onSubmit={handleLogin}>
                        <h3>Login</h3>
                        <input
                            type="email"
                            name="email"
                            placeholder="Email"
                            value={user.email}
                            onChange={handleChange}
                        />
                        <input
                            type="password"
                            name="password"
                            placeholder="Password"
                            value={user.password}
                            onChange={handleChange}
                        />
                        <button type="submit">Login</button>
                        {error && <p style={{ color: "red" }}>{error}</p>}
                        </form>
                    )}
                    </div>
                );
                };

                export default Auth;
                import React, { useState } from "react";

                type PaymentData = {
                cardNumber: string;
                name: string;
                expiry: string;
                cvv: string;
                };

                const Payment: React.FC = () => {
                const [data, setData] = useState<PaymentData>({
                    cardNumber: "",
                    name: "",
                    expiry: "",
                    cvv: "",
                });

                const [status, setStatus] = useState("");
                const [error, setError] = useState("");

                const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
                    setData({ ...data, [e.target.name]: e.target.value });
                };

                const handlePayment = (e: React.FormEvent) => {
                    e.preventDefault();

                    if (!data.cardNumber || !data.name || !data.expiry || !data.cvv) {
                    setError("All fields required");
                    return;
                    }

                    if (data.cardNumber.length < 12 || data.cvv.length < 3) {
                    setError("Invalid card details");
                    return;
                    }

                    setError("");
                    setStatus("Processing...");

                    setTimeout(() => {
                    setStatus("Payment Successful ✅");
                    }, 1500);
                };

                return (
                    <div style={{ maxWidth: 320, margin: "auto", paddingTop: 50 }}>
                    <form onSubmit={handlePayment}>
                        <h3>Payment</h3>

                        <input
                        type="text"
                        name="cardNumber"
                        placeholder="Card Number"
                        value={data.cardNumber}
                        onChange={handleChange}
                        />

                        <input
                        type="text"
                        name="name"
                        placeholder="Card Holder Name"
                        value={data.name}
                        onChange={handleChange}
                        />

                        <input
                        type="text"
                        name="expiry"
                        placeholder="MM/YY"
                        value={data.expiry}
                        onChange={handleChange}
                        />

                        <input
                        type="password"
                        name="cvv"
                        placeholder="CVV"
                        value={data.cvv}
                        onChange={handleChange}
                        />

                        <button type="submit">Pay Now</button>

                        {error && <p style={{ color: "red" }}>{error}</p>}
                        {status && <p>{status}</p>}
                    </form>
                    </div>
                );
                };

                export default Payment;"""
    count = 0
    for i in response:
        count+=1
    if count>500:
        print("coding file is huge, we have to bring RAG ...")
        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,  
        chunk_overlap=20, 
        add_start_index=True,  
        )
        docs = [Document(page_content=response)]

        #Document(
       #     page_content="const Auth: React.FC = () => { ...",
        #    metadata={"file": "auth.tsx"}
        #)

        #Document(
        #    page_content="const handleLogin = ...",
        #    metadata={"file": "auth.tsx"}
        #) the spliiter expects Documents, so things needed to be in this format like page_content and metadata

        all_splits = text_splitter.split_documents(docs)
        print("embedding started .... ")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        print("vector store started .... ")
        vector_store = InMemoryVectorStore(embeddings)
        ids = vector_store.add_documents(documents=all_splits)
        print("data added to v-db")
        retriever = vector_store.as_retriever(search_kwargs={"k": 5})

        rag_res = retriever.invoke(code)
        print("rag res is ",rag_res)
        updated_response = '/n/n'.join([i.page_content for i in rag_res])
        print("rag file is",updated_response)
        return updated_response

@tool
def email_tool(user: str, content: str) -> str:
    """
    Send an email to a user.

    Args:
        user: Email address of the user (e.g. user@gmail.com)
        content: Message/content to send in the email

    Returns:
        Confirmation message after sending email
    """
    print("called email tool",content)
    return "Email sent"
                



tools = [tavily_tool, weather_tool, coding_tool,email_tool]
llm_with_tools = llm.bind_tools(tools)


def planner_node(state: State):
    query = state["messages"][-1].content
    prompt = f"""
                Break task into steps.

                Query: {query}

                Format:
                Step 1:
                Step 2:
                Step 3:
                """
    res = llm.invoke([HumanMessage(content=prompt)])
    return {
        "plan": res.content,
        "messages": [AIMessage(content=f"Plan:\n{res.content}")]
    }



def agent_node(state: State):
    plan = state.get("plan", "")
    system_prompt = f"""
    Follow the plan and solve.

    Plan:
    {plan}

    Rules :
    - Use tools if needed
    - Do proper reasoning and think step by step like human.
    - Call multiple tools when needed .

    Tools :
    - weather_tool : use this tool to fetch weather related information.
    - coding_tool : use this tool to fetch code base and work on that for example: (user : my app.tsx is not working, you: let me call code_tool and fetch app.tsx and work on it).
    - tavily_tool : use this tool to fetch information from internet, for example: current trends, news etc. 
    - email_tool : use this tool to post an email to a user
    """
    res = llm_with_tools.invoke(
        [SystemMessage(content=system_prompt)] + state["messages"]
    )
    return {"messages": [res]}



def routing(state: State):
    last = state["messages"][-1]

    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tool"
    return END


graph_builder = StateGraph(State)
graph_builder.add_node("planner", planner_node)
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("tool", ToolNode(tools))
graph_builder.add_edge(START, "planner")
graph_builder.add_edge("planner", "agent")
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
    config = {"configurable": {"thread_id": "1"}}
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