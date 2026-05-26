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

<h1 align="center">🐺 AI Agents with MCP and LangGraph</h1>

<p align="center">
  A modular AI agent platform built with LangGraph, LangChain, MCP, and Python.
</p>

---

## 🚀 Overview

**AI Agents with MCP and LangGraph** is a multi-agent experimentation hub where every agent is designed to solve a specific real-world task. The project demonstrates how autonomous agents can reason, use tools, call APIs, retrieve data, generate content, and automate workflows using a modular architecture.

The repository is now being organized as an agent platform instead of only a collection of separate scripts. Existing agents still live inside `projects/`, while shared platform code lives inside `src/ai_agents/`.

This gives the project a cleaner path toward:

- a unified FastAPI backend
- a React dashboard for running agents
- shared request and response formats
- centralized configuration
- reusable tools and workflows
- easier testing and contribution

---

## ✨ Key Features

- **Multi-Agent Architecture** — each agent is separated by responsibility and can evolve independently.
- **Shared Core Layer** — common schemas, base interface, registry, and configuration helpers.
- **LangGraph Workflows** — graph-based control flow for reliable agentic systems.
- **LangChain Integration** — LLM orchestration, tool calling, prompts, and chains.
- **MCP Tooling** — Model Context Protocol support for connecting agents with external tools.
- **Extensible Structure** — new agents can be added without rewriting the whole project.
- **Production Direction** — designed to later support API, CLI, UI, tests, and deployment.

---

## 🧠 Agent Overview

| Agent | Name | Purpose | Key Tools / APIs |
| :--- | :--- | :--- | :--- |
| **Agent 1** | [Scraper Agent](./projects/scraper) | Performs intelligent web research and extracts useful information from websites. | Tavily, Firecrawl |
| **Agent 2** | [Podcast Agent](./projects/podcast) | Generates podcast-style content and converts text into speech. | ChatGroq, ElevenLabs, Streamlit |
| **Agent 3** | [Stock Agent](./projects/stock) | Analyzes market data, stock-related news, and financial insights. | Alpha Vantage, NSE, MoneyControl |
| **Agent 4** | [GitHub Agent](./projects/github) | Automates repository tasks such as documentation, repo analysis, and GitHub workflows. | GitHub API, MCP SDK, PyGithub |
| **Agent 5** | [Notion Copilot](./projects/notion) | Helps with research, content structuring, and Notion workspace automation. | Notion API, Tavily, Firecrawl |
| **Agent 6** | [RAG Agent](./projects/rag) | Performs retrieval-augmented generation over external knowledge sources. | Hugging Face |
| **Agent 7** | [Orchestration Worker Agent](./projects/orchestration_workers) | Breaks complex user goals into independent subtasks, routes them to worker agents, and synthesizes the outputs into one response. | LangGraph Send API, ChatOpenAI, OpenRouter |

---

## 🏗️ Project Structure

```bash
Ai_agents/
├── src/
│   └── ai_agents/
│       ├── core/
│       │   ├── base.py
│       │   ├── registry.py
│       │   └── schemas.py
│       ├── config/
│       │   └── settings.py
│       └── cli.py
├── projects/
│   ├── scraper/
│   ├── podcast/
│   ├── stock/
│   ├── github/
│   ├── notion/
│   ├── rag/
│   └── orchestration_workers/
├── public/
├── requirements.txt
├── pyproject.toml
└── README.md
```

### `src/ai_agents/`

This is the shared platform layer. It contains common contracts, configuration helpers, and registry logic used by future production-ready agents.

### `projects/`

This contains the existing experimental agents. These agents can be gradually migrated into the shared architecture without breaking the current code.

---

## 🧩 Core Architecture

The target flow is:

```text
User Input
   ↓
AgentRequest
   ↓
Agent Registry
   ↓
Selected Agent
   ↓
Tools / APIs / LLM / MCP
   ↓
AgentResponse
   ↓
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

## 🛠️ Tech Stack

- **Python** — core programming language
- **LangGraph** — agent workflow orchestration
- **LangChain** — LLM application framework
- **MCP SDK** — tool integration using Model Context Protocol
- **Pydantic** — typed request and response schemas
- **python-dotenv** — local environment loading
- **Streamlit** — UI layer for selected agents
- **External APIs** — research, scraping, audio, finance, GitHub, and Notion integrations

---

## ⚙️ Installation

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
pip install -r requirements.txt
```

For editable development:

```bash
pip install -e .
```

---

## 🔐 Environment Variables

Keep your real keys only in a local `.env` file. The repository ignores `.env` files by default.

Example pattern:

```env
OPENAI_API_KEY=replace_me
OPENROUTER_API_KEY=replace_me
TAVILY_API_KEY=replace_me
```

Only add the keys required by the agent you are running.

---

## ▶️ Usage

Run an existing experimental agent:

```bash
cd projects/scraper
python main.py
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

## 🧩 Adding a New Agent

Recommended structure:

```bash
projects/my-new-agent/
├── main.py
├── tools.py
├── prompts.py
├── graph.py
└── README.md
```

For production-style agents, use the shared base classes inside `src/ai_agents/core/`.

A good agent should have:

- a clear goal
- typed input and output
- well-defined tools
- proper error handling
- clean prompt design
- documentation explaining how to run it

---

## 🗺️ Roadmap

- [ ] Migrate each existing agent to the shared `BaseAgent` interface
- [ ] Add a unified FastAPI backend for all agents
- [ ] Add a frontend dashboard for selecting and running agents
- [ ] Add per-agent README files
- [ ] Add tests for registry and core workflows
- [ ] Add Docker support
- [ ] Add tracing and logging
- [ ] Add deployment guide

---

## 👤 Author

**Suraj Jena**

- LinkedIn: [Suraj Jena](https://www.linkedin.com/in/suraj-jena-0991a121a/)
- X/Twitter: [@jenasuraj_](https://x.com/jenasuraj_)

---

<p align="center">
  Built with ❤️ using LangGraph, LangChain, MCP, and Python.
</p>
