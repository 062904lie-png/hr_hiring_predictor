import streamlit as st
import joblib
import numpy as np
import os

# --- Visual Studio Tip ---
# To run this in VS Code:
# 1. Open the Terminal (Ctrl + `)
# 2. Type: streamlit run app.py
# -------------------------

# Page configuration - changed to "wide" for a dashboard feel
st.set_page_config(page_title="HR Decision AI", page_icon="💼", layout="wide")

# Custom CSS for a modern enterprise dashboard look
st.markdown("""
    <style>
    /* Subtle background color for the main area */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Styling the metric cards */
    [data-testid="stMetric"] {
        background-color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border-left: 5px solid #3498db;
    }
    
    /* Custom classes for the final decision cards */
    .decision-card-pass {
        background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
        padding: 35px;
        border-radius: 15px;
        text-align: center;
        color: #1a5619;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        border: 2px solid #b8e994;
    }
    
    .decision-card-fail {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%);
        padding: 35px;
        border-radius: 15px;
        text-align: center;
        color: #5c1010;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        border: 2px solid #ffb8b8;
    }
    </style>
    """, unsafe_allow_html=True)

# Load the trained Random Forest model efficiently
model_path = "hr.pkl"

@st.cache_resource
def load_model():
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None

model = load_model()

if not model:
    st.error(f"Error: '{model_path}' not found. Please ensure the model file is in the same folder as this script.")
    st.stop()

# ==========================================
# SIDEBAR: Data Entry
# ==========================================
with st.sidebar:
    st.title("⚙️ Candidate Entry")
    st.write("Adjust the sliders below to evaluate a new candidate.")
    st.divider()
    
    years_experience = st.slider("Years of Experience", min_value=0, max_value=50, value=5)
    technical_score = st.slider("Technical Test Score (0-100)", min_value=0, max_value=100, value=85)
    interview_score = st.slider("Interview Score (0-10)", min_value=0, max_value=10, value=8)
    certifications = st.number_input("Certifications Count", min_value=0, max_value=20, value=2)
    
    st.divider()
    analyze_btn = st.button("Analyze Candidate", type="primary", use_container_width=True)

# ==========================================
# MAIN PAGE: Dashboard & Results
# ==========================================
st.title("💼 HR Hiring Decision Dashboard")
st.markdown("Review the candidate's profile metrics and the AI-generated hiring recommendation.")
st.write("")

# Candidate Profile Metrics
st.write("#### Candidate Profile")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Experience", f"{years_experience} Years")
col2.metric("Technical Score", f"{technical_score} / 100")
col3.metric("Interview Score", f"{interview_score} / 10")
col4.metric("Certifications", f"{certifications} Total")

st.divider()

# Results Section
if analyze_btn:
    st.write("#### AI Recommendation")
    
    with st.spinner("Processing candidate data through the AI model..."):
        # Create input array matching the exact feature order
        input_data = np.array([[years_experience, technical_score, interview_score, certifications]])
        
        # Make the prediction
        prediction = model.predict(input_data)
        
        # Display customized decision cards
        if prediction[0] == 1:
            st.markdown("""
                <div class="decision-card-pass">
                    <h1 style="margin:0; font-size: 3em;">✅ SHORTLIST</h1>
                    <p style="font-size: 1.3em; margin-top: 10px;"><b>Outstanding Profile.</b> This candidate exceeds performance thresholds and is highly recommended for the next round.</p>
                </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            st.markdown("""
                <div class="decision-card-fail">
                    <h1 style="margin:0; font-size: 3em;">❌ REJECT</h1>
                    <p style="font-size: 1.3em; margin-top: 10px;"><b>Requirements Not Met.</b> This candidate currently falls below the required technical or interview thresholds.</p>
                </div>
            """, unsafe_allow_html=True)
else:
    # Default state before clicking the button
    st.info("👈 Please adjust the candidate details in the sidebar menu and click **'Analyze Candidate'** to generate a recommendation.")
