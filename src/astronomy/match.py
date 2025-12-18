class MatchMaker:
    def __init__(self):
        # Friendship Table for Moon Signs (Simplified Vedic Logic)
        # Groups: 1=Deves (Aries, Cancer, Leo, Scorpio, Sag, Pisces)
        #         2=Asuras (Taurus, Gemini, Virgo, Libra, Cap, Aq)
        # Rule: Same group = Good. Opposite group = Conflict.
        self.deva_signs = [0, 3, 4, 7, 8, 11] # Ari, Can, Leo, Sco, Sag, Pis
        self.asura_signs = [1, 2, 5, 6, 9, 10] # Tau, Gem, Vir, Lib, Cap, Aqu

    def check_manglik(self, chart):
        """
        Mars in 1, 4, 7, 8, 12 from Ascendant or Moon is considered Manglik.
        """
        mars_houses = []
        
        # 1. Check from Ascendant
        if "Mars" in chart and "Ascendant" in chart:
            asc_id = chart["Ascendant"]["sign_id"]
            mars_id = chart["Mars"]["sign_id"]
            h_asc = (mars_id - asc_id) % 12 + 1
            if h_asc in [1, 4, 7, 8, 12]:
                mars_houses.append(f"Ascendant (House {h_asc})")

        # 2. Check from Moon
        if "Mars" in chart and "Moon" in chart:
            moon_id = chart["Moon"]["sign_id"]
            mars_id = chart["Mars"]["sign_id"]
            h_moon = (mars_id - moon_id) % 12 + 1
            if h_moon in [1, 4, 7, 8, 12]:
                mars_houses.append(f"Moon (House {h_moon})")
                
        is_manglik = len(mars_houses) > 0
        return is_manglik, mars_houses

    def calculate_compatibility(self, chart_a, chart_b):
        """
        Compares Person A vs Person B
        """
        report = {}
        
        # 1. MANGLIK CHECK
        a_manglik, a_reasons = self.check_manglik(chart_a)
        b_manglik, b_reasons = self.check_manglik(chart_b)
        
        report["manglik"] = {
            "p1": {"is_manglik": a_manglik, "causes": a_reasons},
            "p2": {"is_manglik": b_manglik, "causes": b_reasons},
            "match_status": "Neutral"
        }
        
        # Manglik Logic: Best if BOTH are Manglik or BOTH are NOT.
        if a_manglik and b_manglik:
            report["manglik"]["match_status"] = "Perfect (Cancellation)"
            report["manglik"]["desc"] = "Both are Manglik. The fire cancels out."
        elif not a_manglik and not b_manglik:
            report["manglik"]["match_status"] = "Good"
            report["manglik"]["desc"] = "Neither has Mars Dosha. Safe."
        else:
            report["manglik"]["match_status"] = "Clash (Manglik Dosha)"
            report["manglik"]["desc"] = "One is Manglik and the other is not. Potential for intense conflict."

        # 2. MOON COMPATIBILITY (Emotional Sync)
        if "Moon" in chart_a and "Moon" in chart_b:
            m1 = chart_a["Moon"]["sign_id"]
            m2 = chart_b["Moon"]["sign_id"]
            
            p1_group = "Deva" if m1 in self.deva_signs else "Asura"
            p2_group = "Deva" if m2 in self.deva_signs else "Asura"
            
            score = 0
            if p1_group == p2_group:
                status = "Excellent"
                score = 100
            else:
                status = "Challenging"
                score = 40
                
            report["emotional"] = {
                "status": status,
                "score": score,
                "p1_group": p1_group,
                "p2_group": p2_group
            }
            
        # 3. SUN COMPATIBILITY (Ego Check)
        if "Sun" in chart_a and "Sun" in chart_b:
            s1 = chart_a["Sun"]["sign_id"]
            s2 = chart_b["Sun"]["sign_id"]
            # 7th house opposition is Attraction + Conflict
            distance = abs(s1 - s2)
            if distance == 6: 
                report["ego"] = "Opposites Attract (7th House)"
            elif distance == 0:
                report["ego"] = "Same Sign (Conjunction)"
            else:
                report["ego"] = "Neutral"

        return report