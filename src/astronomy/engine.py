import swisseph as swe
import os
from datetime import datetime

class VedicAstroEngine:
    def __init__(self):
        # Point to ephemeris files if they exist locally, else let swe use defaults
        # Usually located in 'ephe' folder relative to project root
        ephe_path = os.path.join(os.path.dirname(__file__), "../../ephe")
        if os.path.exists(ephe_path):
            swe.set_ephe_path(ephe_path)
            
    def get_julian_day(self, year, month, day, hour, minute, tz):
        """
        Converts Local Date/Time to Julian Day (Universal Time)
        """
        # UTC offset adjustment
        decimal_hour = hour + (minute / 60.0) - tz
        return swe.julday(year, month, day, decimal_hour)

    def calculate_varga(self, planet_deg, sign_id, division=9):
        """
        Calculates the sign ID for a planet in a divisional chart (Varga).
        Default is D9 (Navamsa), the most critical divisional chart in Vedic Astrology.
        """
        if division != 9:
            return sign_id # Only D9 implemented for now

        # 1. Determine Pada (Part 0-8)
        # Each Navamsa is 3° 20' = 3.333333 degrees
        part_size = 30.0 / 9.0
        pada_index = int(planet_deg / part_size) 
        
        # 2. Determine Start Sign based on Element (Tattwa)
        # Fire Signs (Aries 0, Leo 4, Sag 8) -> Start Counting from Aries (0)
        # Earth Signs (Taurus 1, Virgo 5, Cap 9) -> Start Counting from Capricorn (9)
        # Air Signs (Gemini 2, Libra 6, Aqua 10) -> Start Counting from Libra (6)
        # Water Signs (Cancer 3, Scorpio 7, Pisces 11) -> Start Counting from Cancer (3)
        
        element_group = sign_id % 4
        
        if element_group == 0:   # Fire
            start_sign = 0 
        elif element_group == 1: # Earth
            start_sign = 9
        elif element_group == 2: # Air
            start_sign = 6
        else:                    # Water
            start_sign = 3
            
        # 3. Final Calculation
        varga_sign_id = (start_sign + pada_index) % 12
        return varga_sign_id

    def calculate_chart(self, year, month, day, hour, minute, lat, lon, tz, ayanamsa_mode="LAHIRI"):
        """
        Main function to calculate planetary positions.
        Returns Dictionary with Planet Data including D1 (Rashi) and D9 (Navamsa).
        """
        jd = self.get_julian_day(year, month, day, hour, minute, tz)
        
        # 1. Set Ayanamsa (Sidereal Offset)
        if ayanamsa_mode == "RAMAN":
            swe.set_sid_mode(swe.SIDM_RAMAN)
        elif ayanamsa_mode == "KP":
            swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
        else:
            swe.set_sid_mode(swe.SIDM_LAHIRI) # Default to Lahiri (Standard Vedic)
            
        ayanamsa_val = swe.get_ayanamsa_ut(jd)
        
        # 2. Define Planets to Calculate
        planets = {
            "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS,
            "Mercury": swe.MERCURY, "Jupiter": swe.JUPITER,
            "Venus": swe.VENUS, "Saturn": swe.SATURN,
            "Rahu": swe.MEAN_NODE # Mean Node is standard in most Vedic software
        }
        
        chart_data = {}
        
        # 3. Calculate 7 Major Planets + Rahu
        for p_name, p_code in planets.items():
            # Calculate Tropical Position
            # flags: swe.FLG_SWIEPH (use ephemeris), swe.FLG_SPEED (calc speed)
            res = swe.calc_ut(jd, p_code, swe.FLG_SWIEPH | swe.FLG_SPEED)
            
            tropical_lon = res[0][0]
            speed = res[0][3]
            
            # Convert to Sidereal (Nirayana)
            sidereal_lon = (tropical_lon - ayanamsa_val) % 360
            
            sign_id = int(sidereal_lon / 30)
            degree_in_sign = sidereal_lon % 30
            is_retrograde = speed < 0
            
            # --- NEW: CALCULATE D9 (NAVAMSA) ---
            d9_sign = self.calculate_varga(degree_in_sign, sign_id, division=9)
            
            chart_data[p_name] = {
                "sign_id": sign_id,
                "degree": degree_in_sign,
                "is_retrograde": is_retrograde,
                "absolute_longitude": sidereal_lon,
                "speed": speed,
                "d9_sign_id": d9_sign
            }
            
        # 4. Calculate Ketu (Always exactly 180 degrees from Rahu)
        rahu = chart_data["Rahu"]
        ketu_lon = (rahu["absolute_longitude"] + 180) % 360
        ketu_sign = int(ketu_lon / 30)
        ketu_deg = ketu_lon % 30
        
        # Ketu's D9
        ketu_d9 = self.calculate_varga(ketu_deg, ketu_sign, division=9)
        
        chart_data["Ketu"] = {
            "sign_id": ketu_sign,
            "degree": ketu_deg,
            "is_retrograde": rahu["is_retrograde"], # Always same motion as Rahu
            "absolute_longitude": ketu_lon,
            "speed": rahu["speed"],
            "d9_sign_id": ketu_d9
        }
        
        # 5. Calculate Ascendant (Lagna)
        # swe.houses_ex returns (cusps, ascmc). ascmc[0] is the Ascendant.
        # We use 'A' (Equal) or 'P' (Placidus) - Ascendant degree is same regardless of house system.
        houses_res = swe.houses_ex(jd, lat, lon, b'A') 
        asc_tropical = houses_res[1][0]
        
        # Convert Ascendant to Sidereal
        asc_sidereal = (asc_tropical - ayanamsa_val) % 360
        asc_sign = int(asc_sidereal / 30)
        asc_deg = asc_sidereal % 30
        
        # Ascendant D9
        asc_d9 = self.calculate_varga(asc_deg, asc_sign, division=9)
        
        chart_data["Ascendant"] = {
            "sign_id": asc_sign,
            "degree": asc_deg,
            "absolute_longitude": asc_sidereal,
            "d9_sign_id": asc_d9
        }
        
        return chart_data