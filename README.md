# Scrapper Agent (Agent-1)
Scrapper Agent (Agent-1) is an intelligent assistant that can search the web, scrape detailed content from URLs, and fetch real-time weather information. It uses a reasoning agent to decide which tool to call, providing accurate and structured responses to user queries

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
