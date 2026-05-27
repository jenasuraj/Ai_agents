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
  A compact multi-agent experimentation hub built with Python, LangGraph, LangChain, MCP, and external APIs.
</p>

---

## 🚀 Overview

**AI Agents with MCP and LangGraph** is a modular agent lab where each agent focuses on one real-world workflow: research, scraping, travel planning, podcast generation, finance, GitHub automation, Notion automation, RAG, and dynamic orchestration.

The repo is moving toward a unified platform architecture: experimental agents live in `projects/`, while reusable platform code lives in `src/ai_agents/`.

---

## 🧠 Agents in `projects/`

| Agent | Path | Purpose | Main Tools / APIs |
| :--- | :--- | :--- | :--- |
| **Scraper Agent** | [`projects/scraper`](./projects/scraper) | Web research, scraping, and structured information extraction. | Tavily, Firecrawl |
| **Travel Agent** | [`projects/travel`](./projects/travel) | Plans trips, explores destinations, and helps with travel-related recommendations. | LLMs, search/travel APIs |
| **Podcast Agent** | [`projects/podcast`](./projects/podcast) | Converts ideas or text into podcast-style audio content. | ChatGroq, ElevenLabs, Streamlit |
| **Stock Agent** | [`projects/stock`](./projects/stock) | Tracks market data, stock news, and financial insights. | Alpha Vantage, NSE, MoneyControl |
| **GitHub Agent** | [`projects/github`](./projects/github) | Automates repository analysis, documentation, and GitHub workflows. | GitHub API, MCP SDK, PyGithub |
| **Notion Copilot** | [`projects/notion`](./projects/notion) | Supports research, writing, and Notion workspace automation. | Notion API, Tavily, Firecrawl |
| **RAG Agent** | [`projects/rag`](./projects/rag) | Answers questions using retrieval-augmented generation over knowledge sources. | Hugging Face |
| **Orchestration Worker Agent** | [`projects/orchestration_workers`](./projects/orchestration_workers) | Splits a complex goal into independent tasks, sends them to workers, and combines the outputs. | LangGraph Send API, ChatOpenAI, OpenRouter |

---

## ✨ What This Repo Demonstrates

- **Agentic workflows** using LangGraph nodes, edges, tools, and state.
- **Tool-using agents** that connect to search, scraping, travel, finance, GitHub, Notion, and audio APIs.
- **MCP integration** for external tool access and automation.
- **Modular structure** where agents can evolve independently.
- **Platform direction** with shared schemas, registry, config, and base agent contracts.

---

## 🏗️ Structure

```bash
Ai_agents/
├── projects/
│   ├── scraper/
│   ├── travel/
│   ├── podcast/
│   ├── stock/
│   ├── github/
│   ├── notion/
│   ├── rag/
│   └── orchestration_workers/
├── src/
│   └── ai_agents/
│       ├── core/
│       ├── config/
│       └── cli.py
├── public/
├── requirements.txt
├── pyproject.toml
└── README.md
```

`projects/` contains the working experimental agents. `src/ai_agents/` contains the shared platform layer for future production-ready agents.

---

## 🛠️ Tech Stack

**Python**, **LangGraph**, **LangChain**, **MCP SDK**, **Pydantic**, **Streamlit**, **python-dotenv**, and APIs for scraping, research, travel, finance, GitHub, Notion, and audio generation.

---

## ⚙️ Setup

```bash
git clone git@github.com:jenasuraj/Ai_agents.git
cd Ai_agents
python -m venv venv
```

Activate the environment:

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

Create a local `.env` file and add only the keys required by the agent you want to run:

```env
OPENAI_API_KEY=replace_me
OPENROUTER_API_KEY=replace_me
TAVILY_API_KEY=replace_me
```

---

## ▶️ Usage

Run an experimental agent:

```bash
cd projects/scraper
python main.py
```

Run the shared CLI:

```bash
python -m ai_agents.cli
```

Run Streamlit-based agents when available:

```bash
streamlit run app.py
```

---

## 🗺️ Roadmap

- Migrate all `projects/` agents to the shared `BaseAgent` contract.
- Add a unified FastAPI backend.
- Add a React dashboard for choosing and running agents.
- Add tests, tracing, Docker support, and deployment docs.

---

## 👤 Author

**Suraj Jena**

- LinkedIn: [Suraj Jena](https://www.linkedin.com/in/suraj-jena-0991a121a/)
- X/Twitter: [@jenasuraj_](https://x.com/jenasuraj_)

---

<p align="center">
  Built with ❤️ using LangGraph, LangChain, MCP, and Python.
</p>
