import os
import requests
import json

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- 1. HOROSCOPE GENERATION ---
def generate_horoscope_reading(predictions, chart_meta):
    rich_context = chart_meta.get('fact_sheet', '')
    asc_sign = chart_meta.get('ascendant_sign', 'Unknown')

    system_instruction = """
    You are an empathetic, wise, and highly skilled Vedic Astrologer.
    Your goal is to translate technical planetary positions into a **Holistic Life Analysis**.
    
    **AUDIENCE:** The user is a layperson. Do NOT use technical jargon without explaining it.
    
    **TONE:** - **Balanced:** Reframe "Brutally Honest Notes" as "Karmic Shadows" or "Psychological Challenges".
    - **Empowering:** If a prediction is negative, frame it as "Requires conscious effort."
    - **Remedial:** Suggest a mindset shift for every problem.

    **STRUCTURE:**
    Organize the output into these exact Markdown sections:
    ### 🦁 Self & Personality
    ### 💼 Career, Wealth & Purpose
    ### ❤️ Love, Relationships & Family
    ### 🧘 Health & Inner Well-being
    ### 🔮 Karmic Path & Remedial Guidance

    **DATA USAGE:**
    - Use the provided "DATA CONTEXT" to form your opinions.
    """

    user_message = f"""
    *** ASTROLOGICAL DATA ***
    Ascendant: {asc_sign}
    {rich_context}
    *** INSTRUCTIONS ***
    Analyze this data and generate the 5-section Life Report.
    """

    return call_llm(system_instruction, user_message)

# --- 2. CHATBOT FUNCTION (THE MISSING PIECE) ---
def chat_with_astrologer(user_query, chart_context):
    system_instruction = """
    You are PanditAI, a wise and empathetic Vedic Astrologer.
    You have access to the user's specific birth chart details in the Context provided.
    
    RULES:
    1. **Personalize:** Always refer to the specific planetary placements in the context.
    2. **Be Honest but Kind:** If the context mentions negative traits, guide them on how to overcome them.
    3. **Stay Relevant:** Only answer astrological questions.
    4. **Concise:** Keep answers under 150 words.
    """

    user_message = f"CONTEXT:\n{chart_context}\n\nUSER QUESTION:\n{user_query}"
    return call_llm(system_instruction, user_message)

# --- 3. HELPER: CALL LLM ---
def call_llm(system_instruction, user_message):
    if GROQ_API_KEY:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.5,
            "max_tokens": 1500
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"Error connecting to Groq: {e}"
    else:
        # Local Ollama Fallback
        OLLAMA_URL = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3.2",
            "prompt": f"{system_instruction}\n\n{user_message}",
            "stream": False,
            "temperature": 0.5
        }
        try:
            response = requests.post(OLLAMA_URL, json=payload)
            return response.json()['response']
        except Exception as e:
            return f"Error connecting to Ollama: {e}"