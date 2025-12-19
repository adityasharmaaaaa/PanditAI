import sys
import os

# 1. FIX MODULE PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import requests
import pandas as pd
from datetime import datetime, time
import io

# --- IMPORTS ---
from src.utils.pdf_generator import PDFReportGenerator
from src.utils.chart_plotter import draw_north_indian_chart

# --- CONFIGURATION ---
BASE = "http://127.0.0.1:8000"
st.set_page_config(page_title="PanditAI", page_icon="🕉️", layout="wide")
st.title("🕉️ PanditAI: Vedic Life Architect")

# --- SESSION STATE ---
if "chat" not in st.session_state: st.session_state["chat"] = []
if "transits" not in st.session_state: st.session_state["transits"] = None

# --- SIDEBAR MODE SELECTOR ---
mode = st.sidebar.radio("Select Mode", ["👤 Individual Destiny", "❤️ Relationship Match"])

# ==========================================
# MODE 1: INDIVIDUAL DESTINY
# ==========================================
if mode == "👤 Individual Destiny":
    with st.sidebar:
        st.header("Birth Details")
        name = st.text_input("Name", value="Aditya")
        d = st.date_input("Date", datetime(1990, 5, 15))
        t = st.time_input("Time", time(14, 30))
        lat = st.number_input("Lat", 28.61); lon = st.number_input("Lon", 77.20); tz = st.number_input("TZ", 5.5)
        
        # ACTION BUTTONS
        if st.button("Analyze Chart", type="primary"):
            dt = datetime.combine(d, t)
            payload = {"year": dt.year, "month": dt.month, "day": dt.day, "hour": dt.hour, "minute": dt.minute, "latitude": lat, "longitude": lon, "timezone": tz, "ayanamsa": "LAHIRI"}
            with st.spinner("Calculating..."):
                res = requests.post(f"{BASE}/predict", json=payload)
                if res.status_code == 200: st.session_state["data"] = res.json()
                else: st.error("Backend Error")
        
        if st.button("Check Transits"):
            dt = datetime.combine(d, t)
            payload = {"year": dt.year, "month": dt.month, "day": dt.day, "hour": dt.hour, "minute": dt.minute, "latitude": lat, "longitude": lon, "timezone": tz, "ayanamsa": "LAHIRI"}
            res = requests.post(f"{BASE}/daily_forecast", json=payload)
            if res.status_code == 200: st.session_state["transits"] = res.json()["transits"]

        if st.button("📄 Generate PDF"):
            if "data" in st.session_state:
                buf = io.BytesIO()
                gen = PDFReportGenerator(buf)
                gen.create_report(name, st.session_state["data"])
                st.download_button("Download PDF", buf.getvalue(), f"{name}_Destiny.pdf", "application/pdf")

    # MAIN CONTENT
    if "data" in st.session_state:
        data = st.session_state["data"]
        
        # 1. TRANSITS
        if st.session_state["transits"]:
            with st.expander("🌌 Today's Sky (Transits)", expanded=True):
                cols = st.columns(3)
                for i, tr in enumerate(st.session_state["transits"]):
                    icon = "🪐" if tr['planet'] in ["Saturn","Jupiter","Mars"] else "⚪"
                    cols[i%3].info(f"**{icon} {tr['planet']}** in H{tr['transiting_house']}\n\n{tr['prediction']}")

        # 2. SCORECARD
        sc = data["meta"]["destiny_score"]
        c1, c2 = st.columns([1,3])
        c1.metric("Destiny Score", f"{sc}/100")
        c2.progress(sc)
        
        # 3. TABS
        t1, t2, t3, t4, t5 = st.tabs(["🔮 Analysis", "⏳ Timeline", "📐 Charts", "💬 Chat", "🧘 Yogas"])
        
        # TAB 1: AI Reading
        with t1: st.markdown(data["ai_reading"])
        
        # TAB 2: INTERACTIVE DASHA
        with t2:
            st.subheader("⏳ Interactive Dasha Explorer")
            full_timeline = data["dasha"]["timeline"]
            
            md_opts = [f"{m['lord']} ({m['start']} ➝ {m['end']})" for m in full_timeline]
            sel_md_idx = st.selectbox("Select Mahadasha", range(len(md_opts)), format_func=lambda x: md_opts[x])
            curr_md = full_timeline[sel_md_idx]
            
            if "sub_periods" in curr_md and curr_md["sub_periods"]:
                st.markdown(f"**📂 Antardashas within {curr_md['lord']}**")
                ad_list = curr_md["sub_periods"]
                ad_opts = [f"{a['lord']} ({a['start']} ➝ {a['end']})" for a in ad_list]
                
                sel_ad_idx = st.selectbox(f"Select Antardasha", range(len(ad_opts)), format_func=lambda x: ad_opts[x])
                curr_ad = ad_list[sel_ad_idx]
                
                st.dataframe(pd.DataFrame(ad_list).drop(columns=["sub_periods", "type"], errors="ignore"), use_container_width=True)

                if "sub_periods" in curr_ad and curr_ad["sub_periods"]:
                    st.divider()
                    st.markdown(f"**📂 Pratyantars within {curr_ad['lord']}**")
                    pd_list = curr_ad["sub_periods"]
                    pd_opts = [f"{p['lord']} ({p['start']} ➝ {p['end']})" for p in pd_list]
                    sel_pd_idx = st.selectbox(f"Select Pratyantar", range(len(pd_opts)), format_func=lambda x: pd_opts[x])
                    curr_pd = pd_list[sel_pd_idx]
                    st.dataframe(pd.DataFrame(pd_list).drop(columns=["sub_periods", "type"], errors="ignore"), use_container_width=True)
                    
                    if "sub_periods" in curr_pd and curr_pd["sub_periods"]:
                        st.divider()
                        st.markdown(f"**📂 Sookshmas within {curr_pd['lord']}**")
                        sd_list = curr_pd["sub_periods"]
                        st.dataframe(pd.DataFrame(sd_list).drop(columns=["sub_periods", "type"], errors="ignore"), use_container_width=True)

        # TAB 3: VISUAL CHARTS
        with t3:
            st.subheader("📐 Vedic Charts (Kundali)")
            st.caption("Visual representation of the Rashi (D1) and Navamsa (D9) charts.")
            
            if "planets" in data and "Ascendant" in data["planets"]:
                asc_id = data["planets"]["Ascendant"]["sign_id"]
                
                # D1 Chart
                d1_buf = draw_north_indian_chart(data["planets"], asc_id, "D1 Rashi (Birth Chart)")
                
                # D9 Chart
                d9_planets = {}
                d9_asc_id = data["planets"]["Ascendant"]["d9_sign_id"]
                for p, info in data["planets"].items():
                    d9_planets[p] = {"sign_id": info["d9_sign_id"], "is_retrograde": info.get("is_retrograde", False)}
                
                d9_buf = draw_north_indian_chart(d9_planets, d9_asc_id, "D9 Navamsa (Strength)")
                
                c1, c2 = st.columns(2)
                with c1: st.image(d1_buf, use_container_width=True)
                with c2: st.image(d9_buf, use_container_width=True)
            
            st.divider()
            st.subheader("Planetary Details")
            rows = [{"Planet":p, "Sign": d["sign_id"], "House": d.get("house_number"), "Deg": f"{d['degree']:.2f}"} for p,d in data["planets"].items()]
            st.dataframe(pd.DataFrame(rows), use_container_width=True)
            
        # TAB 4: CHAT
        with t4:
            for m in st.session_state["chat"]: st.chat_message(m["role"]).write(m["content"])
            if q := st.chat_input("Ask PanditAI..."):
                st.session_state["chat"].append({"role":"user","content":q})
                st.chat_message("user").write(q)
                ctx = data["meta"]["fact_sheet"]
                res = requests.post(f"{BASE}/chat", json={"query":q, "context": ctx}).json()["response"]
                st.session_state["chat"].append({"role":"assistant","content":res})
                st.chat_message("assistant").write(res)
                
        # TAB 5: YOGAS (NEW)
        with t5:
            st.subheader("🧘 Detected Yogas (Planetary Combinations)")
            st.caption("Special auspicious and inauspicious patterns found in your chart.")
            
            if "yogas" in data and data["yogas"]:
                categories = {}
                for y in data["yogas"]:
                    cat = y["category"]
                    if cat not in categories: categories[cat] = []
                    categories[cat].append(y)
                
                for cat, yoga_list in categories.items():
                    with st.expander(f"📌 {cat} Yogas ({len(yoga_list)})", expanded=True):
                        for y in yoga_list:
                            st.markdown(f"**{y['name']}**")
                            st.write(f"_{y['desc']}_")
                            st.divider()
            else:
                st.info("No major classical yogas detected in this simplified scan.")

