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