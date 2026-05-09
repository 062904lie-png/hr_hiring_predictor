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
    --fail-bg: #3a0d14;
    --fail-border: #e74c3c;
}

/* Global Background */
.stApp {
    background-color: var(--navy);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

/* Headers */
h1, h2, h3 {
    font-family: 'DM Serif Display', serif !important;
    color: var(--gold-lt) !important;
}

/* Form Elements Styling */
.stNumberInput > div > div > input, .stSelectbox > div > div > div {
    background-color: var(--navy-mid) !important;
    color: var(--text) !important;
    border: 1px solid var(--slate) !important;
}

/* Primary Button */
div.stButton > button:first-child {
    background-color: var(--gold);
    color: var(--navy);
    border: none;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 1.1rem;
    padding: 0.75rem;
    border-radius: 6px;
    transition: all 0.3s ease;
}
div.stButton > button:first-child:hover {
    background-color: var(--gold-lt);
    box-shadow: 0 4px 12px rgba(201,168,76,0.3);
}

/* Result Panels */
.result-panel {
    padding: 24px;
    border-radius: 8px;
    text-align: center;
    margin-top: 20px;
    border-left: 6px solid;
}
.result-panel.shortlist {
    background-color: var(--success-bg);
    border-color: var(--success-border);
}
.result-panel.reject {
    background-color: var(--fail-bg);
    border-color: var(--fail-border);
}

.result-verdict {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    margin-bottom: 8px;
}
.result-verdict.shortlist { color: var(--success-border); }
.result-verdict.reject { color: var(--fail-border); }

.result-sub {
    font-size: 1.05rem;
    color: var(--text);
}

/* Footer */
.footer {
    text-align: center;
    color: var(--muted);
    font-size: 0.85rem;
    margin-top: 50px;
    padding-top: 20px;
    border-top: 1px solid var(--slate);
}
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown("<h1>🎯 TalentIQ Decision Engine</h1>", unsafe_allow_html=True)
st.write("Advanced applicant screening system utilizing the 10-factor candidate framework.")
st.markdown("<br>", unsafe_allow_html=True)

# ── Load Model ──────────────────────────────────────────────────────────────
model_path = "recruitment_model.pkl"

if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    st.error(f"Error: '{model_path}' not found. Please ensure the new model is in the same folder.")
    st.stop()

# ── Data Input ──────────────────────────────────────────────────────────────
st.markdown("### Candidate Demographics")
col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("Age", min_value=18, max_value=70, value=28)
with col2:
    gender = st.selectbox("Gender", options=[0, 1], format_func=lambda x: "1 (Male)" if x == 1 else "0 (Female)")
with col3:
    education = st.selectbox("Education Level", options=[1, 2, 3, 4], help="1: High School, 2: Bachelor's, 3: Master's, 4: PhD")

st.markdown("### Professional Background")
col4, col5, col6 = st.columns(3)
with col4:
    experience = st.number_input("Experience (Years)", min_value=0, max_value=40, value=5)
with col5:
    companies = st.number_input("Previous Companies", min_value=0, max_value=20, value=2)
with col6:
    distance = st.number_input("Distance from Company", min_value=0.0, max_value=200.0, value=15.5, step=1.0)

st.markdown("### Evaluation Scores")
col7, col8, col9 = st.columns(3)
with col7:
    interview_score = st.slider("Interview Score", min_value=0, max_value=100, value=75)
with col8:
    skill_score = st.slider("Skill Score", min_value=0, max_value=100, value=80)
with col9:
    personality_score = st.slider("Personality Score", min_value=0, max_value=100, value=85)

st.markdown("### Recruitment Strategy")
strategy = st.selectbox("Strategy Method", options=[1, 2, 3], help="Categorical variable representing the recruitment channel.")

# ── Predict ──────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
if st.button("Generate Hiring Decision", type="primary", use_container_width=True):

    # Create input array matching the exact feature order of our advanced dataset:
    # Age, Gender, EducationLevel, ExperienceYears, PreviousCompanies, 
    # DistanceFromCompany, InterviewScore, SkillScore, PersonalityScore, RecruitmentStrategy
    input_data = np.array([[
        age, gender, education, experience, companies, 
        distance, interview_score, skill_score, personality_score, strategy
    ]])
    
    prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.markdown("""
        <div class="result-panel shortlist">
            <div class="result-verdict shortlist">✦ Recommended for Shortlist</div>
            <div class="result-sub shortlist">
                This candidate meets or exceeds the comprehensive performance thresholds.
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
                This candidate does not currently meet the minimum qualification criteria across all 10 factors.
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
