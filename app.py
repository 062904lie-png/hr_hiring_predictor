import streamlit as st
import joblib
import numpy as np
import os

st.set_page_config(page_title="TalentIQ · HR Intelligence", page_icon="⬡", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ─── GLOBAL RESET & BASE ─────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif !important;
}

.stApp {
    background-color: #080c14;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(0, 180, 255, 0.08) 0%, transparent 60%),
        repeating-linear-gradient(
            0deg, transparent, transparent 39px,
            rgba(255,255,255,0.015) 39px, rgba(255,255,255,0.015) 40px
        ),
        repeating-linear-gradient(
            90deg, transparent, transparent 39px,
            rgba(255,255,255,0.015) 39px, rgba(255,255,255,0.015) 40px
        );
    color: #e2e8f0;
}

/* ─── HIDE STREAMLIT CHROME ──────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 3rem 4rem 3rem !important; max-width: 1400px; }

/* ─── SIDEBAR ─────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #0b1120 !important;
    border-right: 1px solid rgba(0, 200, 255, 0.12) !important;
    padding-top: 0 !important;
}

[data-testid="stSidebar"]::before {
    content: '';
    display: block;
    height: 4px;
    background: linear-gradient(90deg, #00c8ff, #0066ff, #7b2fff);
    margin-bottom: 2rem;
}

[data-testid="stSidebar"] .block-container {
    padding: 0 1.5rem 2rem 1.5rem !important;
}

/* Sidebar labels */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] p {
    color: #7a95b8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* Slider track */
[data-testid="stSidebar"] .stSlider > div > div > div > div {
    background: linear-gradient(90deg, #00c8ff, #0066ff) !important;
}
[data-testid="stSidebar"] .stSlider > div > div > div > div > div {
    background: #ffffff !important;
    border: 2px solid #00c8ff !important;
    box-shadow: 0 0 10px rgba(0,200,255,0.5) !important;
}

/* Number input */
[data-testid="stSidebar"] input[type="number"] {
    background: #0d1929 !important;
    border: 1px solid rgba(0, 200, 255, 0.25) !important;
    border-radius: 6px !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Divider */
[data-testid="stSidebar"] hr {
    border-color: rgba(0, 200, 255, 0.1) !important;
    margin: 1.5rem 0 !important;
}

/* Sidebar button */
[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, #00c8ff 0%, #0066ff 100%) !important;
    color: #ffffff !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.75rem 1.5rem !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 0 20px rgba(0, 150, 255, 0.3) !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    box-shadow: 0 0 35px rgba(0, 150, 255, 0.55) !important;
    transform: translateY(-1px) !important;
}

/* ─── METRIC CARDS ────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #0d1929 0%, #0b1522 100%) !important;
    border: 1px solid rgba(0, 200, 255, 0.14) !important;
    border-radius: 12px !important;
    padding: 1.4rem 1.6rem !important;
    position: relative !important;
    overflow: hidden !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(0, 200, 255, 0.4) !important;
    box-shadow: 0 0 25px rgba(0, 150, 255, 0.1) !important;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, #00c8ff, #7b2fff);
}

[data-testid="stMetric"] label {
    color: #4a7080 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    color: #e2e8f0 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
}

/* ─── DIVIDER ─────────────────────────────────────────────────────── */
hr {
    border-color: rgba(0, 200, 255, 0.1) !important;
}

/* ─── INFO BOX ────────────────────────────────────────────────────── */
[data-testid="stAlert"] {
    background: rgba(0, 100, 200, 0.08) !important;
    border: 1px solid rgba(0, 200, 255, 0.2) !important;
    border-radius: 10px !important;
    color: #7ab8d4 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
}

/* ─── SPINNER ─────────────────────────────────────────────────────── */
.stSpinner > div {
    border-top-color: #00c8ff !important;
}

/* ─── SECTION LABELS ──────────────────────────────────────────────── */
h4 {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: #3a6080 !important;
    margin-bottom: 1rem !important;
}

/* ─── DECISION CARDS ──────────────────────────────────────────────── */
@keyframes card-in {
    0% { opacity: 0; transform: translateY(30px) scale(0.96); }
    100% { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes pulse-glow-green {
    0%, 100% { box-shadow: 0 0 40px rgba(0, 230, 120, 0.2), 0 20px 60px rgba(0,0,0,0.4); }
    50% { box-shadow: 0 0 70px rgba(0, 230, 120, 0.4), 0 20px 60px rgba(0,0,0,0.4); }
}
@keyframes pulse-glow-red {
    0%, 100% { box-shadow: 0 0 40px rgba(255, 60, 80, 0.2), 0 20px 60px rgba(0,0,0,0.4); }
    50% { box-shadow: 0 0 70px rgba(255, 60, 80, 0.4), 0 20px 60px rgba(0,0,0,0.4); }
}
@keyframes scan-line {
    0% { top: 0%; }
    100% { top: 100%; }
}

.decision-card-pass {
    background: linear-gradient(135deg, #011a0e 0%, #021f10 50%, #011810 100%);
    border: 1px solid rgba(0, 230, 120, 0.35);
    border-radius: 16px;
    padding: 4rem 3rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    animation: card-in 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) both,
               pulse-glow-green 3s ease-in-out 0.6s infinite;
}
.decision-card-pass::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, #00e678, #00ffaa, #00e678, transparent);
}
.decision-card-pass::after {
    content: '';
    position: absolute;
    left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(0, 230, 120, 0.3), transparent);
    animation: scan-line 3s linear 0.8s infinite;
    pointer-events: none;
}
.decision-card-pass .verdict {
    font-family: 'Syne', sans-serif;
    font-size: 3.5rem;
    font-weight: 800;
    color: #00e678;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 0;
    text-shadow: 0 0 40px rgba(0, 230, 120, 0.5);
}
.decision-card-pass .sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: rgba(0, 230, 120, 0.65);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.5rem;
    margin-bottom: 1.5rem;
}
.decision-card-pass .desc {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    color: #4aad7a;
    max-width: 500px;
    margin: 0 auto;
    line-height: 1.6;
}

.decision-card-fail {
    background: linear-gradient(135deg, #1a0508 0%, #1f060a 50%, #180408 100%);
    border: 1px solid rgba(255, 60, 80, 0.3);
    border-radius: 16px;
    padding: 4rem 3rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    animation: card-in 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) both,
               pulse-glow-red 3s ease-in-out 0.6s infinite;
}
.decision-card-fail::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, #ff3c50, #ff6b7a, #ff3c50, transparent);
}
.decision-card-fail::after {
    content: '';
    position: absolute;
    left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(255, 60, 80, 0.25), transparent);
    animation: scan-line 3s linear 0.8s infinite;
    pointer-events: none;
}
.decision-card-fail .verdict {
    font-family: 'Syne', sans-serif;
    font-size: 3.5rem;
    font-weight: 800;
    color: #ff3c50;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 0;
    text-shadow: 0 0 40px rgba(255, 60, 80, 0.5);
}
.decision-card-fail .sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: rgba(255, 60, 80, 0.55);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.5rem;
    margin-bottom: 1.5rem;
}
.decision-card-fail .desc {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    color: #a04555;
    max-width: 500px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ─── STAT BARS ───────────────────────────────────────────────────── */
.stat-bar-wrap {
    background: #0b1120;
    border: 1px solid rgba(0,200,255,0.1);
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.8rem;
}
.stat-bar-label {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
}
.stat-bar-label span:first-child {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #4a7080;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.stat-bar-label span:last-child {
    font-family: 'Syne', sans-serif;
    font-size: 0.9rem;
    font-weight: 700;
    color: #a0c8e0;
}
.stat-bar-track {
    background: rgba(0,200,255,0.08);
    border-radius: 4px;
    height: 6px;
    overflow: hidden;
}
.stat-bar-fill {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #00c8ff, #0066ff);
    box-shadow: 0 0 10px rgba(0,150,255,0.4);
}
</style>
""", unsafe_allow_html=True)

# ─── MODEL ────────────────────────────────────────────────────────────────────
model_path = "hr.pkl"

@st.cache_resource
def load_model():
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None

model = load_model()

if not model:
    st.error(f"Model file `{model_path}` not found. Place it in the same directory as this script.")
    st.stop()

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 1.5rem 0 0.5rem 0;">
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.62rem; 
                    letter-spacing:0.2em; color:#2a4060; text-transform:uppercase; 
                    margin-bottom:0.3rem;">TalentIQ · v2.4</div>
        <div style="font-family:'Syne',sans-serif; font-size:1.25rem; font-weight:800; 
                    color:#e2e8f0;">Candidate Profile</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    years_experience = st.slider("Years of Experience", 0, 50, 5)
    technical_score  = st.slider("Technical Score (0–100)", 0, 100, 85)
    interview_score  = st.slider("Interview Score (0–10)", 0, 10, 8)
    certifications   = st.number_input("Certifications", min_value=0, max_value=20, value=2)

    st.divider()
    analyze_btn = st.button("Run Analysis", type="primary", use_container_width=True)

# ─── MAIN ─────────────────────────────────────────────────────────────────────
# Header
st.markdown("""
<div style="display:flex; align-items:baseline; gap:1rem; margin-bottom:0.3rem;">
    <span style="font-family:'Syne',sans-serif; font-size:2.4rem; font-weight:800; 
                 color:#e2e8f0; letter-spacing:-0.01em;">HR Intelligence</span>
    <span style="font-family:'JetBrains Mono',monospace; font-size:0.7rem; 
                 color:#2a6080; letter-spacing:0.18em; text-transform:uppercase; 
                 background:rgba(0,200,255,0.07); border:1px solid rgba(0,200,255,0.15); 
                 border-radius:4px; padding:3px 10px;">AI-Powered · Random Forest</span>
</div>
<div style="font-family:'JetBrains Mono',monospace; font-size:0.8rem; color:#2a5070; 
             margin-bottom:2.5rem; letter-spacing:0.05em;">
    Evaluate candidate fitness across four performance dimensions in real time.
</div>
""", unsafe_allow_html=True)

# Metric cards
st.write("#### ◈ Candidate Snapshot")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Experience", f"{years_experience} yrs")
c2.metric("Technical", f"{technical_score} / 100")
c3.metric("Interview", f"{interview_score} / 10")
c4.metric("Certs", f"{certifications}")

st.divider()

# Visual stat bars
st.write("#### ◈ Signal Breakdown")

def pct(val, mx): return int(val / mx * 100)

st.markdown(f"""
<div class="stat-bar-wrap">
    <div class="stat-bar-label">
        <span>Experience</span><span>{years_experience} / 50 yrs</span>
    </div>
    <div class="stat-bar-track">
        <div class="stat-bar-fill" style="width:{pct(years_experience,50)}%; 
             background:linear-gradient(90deg,#00c8ff,#0055dd);"></div>
    </div>
</div>
<div class="stat-bar-wrap">
    <div class="stat-bar-label">
        <span>Technical Score</span><span>{technical_score} / 100</span>
    </div>
    <div class="stat-bar-track">
        <div class="stat-bar-fill" style="width:{pct(technical_score,100)}%; 
             background:linear-gradient(90deg,#7b2fff,#c44dff);"></div>
    </div>
</div>
<div class="stat-bar-wrap">
    <div class="stat-bar-label">
        <span>Interview Score</span><span>{interview_score} / 10</span>
    </div>
    <div class="stat-bar-track">
        <div class="stat-bar-fill" style="width:{pct(interview_score,10)}%; 
             background:linear-gradient(90deg,#00c8ff,#00e6aa);"></div>
    </div>
</div>
<div class="stat-bar-wrap">
    <div class="stat-bar-label">
        <span>Certifications</span><span>{certifications} / 20</span>
    </div>
    <div class="stat-bar-track">
        <div class="stat-bar-fill" style="width:{pct(certifications,20)}%; 
             background:linear-gradient(90deg,#ffaa00,#ff6600);"></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─── RESULT ───────────────────────────────────────────────────────────────────
st.write("#### ◈ AI Verdict")

if analyze_btn:
    with st.spinner("Processing neural inference..."):
        input_data = np.array([[years_experience, technical_score, interview_score, certifications]])
        prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.markdown("""
        <div class="decision-card-pass">
            <div class="sub">◈ Candidate Assessment Complete</div>
            <div class="verdict">✦ Shortlisted</div>
            <div style="height:1.2rem;"></div>
            <div class="desc">
                Outstanding profile. This candidate clears all performance thresholds
                and is strongly recommended for the next evaluation round.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown("""
        <div class="decision-card-fail">
            <div class="sub">◈ Candidate Assessment Complete</div>
            <div class="verdict">✕ Rejected</div>
            <div style="height:1.2rem;"></div>
            <div class="desc">
                Requirements not met. This candidate falls below the minimum
                technical or interview thresholds at this time.
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="background:rgba(0,100,200,0.05); border:1px dashed rgba(0,200,255,0.18); 
                border-radius:12px; padding:2.5rem; text-align:center;">
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.75rem; 
                    color:#2a6080; letter-spacing:0.15em; text-transform:uppercase; 
                    margin-bottom:0.6rem;">Awaiting Input</div>
        <div style="font-family:'Syne',sans-serif; font-size:1.05rem; color:#3a7090;">
            Configure the candidate profile in the sidebar,<br>then click <b style="color:#00c8ff;">Run Analysis</b> to generate a verdict.
        </div>
    </div>
    """, unsafe_allow_html=True)
