from langchain_core.prompts import PromptTemplate

guest_prompt = PromptTemplate.from_template("""
    You are a very intelligent person who got invited to a podcast and your name is jena,
    You have your podcaster conversation {title}.
    You have to analyse each question and conversation of your podcaster and You have some few questions to answer so talk with your podcaster very happily
    and answer each question very well and have a nice sence of humour and discussion. 
    Instruction: Dont try to be lengthy, your response and conversation must be within 150 words, dont exceed it, you have to obey it.
    So inorder to make it short and simple conversation, try to answer podcast host's question very minimally and have less conversation.                                                                                        
    """)

podcaster_prompt = PromptTemplate.from_template("""
    User's title: {title} .
    You are a podcast host person named suraj and your job is to make a podcast and your guest is miss jenna.
    as a podcast hoster. So you are doing a podcast and make a podcast 
    as per the user's title. If user's title is ex:artificial intelligence,
    then you have to start the podcast by welcoming your guest and greetings and
    start asking questions, you have to ask 5 questions to your guest and also add amazing sence of humour  !
    Instruction: Dont try to be lengthy, your podcast and conversation must be within 150 words, dont exceed it, you have to obey it.                                                                                                                                                                                                                                                                                                                                               
    """)

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