import streamlit as st
import joblib
import numpy as np
import os

st.set_page_config(page_title="Meridian HR · Hiring Suite", page_icon="🌿", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ─── BASE ─────────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

.stApp {
    background-color: #f5f0e8;
    background-image:
        radial-gradient(ellipse 70% 40% at 80% 10%, rgba(196, 98, 45, 0.06) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 10% 90%, rgba(139, 109, 56, 0.07) 0%, transparent 55%);
    color: #2c1f14;
}

/* ─── HIDE DEFAULT CHROME ──────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2.5rem 3.5rem 4rem 3.5rem !important;
    max-width: 1300px;
}

/* ─── SIDEBAR ──────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #2c1f14 !important;
    border-right: none !important;
}

[data-testid="stSidebar"] .block-container {
    padding: 2rem 1.6rem !important;
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] .stSlider label {
    color: #b8a48a !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
}

[data-testid="stSidebar"] input[type="number"] {
    color: #f5f0e8 !important;
    font-family: 'DM Sans', sans-serif !important;
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(184, 164, 138, 0.25) !important;
    border-radius: 8px !important;
}

/* Slider track */
[data-testid="stSidebar"] .stSlider > div > div > div > div {
    background: linear-gradient(90deg, #c4622d, #8b6d38) !important;
}
[data-testid="stSidebar"] .stSlider > div > div > div > div > div {
    background: #f5f0e8 !important;
    border: 2px solid #c4622d !important;
    box-shadow: 0 2px 8px rgba(196, 98, 45, 0.4) !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(184, 164, 138, 0.2) !important;
    margin: 1.4rem 0 !important;
}

[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, #c4622d 0%, #9e4e24 100%) !important;
    color: #faf7f2 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.8rem !important;
    width: 100% !important;
    box-shadow: 0 4px 18px rgba(196, 98, 45, 0.35) !important;
    transition: all 0.25s ease !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    box-shadow: 0 6px 24px rgba(196, 98, 45, 0.55) !important;
    transform: translateY(-1px) !important;
}

/* ─── METRIC CARDS ─────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: #faf7f2 !important;
    border: 1px solid rgba(139, 109, 56, 0.18) !important;
    border-radius: 14px !important;
    padding: 1.4rem 1.6rem 1.3rem !important;
    box-shadow: 0 2px 16px rgba(44, 31, 20, 0.06), 0 1px 4px rgba(44,31,20,0.05) !important;
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #c4622d, #8b6d38, #c4a45a);
    border-radius: 0 0 14px 14px;
}

[data-testid="stMetric"] label {
    color: #9a836a !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.09em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
}
[data-testid="stMetricValue"] {
    color: #2c1f14 !important;
    font-family: 'Playfair Display', serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
}

/* ─── DIVIDER ──────────────────────────────────────────────────── */
hr {
    border-color: rgba(139, 109, 56, 0.2) !important;
    margin: 1.8rem 0 !important;
}

/* ─── SECTION HEADINGS ─────────────────────────────────────────── */
h4 {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #b8a070 !important;
    font-weight: 600 !important;
    margin-bottom: 1.1rem !important;
}

/* ─── STAT BARS ─────────────────────────────────────────────────── */
.stat-row {
    background: #faf7f2;
    border: 1px solid rgba(139, 109, 56, 0.15);
    border-radius: 12px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 0.7rem;
    box-shadow: 0 1px 6px rgba(44,31,20,0.04);
}
.stat-row-top {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.55rem;
}
.stat-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #9a836a;
    font-weight: 500;
}
.stat-value {
    font-family: 'Playfair Display', serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: #2c1f14;
}
.track {
    background: rgba(139, 109, 56, 0.1);
    border-radius: 99px;
    height: 7px;
    overflow: hidden;
}
.fill {
    height: 100%;
    border-radius: 99px;
}

/* ─── IDLE STATE ───────────────────────────────────────────────── */
.idle-card {
    background: #faf7f2;
    border: 1px solid rgba(139, 109, 56, 0.2);
    border-radius: 14px;
    padding: 3rem 2.5rem;
    text-align: center;
    box-shadow: 0 2px 12px rgba(44,31,20,0.05);
}
.idle-card .idle-icon { font-size: 2.8rem; margin-bottom: 0.8rem; }
.idle-card .idle-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: #2c1f14;
    margin-bottom: 0.5rem;
}
.idle-card .idle-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    color: #9a836a;
    line-height: 1.65;
}

/* ─── RESULT CARDS ──────────────────────────────────────────────── */
@keyframes rise-in {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}

