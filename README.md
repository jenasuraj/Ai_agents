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
  A collection of modular AI agents built with LangGraph, LangChain, MCP, and modern LLM tooling.
</p>

---

## 🚀 Overview

**AI Agents with MCP and LangGraph** is a multi-agent experimentation hub where every agent is designed to solve a specific real-world task. The project demonstrates how autonomous agents can reason, use tools, call APIs, retrieve data, generate content, and automate workflows using a modular architecture.

This repository explores practical agentic patterns such as:

- Web research and intelligent scraping
- Podcast generation from text or ideas
- Stock market research and financial analysis
- GitHub repository automation
- Notion-based research and content organization
- Retrieval-Augmented Generation using external knowledge sources
- Tool calling through MCP-based integrations

The main goal of this project is to understand how specialized agents can be designed, composed, and extended into production-ready AI workflows.

---

## ✨ Key Features

- **Multi-Agent Architecture** — each agent is separated by responsibility and can evolve independently.
- **LangGraph Workflows** — graph-based control flow for building reliable agentic systems.
- **LangChain Integration** — support for LLM orchestration, tools, prompts, and chains.
- **MCP Tooling** — Model Context Protocol support for connecting agents with external tools.
- **API-Powered Agents** — integrations with services such as Tavily, Firecrawl, GitHub, Notion, ElevenLabs, and financial APIs.
- **Extensible Structure** — new agents can be added without rewriting the whole codebase.
- **Real-World Use Cases** — every agent targets a useful automation or productivity workflow.

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

---

## 🏗️ Project Structure

```bash
Ai_agents/
├── public/
│   └── img.png
├── projects/
│   ├── scraper/
│   ├── podcast/
│   ├── stock/
│   ├── github/
│   ├── notion/
│   └── rag/
├── requirements.txt
└── README.md
```

Each folder inside `projects/` contains an individual agent with its own logic, tools, and execution flow.

---

## 🛠️ Tech Stack

- **Python** — core programming language
- **LangGraph** — agent workflow orchestration
- **LangChain** — LLM application framework
- **MCP SDK** — tool integration using Model Context Protocol
- **OpenRouter / Groq / LLM Providers** — model access and reasoning
- **Streamlit** — UI layer for selected agents
- **Tavily / Firecrawl** — web search and scraping
- **ElevenLabs** — text-to-speech generation
- **GitHub API / PyGithub** — GitHub automation
- **Notion API** — Notion workspace automation

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

---

## 🔐 Environment Variables

Create a `.env` file in the root directory or inside the specific agent folder depending on the agent you are running.

Example:

```env
OPENAI_API_KEY=your_openai_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
FIRECRAWL_API_KEY=your_firecrawl_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
GITHUB_TOKEN=your_github_token
NOTION_API_KEY=your_notion_api_key
```

> You only need the keys required by the specific agent you want to run.

---

## ▶️ Usage

Move into the agent folder you want to run:

```bash
cd projects/scraper
```

Run the main Python file for that agent:

```bash
python main.py
```

Some agents may use Streamlit:

```bash
streamlit run app.py
```

If a specific agent has a different entry file, check that agent folder and run the relevant Python file.

---

## 🧩 Adding a New Agent

To add a new agent, create a new folder inside `projects/`:

```bash
projects/my-new-agent/
```

Recommended structure:

```bash
my-new-agent/
├── main.py
├── tools.py
├── prompts.py
├── graph.py
└── README.md
```

A good agent should have:

- A clear goal
- Well-defined tools
- Strong prompt design
- Proper error handling
- Consistent input and output format
- Documentation explaining how to run it

---

## 🗺️ Roadmap

- [ ] Add a unified FastAPI backend for running all agents from one API
- [ ] Add a frontend dashboard for selecting and executing agents
- [ ] Add shared response format for all agents
- [ ] Add Docker support
- [ ] Add per-agent README files
- [ ] Add tests for core agent workflows
- [ ] Add centralized logging and tracing
- [ ] Add deployment guide

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

You can contribute by:

- Improving existing agents
- Adding new agents
- Fixing bugs
- Improving documentation
- Adding examples and demos
- Creating better UI or API integrations

---

## 📌 Notes

This project is built for learning, experimentation, and showcasing practical AI automation patterns. Some agents may require paid or rate-limited APIs, so make sure your environment variables are configured correctly before running them.

---

## 👤 Author

**Suraj Jena**

- LinkedIn: [Suraj Jena](https://www.linkedin.com/in/suraj-jena-0991a121a/)
- X/Twitter: [@jenasuraj_](https://x.com/jenasuraj_)

---

<p align="center">
  Built with ❤️ using LangGraph, LangChain, MCP, and Python.
</p>
