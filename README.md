<p align="center">
  <img src="public/img.png" width="900px" alt="AI Agents with MCP and LangGraph" />
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/suraj-jena-0991a121a/">
    <img src="https://img.shields.io/badge/-Follow%20Suraj%20Jena-blue?logo=linkedin&style=flat-square" alt="LinkedIn" />
  </a>
  <a href="https://x.com/jenasuraj_">
    <img src="https://img.shields.io/twitter/follow/jenasuraj_" alt="Twitter" />
  </a>
</p>

<h1 align="center">AI Agents with MCP and LangGraph</h1>

<p align="center">
  A modular AI agent experimentation hub built with LangGraph, LangChain, MCP, and Python.
</p>

---

## Overview

**AI Agents with MCP and LangGraph** is a multi-agent experimentation hub where each agent is designed around a specific real-world workflow. The project demonstrates how autonomous agents can reason, use tools, call APIs, retrieve data, generate content, and coordinate multiple workers through graph-based control flow.

The repository is being organized as an agent platform instead of only a collection of scripts. Experimental agents live inside `projects/`, while shared platform code lives inside `src/ai_agents/`.

This gives the project a cleaner path toward:

- a unified FastAPI backend
- a React dashboard for running agents
- shared request and response formats
- centralized configuration
- reusable tools and workflows
- easier testing and contribution

---

## Key Features

- **Multi-agent architecture**: each agent is separated by responsibility and can evolve independently.
- **Supervisor routing**: the supervisor agent plans the task, selects only the needed workers, and sends work through ordered routes.
- **Tool-aware worker nodes**: worker agents can call tools through LangGraph `ToolNode` routing and then resume their own reasoning.
- **Shared core layer**: common schemas, base interface, registry, and configuration helpers.
- **LangGraph workflows**: graph-based control flow for reliable agentic systems.
- **LangChain integration**: LLM orchestration, tool calling, prompts, and chains.
- **MCP tooling**: Model Context Protocol support for connecting agents with external tools.
- **Extensible structure**: new agents can be added without rewriting the whole project.

---

## Agent Overview

| Agent | Name | Purpose | Key Tools / APIs |
| :--- | :--- | :--- | :--- |
| **Agent 1** | [Scraper Agent](./projects/scraper) | Performs intelligent web research and extracts useful information from websites. | Tavily, Firecrawl |
| **Agent 2** | [Podcast Agent](./projects/podcast) | Generates podcast-style content and converts text into speech. | ChatGroq, ElevenLabs, Streamlit |
| **Agent 3** | [Stock Agent](./projects/stock) | Analyzes market data, stock-related news, and financial insights. | Alpha Vantage, NSE, MoneyControl |
| **Agent 4** | [GitHub Agent](./projects/github) | Automates repository tasks such as documentation, repo analysis, and GitHub workflows. | GitHub API, MCP SDK, PyGithub |
| **Agent 5** | [Notion Copilot](./projects/notion) | Helps with research, content structuring, and Notion workspace automation. | Notion API, Tavily, Firecrawl |
| **Agent 6** | [Agentic RAG](./projects/agentic_rag) | Performs retrieval-augmented generation over external knowledge sources. | Hugging Face |
| **Agent 7** | [Orchestration Worker Agent](./projects/orchestration_workers) | Breaks complex user goals into independent subtasks, routes them to worker agents, and synthesizes outputs. | LangGraph Send API, ChatOpenAI, OpenRouter |
| **Agent 8** | [Supervisor Agent](./projects/supervisor) | Uses a supervisor node to plan, choose worker agents, route tool calls, and synthesize the final answer. | LangGraph, ToolNode, ChatOpenAI, OpenRouter |
| **Agent 9** | [Travel Agent](./projects/travel) | Creates travel plans with planning, tool usage, and structured frontend-friendly output. | LangGraph, ToolNode, Pydantic |
| **Agent 10** | [Deep Agent](./projects/deep_agent) | Experimental deeper agent workflow split across app, state, and tool modules. | LangGraph, custom tools |

---

## Supervisor Agent

The new `projects/supervisor` workflow demonstrates a proper supervisor-worker graph.

Flow:

```text
User Input
   |
Supervisor
   |-- creates a plan
   |-- selects ordered worker routes
   v
Worker Agent
   |-- coding
   |-- research
   |-- weather
   v
Tool Routing
   |-- if the worker requests a tool, run ToolNode
   |-- return to the same worker after tool output
   v
Synthesizer
   |
Final Answer
```

Current worker nodes:

- `coding`: programming, debugging, architecture, and code explanations
- `research`: fact gathering, comparison, and general research-style reasoning
- `weather`: weather-related questions using the available weather tool

