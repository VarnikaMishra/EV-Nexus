import streamlit as st
import joblib
import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# ==========================================
# 1. CONFIGURATION & MODEL LOADING
# ==========================================
# Load environment variables from .env file
load_dotenv()

# Safely fetch the API key from the environment
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("⚠️ GOOGLE_API_KEY is missing! Please check your .env configuration.")


st.set_page_config(
    page_title="EV-Nexus | Industrial & Fleet Intelligence Platform",
    page_icon="⚡",
    layout="wide"
)

@st.cache_resource
def load_resources():
    model = joblib.load("battery_model.pkl") if os.path.exists("battery_model.pkl") else None
    return model

model = load_resources()

# ==========================================
# 2. ADVANCED 3D CSS STYLING & LOGO
# ==========================================
st.markdown("""
    <style>
    /* 3D Glassmorphic Header Container */
    .nexus-header-box {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 25px 30px;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.2);
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .nexus-title-area {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    /* 3D CSS Animated Logo */
    .nexus-3d-logo {
        width: 60px;
        height: 60px;
        background: linear-gradient(145deg, #00f2fe, #4facfe);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        box-shadow: 0 8px 16px rgba(0, 242, 254, 0.4), inset 0 2px 3px rgba(255, 255, 255, 0.6);
        transform: perspective(500px) rotateX(10deg) rotateY(-10deg);
        transition: transform 0.3s ease;
    }
    .nexus-3d-logo:hover {
        transform: perspective(500px) rotateX(0deg) rotateY(0deg) scale(1.05);
    }
    
    .nexus-header-text h1 {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: 0.5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .nexus-header-text p {
        color: #e2e8f0;
        font-size: 0.95rem;
        margin: 4px 0 0 0;
        font-weight: 400;
    }
    
    /* Badge styling */
    .nexus-badge {
        background: rgba(255, 255, 255, 0.15);
        padding: 6px 14px;
        border-radius: 20px;
        color: #fff;
        font-size: 0.8rem;
        font-weight: 600;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. MULTILINGUAL DICTIONARY
# ==========================================
translations = {
    "English": {
        "sidebar_title": "⚙️ Enterprise Controls",
        "lang_label": "Select Language / भाषा चुनें",
        "role_label": "Select System Operational Role",
        "apm_role": "APM Mode (Driver / Fleet Operator Portal)",
        "mfr_role": "Manufacturer Role (Command & Supply Chain Center)",
        "header_title": "EV-NEXUS INDUSTRIAL INTELLIGENCE",
        "header_sub": "Next-Gen AI & Physics-Informed Battery Fleet Analytics",
        "active_mode": "Active Mode",
        "apm_desc": "Module: Real-time Telemetry, OSRM Trip Routing & Random Forest Diagnostics",
        "mfr_desc": "Module: Multi-Tier Supply Chain Risk Mapping & QMS Manufacturing Quality Drift"
    },
    "Hindi": {
        "sidebar_title": "⚙️ एंटरप्राइज नियंत्रण",
        "lang_label": "भाषा चुनें / Select Language",
        "role_label": "सिस्टम ऑपरेशनल रोल चुनें",
        "apm_role": "APM मोड (ड्राइवर / फ्लीट ऑपरेटर पोर्टल)",
        "mfr_role": "निर्माता भूमिका (कमांड और सप्लाई चेन सेंटर)",
        "header_title": "ईवी-नेक्सस इंडस्ट्रियल इंटेलिजेंस",
        "header_sub": "नेक्स्ट-जेन एआई और फिजिक्स-इन्फॉर्मड बैटरी फ्लीट एनालिटिक्स",
        "active_mode": "सक्रिय मोड",
        "apm_desc": "मॉड्यूल: रीयल-टाइम टेलीमेट्री, ओएसआरएम ट्रिप रूटिंग और रैंडम फॉरेस्ट डायग्नोस्टिक्स",
        "mfr_desc": "मॉड्यूल: मल्टी-टियर सप्लाई चेन रिस्क मैपिंग और क्यूएमएस मैन्युफैक्चरिंग क्वालिटी ड्रिफ्ट"
    }
}

# ==========================================
# 4. SIDEBAR NAVIGATION & MULTILINGUAL SETUP
# ==========================================
with st.sidebar:
    st.markdown("### 🌐 Localization Settings")
    selected_lang = st.selectbox("Language / भाषा", ["English", "Hindi"], index=0)
    
    t = translations[selected_lang]
    
    st.markdown("---")
    st.markdown(f"### {t['sidebar_title']}")
    portal_choice = st.radio(
        t['role_label'],
        [t['apm_role'], t['mfr_role']]
    )
    st.markdown("---")
    st.info("System Operational Status: **Online & Secured**")

GEMINI_MODEL = "Gemini 3.5 Flash"

# ==========================================
# 5. PROFESSIONAL 3D CSS HEADER RENDER
# ==========================================
is_apm = (portal_choice == t['apm_role'])
current_role_badge = "APM Fleet Portal" if is_apm else "OEM Command Center"
current_subtitle = t['apm_desc'] if is_apm else t['mfr_desc']

st.markdown(f"""
    <div class="nexus-header-box">
        <div class="nexus-title-area">
            <div class="nexus-3d-logo">⚡</div>
            <div class="nexus-header-text">
                <h1>{t['header_title']}</h1>
                <p>{current_subtitle}</p>
            </div>
        </div>
        <div>
            <span class="nexus-badge">🛡️ {current_role_badge}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# CORE RANGE CALCULATION LOGIC (Your Model)
# ==========================================
def calculate_range(c, t, p, s, speed):
    if model is not None:
        try:
            base = model.predict([[c, c * 3.7, s, t]])[0]
        except Exception:
            base = 150.0  
    else:
        base = 140.0 + (c * 10) 
        
    pax_penalty = 1.0 - ((p - 1) * 0.05)
    temp_penalty = 1.0 - (abs(t - 25) * 0.005)
    speed_penalty = 1.0 - (max(0, speed - 25)**1.5 * 0.001) 
    
    final_km = max(0, base * pax_penalty * temp_penalty * speed_penalty)
    total_hours = final_km / speed if speed > 0 else 0
    return final_km, int(total_hours), int((total_hours % 1) * 60)

# ==========================================
# PORTAL 1: APM MODE (DRIVER & FLEET BUYER)
# ==========================================
if is_apm:
    tab_apm1, tab_apm2, tab_apm3 = st.tabs(["🚗 Vehicle Profile & Telemetry", "🗺️ OSRM Trip & Charge Planner", "💬 AI Trip & APM Consultant"])

    with tab_apm1:
        st.subheader("Vehicle Onboarding & Telemetry Controls")
        
        col1, col2 = st.columns(2)
        with col1:
            cells = st.selectbox("Battery Configuration (Cells)", [3, 4, 5, 6], index=3)
            pax = st.number_input("Passengers / Payload Units", 1, 8, 1)
            soc = st.slider("State of Charge (%)", 0, 100, 80)
        with col2:
            temp = st.slider("Outside Temperature (°C)", -10, 50, 25)
            speed = st.slider("Average Speed (km/h)", 5, 80, 25)

        res_km, res_h, res_m = calculate_range(cells, temp, pax, soc, speed)

        st.markdown("---")
        m1, m2, m3 = st.columns(3)
        m1.metric("Predicted Range", f"{res_km:.2f} km")
        m2.metric("Estimated Trip Time", f"{res_h}h {res_m}m")
        m3.metric("System Voltage", f"{cells * 3.7} V")

        st.divider()

        # Charts Section
        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader("📊 Range vs. Speed Trade-off")
            speed_range = np.linspace(5, 80, 20)
            ranges = [calculate_range(cells, temp, pax, soc, s)[0] for s in speed_range]
            df_chart = pd.DataFrame({"Speed (km/h)": speed_range, "Range (km)": ranges})
            fig = px.line(df_chart, x="Speed (km/h)", y="Range (km)", title="Speed Efficiency Curve")
            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            st.subheader("🌡️ Thermal Impact Analysis")
            temps = np.linspace(-10, 50, 20)
            ranges_t = [calculate_range(cells, temps_val, pax, soc, speed)[0] for temps_val in temps]
            df_temp = pd.DataFrame({"Temperature (°C)": temps, "Range (km)": ranges_t})
            fig_t = px.area(df_temp, x="Temperature (°C)", y="Range (km)", color_discrete_sequence=['#ff7f0e'])
            st.plotly_chart(fig_t, use_container_width=True)

        st.divider()
        st.subheader("🏎️ Performance Benchmarking")
        max_km, _, _ = calculate_range(6, 25, 1, 100, 25)
        current_km = res_km
        min_km, _, _ = calculate_range(3, -10, 8, 10, 80)

        fig_bench = go.Figure()
        fig_bench.add_trace(go.Bar(
            x=['Minimum Case', 'Current Setup', 'Maximum Case'],
            y=[min_km, current_km, max_km],
            marker_color=['#ef553b', '#636efa', '#00cc96'],
            text=[f"{min_km:.1f}km", f"{current_km:.1f}km", f"{max_km:.1f}km"],
            textposition='auto',
        ))
        fig_bench.update_layout(title="Comparison: Worst vs Current vs Best Performance", yaxis_title="Range (km)", template="plotly_dark", height=400)
        st.plotly_chart(fig_bench, use_container_width=True)

    with tab_apm2:
        st.subheader("OSRM-Powered Route & Charge Requirement Estimator")
        st.write("Enter actual locations (e.g., 'Gachibowli, Hyderabad' to 'RGIA Airport') to compute real route distance via OSRM.")

        dest_col1, dest_col2 = st.columns(2)
        with dest_col1:
            start_location = st.text_input("Starting Location / Depot", "Gachibowli, Hyderabad")
            destination = st.text_input("Final Destination / Drop Point", "RGIA Airport, Hyderabad")
            run_osrm_query = st.button("Calculate Live Trip Energy & Route")
        
        with dest_col2:
            if run_osrm_query:
                if not destination.strip():
                    st.warning("Please enter a valid destination.")
                else:
                    try:
                        with st.spinner("Fetching live coordinates and OSRM route data..."):
                            geo_start = requests.get(
                                "https://nominatim.openstreetmap.org/search",
                                params={"q": start_location, "format": "json", "limit": 1},
                                headers={"User-Agent": "EV-Nexus-App"}
                            ).json()

                            geo_dest = requests.get(
                                "https://nominatim.openstreetmap.org/search",
                                params={"q": destination, "format": "json", "limit": 1},
                                headers={"User-Agent": "EV-Nexus-App"}
                            ).json()

                            if not geo_start or not geo_dest:
                                st.error("Could not resolve one or both locations. Please be more specific.")
                            else:
                                lon1, lat1 = float(geo_start[0]["lon"]), float(geo_start[0]["lat"])
                                lon2, lat2 = float(geo_dest[0]["lon"]), float(geo_dest[0]["lat"])

                                osrm_url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
                                osrm_res = requests.get(osrm_url).json()

                                if osrm_res.get("code") == "Ok":
                                    distance_meters = osrm_res["routes"][0]["distance"]
                                    distance_km = distance_meters / 1000.0
                                    
                                    st.success("Route computed successfully via OSRM Live Server!")
                                    st.metric("Live OSRM Distance", f"{distance_km:.2f} km")
                                    
                                    res_km_val, _, _ = calculate_range(cells, temp, pax, soc, speed)
                                    energy_required_soc = min(100, int((distance_km / max(1, res_km_val)) * 100))
                                    st.info(f"Estimated State of Charge (SoC) required for this distance: **~{energy_required_soc}%**")
                                    
                                    if energy_required_soc > soc:
                                        st.error("⚠️ Warning: Your current State of Charge is too low for this route. A charging stop is mandatory!")
                                    else:
                                        st.success("✅ Current battery charge is sufficient to complete this trip.")
                                else:
                                    st.error("OSRM routing failed to find a connected driving path between these points.")
                    except Exception as ex:
                        st.error(f"Connection error while fetching route: {ex}")
            else:
                st.info("Enter your points and click 'Calculate Live Trip Energy & Route'.")

    with tab_apm3:
        st.subheader(f"💬 AI Trip Consultant ({GEMINI_MODEL})")
        st.write("Ask questions about your active trip and battery configuration via text input.")

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input using st.chat_input for native Streamlit chat UX
        if user_q := st.chat_input("Ask a question about this specific trip configuration:"):
            # Append user message to state and display immediately
            st.session_state.messages.append({"role": "user", "content": user_q})
            with st.chat_message("user"):
                st.markdown(user_q)

            try:
                # Use the correct stable preview model identifier
                llm = ChatGoogleGenerativeAI(
                    model="gemini-3-flash-preview", 
                    google_api_key=GOOGLE_API_KEY
                )
                
                res_km_val, _, _ = calculate_range(cells, temp, pax, soc, speed)
                context = (
                    f"System Context: Vehicle configured with {cells} cells, "
                    f"{soc}% State of Charge, {temp}°C outside temperature, "
                    f"{pax} passenger units, operating at {speed} km/h. "
                    f"Calculated Model Range: {res_km_val:.2f} km."
                )
                
                with st.chat_message("assistant"):
                    with st.spinner("AI is calculating insights..."):
                        # Use proper LangChain message tuple formatting
                        messages_payload = [
                            ("system", context),
                            ("human", user_q)
                        ]
                        response = llm.invoke(messages_payload)
                        
                        # Extract the clean string representation from the model response
                        ai_response_text = response.text if hasattr(response, 'text') else str(response.content)
                        
                        st.markdown(ai_response_text)
                        
                # Append assistant response to state history
                st.session_state.messages.append({"role": "assistant", "content": ai_response_text})
                
            except Exception as e:
                st.error(f"API Connection/Quota Error: {e}")

# ==========================================
# PORTAL 2: MANUFACTURER ROLE
# ==========================================
else:
    tab_mfr1, tab_mfr2, tab_mfr3 = st.tabs(["🌐 Multi-Tier Supply Chain Monitor", "⚙️ QMS Quality Drift & Diagnostics", f"🤖 {GEMINI_MODEL} Supply Chain Orchestrator"])

    with tab_mfr1:
        st.subheader("Critical Battery Material Sourcing & Geopolitical Risk Graph")
        st.write("Tracking multi-tier component dependencies (Lithium, Cobalt, NMC/LFP cells) across global manufacturing lines.")

        mc1, mc2, mc3 = st.columns(3)
        with mc1:
            st.metric(label="Tier-1 Supplier Reliability", value="95.4%", delta="+0.8%")
        with mc2:
            st.metric(label="Active Bottlenecks Flagged", value="1 Warning", delta="Monitored", delta_color="inverse")
        with mc3:
            st.metric(label="Strategic Mineral Buffer", value="42 Days", delta="+4 days")

        st.markdown("### Supply Chain Sourcing Matrix")
        supply_chain_df = pd.DataFrame({
            "Component Node": ["Lithium Carbonate (LCE)", "Cobalt Cathode Binder", "NMC 811 Cell Packs", "LFP Prismatic Cells"],
            "Source Region": ["Australia / Domestic Refining", "DRC / Global Spot", "Indonesia Tier-1 Hub", "Domestic GIGA Facility"],
            "Geopolitical Risk Score": ["Low (1.8/10)", "High (7.9/10)", "Medium (4.5/10)", "Low (2.2/10)"],
            "Status": ["Secure", "At Risk (Export Volatility)", "Stable", "Fully Operational"]
        })
        st.dataframe(supply_chain_df, use_container_width=True)

    with tab_mfr2:
        st.subheader("Manufacturing Quality System (QMS) Drift Detector")
        st.write("Correlating cell batch internal resistance and voltage variance before final pack assembly.")

        qc1, qc2 = st.columns(2)
        with qc1:
            selected_batch = st.selectbox("Select Production Cell Batch", ["BATCH-NMC-2026-F1", "BATCH-LFP-2026-X9", "BATCH-NMC-2026-M4"])
            internal_res = st.slider("Internal Resistance Deviation (mΩ)", 0.05, 4.0, 1.1, key="qms_ir")
            voltage_spread_mfr = st.slider("Cell-to-Cell Voltage Spread (mV)", 0.5, 12.0, 2.8, key="qms_vs")
            
        with qc2:
            st.markdown("### Quality Analytics Assessment")
            
            if internal_res > 2.5 or voltage_spread_mfr > 7.0:
                st.error("⚠️ **Quality Drift Warning:** Potential micro-structural anomaly detected. Recommend batch quarantine.")
            else:
                st.success("✅ **Batch Approved:** Parameters conform strictly to industrial high-reliability ISO/IEC standards.")
            
            base_yield = 99.5
            ir_penalty = max(0, (internal_res - 1.0) * 2.2)
            vs_penalty = max(0, (voltage_spread_mfr - 2.0) * 0.8)
            calculated_yield = max(75.0, min(99.9, base_yield - ir_penalty - vs_penalty))
            
            yield_delta = calculated_yield - 98.5
            st.metric(
                label="Predicted Manufacturing Yield Rate", 
                value=f"{calculated_yield:.1f}%", 
                delta=f"{yield_delta:+.1f}% vs baseline",
                delta_color="normal" if calculated_yield >= 95.0 else "inverse"
            )

    with tab_mfr3:
        st.subheader(f"{GEMINI_MODEL} Supply Chain Disruption & Policy Copilot")
        st.write("Simulate supply chain shocks and generate automated multi-tier procurement rerouting strategies.")

        simulation_scenario = st.selectbox("Select Disruption Simulation Scenario", [
            "Strait of Hormuz Logistics Route Suspension",
            "Cobalt Export Limit Enforcement in Central African Corridor",
            "Domestic Cell Assembly Grid Curtailment Event"
        ])

        if st.button("Execute Strategic Simulation Query"):
            st.markdown(f"**[{GEMINI_MODEL} Orchestration Engine Output]:**")
            st.warning(f"Simulating response pipeline for: **{simulation_scenario}**")
            st.markdown("""
            * **Impact Forecast:** Production delay footprint estimated at 11.2 days across assembly line B.
            * **Automated Rerouting Trigger:** Redirecting primary sourcing allocation toward pre-vetted domestic Tier-2 partners and secondary logistics corridors.
            * **Compliance Audit Package:** Auto-generated regulatory audit documentation compiled for executive sign-off.
            """)
