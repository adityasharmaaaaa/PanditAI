import json
import os
import uvicorn
import torch
import torch.nn as nn
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from collections import defaultdict
import time
from src.api.schemas import BirthDetails, ChartResponse

# --- IMPORT ENGINES ---
from src.astronomy.engine import VedicAstroEngine
from src.astronomy.dasha import VimshottariDasha
from src.astronomy.transits import TransitEngine
from src.astronomy.match import MatchMaker
from src.astronomy.yogas import YogaEngine
from src.model.inference import generate_horoscope_reading, chat_with_astrologer
from src.utils.chart_plotter import draw_north_indian_chart

app = FastAPI(title="PanditAI: Neuro-Symbolic Engine")

# --- RATE LIMITING MIDDLEWARE ---

RATE_LIMIT_DELAY = 1.0
_ip_timestamps = defaultdict(float)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    now = time.time()
    last_time = _ip_timestamps[client_ip]

    if now - last_time < RATE_LIMIT_DELAY:
        if request.method == "OPTIONS":
            return await call_next(request)

        return Response(
            content=json.dumps({"detail": "Rate limit exceeded. Please wait."}),
            status_code=429,
            media_type="application/json",
        )

    _ip_timestamps[client_ip] = now
    response = await call_next(request)
    return response


# --- CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 1. INITIALIZE ENGINES
# ==========================================
astro_engine = VedicAstroEngine()
dasha_engine = VimshottariDasha()
transit_engine = TransitEngine()
match_engine = MatchMaker()
yoga_engine = YogaEngine()

# ==========================================
# 2. LOAD PREDICTION DATA
# ==========================================
PREDICTION_DB = {}


# Helper to normalize keys from custom_rules (e.g. "Sun_H1_Aries" -> "SUN_ARI_H1")
def normalize_custom_key(custom_id):
    try:
        parts = custom_id.split("_")  # Sun, H1, Aries
        if len(parts) != 3:
            return None

        planet_map = {
            "Sun": "SUN",
            "Moon": "MOON",
            "Mars": "MAR",
            "Mercury": "MER",
            "Jupiter": "JUP",
            "Venus": "VEN",
            "Saturn": "SAT",
            "Rahu": "RAH",
            "Ketu": "KET",
        }
        sign_map = {
            "Aries": "ARI",
            "Taurus": "TAU",
            "Gemini": "GEM",
            "Cancer": "CAN",
            "Leo": "LEO",
            "Virgo": "VIR",
            "Libra": "LIB",
            "Scorpio": "SCO",
            "Sagittarius": "SAG",
            "Capricorn": "CAP",
            "Aquarius": "AQU",
            "Pisces": "PIS",
        }

        p = planet_map.get(parts[0])
        h = parts[1]  # H1
        s = sign_map.get(parts[2])

        if p and s:
            return f"{p}_{s}_{h}"
        return None
    except:
        return None


# 1. Load default data first
p_path = os.path.join("data", "planets_data.json")
if os.path.exists(p_path):
    with open(p_path, "r", encoding="utf-8") as f:
        for item in json.load(f):
            PREDICTION_DB[item["id"]] = item

l_path = os.path.join("data", "house_lords.json")
if os.path.exists(l_path):
    with open(l_path, "r", encoding="utf-8") as f:
        for item in json.load(f):
            PREDICTION_DB[item["id"]] = item

# 2. Override with Custom Rules (Lenient)
c_path = os.path.join("data", "custom_rules.json")
if os.path.exists(c_path):
    print(f"  Loading Custom Rules from {c_path}...")
    with open(c_path, "r", encoding="utf-8") as f:
        custom_data = json.load(f)
        count = 0
        for item in custom_data:
            # item has "results": { "general": "...", "positive": "...", "negative": "..." }
            # We need to flatten this to "prediction" key for compatibility

            # 1. Construct backward-compatible prediction text
            prediction_text = item["results"]["general"]
            if item["results"]["positive"]:
                prediction_text += " " + item["results"]["positive"]
            # Only add negative if it's not too harsh? User wants leniency.
            # But let's include it for completeness, maybe the text itself is softer now.
            if item["results"]["negative"]:
                prediction_text += " Challenge: " + item["results"]["negative"]

            new_item = item.copy()
            new_item["prediction"] = prediction_text

            # 2. Map ID
            new_id = normalize_custom_key(item["id"])
            if new_id:
                new_item["id"] = new_id
                PREDICTION_DB[new_id] = new_item  # OVERRIDE
                count += 1
        print(f"  Overridden {count} rules with Custom/Lenient versions.")


