import os
import base64
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
load_dotenv()
from langgraph.prebuilt import create_react_agent
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage
from langchain_groq.chat_models import ChatGroq
import re
import json

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
llm = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL"),
    model="google/gemini-2.5-flash",
    #temperature=0.5,
    top_p=0.3,)
groq_llm = ChatGroq(model="openai/gpt-oss-20b")


class State(TypedDict):
    podcaster_data:Annotated[list,add_messages]
    guest_data:Annotated[list,add_messages]
    messages:Annotated[list,add_messages]


def podcaster(state:State):
    print("Entered podcaster node...")
    title = state["messages"][-1].content
    podcaster_prompt = PromptTemplate.from_template("""
    User's title: {title} .
    You are a podcast host person named suraj and your job is to make a podcast and your guest is miss jenna.
    as a podcast hoster. So you are doing a podcast and make a podcast 
    as per the user's title. If user's title is ex:artificial intelligence,
    then you have to start the podcast by welcoming your guest and greetings and
    start asking questions, you have to ask 5 questions to your guest and also add amazing sence of humour  !
    Instruction: Dont try to be lengthy, your podcast and conversation must be within 150 words, dont exceed it, you have to obey it.                                                                                                                                                                                                                                                                                                                                               
    """)
    podcaster_chain = podcaster_prompt | groq_llm
    response = podcaster_chain.invoke({"title":title})
    return{
        "podcaster_data":[AIMessage(content=response.content)]
    }


def guest(state:State):
    print("Entered guest node...")
    podcast_data = state["podcaster_data"][-1].content
    guest_prompt = PromptTemplate.from_template("""
    You are a very intelligent person who got invited to a podcast and your name is jena,
    You have your podcaster conversation {title}.
    You have to analyse each question and conversation of your podcaster and You have some few questions to answer so talk with your podcaster very happily
    and answer each question very well and have a nice sence of humour and discussion. 
    Instruction: Dont try to be lengthy, your response and conversation must be within 150 words, dont exceed it, you have to obey it.
    So inorder to make it short and simple conversation, try to answer podcast host's question very minimally and have less conversation.                                                                                        
    """)
    guest_chain = guest_prompt | groq_llm
    response = guest_chain.invoke({"title":podcast_data})
    return{
        "guest_data":[AIMessage(content=response.content)]
    }
    


def final_agent(state:State):
    print("entered final agent ...")
    podcast_data = state["podcaster_data"][-1].content
    guest_data = state["guest_data"][-1].content
    prompt = PromptTemplate.from_template("""
    You are the final agent. Your task is to structure a conversation between a podcaster and a guest.
    Input:
    Podcaster: {podcaster}
    Guest: {guest}

    Requirements:
    1. Strictly use ONLY the keys "podcaster" and "guest".
    2. Remove all emojis, musical text, sound effects, and any special symbols.
    3. Use plain English only.
    4. Structure the conversation as a JSON array of turns.
    5. Each turn should be a dict with both keys, even if one side just replies with a simple greeting.
    6. Do NOT include any extra keys or commentary.
    7. You must return JSON with only 250 words total. 
       Count each word carefully. Do not exceed 250 words.
                                     
    Example output:
    [
    {{"podcaster": "Hello, welcome to our show."}},
    {{"guest": "Sure, I studied AI research."}}
    ]
    Output must be **valid JSON**.
    """)
    final_message = {"podcaster":podcast_data,"guest":guest_data} 
    final_chain = prompt | llm
    response = final_chain.invoke(final_message)
    return{
        "messages":[AIMessage(content=response.content)]
    }


# Build graph
graph_builder = StateGraph(State)
graph_builder.add_node("podcaster", podcaster)
graph_builder.add_node("guest", guest)
graph_builder.add_node("final_agent", final_agent)
graph_builder.add_edge(START, "podcaster")
graph_builder.add_edge("podcaster", "guest")
graph_builder.add_edge("guest", "final_agent")
graph_builder.add_edge("final_agent", END)
graph = graph_builder.compile()



# Streamlit app
st.title("AuralAI ⚛")
data = st.text_input("Enter the title of the podcast:")

if st.button("Submit"):
    with st.spinner("Generating podcast and audio, please wait..."):
        initial_state = {"messages": [{"role": "user", "content": data}]}
        response = graph.invoke(initial_state)

        if response:
            text = response["messages"][-1].content
            clean_json_str = re.sub(r"^```json\s*|```$", "", text.strip(), flags=re.MULTILINE)
            final_response = json.loads(clean_json_str)
            
            voice_collection = []
            for item in final_response:
                if item.get("podcaster"):
                    podcaster_tts = client.text_to_speech.convert(
                        text=item["podcaster"],
                        voice_id="nPczCjzI2devNBz1zQrb",
                        model_id="eleven_multilingual_v2",
                        output_format="mp3_44100_128",
                        voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.7)
                    )
                    if podcaster_tts:
                        voice_collection.append(podcaster_tts)

                if item.get("guest"):
                    guest_tts = client.text_to_speech.convert(
                        text=item["guest"],
                        voice_id="eRALiEwGnmo3g1ze76Y2",
                        model_id="eleven_multilingual_v2",
                        output_format="mp3_44100_128",
                        voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.7)
                    )
                    if guest_tts:
                        voice_collection.append(guest_tts)

            # Combine all audio bytes
            audio_bytes = b"".join(chunk for voice_gen in voice_collection for chunk in voice_gen)
            audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
            
            st.audio(f"data:audio/mp3;base64,{audio_base64}", format="audio/mp3")