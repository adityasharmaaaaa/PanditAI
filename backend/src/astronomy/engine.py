import swisseph as swe
import os
from .ayanamsa import AyanamsaSystem

class VedicAstroEngine:
    def __init__(self, ephe_path='./data/ephemeris', ayanamsa="LAHIRI"):
        abs_path = os.path.abspath(ephe_path)
        swe.set_ephe_path(abs_path)
        AyanamsaSystem.set_mode(ayanamsa)
        
        self.planet_map = {
            swe.SUN: "Sun", swe.MOON: "Moon", swe.MARS: "Mars",
            swe.MERCURY: "Mercury", swe.JUPITER: "Jupiter",
            swe.VENUS: "Venus", swe.SATURN: "Saturn",
            swe.MEAN_NODE: "Rahu"
        }

    def get_julian_day(self, year, month, day, hour, minute, timezone):
        decimal_local_time = hour + (minute / 60.0)
        decimal_utc = decimal_local_time - timezone
        return swe.julday(year, month, day, decimal_utc)

    def calculate_chart(self, year, month, day, hour, minute, lat, lon, timezone=0.0):
        jd = self.get_julian_day(year, month, day, hour, minute, timezone)
        chart_data = {}
        
        # CRITICAL FIX: Add swe.FLG_SPEED to ensure retrograde status is checked
        flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
        
        for pid, name in self.planet_map.items():
            try:
                # SAFE CALCULATION BLOCK
                res = swe.calc_ut(jd, pid, flags)
                
                # Handle nested tuple return types safely
                if isinstance(res, tuple) and len(res) > 0:
                    if isinstance(res[0], tuple): 
                        properties = res[0]
                    else:
                        properties = res
                    
                    longitude = properties[0]
                    speed = properties[3]  # Index 3 is always speed in longitude

                    # Debug print to verify speed (Negative = Retrograde)
                    # print(f"DEBUG: {name} Speed: {speed}") 

                    chart_data[name] = {
                        "id": pid,
                        "absolute_longitude": longitude,
                        "sign_id": int(longitude // 30),
                        "degree": longitude % 30,
                        "is_retrograde": speed < 0
                    }
                else:
                    # Fallback for empty results
                    print(f"⚠️ Warning: No data for {name}")
                    chart_data[name] = {
                        "id": pid, "absolute_longitude": 0, "sign_id": 0, "degree": 0, "is_retrograde": False
                    }
                    
            except Exception as e:
                print(f"❌ Error {name}: {e}")
                chart_data[name] = {
                    "id": pid, "absolute_longitude": 0, "sign_id": 0, "degree": 0, "is_retrograde": False
                }

        # Calculate Ketu (Always opposite Rahu)
        if "Rahu" in chart_data:
            rahu_long = chart_data["Rahu"]["absolute_longitude"]
            rahu_retro = chart_data["Rahu"]["is_retrograde"]
            ketu_long = (rahu_long + 180) % 360
            chart_data["Ketu"] = {
                "id": -1,
                "absolute_longitude": ketu_long,
                "sign_id": int(ketu_long // 30),
                "degree": ketu_long % 30,
                "is_retrograde": rahu_retro # Ketu matches Rahu's motion
            }

        # Calculate Ascendant
        try:
            cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', flags)
            asc_long = ascmc[0]
            chart_data["Ascendant"] = {
                "id": 0,
                "absolute_longitude": asc_long,
                "sign_id": int(asc_long // 30),
                "degree": asc_long % 30,
                "is_retrograde": False
            }
        except Exception as e:
             chart_data["Ascendant"] = {"id": 0, "absolute_longitude": 0, "sign_id": 0, "degree": 0, "is_retrograde": False}

        return chart_data