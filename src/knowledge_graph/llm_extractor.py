import requests
import json
import os
import re

# Connect to your local Llama 3
OLLAMA_URL = "http://localhost:11434/api/generate"

def clean_json_string(s):
    """
    Robust helper to extract JSON from LLM's response.
    Handles Markdown code blocks and chatty preambles.
    """
    # 1. Try to find content within ```json ... ``` blocks
    match = re.search(r'```json\s*(\[.*?\])\s*```', s, re.DOTALL)
    if match:
        return match.group(1)
    
    # 2. Try to find content within standard brackets [ ... ]
    match = re.search(r'\[.*\]', s, re.DOTALL)
    if match:
        return match.group(0)
        
    return s

def extract_logic_from_text(raw_text_path):
    print(f"📖 Reading raw text from {raw_text_path}...")
    
    if not os.path.exists(raw_text_path):
        print(f"❌ File not found: {raw_text_path}")
        return []
    
    with open(raw_text_path, 'r', encoding='utf-8') as f:
        text_content = f.read()

    # --- THE INDUSTRY-LEVEL PROMPT ---
    # We strictly enforce the "Yoga" structure (Condition + Modification = Result)
    system_prompt = """
    You are an Expert Vedic Astrologer. Extract structured rules from the text.
    
    CRITICAL FOCUS: "Lordship" Rules.
    - Look for patterns like "Lord of the 5th in the 9th" or "Ruler of Dharma in Karma Bhava".
    - These are the most important rules to extract.

    JSON Schema:
    {
        "id": "rule_unique_id",
        "type": "lordship_placement",  <-- NEW TYPE
        "entities": ["Sun", "Moon", "5th Lord", "9th Lord"],
        "main_condition": "5th Lord in 9th House",
        "result": "The native will be extremely fortunate and a teacher of dharma.",
        "source": "BPHS Ch 24"
    }
    """

    print("🧠 Sending to Llama 3 for Deep Extraction (Finding Yogas)...")
    
    payload = {
        "model": "llama3.2",
        "prompt": f"{system_prompt}\n\nRAW TEXT TO ANALYZE:\n{text_content}\n\nJSON OUTPUT:",
        "stream": False,
        "context_window": 4096, # Ensure enough context for larger chapters
        "temperature": 0.1      # Keep it strict
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result_text = response.json()["response"]
        
        # Clean and Parse
        json_str = clean_json_string(result_text)
        data = json.loads(json_str)
        
        # Validation: Ensure it's a list
        if not isinstance(data, list):
            print("⚠️ Warning: Output was not a list. Wrapping it.")
            data = [data]

        output_path = "./data/processed_graph/extracted_rules.json"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        print(f"✅ Successfully extracted {len(data)} Complex Yogas!")
        print(f"📂 Saved to {output_path}")
        print("👉 NEXT STEP: Run 'ingest_vectors.py' to update the Graph.")
        return data
        
    except json.JSONDecodeError:
        print("❌ JSON Decode Error. The model output was not valid JSON.")
        print("Partial Output:", result_text[:500])
        return []
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        return []

if __name__ == "__main__":
    # Point this to your specific text file
    extract_logic_from_text("./data/raw_texts/bphs_chapter_24.txt")