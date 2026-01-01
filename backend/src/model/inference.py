import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def generate_horoscope_reading(predictions, chart_meta):
    fact_context = chart_meta.get("fact_sheet", "")

    # Format the rules
    rules_text = ""
    if predictions:
        for item in predictions:
            r_type = item.get("type", "General")
            r_text = item.get("rule", "")
            rules_text += f"- [Potential Rule for {r_type}] {r_text}\n"
    else:
        rules_text = (
            "No specific text rules found. Rely strictly on planetary positions."
        )

    # --- 1. SYSTEM INSTRUCTION (The Persona) ---
    system_instruction = """
    You are PanditAI, an expert Vedic Astrologer.
    You MUST return ONLY valid JSON. No markdown, no explanations, no extra text.
    
    The JSON must have EXACTLY these 6 keys:
    - personality
    - health
    - money
    - career
    - love
    - miscellaneous
    
    Each value must be a detailed, insightful string (2-3 paragraphs) based on Vedic astrology principles.
    """

    # --- 2. USER MESSAGE (The Data) ---
    user_message = f"""
    Analyze this birth chart and return STRICT JSON format.
    
    CHART DATA:
    {fact_context}
    
    REFERENCE RULES:
    {rules_text}
    
    Return astrology prediction in STRICT JSON format.
    
    Keys must be exactly:
    personality
    health
    money
    career
    love
    miscellaneous
    
    Each value must be a string (2-3 detailed paragraphs).
    Do NOT add any extra keys.
    Do NOT add explanations.
    Do NOT add markdown.
    Do NOT wrap in code blocks.
    
    Return ONLY the raw JSON object.
    """

    # --- THE BRAIN SWITCHER ---

    # OPTION A: CLOUD (Groq)
    if GROQ_API_KEY:
        print("☁️ Using Groq Cloud Brain...")
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            # "llama-3.3-70b-versatile" is the newest, most robust model
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_message},
            ],
            "temperature": 0.1,
            "max_tokens": 7000,
        }
        try:
            response = requests.post(url, json=payload, headers=headers)

            # --- DEBUG BLOCK: PRINT ERROR DETAILS IF FAILED ---
            if response.status_code != 200:
                print(f"  Groq API Error: {response.status_code}")
                print(f"  Details: {response.text}")
                response.raise_for_status()

            raw_content = response.json()["choices"][0]["message"]["content"]

            # Parse and validate JSON
            try:
                parsed_json = json.loads(raw_content)

                # Validate required keys
                required_keys = {
                    "personality",
                    "health",
                    "money",
                    "career",
                    "love",
                    "miscellaneous",
                }
                if not all(key in parsed_json for key in required_keys):
                    print(
                        "⚠️ Warning: LLM response missing required keys, returning raw content"
                    )
                    return raw_content

                return parsed_json
            except json.JSONDecodeError as e:
                print(f"⚠️ Warning: Could not parse JSON from LLM: {e}")
                print(f"Raw content: {raw_content[:200]}...")
                return raw_content

        except Exception as e:
            return f"Cloud Brain Error: {str(e)}"

    # OPTION B: LOCAL (Ollama)
    else:
        print("💻 Using Local Ollama Brain...")
        OLLAMA_URL = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3.2",
            "prompt": f"{system_instruction}\n\n{user_message}",
            "stream": False,
            "temperature": 0.1,
            "num_ctx": 8192,
        }
        try:
            response = requests.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            return f"Local Brain Error: {str(e)}"


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

    # Reuse the same logic for calling LLM (simplified for brevity, usually refactor into helper)
    if GROQ_API_KEY:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_message},
            ],
            "temperature": 0.5,
            "max_tokens": 1500,
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {e}"
    else:
        # Fallback to Ollama
        return "Chat feature requires Cloud Brain for best results."
