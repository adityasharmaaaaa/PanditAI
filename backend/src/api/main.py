from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.api.schemas import BirthDetails, ChartResponse
from src.astronomy.engine import VedicAstroEngine
from src.astronomy.vargas import calculate_d9_navamsa
from src.astronomy.jaimini import get_chara_karakas
from src.astronomy.aspects import get_planet_aspects
from src.astronomy.arudhas import calculate_arudha_padas
from src.knowledge_graph.query import PanditGraphQuery
from src.model.inference import generate_horoscope_reading

# --- GLOBAL DATABASE INSTANCE ---
graph_db = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global graph_db
    try:
        print("🔌 Initializing Knowledge Graph Connection...")
        graph_db = PanditGraphQuery()
        print("✅ Graph Connected.")
    except Exception as e:
        print(f"⚠️ Warning: Could not connect to Neo4j: {e}")
        print("   The API will function, but 'AI Readings' will be limited.")
        graph_db = None

    yield

    if graph_db:
        print("🔌 Closing Graph Connection...")
        graph_db.close()


app = FastAPI(title="PanditAI Core", version="0.4.0", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/calculate", response_model=ChartResponse)
async def calculate_chart(input: BirthDetails):
    global graph_db

    try:
        # 1. Astronomical Calculations
        engine = VedicAstroEngine(ayanamsa=input.ayanamsa)
        chart_data = engine.calculate_chart(
            input.year,
            input.month,
            input.day,
            input.hour,
            input.minute,
            input.latitude,
            input.longitude,
            input.timezone,
        )

        # 2. House & Ruler Logic
        signs = [
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
        ]

        RULER_MAP = {
            "Aries": "Mars",
            "Taurus": "Venus",
            "Gemini": "Mercury",
            "Cancer": "Moon",
            "Leo": "Sun",
            "Virgo": "Mercury",
            "Libra": "Venus",
            "Scorpio": "Mars",
            "Sagittarius": "Jupiter",
            "Capricorn": "Saturn",
            "Aquarius": "Saturn",
            "Pisces": "Jupiter",
        }

        asc_sign_id = chart_data["Ascendant"]["sign_id"]
        asc_sign_name = signs[asc_sign_id]
        asc_ruler_name = RULER_MAP[asc_sign_name]

        house_details = {}
        for h in range(1, 13):
            current_sign_id = (asc_sign_id + h - 1) % 12
            s_name = signs[current_sign_id]
            house_details[f"House {h}"] = {"Sign": s_name, "Ruler": RULER_MAP[s_name]}

        for p_name, data in chart_data.items():
            if p_name == "Ascendant":
                continue
            p_sign = data["sign_id"]

            house_num = (p_sign - asc_sign_id) + 1
            if house_num <= 0:
                house_num += 12
            data["house_number"] = house_num

            if "absolute_longitude" in data:
                data["navamsa_sign_id"] = calculate_d9_navamsa(
                    data["absolute_longitude"]
                )

        # 3. Advanced Calculations
        aspect_list = get_planet_aspects(chart_data)
        arudha_data = calculate_arudha_padas(chart_data, house_details)
        karakas = get_chara_karakas(chart_data)

        # 4. Retrieval (RAG)
        predictions = []
        if graph_db:
            try:
                # Support both new and old query.py versions
                if hasattr(graph_db, "get_comprehensive_rules"):
                    predictions = graph_db.get_comprehensive_rules(
                        chart_data, house_details
                    )
                else:
                    for p_name, p_data in chart_data.items():
                        if p_name == "Ascendant":
                            continue
                        h_num = p_data.get("house_number")
                        # Ensure h_num is not None before passing to get_rules_for_planet_in_house
                        if h_num is not None:
                            rules = graph_db.get_rules_for_planet_in_house(
                                p_name, h_num
                            )
                            for r in rules:
                                predictions.append(
                                    {
                                        "type": "Placement",
                                        "rule": r.get("rule_text", r.get("text", "")),
                                        "condition": r.get("condition", ""),
                                    }
                                )
            except Exception as e:
                print(f"❌ Graph Query Error: {e}")

        # 5. Build Context for LLM
        # Ensure this block in main.py is strictly creating the string
        fact_sheet = "--- SECTION 1: IDENTITY ---\n"
        fact_sheet += f"ASCENDANT: {asc_sign_name} (Ruled by {asc_ruler_name})\n"

        fact_sheet += "\n--- SECTION 2: PLANETARY POSITIONS ---\n"
        for p_name, p_data in chart_data.items():
            if p_name == "Ascendant":
                continue
            s_name = signs[p_data["sign_id"]]
            h_num = p_data["house_number"]

            # Explicitly formatting the line to be unambiguous for the AI
            fact_sheet += f"Planet: {p_name} | Sign: {s_name} | House: {h_num}\n"

        fact_sheet += "\n--- SECTION 3: NAVAMSA (D9) ---\n"
        for p_name, p_data in chart_data.items():
            if "navamsa_sign_id" in p_data:
                fact_sheet += f"- {p_name} (D9): {signs[p_data['navamsa_sign_id']]}\n"

        fact_sheet += "\n--- SECTION 4: ASPECTS & SPECIAL LAGNAS ---\n"
        if aspect_list:
            for aspect in aspect_list:
                fact_sheet += f"- {aspect}\n"

        ul_sign = arudha_data.get("UL (Upapada)", {}).get("sign", "Unknown")
        fact_sheet += f"- Upapada Lagna (UL): {ul_sign}\n"
        # Access 'name' safely with .get() as karakas might not always have 'name'
        ak_name = karakas.get("Atmakaraka (AK)", {}).get("name", "Unknown")
        fact_sheet += f"- Atmakaraka (Soul): {ak_name}\n"

        chart_meta = {
            "ascendant_sign": asc_sign_name,
            "ascendant_ruler": asc_ruler_name,
            "fact_sheet": fact_sheet,
            "house_structure": house_details,
        }

        # 6. Generate AI Reading
        reading_text = generate_horoscope_reading(predictions, chart_meta)

        return {
            "meta": chart_meta,
            "planets": chart_data,
            "jaimini_karakas": karakas,
            "predictions": predictions,
            "ai_reading": reading_text,
        }

    except Exception as e:
        print(f"🔥 Critical Server Error: {e}")
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    # Use standard uvicorn string format to allow reload
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