.result-pass {
    background: linear-gradient(145deg, #f0f7ee 0%, #e8f5e3 100%);
    border: 1px solid rgba(88, 150, 70, 0.3);
    border-radius: 16px;
    padding: 3.5rem 3rem;
    text-align: center;
    box-shadow: 0 8px 40px rgba(88, 150, 70, 0.12), 0 2px 10px rgba(44,31,20,0.05);
    animation: rise-in 0.55s cubic-bezier(0.22, 1, 0.36, 1) both;
    position: relative;
    overflow: hidden;
}
.result-pass::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(90deg, #589646, #82c36d, #589646);
}
.result-pass .badge {
    display: inline-block;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #589646;
    background: rgba(88,150,70,0.12);
    border: 1px solid rgba(88,150,70,0.25);
    border-radius: 99px;
    padding: 4px 14px;
    margin-bottom: 1rem;
}
.result-pass .verdict {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    color: #3a6b2a;
    margin: 0.3rem 0 1rem;
}
.result-pass .desc {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    color: #5a7a52;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.7;
}

.result-fail {
    background: linear-gradient(145deg, #faf0ee 0%, #f7e8e5 100%);
    border: 1px solid rgba(196, 80, 60, 0.25);
    border-radius: 16px;
    padding: 3.5rem 3rem;
    text-align: center;
    box-shadow: 0 8px 40px rgba(196, 80, 60, 0.1), 0 2px 10px rgba(44,31,20,0.05);
    animation: rise-in 0.55s cubic-bezier(0.22, 1, 0.36, 1) both;
    position: relative;
    overflow: hidden;
}
.result-fail::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(90deg, #c4503c, #e07060, #c4503c);
}
.result-fail .badge {
    display: inline-block;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #c4503c;
    background: rgba(196,80,60,0.1);
    border: 1px solid rgba(196,80,60,0.22);
    border-radius: 99px;
    padding: 4px 14px;
    margin-bottom: 1rem;
}
.result-fail .verdict {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    color: #963028;
    margin: 0.3rem 0 1rem;
}
.result-fail .desc {
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    color: #8a5048;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.7;
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
    <div style="padding-bottom:0.5rem;">
        <div style="font-family:'DM Sans',sans-serif; font-size:0.65rem; color:#7a6050;
                    letter-spacing:0.16em; text-transform:uppercase; margin-bottom:0.35rem;">
            Meridian HR Suite
        </div>
        <div style="font-family:'Playfair Display',serif; font-size:1.4rem; font-weight:700;
                    color:#f5f0e8; line-height:1.3;">
            Candidate<br>Evaluation
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    years_experience = st.slider("Years of Experience", 0, 50, 5)
    technical_score  = st.slider("Technical Score (0–100)", 0, 100, 85)
    interview_score  = st.slider("Interview Score (0–10)", 0, 10, 8)
    certifications   = st.number_input("Certifications", min_value=0, max_value=20, value=2)

    st.divider()
    analyze_btn = st.button("Run Evaluation", type="primary", use_container_width=True)

# ─── MAIN ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:2rem;">
    <div style="font-family:'DM Sans',sans-serif; font-size:0.68rem; color:#b8a070;
                letter-spacing:0.16em; text-transform:uppercase; font-weight:600;
                margin-bottom:0.4rem;">AI · Hiring Intelligence</div>
    <div style="font-family:'Playfair Display',serif; font-size:2.6rem; font-weight:700;
                color:#2c1f14; line-height:1.2; margin-bottom:0.5rem;">
        HR Decision Dashboard
    </div>
    <div style="font-family:'DM Sans',sans-serif; font-size:0.95rem; color:#9a836a;
                font-weight:300; max-width:560px; line-height:1.65;">
        Enter the candidate's details in the sidebar and run an evaluation
        to receive an AI-generated hiring recommendation.
    </div>
</div>
""", unsafe_allow_html=True)

st.write("#### Candidate Snapshot")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Experience", f"{years_experience} yrs")
c2.metric("Technical",  f"{technical_score} / 100")
c3.metric("Interview",  f"{interview_score} / 10")
c4.metric("Certifications", str(certifications))

st.divider()

st.write("#### Score Breakdown")
bars = [
    ("Years of Experience", years_experience, 50,  "#c4622d", f"{years_experience} / 50 yrs"),
    ("Technical Score",     technical_score,  100, "#8b6d38", f"{technical_score} / 100"),
    ("Interview Score",     interview_score,  10,  "#c4a45a", f"{interview_score} / 10"),
    ("Certifications",      certifications,   20,  "#7a9660", f"{certifications} / 20"),
]
for label, val, mx, color, display in bars:
    pct = int(val / mx * 100)
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-row-top">
            <span class="stat-label">{label}</span>
            <span class="stat-value">{display}</span>
        </div>
        <div class="track">
            <div class="fill" style="width:{pct}%; background:{color};"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.write("#### Hiring Recommendation")

if analyze_btn:
    with st.spinner("Analysing candidate profile..."):
        input_data = np.array([[years_experience, technical_score, interview_score, certifications]])
        prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.markdown("""
        <div class="result-pass">
            <div class="badge">✓ Evaluation Complete</div>
            <div class="verdict">Shortlisted</div>
            <div class="desc">
                This candidate meets and exceeds the required thresholds. They are
                recommended to proceed to the next stage of the hiring process.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown("""
        <div class="result-fail">
            <div class="badge">✕ Evaluation Complete</div>
            <div class="verdict">Not Progressing</div>
            <div class="desc">
                This candidate does not currently meet the minimum requirements.
                Consider re-evaluating after further development or experience.
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="idle-card">
        <div class="idle-icon">🌿</div>
        <div class="idle-title">Ready to Evaluate</div>
        <div class="idle-sub">
            Adjust the candidate's details in the sidebar panel,<br>
            then click <strong>Run Evaluation</strong> to generate a recommendation.
        </div>
    </div>
    """, unsafe_allow_html=True)
