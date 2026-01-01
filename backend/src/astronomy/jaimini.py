def get_chara_karakas(chart_data, include_rahu=False):
    """
    Calculates Jaimini Chara Karakas (AK, AmK, etc.) based on planetary degrees.
    """
    
    # 1. Select candidates (usually 7 planets: Sun through Saturn)
    valid_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    if include_rahu:
        valid_planets.append("Rahu")
        
    candidates = []
    
    for p_name in valid_planets:
        if p_name not in chart_data:
            continue
            
        p_data = chart_data[p_name]
        
        # Jaimini comparisons are based on degree within the sign (0-30), 
        # ignoring the sign itself.
        candidates.append({
            "name": p_name,
            "degree": p_data["degree"],
            "sign": p_data["sign_id"]
        })
    
    # 2. Sort Descending by Degree
    # Logic: Highest degree = Atmakaraka (AK)
    sorted_planets = sorted(candidates, key=lambda x: x["degree"], reverse=True)
    
    # 3. Assign Roles (Standard 7-Karaka Scheme)
    roles = [
        "Atmakaraka (AK)",      # Self
        "Amatyakaraka (AmK)",   # Career
        "Bhatrikaraka (BK)",    # Siblings
        "Matrikaraka (MK)",     # Mother
        "Putrakaraka (PK)",     # Children
        "Gnatikaraka (GK)",     # Relations/Rivals
        "Darakaraka (DK)"       # Spouse
    ]
    
    results = {}
    
    # Assign available planets to roles
    count = min(len(sorted_planets), len(roles))
    for i in range(count):
        results[roles[i]] = sorted_planets[i]
        
    return results