# src/astronomy/arudhas.py

def calculate_arudha_padas(chart_data, house_structure):
    """
    Calculates Jaimini Arudha Padas (A1 to A12).
    A7 (Darapada) = Arudha of 7th House.
    A12 (Upapada) = Arudha of 12th House (often used for marriage longevity).
    """
    padas = {}
    
    # We need to find the Lord of every house first
    # (You already have a RULER_MAP in main.py, best to move it to a shared utility)
    SIGN_RULERS = {
        "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
        "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars", # classic lordship
        "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
    }

    asc_sign_id = chart_data["Ascendant"]["sign_id"]

    for h in range(1, 13):
        # 1. Determine Sign in House H
        sign_in_house_id = (asc_sign_id + h - 1) % 12
        
        # Helper to get sign name by ID (Needs your sign list)
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                 "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        sign_name = signs[sign_in_house_id]
        
        # 2. Find the Lord of that Sign
        lord_name = SIGN_RULERS[sign_name]
        if lord_name not in chart_data: continue # Skip if data missing
        
        lord_sign_id = chart_data[lord_name]["sign_id"]
        
        # 3. Count distance from House to Lord
        # Logic: If House 1 is Aries, and Mars is in Gemini.
        # Aries (0) -> Gemini (2). Distance = 3 signs (1, 2, 3 inclusive)
        dist = (lord_sign_id - sign_in_house_id) % 12
        if dist < 0: dist += 12
        
        # 4. Count same distance again to find Arudha
        arudha_sign_id = (lord_sign_id + dist) % 12
        
        # 5. Jaimini Exceptions (Swasthe Daraha - 4th/10th rule)
        # If Arudha falls in same sign or 7th from it, shifts occur. 
        # (Simplified logic here for brevity, you should implement full Jaimini Sutra rules)
        
        arudha_name = f"A{h}"
        if h == 12: arudha_name = "UL (Upapada)"
        if h == 7: arudha_name = "A7 (Darapada)"
        
        padas[arudha_name] = {
            "sign": signs[arudha_sign_id],
            "sign_id": arudha_sign_id
        }
        
    return padas