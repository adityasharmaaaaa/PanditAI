import ephem
import math
from datetime import datetime, timedelta

def decimal_to_dms(deg):
    """Helper to convert decimal degrees to Degrees:Minutes:Seconds"""
    d = int(deg)
    m = int((deg - d) * 60)
    s = round(((deg - d) * 60 - m) * 60, 2)
    return f"{d}° {m}' {s}\""

def get_zodiac_sign(lon_degrees):
    """Returns the Vedic Zodiac sign based on longitude."""
    signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", 
             "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    # Normalize to 0-360
    lon_degrees = lon_degrees % 360
    index = int(lon_degrees / 30)
    return signs[index]

def calculate_gulika(lat, lon, year, month, day, hour, minute):
    """
    Calculates the time and position (longitude) of Gulika.
    """
    
    # 1. Setup the Observer
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.date = datetime(year, month, day, hour, minute)
    
    # Sun object to find rising/setting
    sun = ephem.Sun()
    
    # 2. Determine Sunrise and Sunset relative to the given time
    # We look for the sunrise immediately preceding the time, and the next sunset
    prev_sunrise = observer.previous_rising(sun)
    next_sunset = observer.next_setting(sun)
    next_sunrise = observer.next_rising(sun)
    
    # Convert ephem dates to python datetime for easier comparison
    dt_current = observer.date.datetime()
    dt_sunrise = prev_sunrise.datetime()
    dt_sunset = next_sunset.datetime()
    
    is_daytime = dt_sunrise <= dt_current < dt_sunset

    # 3. Determine the segment length and Weekday
    # Note: In Vedic astrology, the day starts at Sunrise, not Midnight.
    # The weekday is determined by the Sunrise of that period.
    
    if is_daytime:
        day_duration = dt_sunset - dt_sunrise
        segment_length = day_duration / 8
        weekday = dt_sunrise.weekday() # Mon=0, Sun=6
        base_time = dt_sunrise
        period_type = "Day"
    else:
        # It is night. We need the duration between Sunset and the *Next* Sunrise
        # If we are strictly before sunrise (e.g., 2 AM), the "Vedic Day" is yesterday.
        
        # We need the sunset that started this night
        if dt_current < dt_sunrise: 
            # It's early morning, so the night started yesterday evening
            temp_obs = ephem.Observer()
            temp_obs.lat, temp_obs.lon = observer.lat, observer.lon
            temp_obs.date = dt_current
            night_start = temp_obs.previous_setting(sun).datetime()
            night_end = temp_obs.next_rising(sun).datetime()
        else:
            # It's evening, night started today
            night_start = dt_sunset
            night_end = next_sunrise.datetime()
            
        day_duration = night_end - night_start
        segment_length = day_duration / 8
        
        # The weekday for the night calculation is the day preceding the night
        weekday = night_start.weekday() 
        base_time = night_start
        period_type = "Night"

    # 4. Determine Gulika's Segment Index based on Weekday
    # Indices are 0-7. Gulika is located at a specific index depending on the ruler.
    
    # Mapping Weekday (Mon=0...Sun=6) to Gulika's Index
    # Day Logic: Sun(6), Mon(5), Tue(4), Wed(3), Thu(2), Fri(1), Sat(0)
    # Night Logic: Sun(2), Mon(1), Tue(0), Wed(6), Thu(5), Fri(4), Sat(3)
    
    gulika_indices_day = {
        6: 6, # Sunday: Saturn is 7th part (Index 6)
        0: 5, # Monday: Saturn is 6th part
        1: 4, # Tuesday
        2: 3, # Wednesday
        3: 2, # Thursday
        4: 1, # Friday
        5: 0  # Saturday
    }
    
    gulika_indices_night = {
        6: 2, # Sunday Night
        0: 1, # Monday Night
        1: 0, # Tuesday Night
        2: 6, # Wednesday Night
        3: 5, # Thursday Night
        4: 4, # Friday Night
        5: 3  # Saturday Night
    }

    if period_type == "Day":
        gulika_idx = gulika_indices_day[weekday]
    else:
        gulika_idx = gulika_indices_night[weekday]

    # 5. Calculate Gulika Start Time
    # Gulika's position is the Ascendant at the BEGINNING of Saturn's segment
    gulika_start_time = base_time + (segment_length * gulika_idx)
    
    # 6. Calculate Ascendant (Lagna) at Gulika Start Time
    observer.date = gulika_start_time
    
    # Calculate Sidereal Time (RAMC)
    # Ephem is Tropical. To get Vedic (Sidereal), we must subtract Ayanamsa.
    # Using a simplified Lahiri Ayanamsa approximation for the current era (~24 degrees)
    # For high precision, use pyswisseph. Here we approximate.
    ayanamsa_deg = 24.1  # Approximate for 2024-2025
    
    ra_asc, dec_asc = observer.radec_of(0, '0') # RA of the meridian
    # The standard ephem way to get RA of Ascendant is complex, 
    # but a simpler way is to compute the horizon for the specific time.
    # A standard shortcut in PyEphem isn't available for Ascendant directly without math.
    # We will use the standard formula: tan(Asc) = cos(OA) / (sin(OA)cos(E) - tan(Lat)sin(E))
    # OR, strictly for this script, we assume the user accepts a Tropical->Sidereal conversion.
    
    # Let's use a simpler known method for Ascendant calculation logic:
    # 1. Get Local Sidereal Time (LST)
    lst = observer.sidereal_time()
    
    # 2. Calculate Obliquity of Ecliptic (approx 23.44)
    eps = 23.44 * (math.pi / 180.0)
    
    # 3. Calculate Ascendant using standard formula
    # tan(lambda) = (-cos(LST) / (sin(LST)*cos(eps) + tan(lat)*sin(eps)))
    # Note: Python's math functions use radians
    lat_rad = float(lat) * (math.pi / 180.0)
    
    # LST is in radians in Ephem
    sin_lst = math.sin(lst)
    cos_lst = math.cos(lst)
    tan_lat = math.tan(lat_rad)
    sin_eps = math.sin(eps)
    cos_eps = math.cos(eps)
    
    numerator = -1 * cos_lst
    denominator = (sin_lst * cos_eps) + (tan_lat * sin_eps)
    
    asc_rad = math.atan2(numerator, denominator)
    asc_deg = asc_rad * (180.0 / math.pi)
    
    # Normalize
    asc_deg = (asc_deg + 360) % 360
    
    # Convert to Vedic (Sidereal)
    sidereal_asc_deg = (asc_deg - ayanamsa_deg) % 360

    return {
        "period": period_type,
        "gulika_time": gulika_start_time,
        "gulika_long": sidereal_asc_deg,
        "sign": get_zodiac_sign(sidereal_asc_deg)
    }

# --- usage ---
# Coordinates for Bangalore, India
lat = 28.6216
lon = 78.0646

# Date: 2023-10-25, 10:30 AM
result = calculate_gulika(lat, lon, 2004, 5, 20, 9, 40)

print(f"--- Gulika Calculation ---")
print(f"Time of Calculation: Day/Night Period: {result['period']}")
print(f"Gulika Start Time: {result['gulika_time']}")
print(f"Gulika Position: {decimal_to_dms(result['gulika_long'])} ({result['sign']})")