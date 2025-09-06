from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import asyncio
from langchain_groq.chat_models import ChatGroq
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model='openai/gpt-oss-20b')
client = MultiServerMCPClient(
    {
        "myserver": {
            "url": "http://127.0.0.1:8000/mcp",
            "transport": "streamable_http",
        }
    }
)

async def call():
    tools = await client.get_tools()
    agent = create_react_agent(model=llm,tools=tools)
    response = await agent.ainvoke(
    {"messages": [{"role": "user", "content": "what is current temperature in new delhi ?"}]}
    )
    print(response["messages"][-1].content)
asyncio.run(call())



