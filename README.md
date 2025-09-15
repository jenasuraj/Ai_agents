# <div align="center">Ai agents with mcp and langgraph</div>

<div align="center">
Welcome to the hub of specialized AI agents. This repository is a cutting-edge demonstration of multi-agent systems, where each agent is a master of its domain. Built on a robust foundation of **LangGraph** and **LangChain**, these agents leverage the Model Context Protocol (MCP) for seamless tool integration and use powerful LLMs via **OpenRouter** to reason, execute, and deliver intelligent results. From scraping the web and generating podcasts to analyzing stocks and managing GitHub repositories, this project showcases the power of modular, AI-driven automation.
</div>

---

## 🧭 Agent Overview

| Agent | Name | Primary Function | Key Tools & APIs |
| :--- | :--- | :--- | :--- |
| **Agent-1** | **Scrapper Agent** | Intelligent web research & data extraction | Tavily, Firecrawl, OpenWeather |
| **Agent-2** | **AuralAI (Podcast Agent)** | Dynamic podcast generation & text-to-speech | ChatGroq, ElevenLabs, Streamlit |
| **Agent-3** | **Stock Agent** | Real-time financial market analysis & news | Alpha Vantage, NSE, MoneyControl |
| **Agent-4** | **GitHub Agent** | Automated repository management & documentation | GitHub API, MCP SDK, PyGithub |
| **Agent-5** | **Notion Copilot** | Research, content structuring & Notion automation | Notion API, Tavily, Firecrawl |






# Scrapper Agent (Agent-1)
Scrapper Agent (Agent-1) is an intelligent assistant that can search the web, scrape detailed content from URLs, and fetch real-time weather information. It uses a reasoning agent to decide which tool to call, providing accurate and structured responses to user queries.

## Features
- **Web Search (Tavily API)** → Finds relevant URLs for queries
- **Content Scraping (Firecrawl API)** → Extracts detailed content (Markdown/HTML) from URLs
- **Weather Lookup (OpenWeather API)** → Provides real-time temperature for any city
- **Reasoning Agent** → Uses `create_react_agent` to choose the right tool automatically

## Tech Stack
- Python 3.9+
- LangGraph (state-based graph execution)
- LangChain (LLM orchestration + tools)
- OpenRouter LLMs (Google Gemini 2.5 Flash in this setup)
- Firecrawl API (content scraping)
- Tavily API (URL extraction/search)
- OpenWeather API (weather data)


# Podcast Agent (Agent-2)
AuralAI is an AI-powered podcast agent that can generate engaging podcasts on any topic. It orchestrates conversations between a host (podcaster) and a guest using LLMs and converts the conversation into lifelike audio using ElevenLabs TTS.

## Features
- **Dynamic Podcast Generation** → Creates structured conversations between host and guest based on user input
- **Short, Engaging Dialogue** → Limits content to 150–250 words for concise podcasts
- **Humor & Personality** → Adds personality and humor in the conversation
- **Text-to-Speech (ElevenLabs)** → Converts podcaster and guest text into high-quality audio
- **Streamlit UI** → Allows users to input a podcast topic and play generated audio

## Tech Stack
- LangGraph (state-based graph execution)
- LangChain & ChatGroq (LLM orchestration)
- OpenRouter LLMs (Google Gemini 2.5 Flash)
- ElevenLabs API (Text-to-Speech)
- Streamlit (interactive web interface)


# Stock Agent (Agent-3)
Stock Agent (Agent-3) is an AI-powered financial assistant that provides real-time and historical stock market data, financial news, and community sentiment analysis. It integrates multiple APIs and scraping tools to deliver structured insights and uses a reasoning agent to decide the best data source for a given query.

## Features
- **Market Data (Alpha Vantage API)** → Fetches stock prices, indicators, and company data
- **Indian Market Data (NSE / MoneyControl via Firecrawl)** → Provides stock and index data from Indian markets
- **Financial News ( Firecrawl)** → Extracts news articles and performs sentiment analysis
- **Reasoning Agent** → Uses `create_react_agent` to automatically decide whether to pull data from markets, news, or social sentiment

## Tech Stack
- Python 3.9+
- LangGraph (state-based graph execution)
- LangChain (LLM orchestration + tools)
- OpenRouter LLMs (Google Gemini 2.5 Flash)
- Alpha Vantage API (global stock data)
- NSE / MoneyControl (Indian stock data)
- Firecrawl API (financial news scraping)



# GitHub Agent (Agent-4)
GitHub Agent (Agent-4) is an AI-powered assistant that can interact with GitHub repositories using Model Context Protocol (MCP). It can read, analyze, and update repository files, particularly focusing on maintaining and improving README.md documentation.

## Features
- **Repository Access (MCP)** → Connects to GitHub repositories via Model Context Protocol
- **File Reading & Analysis** → Examines repository structure and existing documentation
- **README Management** → Updates, enhances, and maintains README.md files
- **Content Generation** → Creates comprehensive documentation based on code analysis
- **Version Control Integration** → Commits changes with meaningful messages

## Tech Stack
- Model Context Protocol (MCP) SDK
- GitHub REST API
- PyGithub library
- LangGraph (state-based graph execution)
- LangChain (LLM orchestration + tools)
- OpenRouter LLMs (Google Gemini 2.5 Flash)