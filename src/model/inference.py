import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_horoscope_reading(predictions, chart_meta):
    
    fact_context = chart_meta.get('fact_sheet', '')
    asc_sign = chart_meta.get('ascendant_sign', 'Unknown')
    asc_ruler = chart_meta.get('ascendant_ruler', 'Unknown')

    # Format the rules for the LLM
    rules_text = ""
    if predictions:
        for item in predictions:
            r_type = item.get("type", "General")
            r_text = item.get("rule", "")
            rules_text += f"- [Potential Rule for {r_type}] {r_text}\n"
    else:
        rules_text = "No specific text rules found. Rely strictly on planetary positions."

    # --- THE "COMPLETE HOROSCOPE" PROMPT ---
    system_prompt = f"""
    You are PanditAI, an exhaustive and detailed Vedic Astrologer.
    
    MISSION:
    Generate a complete Birth Chart analysis covering ALL Planets and ALL 12 Houses.
    You must be systematic. Do not skip any house.

    ---------------------------------------------------
    PART 1: THE FACTS (Absolute Truth)
    {fact_context}
    ---------------------------------------------------
    
    PART 2: THE LIBRARY (Reference Rules)
    {rules_text}
    ---------------------------------------------------

    OUTPUT STRUCTURE:

    **1. Lagna (The Self)**
    - Analyze the Ascendant ({asc_sign}) and the placement of its Ruler ({asc_ruler}). 
    - What does this say about the person's vitality and general nature?

    **2. The 9 Grahas (Planetary Details)**
    - Iterate through Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, and Ketu.
    - For EACH, state: "Planet in [Sign] in [House]." then give a 1-sentence interpretation.

    **3. The 12 Bhavas (House-by-House Lordship Analysis)**
    *CRITICAL INSTRUCTION: You must output a bullet point for EVERY House from 1 to 12.*
    *For each house, identify the Ruler (Lord) based on the sign in that house, and see where that Lord is placed.*
    
    - **1st House (Self):** Sign is {asc_sign}. Lord is {asc_ruler} placed in House [X]. Result?
    - **2nd House (Wealth/Speech):** Lord is placed in House [X]...
    - **3rd House (Siblings/Courage):** Lord is placed in House [X]...
    - **4th House (Mother/Home):** Lord is placed in House [X]...
    - **5th House (Children/Intelligence):** Lord is placed in House [X]...
    - **6th House (Enemies/Health):** Lord is placed in House [X]...
    - **7th House (Partnership):** Lord is placed in House [X]...
    - **8th House (Transformation/Longevity):** Lord is placed in House [X]...
    - **9th House (Dharma/Fortune):** Lord is placed in House [X]...
    - **10th House (Career/Karma):** Lord is placed in House [X]...
    - **11th House (Gains/Network):** Lord is placed in House [X]...
    - **12th House (Loss/Liberation):** Lord is placed in House [X]...

    **4. Final Synthesis**
    - Summarize the strongest area of life based on the chart.

    **CONSTRAINTS:**
    - Use the FACTS section to find where the Lords are located. 
    - Example: If 2nd House is Leo, Lord is Sun. If Facts say "Sun in 11th", then say "2nd Lord in 11th creates a Dhan Yoga (Wealth through networks)."
    - Do not hallucinate positions.

    Generate the full report now.
    """

    payload = {
        "model": "llama3.2",
        "prompt": system_prompt,
        "stream": False,
        "temperature": 0.1, 
        "num_ctx": 8192 # Increased context window to handle the longer output
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"Error: {str(e)}"