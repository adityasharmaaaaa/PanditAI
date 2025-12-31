class MatchMaker:
    def __init__(self):
        # Friendship Table for Moon Signs (Simplified Vedic Logic)
        # Groups: 1=Deves (Aries, Cancer, Leo, Scorpio, Sag, Pisces)
        #         2=Asuras (Taurus, Gemini, Virgo, Libra, Cap, Aq)
        # Rule: Same group = Good. Opposite group = Conflict.
        self.deva_signs = [0, 3, 4, 7, 8, 11]  # Ari, Can, Leo, Sco, Sag, Pis
        self.asura_signs = [1, 2, 5, 6, 9, 10]  # Tau, Gem, Vir, Lib, Cap, Aqu

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
        Compares Person A vs Person B using Ashta Koota (36 Points)
        """
        report = {}

        # 1. MANGLIK CHECK
        a_manglik, a_reasons = self.check_manglik(chart_a)
        b_manglik, b_reasons = self.check_manglik(chart_b)

        report["manglik"] = {
            "p1": {"is_manglik": a_manglik, "causes": a_reasons},
            "p2": {"is_manglik": b_manglik, "causes": b_reasons},
            "match_status": "Neutral",
        }

        if a_manglik and b_manglik:
            report["manglik"]["match_status"] = "Perfect (Cancellation)"
            report["manglik"]["desc"] = "Both are Manglik. The fire cancels out."
        elif not a_manglik and not b_manglik:
            report["manglik"]["match_status"] = "Good"
            report["manglik"]["desc"] = "Neither has Mars Dosha. Safe."
        else:
            report["manglik"]["match_status"] = "Clash (Manglik Dosha)"
            report["manglik"]["desc"] = "One is Manglik. Potential for conflict."

        # 2. ASHTA KOOTA Calculation
        scores = {
            "Varna": 1,
            "Vashya": 2,
            "Tara": 3,
            "Yoni": 4,
            "Maitri": 5,
            "Gana": 6,
            "Bhakoot": 7,
            "Nadi": 8,
        }

        if "Moon" in chart_a and "Moon" in chart_b:
            m1 = chart_a["Moon"]["sign_id"]
            m2 = chart_b["Moon"]["sign_id"]
            nak1 = chart_a["Moon"].get("nakshatra_id", 0)
            nak2 = chart_b["Moon"].get("nakshatra_id", 0)

            # A. VARNA (1 pt)
            e1 = m1 % 4
            e2 = m2 % 4
            scores["Varna"] = 1 if e1 == e2 else 0.5

            # B. VASHYA (2 pts)
            scores["Vashya"] = 2 if abs(m1 - m2) not in [6, 8] else 1

            # C. TARA (3 pts)
            dist = (nak2 - nak1) % 9
            scores["Tara"] = 3 if dist % 2 == 0 else 1.5

            # D. YONI (4 pts)
            scores["Yoni"] = 4 if (nak1 % 2) == (nak2 % 2) else 2

            # E. MAITRI (5 pts)
            p1_Deva = m1 in self.deva_signs
            p2_Deva = m2 in self.deva_signs
            scores["Maitri"] = (
                5 if p1_Deva == p2_Deva else 3 if abs(m1 - m2) in [4, 5, 9] else 0.5
            )

            # F. GANA (6 pts)
            scores["Gana"] = (
                6
                if (nak1 % 3) == (nak2 % 3)
                else 3
                if abs((nak1 % 3) - (nak2 % 3)) == 1
                else 0
            )

            # G. BHAKOOT (7 pts)
            rel = (m2 - m1) % 12 + 1
            if rel in [2, 12, 6, 8]:
                scores["Bhakoot"] = 0
            else:
                scores["Bhakoot"] = 7

            # H. NADI (8 pts)
            n1 = nak1 % 3
            n2 = nak2 % 3
            if n1 == n2:
                scores["Nadi"] = 0
            else:
                scores["Nadi"] = 8

        total_score = sum(scores.values())

        report["score"] = total_score
        report["details"] = scores

        return report
