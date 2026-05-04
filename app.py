import streamlit as st
import joblib
import numpy as np
import os

# --- To run this app ---
# Open Terminal (Ctrl + `) and type: streamlit run app.py
# -----------------------

st.set_page_config(
    page_title="TalentIQ · HR Decision Engine",
    page_icon="🎯",
    layout="centered"
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
/* ── Root palette ── */
:root {
    --navy:    #0d1b2a;
    --navy-mid:#132336;
    --slate:   #1e3a5f;
    --gold:    #c9a84c;
    --gold-lt: #e8c97e;
    --text:    #e8edf3;
    --muted:   #7b91a8;
    --border:  rgba(201,168,76,0.25);
    --glass:   rgba(19,35,54,0.85);
    --success-bg: #0a2e1a;
    --success-border: #2ecc71;
    --success-text: #a8f0c6;
    --reject-bg: #2e0a0a;
    --reject-border: #e74c3c;
    --reject-text: #f0a8a8;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--navy) !important;
    color: var(--text) !important;
}

.stApp {
    background: var(--navy) !important;
}

/* Subtle grid texture overlay */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(201,168,76,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(201,168,76,0.03) 1px, transparent 1px);
    background-size: 48px 48px;
    pointer-events: none;
    z-index: 0;
}

/* ── Block container ── */
.block-container {
    max-width: 760px !important;
    padding: 2.5rem 2rem !important;
    position: relative;
    z-index: 1;
}

/* ── Header ── */
.header-wrap {
    text-align: center;
    margin-bottom: 2.5rem;
}

.brand-label {
    display: inline-block;
    letter-spacing: 0.35em;
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    color: var(--gold);
    background: rgba(201,168,76,0.1);
    border: 1px solid var(--border);
    padding: 4px 14px;
    border-radius: 100px;
    margin-bottom: 1.1rem;
}

.main-title {
    font-family: 'DM Serif Display', serif !important;
    font-size: 2.6rem !important;
    font-weight: 400 !important;
    color: var(--text) !important;
    line-height: 1.15 !important;
    margin: 0 0 0.5rem !important;
}

.main-title span {
    color: var(--gold);
}

.subtitle {
    color: var(--muted);
    font-size: 0.95rem;
    font-weight: 300;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.8rem 0 !important;
}

/* ── Section heading ── */
.section-heading {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-heading::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Number inputs ── */
div[data-testid="stNumberInput"] label,
div[data-testid="stNumberInput"] p {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    margin-bottom: 6px !important;
}

div[data-testid="stNumberInput"] input {
    background: var(--navy-mid) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-size: 1.15rem !important;
    font-weight: 500 !important;
    padding: 10px 14px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

div[data-testid="stNumberInput"] input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(201,168,76,0.15) !important;
}

/* Hide number input arrow buttons */
div[data-testid="stNumberInput"] button {
    background: transparent !important;
    border: none !important;
    color: var(--muted) !important;
}

/* ── Metric cards ── */
.metric-card {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 20px;
    backdrop-filter: blur(8px);
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
}

/* ── Primary button ── */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #b8922d 0%, var(--gold) 50%, var(--gold-lt) 100%) !important;
    color: var(--navy) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    height: 3.2em !important;
    width: 100% !important;
    border-radius: 10px !important;
    border: none !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(201,168,76,0.3) !important;
}

div.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(201,168,76,0.45) !important;
    filter: brightness(1.06) !important;
}

div.stButton > button[kind="primary"]:active {
    transform: translateY(0) !important;
}

/* ── Result panels ── */
.result-panel {
    border-radius: 12px;
    padding: 28px 28px 24px;
    border-left: 4px solid;
    position: relative;
    overflow: hidden;
    animation: slideUp 0.4s ease;
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}

.result-panel.shortlist {
    background: var(--success-bg);
    border-color: var(--success-border);
}

.result-panel.reject {
    background: var(--reject-bg);
    border-color: var(--reject-border);
}

.result-verdict {
    font-family: 'DM Serif Display', serif;
    font-size: 1.7rem;
    margin: 0 0 6px;
}

.result-verdict.shortlist { color: var(--success-text); }
.result-verdict.reject    { color: var(--reject-text); }

.result-sub {
    font-size: 0.88rem;
    font-weight: 400;
    opacity: 0.75;
}

.result-sub.shortlist { color: var(--success-text); }
.result-sub.reject    { color: var(--reject-text); }

/* ── Footer ── */
.footer {
    text-align: center;
    font-size: 0.72rem;
    color: var(--muted);
    margin-top: 2.5rem;
    letter-spacing: 0.05em;
    opacity: 0.6;
}

/* ── Streamlit chrome cleanup ── */
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stToolbar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Load model ───────────────────────────────────────────────────────────────
model_path = "hr.pkl"

if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    st.error(f"Model file '{model_path}' not found. Place it in the same directory as this script.")
    st.stop()

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-wrap">
    <div class="brand-label">TalentIQ · HR Decision Engine</div>
    <h1 class="main-title">Candidate <span>Evaluation</span></h1>
    <p class="subtitle">Enter candidate profile data below to generate an AI-assisted hiring recommendation.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ── Input form ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-heading">Candidate Profile</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")

with col1:
    years_experience = st.number_input(
        "Years of Experience",
        min_value=0, max_value=50, value=5,
        help="Total years of relevant professional experience"
    )
    interview_score = st.number_input(
        "Interview Score (0 – 10)",
        min_value=0, max_value=10, value=8,
        help="Score assigned by the interview panel"
    )

with col2:
    technical_score = st.number_input(
        "Technical Test Score (0 – 100)",
        min_value=0, max_value=100, value=85,
        help="Result from standardized technical assessment"
    )
    certifications = st.number_input(
        "Certifications Count",
        min_value=0, max_value=20, value=2,
        help="Number of relevant professional certifications"
    )

st.markdown("<hr>", unsafe_allow_html=True)

# ── Predict ──────────────────────────────────────────────────────────────────
if st.button("Generate Hiring Decision", type="primary", use_container_width=True):

    input_data = np.array([[years_experience, technical_score, interview_score, certifications]])
    prediction = model.predict(input_data)

    st.markdown("<br>", unsafe_allow_html=True)

    if prediction[0] == 1:
        st.markdown("""
        <div class="result-panel shortlist">
            <div class="result-verdict shortlist">✦ Recommended for Shortlist</div>
            <div class="result-sub shortlist">
                This candidate meets or exceeds the required performance thresholds.
                Proceed to the next stage of the hiring process.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown("""
        <div class="result-panel reject">
            <div class="result-verdict reject">✕ Not Recommended</div>
            <div class="result-sub reject">
                This candidate does not currently meet the minimum qualification criteria.
                Consider re-evaluation or alternative roles.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Powered by a Random Forest classifier &nbsp;·&nbsp; For internal HR use only
</div>
""", unsafe_allow_html=True)