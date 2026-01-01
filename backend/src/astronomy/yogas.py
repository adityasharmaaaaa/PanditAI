class YogaEngine:
    def __init__(self):
        # 1. SIGN LORDS (0=Aries ... 11=Pisces)
        self.SIGN_LORDS = {
            0: "Mars", 1: "Venus", 2: "Mercury", 3: "Moon", 4: "Sun", 5: "Mercury",
            6: "Venus", 7: "Mars", 8: "Jupiter", 9: "Saturn", 10: "Saturn", 11: "Jupiter"
        }
        
        # 2. DIGNITY RULES (Strict 0-based Integers)
        # Exaltation Signs: Sun(0), Moon(1), Mars(9), Mer(5), Jup(3), Ven(11), Sat(6)
        self.EXALTATION = {
            "Sun": 0, "Moon": 1, "Mars": 9, "Mercury": 5, 
            "Jupiter": 3, "Venus": 11, "Saturn": 6
        }
        
        # Own Signs
        self.OWN_SIGNS = {
            "Sun": [4], "Moon": [3], "Mars": [0, 7], "Mercury": [2, 5],
            "Jupiter": [8, 11], "Venus": [1, 6], "Saturn": [9, 10]
        }
        
        # Debilitation Signs
        self.DEBILITATION = {
            "Sun": 6, "Moon": 7, "Mars": 3, "Mercury": 11, 
            "Jupiter": 9, "Venus": 5, "Saturn": 0
        }
    
    def get_house_lord(self, house_num_from_asc, asc_sign_id):
        """
        Returns the planet name ruling a specific house.
        house_num_from_asc: 1 to 12
        asc_sign_id: 0 to 11
        """
        # Formula: (Asc + House - 1) % 12
        sign_in_house = (int(asc_sign_id) + int(house_num_from_asc) - 1) % 12
        return self.SIGN_LORDS[sign_in_house]

    def check_yogas(self, chart):
        yogas_found = []
        
        # Safety Check
        if "Ascendant" not in chart: return []
        asc_sign = int(chart["Ascendant"]["sign_id"])
        
        # Helper: Get Sanitized Planet Data
        def get_p_data(planet):
            if planet in chart and chart[planet]:
                d = chart[planet]
                
                # 1. Get Sign ID (Force Int)
                s_id = int(d.get("sign_id", 0))
                
                # 2. Get House Number (Force Int, Calculate if missing)
                if "house_number" in d:
                    h_num = int(d["house_number"])
                else:
                    # Fallback Calc: (Sign - Asc) % 12 + 1
                    h_num = (s_id - asc_sign) % 12 + 1
                    
                return s_id, h_num
            return None, None

        # ==========================================
        # 1. PANCHA MAHAPURUSHA YOGAS
        # ==========================================
        # Rule: Planet in Own/Exalted Sign AND in Kendra (1, 4, 7, 10)
        p_configs = [
            ("Mars", "Ruchaka Yoga", "Divine strength, courage, and leadership."),
            ("Mercury", "Bhadra Yoga", "Intellect, wit, and communication skills."),
            ("Jupiter", "Hamsa Yoga", "Wisdom, spirituality, and respect."),
            ("Venus", "Malavya Yoga", "Luxury, beauty, and artistic success."),
            ("Saturn", "Sasa Yoga", "Authority, discipline, and political power.")
        ]
        
        for p_name, y_name, y_desc in p_configs:
            sid, hnum = get_p_data(p_name)
            
            if sid is not None and hnum is not None:
                # A. Check Placement (Must be Kendra)
                if hnum not in [1, 4, 7, 10]:
                    continue
                    
                # B. Check Dignity (Must be Own or Exalted)
                is_own = sid in self.OWN_SIGNS.get(p_name, [])
                is_exalt = sid == self.EXALTATION.get(p_name)
                
                if is_own or is_exalt:
                    yogas_found.append({"name": y_name, "category": "Mahapurusha", "desc": y_desc})

        # ==========================================
        # 2. RAJA YOGAS
        # ==========================================
        
        # Gaja Kesari: Jupiter in 1, 4, 7, 10 from Moon
        j_sid, _ = get_p_data("Jupiter")
        m_sid, _ = get_p_data("Moon")
        
        if j_sid is not None and m_sid is not None:
            # Distance: (Jupiter - Moon) % 12 + 1
            dist = (j_sid - m_sid) % 12 + 1
            if dist in [1, 4, 7, 10]:
                yogas_found.append({"name": "Gaja Kesari Yoga", "category": "Raja", "desc": "Fame, virtue, and lasting reputation."})

        # Dharma-Karmadhipati: 9th Lord & 10th Lord Conjunction
        lord9 = self.get_house_lord(9, asc_sign)
        lord10 = self.get_house_lord(10, asc_sign)
        
        l9_sid, _ = get_p_data(lord9)
        l10_sid, _ = get_p_data(lord10)
        
        if l9_sid is not None and l9_sid == l10_sid:
             yogas_found.append({"name": "Dharma-Karmadhipati Yoga", "category": "Raja", "desc": "Professional success and righteous power."})

        # ==========================================
        # 3. VIPREET RAJA YOGA (Corrected)
        # ==========================================
        # Harsha: 6th Lord in 6, 8, 12
        l6_planet = self.get_house_lord(6, asc_sign)
        _, l6_h = get_p_data(l6_planet)
        if l6_h in [6, 8, 12]:
             yogas_found.append({"name": "Harsha Yoga", "category": "Vipreet", "desc": "Invincibility against enemies and health resilience."})

        # Sarala: 8th Lord in 6, 8, 12
        l8_planet = self.get_house_lord(8, asc_sign)
        _, l8_h = get_p_data(l8_planet)
        if l8_h in [6, 8, 12]:
             yogas_found.append({"name": "Sarala Yoga", "category": "Vipreet", "desc": "Fearlessness, longevity, and success through risks."})

        # Vimala: 12th Lord in 6, 8, 12
        l12_planet = self.get_house_lord(12, asc_sign)
        _, l12_h = get_p_data(l12_planet)
        if l12_h in [6, 8, 12]:
             yogas_found.append({"name": "Vimala Yoga", "category": "Vipreet", "desc": "Independence, savings, and spiritual elevation."})

        # ==========================================
        # 4. DHANA YOGAS
        # ==========================================
        # 2nd Lord with 11th Lord
        l2_planet = self.get_house_lord(2, asc_sign)
        l11_planet = self.get_house_lord(11, asc_sign)
        
        l2_s, _ = get_p_data(l2_planet)
        l11_s, _ = get_p_data(l11_planet)
        
        if l2_s is not None and l2_s == l11_s:
            yogas_found.append({"name": "Dhana Yoga (2-11 Link)", "category": "Wealth", "desc": "Great accumulation of financial assets."})

        # ==========================================
        # 5. NEECHA BHANGA RAJA YOGA
        # ==========================================
        for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            pid, phouse = get_p_data(p)
            
            # Check if Debilitated
            if pid is not None and pid == self.DEBILITATION.get(p):
                is_cancelled = False
                
                # Condition A: Lord of that Sign is in Kendra from Lagna
                deb_sign_lord = self.SIGN_LORDS[pid]
                _, lord_h = get_p_data(deb_sign_lord)
                if lord_h in [1, 4, 7, 10]: 
                    is_cancelled = True
                
                # Condition B: Planet exalted in that Sign is in Kendra from Lagna
                exalt_planet = [k for k, v in self.EXALTATION.items() if v == pid]
                if exalt_planet:
                    _, ex_h = get_p_data(exalt_planet[0])
                    if ex_h in [1, 4, 7, 10]:
                        is_cancelled = True
                
                if is_cancelled:
                    yogas_found.append({
                        "name": f"Neecha Bhanga Raja Yoga ({p})", 
                        "category": "Cancellation", 
                        "desc": f"Debilitation of {p} is cancelled, converting weakness into strength."
                    })

        return yogas_found