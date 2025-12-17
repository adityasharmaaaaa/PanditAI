import streamlit as st
import requests
import json
from datetime import datetime, time

# Config
API_URL = "http://127.0.0.1:8000/calculate"
st.set_page_config(page_title="PanditAI", page_icon="🕉️", layout="wide")

# Custom CSS for "Mystical" Vibe
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6
    }
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        color: #4B0082;
    }
    .prediction-box {
        background-color: #f9f9f9;
        border-left: 5px solid #6c5ce7;
        padding: 20px;
        border-radius: 5px;
        margin-top: 20px;
        color: #000000; /* <--- FORCE TEXT TO BE BLACK */
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🕉️ PanditAI: Neuro-Symbolic Vedic Astrologer")
st.markdown("### *Grounded in BPHS, Powered by Llama 3*")

# Input Form (Sidebar)
with st.sidebar:
    st.header("Enter Birth Details")
    
    # Date & Time
    b_date = st.date_input(
        "Date of Birth", 
        value=datetime(1990, 5, 15),
        min_value=datetime(1900, 1, 1),
        max_value=datetime(2100, 12, 31)
    )
    b_time = st.time_input("Time of Birth", value=time(14, 0))
    
    # Location (Simple Manual Input for now)
    st.subheader("Location Coordinates")
    lat = st.number_input("Latitude", value=28.61, format="%.2f", help="Positive for North, Negative for South")
    lon = st.number_input("Longitude", value=77.20, format="%.2f", help="Positive for East, Negative for West")
    tz = st.number_input("Timezone (Offset from UTC)", value=5.5, step=0.5, help="India is 5.5, EST is -5.0")
    
    ayanamsa = st.selectbox("Ayanamsa", ["LAHIRI", "RAMAN"])
    
    submit = st.button("Generate Horoscope 🔮", type="primary")

# Main Logic
if submit:
    # Prepare Payload
    payload = {
        "year": b_date.year,
        "month": b_date.month,
        "day": b_date.day,
        "hour": b_time.hour,
        "minute": b_time.minute,
        "timezone": tz,
        "latitude": lat,
        "longitude": lon,
        "ayanamsa": ayanamsa
    }
    
    with st.spinner("Consulting the stars and querying the Knowledge Graph..."):
        try:
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            data = response.json()
            
            # --- DISPLAY RESULTS ---
            
            # 1. The AI Reading (Hero Section)
            st.markdown("---")
            st.subheader("📜 The Pandit's Reading")
            if data.get("ai_reading"):
                st.markdown(f"""
                <div class="prediction-box">
                    {data['ai_reading'].replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("No specific text rules found for this chart in the current graph.")

            # 2. Planetary Table (The Math)
            st.markdown("---")
            st.subheader("🪐 Planetary Positions (Sidereal)")
            
            planet_rows = []
            signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
            
            # Helper function to format rows
            def format_row(p_name, p_data):
                sign_name = signs[p_data["sign_id"]]
                deg = int(p_data["degree"])
                mins = int((p_data["degree"] - deg) * 60)
                retro = " (R)" if p_data.get("is_retrograde") else ""
                
                return {
                    "Planet": p_name,
                    "Sign": sign_name,
                    "Position": f"{deg}° {mins}'{retro}",
                    "House": p_data.get("house_number", 1) # Ascendant is always House 1
                }

            # 1. Add Ascendant (Lagna) First
            if "Ascendant" in data["planets"]:
                planet_rows.append(format_row("Ascendant", data["planets"]["Ascendant"]))

            # 2. Add Planets in Standard Vedic Order
            sort_order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
            
            for p_name in sort_order:
                if p_name in data["planets"]:
                    planet_rows.append(format_row(p_name, data["planets"][p_name]))
            
            # Display the table
            st.table(planet_rows)
            
            # 3. Technical Details
            with st.expander("Show Technical Details (JSON)"):
                st.json(data)
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to the Backend API. Is 'uvicorn' running?")
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")