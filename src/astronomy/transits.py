import swisseph as swe
from datetime import datetime
from .engine import VedicAstroEngine

class TransitEngine(VedicAstroEngine):
    def calculate_current_transits(self, birth_chart, location_data):
        """
        Compares NOW (Current Sky) vs BIRTH (User's Chart).
        """
        now = datetime.now()
        
        # 1. Calculate Current Planetary Positions (The Sky Right Now)
        transit_chart = self.calculate_chart(
            now.year, now.month, now.day, 
            now.hour, now.minute, 
            location_data['lat'], location_data['lon'], location_data['tz']
        )
        
        # 2. Get User's Birth Ascendant
        if "Ascendant" not in birth_chart:
            return []
            
        asc_sign_id = birth_chart['Ascendant']['sign_id']
        transit_report = []
        
        zodiac = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
                  "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        
        # 3. Compare Transit Planet vs Birth Ascendant
        for p_name, p_data in transit_chart.items():
            if p_name == "Ascendant": continue
            
            # Current Sign of the Planet
            transit_sign_id = p_data['sign_id']
            
            # Calculate House relative to Birth Ascendant
            # Formula: (TransitSign - BirthAsc + 12) % 12 + 1
            transit_house = (transit_sign_id - asc_sign_id) % 12 + 1
            
            # Get Prediction using your dictionary
            prediction = self.get_transit_prediction(p_name, transit_house)
            
            transit_report.append({
                "planet": p_name,
                "current_sign": zodiac[transit_sign_id],
                "transiting_house": transit_house,
                "prediction": prediction,
                "is_retrograde": p_data['is_retrograde']
            })
            
        return transit_report

    def get_transit_prediction(self, planet, house):
        """
        Comprehensive BPHS-based transit results for all 9 Grahas.
        """
        predictions = {
            "Sun": {
                1: "Fatigue, irritability, and difficult journeys.",
                2: "Loss of wealth, eye strain, and family disputes.",
                3: "Acquisition of wealth, health, and victory over enemies.",
                4: "Mental distress, domestic disturbances, and lack of comfort.",
                5: "Anxiety regarding children, mental confusion, and illness.",
                6: "Success in all undertakings, health, and joy.",
                7: "Fatiguing travel, stomach issues, and marital tension.",
                8: "Fear, excessive heat in body, and fear of authority.",
                9: "Loss of prestige, mental anguish, and obstacles.",
                10: "Success in profession, new honors, and accomplishment.",
                11: "New position, honor, and financial prosperity.",
                12: "Heavy expenses and physical exhaustion."
            },
            "Moon": {
                1: "Arrival of good food, garments, and physical joy.",
                2: "Obstacles in work and financial instability.",
                3: "Gains from siblings, courage, and success.",
                4: "Lack of mental peace and issues with home/mother.",
                5: "Sorrow, mental instability, and indigestion.",
                6: "Victory over enemies, health, and profit.",
                7: "Comforts, vehicles, and social success.",
                8: "Danger to health and mental distress.",
                9: "Fear of debt and lack of fortune.",
                10: "Fulfillment of desires and professional rise.",
                11: "Acquisition of wealth and meeting with friends.",
                12: "Expenditure, losses, and fatigue."
            },
            "Mars": {
                1: "Heat-related ailments and mental agitation.",
                2: "Harsh speech and financial losses.",
                3: "Great success, courage, and gain of property.",
                4: "Conflict with relatives and domestic stress.",
                5: "Anger, issues with children, and fever.",
                6: "Destruction of enemies and victory in disputes.",
                7: "Quarrels with spouse and eye trouble.",
                8: "Physical injuries or sudden health issues.",
                9: "Humiliation and loss of vitality.",
                10: "Irregular behavior but professional activity.",
                11: "Gain of gold, property, and happiness.",
                12: "Loss of wealth and excessive anger."
            },
            "Mercury": {
                1: "Loss of wealth through harsh speech.",
                2: "Financial gains and increase in knowledge.",
                3: "Fear of enemies and mental instability.",
                4: "Happiness from family and success in education.",
                5: "Discord with wife and children.",
                6: "Success, fame, and victory in debates.",
                7: "Domestic arguments and lack of peace.",
                8: "Happiness and increase in wealth.",
                9: "Obstacles in work and mental fatigue.",
                10: "Mental peace, wealth, and success.",
                11: "Gains from various sources and social happiness.",
                12: "Fear of failure and unnecessary expenses."
            },
            "Jupiter": {
                1: "Relocation, loss of wealth, and fatigue.",
                2: "Financial prosperity and family happiness.",
                3: "Loss of position and obstacles in work.",
                4: "Sorrow regarding relatives and home life.",
                5: "Birth of children, gain of knowledge, and joy.",
                6: "Health issues and disputes with enemies.",
                7: "Marriage, travel, and physical comforts.",
                8: "Fatigue, illness, and unsuccessful journeys.",
                9: "Spiritual growth, luck, and prosperity.",
                10: "Obstacles in profession and lack of recognition.",
                11: "Great wealth, new opportunities, and honors.",
                12: "Mental grief and spiritual detachment."
            },
            "Venus": {
                1: "Sensual pleasures, luxury, and happiness.",
                2: "Financial gains and birth of a child.",
                3: "Prosperity, influence, and social success.",
                4: "New vehicles, house, and domestic joy.",
                5: "Happiness from children and romance.",
                6: "Conflict with women and health issues.",
                7: "Success in marriage and partnerships.",
                8: "Unexpected wealth and luxury items.",
                9: "Religious deeds and general prosperity.",
                10: "Recognition and professional success.",
                11: "Gains from friends and liquid cash.",
                12: "Gains of comfort and luxury, but high spending."
            },
            "Saturn": {
                1: "Heavy responsibilities, fatigue, and delays.",
                2: "Loss of wealth and family friction.",
                3: "Destruction of enemies and gain of power.",
                4: "Separation from home and mental distress.",
                5: "Loss of intelligence and worry for children.",
                6: "Total success and physical strength.",
                7: "Wearisome journeys and relationship stress.",
                8: "Accidents or chronic health issues.",
                9: "Poverty and lack of focus.",
                10: "Hard work with slow rewards.",
                11: "Sudden wealth and high status.",
                12: "Excessive expenditure and mental agony."
            },
            "Rahu": {
                1: "Confusion and health concerns.",
                2: "Loss of wealth and harsh speech.",
                3: "Unexpected gains and victory over rivals.",
                4: "Fear and domestic instability.",
                5: "Anxiety and speculative losses.",
                6: "Physical health and defeat of enemies.",
                7: "Conflict in partnerships.",
                8: "Sudden obstacles and danger.",
                9: "Confusion in belief systems.",
                10: "Professional change or success through shortcuts.",
                11: "Massive gains and influential contacts.",
                12: "Secret expenses and insomnia."
            },
            "Ketu": {
                # Ketu mirrors Rahu but with a spiritual/detachment twist
                3: "Spiritual courage and victory.",
                6: "Freedom from debt and enemies.",
                11: "Inward gains and intuitive success.",
                "default": "A period of detachment and internal searching."
            }
        }

        planet_dict = predictions.get(planet, {})
        return planet_dict.get(house, planet_dict.get("default", "Mixed results according to planetary strength."))