# ==========================================
# 3. DEEP LEARNING MODEL
# ==========================================
class DestinyNet(nn.Module):
    def __init__(self):
        super(DestinyNet, self).__init__()
        self.fc1 = nn.Linear(18, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 32)
        self.fc4 = nn.Linear(32, 1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        return self.sigmoid(
            self.fc4(self.relu(self.fc3(self.relu(self.fc2(self.relu(self.fc1(x)))))))
        )


destiny_model = DestinyNet()
if os.path.exists("models/destiny_net.pth"):
    try:
        destiny_model.load_state_dict(torch.load("models/destiny_net.pth"))
        destiny_model.eval()
        print("  DL Model Loaded")
    except:
        print("⚠️ DL Model Load Failed")


def get_dl_vector(chart):
    vec = []
    for p in [
        "Sun",
        "Moon",
        "Mars",
        "Mercury",
        "Jupiter",
        "Venus",
        "Saturn",
        "Rahu",
        "Ketu",
    ]:
        if p in chart:
            vec.extend([chart[p]["sign_id"], chart[p].get("house_number", 1)])
        else:
            vec.extend([0, 0])
    return torch.tensor([vec], dtype=torch.float32)


# ==========================================
# 4. HELPER: RULE KEY GENERATOR
# ==========================================
def get_rules_for_chart(chart, asc_id):
    found_rules = []
    text_summary = "=== PLANETARY PLACEMENTS ===\n"

    for p, data in chart.items():
        if p == "Ascendant":
            continue
        h = data["house_number"]
        sign_short = [
            "ARI",
            "TAU",
            "GEM",
            "CAN",
            "LEO",
            "VIR",
            "LIB",
            "SCO",
            "SAG",
            "CAP",
            "AQU",
            "PIS",
        ][data["sign_id"]]
        p_short = {
            "Sun": "SUN",
            "Moon": "MOON",
            "Mars": "MAR",
            "Mercury": "MER",
            "Jupiter": "JUP",
            "Venus": "VEN",
            "Saturn": "SAT",
            "Rahu": "RAH",
            "Ketu": "KET",
        }.get(p)

        if p_short:
            key = f"{p_short}_{sign_short}_H{h}"
            if key in PREDICTION_DB:
                rule = PREDICTION_DB[key]
                found_rules.append(rule)
                text_summary += f"* {p} in House {h}: {rule.get('prediction', '')}\n"

    return found_rules, text_summary


# ==========================================
# 5. API ENDPOINTS
# ==========================================


# Maintain backward compatibility with /calculate if needed by frontend
@app.post("/calculate", response_model=ChartResponse)
@app.post("/predict")
def predict_horoscope(d: BirthDetails):
    try:
        # A. Calculate Chart
        chart = astro_engine.calculate_chart(
            d.year,
            d.month,
            d.day,
            d.hour,
            d.minute,
            d.latitude,
            d.longitude,
            d.timezone,
        )
        asc_id = chart["Ascendant"]["sign_id"]

        # B. Assign House Numbers
        for p, data in chart.items():
            if p != "Ascendant":
                data["house_number"] = (data["sign_id"] - asc_id) % 12 + 1

        # C. DL Score
        try:
            raw_score = int(destiny_model(get_dl_vector(chart)).item() * 100)

            score = min(int(raw_score * 1.2) + 15, 98)
        except:
            score = 75

        # D. Get Rules
        rules, fact_sheet = get_rules_for_chart(chart, asc_id)

        # E. DASHA CALCULATION
        dasha_data = {"timeline": [], "current": {}}
        if "Moon" in chart:
            moon_deg = chart["Moon"]["absolute_longitude"]
            birth_dt = datetime(d.year, d.month, d.day, d.hour, d.minute)

            raw_timeline = dasha_engine.calculate_dashas(moon_deg, birth_dt)
            raw_current = dasha_engine.get_current_dasha_details(raw_timeline)

            def serialize_node(node):
                obj = {
                    "lord": node["lord"],
                    "start": node["start"].strftime("%Y-%m-%d"),
                    "end": node["end"].strftime("%Y-%m-%d"),
                    "type": node.get("type", "Unknown"),
                }
                if "sub_periods" in node and node["sub_periods"]:
                    obj["sub_periods"] = [
                        serialize_node(child) for child in node["sub_periods"]
                    ]
                return obj

            dasha_data["timeline"] = [serialize_node(md) for md in raw_timeline]

            if raw_current:
                for k, v in raw_current.items():
                    dasha_data["current"][k] = {
                        "lord": v["lord"],
                        "start": v["start"].strftime("%Y-%m-%d"),
                        "end": v["end"].strftime("%Y-%m-%d"),
                    }

        # F. YOGA CALCULATION
        yogas = yoga_engine.check_yogas(chart)

        # G. AI Generation
        meta = {
            "fact_sheet": fact_sheet,
            "ascendant_sign": [
                "Aries",
                "Taurus",
                "Gemini",
                "Cancer",
                "Leo",
                "Virgo",
                "Libra",
                "Scorpio",
                "Sagittarius",
                "Capricorn",
                "Aquarius",
                "Pisces",
            ][asc_id],
            "destiny_score": score,
            "house_structure": {},
        }
        ai_reading = generate_horoscope_reading(rules, meta)

        return {
            "planets": chart,
            "predictions": rules,
            "meta": meta,
            "ai_reading": ai_reading,
            "dasha": dasha_data,
            "yogas": yogas,
            "jaimini_karakas": {},
        }

    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/daily_forecast")
def daily_forecast(d: BirthDetails):
    c = astro_engine.calculate_chart(
        d.year, d.month, d.day, d.hour, d.minute, d.latitude, d.longitude, d.timezone
    )
    return {
        "transits": transit_engine.calculate_current_transits(
            c, {"lat": d.latitude, "lon": d.longitude, "tz": d.timezone}
        )
    }


class MatchRequest(BaseModel):
    p1: BirthDetails
    p2: BirthDetails


@app.post("/match")
def match_charts(r: MatchRequest):
    c1 = astro_engine.calculate_chart(
        r.p1.year,
        r.p1.month,
        r.p1.day,
        r.p1.hour,
        r.p1.minute,
        r.p1.latitude,
        r.p1.longitude,
        r.p1.timezone,
    )
    c2 = astro_engine.calculate_chart(
        r.p2.year,
        r.p2.month,
        r.p2.day,
        r.p2.hour,
        r.p2.minute,
        r.p2.latitude,
        r.p2.longitude,
        r.p2.timezone,
    )
    analysis = match_engine.calculate_compatibility(c1, c2)

    # Construct a detailed prompt for the AI
    details = analysis.get("details", {})
    prompt = f"""
    You are an UNFILTERED, brutally honest Vedic Astrologer. Analyze this relationship compatibility (Ashta Koota):
    
    TOTAL SCORE: {analysis.get("score")} / 36
    
    DETAILED BREAKDOWN:
    1. Varna (Work/Ego): {details.get("Varna")}/1
    2. Vashya (Dominance/Control): {details.get("Vashya")}/2
    3. Tara (Destiny/Luck): {details.get("Tara")}/3
    4. Yoni (Intimacy/Nature): {details.get("Yoni")}/4
    5. Maitri (Friendship/Mental): {details.get("Maitri")}/5
    6. Gana (Temperament): {details.get("Gana")}/6
    7. Bhakoot (Love/Emotional Flow): {details.get("Bhakoot")}/7
    8. Nadi (Health/Genetics): {details.get("Nadi")}/8
    
    Manglik Status: {analysis.get("manglik", {}).get("match_status")}
    
    INSTRUCTIONS:
    - Provide a bulleted list of RAW, SENSATIONAL insights.
    - **CRITICAL**: DO NOT mention the numeric score (e.g. don't say "A score of 7/7 means..."). The user already sees the score. Just give the INTERPRETATION.
    - Keep each point concise (1-2 sentences).
    - Use heavy, dramatic words.
    
    FORMAT:
    * **Varna**: [Concise, punchy insight]
    * **Vashya**: [Concise, punchy insight]
    ...
    * **Final Verdict**: [Brutal Conclusion] [with hope and what needs to be done to save the relation]

    """

    verdict = chat_with_astrologer(prompt, "Relationship Context")
    return {"analysis": analysis, "ai_verdict": verdict}


class ChatRequest(BaseModel):
    query: str
    context: str


@app.post("/chat")
def chat_endpoint(r: ChatRequest):
    return {"response": chat_with_astrologer(r.query, r.context)}


@app.post("/chart-image")
def get_chart_image(style: str, d: BirthDetails):
    """
    Generates a D1 or D9 chart image.
    Query param: style ('d1' or 'd9')
    Body: BirthDetails
    """
    # Calculate Chart
    chart = astro_engine.calculate_chart(
        d.year, d.month, d.day, d.hour, d.minute, d.latitude, d.longitude, d.timezone
    )

    if style.lower() == "d9":
        # Prepare data for D9 (Navamsa)
        d9_planets = {}
        asc_id = chart["Ascendant"]["d9_sign_id"]
        for p, info in chart.items():
            # For D9, we use the D9 sign ID as the 'sign_id' for plotting
            d9_planets[p] = {
                "sign_id": info["d9_sign_id"],
                "is_retrograde": info.get("is_retrograde", False),
            }
        buf = draw_north_indian_chart(d9_planets, asc_id, "D9 Navamsa")
    else:
        # Prepare data for D1 (Rashi)
        asc_id = chart["Ascendant"]["sign_id"]
        buf = draw_north_indian_chart(chart, asc_id, "D1 Rashi")

    return StreamingResponse(buf, media_type="image/png")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
