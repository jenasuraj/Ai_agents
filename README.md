# Scrapper Agent (Agent-1)

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