The supervisor returns a structured route list, for example:

```python
routes = ["research", "coding"]
```

Each selected worker runs in order. If a worker calls a tool, `tool_routing()` sends the graph to `ToolNode`, then `route_after_tool()` returns the graph back to the worker that requested the tool. Once all selected workers finish, the `synthesizer` creates one final response.

Run it:

```bash
cd projects/supervisor
python app.py
```

Required environment variables:

```env
OPENROUTER_API_KEY=replace_me
OPENROUTER_BASE_URL=replace_me
```

---

## Project Structure

```bash
Ai_agents/
|-- src/
|   `-- ai_agents/
|       |-- core/
|       |   |-- base.py
|       |   |-- registry.py
|       |   `-- schemas.py
|       |-- config/
|       |   `-- settings.py
|       `-- cli.py
|-- projects/
|   |-- scraper/
|   |-- podcast/
|   |-- stock/
|   |-- github/
|   |-- notion/
|   |-- agentic_rag/
|   |-- orchestration_workers/
|   |-- supervisor/
|   |-- travel/
|   `-- deep_agent/
|-- public/
|-- projects/requirements.txt
|-- pyproject.toml
`-- README.md
```

### `src/ai_agents/`

This is the shared platform layer. It contains common contracts, configuration helpers, and registry logic used by future production-ready agents.

### `projects/`

This contains the experimental agents. These agents can be gradually migrated into the shared architecture without breaking the current code.

---

## Core Architecture

The target platform flow is:

```text
User Input
   |
AgentRequest
   |
Agent Registry
   |
Selected Agent
   |
Tools / APIs / LLM / MCP
   |
AgentResponse
   |
CLI / FastAPI / Frontend
```

Every mature agent should eventually follow this contract:

```python
class MyAgent(BaseAgent):
    info = AgentInfo(
        name="My Agent",
        slug="my-agent",
        description="What this agent does",
        tools=["tool-a", "tool-b"],
    )

    def run(self, request: AgentRequest) -> AgentResponse:
        ...
```

---

## Tech Stack

- **Python**: core programming language
- **LangGraph**: agent workflow orchestration
- **LangChain**: LLM application framework
- **MCP SDK**: tool integration using Model Context Protocol
- **Pydantic**: typed request and response schemas
- **python-dotenv**: local environment loading
- **Streamlit**: UI layer for selected agents
- **External APIs**: research, scraping, audio, finance, GitHub, Notion, and weather integrations

---

## Installation

### 1. Clone the repository

```bash
git clone git@github.com:jenasuraj/Ai_agents.git
```

### 2. Move into the project

```bash
cd Ai_agents
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

For Windows:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r projects/requirements.txt
```

For editable development:

```bash
pip install -e .
```

---

## Environment Variables

Keep your real keys only in a local `.env` file. The repository ignores `.env` files by default.

Example pattern:

```env
OPENAI_API_KEY=replace_me
OPENROUTER_API_KEY=replace_me
OPENROUTER_BASE_URL=replace_me
TAVILY_API_KEY=replace_me
```

Only add the keys required by the agent you are running.

---

## Usage

Run an existing experimental agent:

```bash
cd projects/scraper
python main.py
```

Run the supervisor agent:

```bash
cd projects/supervisor
python app.py
```

Run the platform CLI:

```bash
python -m ai_agents.cli
```

Some agents may use Streamlit:

```bash
streamlit run app.py
```

---

## Adding a New Agent

Recommended structure:

```bash
projects/my-new-agent/
|-- main.py
|-- tools.py
|-- prompts.py
|-- graph.py
`-- README.md
```

A good agent should have:

- a clear goal
- typed input and output
- well-defined tools
- proper error handling
- clean prompt design
- documentation explaining how to run it

For production-style agents, use the shared base classes inside `src/ai_agents/core/`.

---

## Roadmap

- [ ] Migrate each existing agent to the shared `BaseAgent` interface
- [ ] Add a unified FastAPI backend for all agents
- [ ] Add a frontend dashboard for selecting and running agents
- [ ] Add per-agent README files
- [ ] Add tests for registry and core workflows
- [ ] Add Docker support
- [ ] Add tracing and logging
- [ ] Add deployment guide

---

## Author

**Suraj Jena**

- LinkedIn: [Suraj Jena](https://www.linkedin.com/in/suraj-jena-0991a121a/)
- X/Twitter: [@jenasuraj_](https://x.com/jenasuraj_)

---

<p align="center">
  Built with LangGraph, LangChain, MCP, and Python.
</p>
