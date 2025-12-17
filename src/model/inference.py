import os
import requests
import json

# Try to get the Groq Key from the environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_horoscope_reading(predictions, chart_meta):
    
    fact_context = chart_meta.get('fact_sheet', '')
    asc_sign = chart_meta.get('ascendant_sign', 'Unknown')
    asc_ruler = chart_meta.get('ascendant_ruler', 'Unknown')

    # Format the rules
    rules_text = ""
    if predictions:
        for item in predictions:
            r_type = item.get("type", "General")
            r_text = item.get("rule", "")
            rules_text += f"- [Potential Rule for {r_type}] {r_text}\n"
    else:
        rules_text = "No specific text rules found. Rely strictly on planetary positions."

    # --- 1. SYSTEM INSTRUCTION (The Persona) ---
    system_instruction = """
    You are PanditAI, an exhaustive and detailed Vedic Astrologer.
    Your mission is to generate a complete Birth Chart analysis covering ALL Planets and ALL 12 Houses.
    Do not summarize. Be systematic.
    """

    # --- 2. USER MESSAGE (The Data) ---
    user_message = f"""
    Here is the birth chart data you must analyze.
    
    PART 1: THE FACTS (Absolute Truth)
    {fact_context}
    
    PART 2: THE LIBRARY (Reference Rules)
    {rules_text}
    
    OUTPUT STRUCTURE REQUIRED:
    **1. Lagna (The Self)**: Analyze Ascendant ({asc_sign}) and Ruler ({asc_ruler}).
    **2. The 9 Grahas**: Iterate through Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu.
    **3. The 12 Bhavas**: Bullet point for EVERY House 1-12. Identify Ruler and placement.
    **4. Final Synthesis**: Summary.
    
    CONSTRAINTS:
    - Use FACTS to find Lords. Do not hallucinate.
    - If a rule contradicts the facts, trust the facts.
    """

    # --- THE BRAIN SWITCHER ---
    
    # OPTION A: CLOUD (Groq)
    if GROQ_API_KEY:
        print("☁️ Using Groq Cloud Brain...")
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            # "llama-3.3-70b-versatile" is the newest, most robust model
            "model": "llama-3.3-70b-versatile", 
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_message} # <--- SPLIT INTO USER MSG
            ],
            "temperature": 0.1,
            "max_tokens": 7000 
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            
            # --- DEBUG BLOCK: PRINT ERROR DETAILS IF FAILED ---
            if response.status_code != 200:
                print(f"❌ Groq API Error: {response.status_code}")
                print(f"❌ Details: {response.text}") # <--- THIS WILL SHOW THE REAL REASON
                response.raise_for_status()
                
            return response.json()['choices'][0]['message']['content']
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
            "num_ctx": 8192
        }
        try:
            response = requests.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            return f"Local Brain Error: {str(e)}"