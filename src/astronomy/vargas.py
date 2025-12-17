def calculate_d9_navamsa(absolute_longitude):
    """
    Calculates the Sign ID (0-11) of a planet in the Navamsa (D-9) chart.
    
    Algorithm:
    1. A sign is 30 degrees. D-9 divides it into 9 parts of 3deg 20min (3.333 deg).
    2. The mapping depends on the element of the Rashi sign (Fire, Earth, Air, Water).
    """
    
    rashi_sign_id = int(absolute_longitude // 30)
    degree_in_sign = absolute_longitude % 30
    
    # 1. Determine the 'pada' (segment 0-8)
    # 30 degrees / 9 segments = 3.33333 degrees per segment
    pada_length = 30.0 / 9.0
    pada = int(degree_in_sign / pada_length)
    
    # 2. Determine start sign based on Element of Rashi
    # Fire (Aries, Leo, Sag) -> Starts from Aries (0)
    # Earth (Taurus, Virgo, Cap) -> Starts from Capricorn (9)
    # Air (Gemini, Libra, Aq) -> Starts from Libra (6)
    # Water (Cancer, Scorpio, Pisces) -> Starts from Cancer (3)
    
    element_remainder = rashi_sign_id % 4
    start_sign = 0
    
    if element_remainder == 0:   # Fire
        start_sign = 0 
    elif element_remainder == 1: # Earth
        start_sign = 9
    elif element_remainder == 2: # Air
        start_sign = 6
    elif element_remainder == 3: # Water
        start_sign = 3
        
    # 3. Calculate Final D9 Sign
    d9_sign_id = (start_sign + pada) % 12
    
    return d9_sign_id