# ==========================================
# MODE 2: RELATIONSHIP MATCH
# ==========================================
elif mode == "❤️ Relationship Match":
    c1, c2 = st.columns(2)
    with c1: st.subheader("Partner A"); d1 = st.date_input("Date A", datetime(1990,1,1)); t1 = st.time_input("Time A", time(12,0))
    with c2: st.subheader("Partner B"); d2 = st.date_input("Date B", datetime(1995,1,1)); t2 = st.time_input("Time B", time(12,0))
    
    if st.button("Check Match"):
        p = {"latitude": 28.61, "longitude": 77.20, "timezone": 5.5, "ayanamsa": "LAHIRI"}
        pl = {"p1": {**p, "year":d1.year, "month":d1.month, "day":d1.day, "hour":t1.hour, "minute":t1.minute},
              "p2": {**p, "year":d2.year, "month":d2.month, "day":d2.day, "hour":t2.hour, "minute":t2.minute}}
        
        res = requests.post(f"{BASE}/match", json=pl).json()
        ana = res["analysis"]
        
        st.divider()
        st.metric("Mars Dosha", ana["manglik"]["status"])
        st.caption(ana["manglik"]["desc"])
        st.metric("Emotional Sync", f"{ana['emotional']['score']}/100")
        st.info(f"AI Verdict: {res['ai_verdict']}")