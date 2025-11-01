import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load local .env (ignored on Hugging Face Spaces where secrets are env vars)
load_dotenv()

SERVICE_URL = "https://concrete-api-301401238543.europe-west1.run.app/predict"
API_KEY = os.getenv("API_KEY")

# Page Setup 
st.set_page_config(
    page_title="Concrete Strength Comparator",
    page_icon="🧱", 
    layout="wide"
)

# Title and Description 
st.title("Concrete Mix Strength Comparator")
st.caption(
    """
    This web app predicts and compares the **compressive strength of concrete** based on its mix composition.  
    It is part of a 3-repository project that includes:  
    - 🧠 [Model Training](https://github.com/ApostolosApostolou/concrete-strength-prediction-model-training) — development and optimization of a Random Forest regression model  
    - ⚙️ [API Service](https://github.com/ApostolosApostolou/concrete-strength-prediction-api) — FastAPI deployment on Google Cloud Run providing secure access to predictions  
    
    The model was trained on the [Concrete Compressive Strength Dataset](https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength) from the UCI Machine Learning Repository.  
    This app allows users to test up to **three concrete mixes simultaneously** and view their predicted strengths in real time.
    """
)

if not API_KEY:
    st.warning("⚠️ API key not found. Set `API_KEY` in your .env (local) or in Secrets (Hugging Face).")
    st.stop()

# Session State for Persistent Results 
for i in range(1, 4):
    st.session_state.setdefault(f"strength_{i}", None)

# Prediction Function 
def get_prediction(params):
    headers = {"x-api-key": API_KEY}
    r = requests.get(SERVICE_URL, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    return round(r.json().get("predicted_strength", 0), 2)

# UI Layout for 3 Mixes 
for i in range(1, 4):
    st.markdown("---")
    st.subheader(f"Mix {i}")

    left_col, right_col = st.columns([3, 1], vertical_alignment="top")

    with left_col:
        st.markdown("**Input Parameters**")
        c1, c2, c3, c4 = st.columns(4)
        cement = c1.number_input("Cement (kg/m³)", min_value=0.0, value=213.7, key=f"cement_{i}")
        slag = c2.number_input("Blast Furnace Slag (kg/m³)", min_value=0.0, value=98.1, key=f"slag_{i}")
        fly_ash = c3.number_input("Fly Ash (kg/m³)", min_value=0.0, value=24.5, key=f"flyash_{i}")
        water = c4.number_input("Water (kg/m³)", min_value=0.0, value=181.7, key=f"water_{i}")

        c5, c6, c7, c8 = st.columns(4)
        superplasticizer = c5.number_input("Superplasticizer (kg/m³)", min_value=0.0, value=6.9, key=f"superplasticizer_{i}")
        coarse = c6.number_input("Coarse Aggregate (kg/m³)", min_value=0.0, value=1065.8, key=f"coarse_{i}")
        fine = c7.number_input("Fine Aggregate (kg/m³)", min_value=0.0, value=785.4, key=f"fine_{i}")
        age = c8.number_input("Age (days)", min_value=1, value=3, key=f"age_{i}")

        if st.button(f"Predict Strength for Mix {i}", key=f"predict_{i}"):
            with st.spinner("Predicting..."):
                try:
                    params = dict(
                        cement=cement,
                        blast_furnace_slag=slag,
                        fly_ash=fly_ash,
                        water=water,
                        superplasticizer=superplasticizer,
                        coarse_aggregate=coarse,
                        fine_aggregate=fine,
                        age=age,
                    )
                    st.session_state[f"strength_{i}"] = get_prediction(params)
                except requests.HTTPError as e:
                    st.error(f"Request failed: {e.response.status_code} – {e.response.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

    with right_col:
        st.markdown("**Predicted Strength (MPa)**")
        val = st.session_state[f"strength_{i}"]
        label = f"Mix {i} prediction"

        if val is None:
            st.metric(label=label, value="—", label_visibility="collapsed")
        else:
            st.metric(label=label, value=f"{val:.2f} MPa", label_visibility="collapsed")
