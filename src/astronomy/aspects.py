# src/astronomy/aspects.py

def get_planet_aspects(chart_data):
    """
    Calculates Parashari Aspects (Drishti).
    Returns a list of strings describing interactions.
    """
    aspects_log = []
    
    # Standard Parashari Aspect Rules (Offsets from planet position)
    # Every planet aspects the 7th house from itself.
    # Mars: 4, 7, 8
    # Jupiter: 5, 7, 9
    # Saturn: 3, 7, 10
    
    ASPECT_RULES = {
        "Mars": [4, 7, 8],
        "Jupiter": [5, 7, 9],
        "Saturn": [3, 7, 10],
        "Rahu": [5, 7, 9], # Often considered similar to Jupiter in some traditions
        "Ketu": [],
        "Sun": [7], "Moon": [7], "Mercury": [7], "Venus": [7]
    }
    
    for looker_name, looker_data in chart_data.items():
        if looker_name == "Ascendant" or looker_name == "Ketu": continue
        
        looker_sign = looker_data["sign_id"]
        rules = ASPECT_RULES.get(looker_name, [7])
        
        for offset in rules:
            # Calculate the target sign index (0-11)
            # -1 because counting starts from the planet itself
            target_sign_id = (looker_sign + offset - 1) % 12
            
            # Check if any planet is in that target sign
            for target_name, target_data in chart_data.items():
                if target_name == "Ascendant" or target_name == looker_name: continue
                
                if target_data["sign_id"] == target_sign_id:
                    # Logic: Saturn in Aries (0) aspects Libra (6) -> 7th aspect
                    aspects_log.append(f"{looker_name} casts {offset}th aspect on {target_name}")
                    
    return aspects_log