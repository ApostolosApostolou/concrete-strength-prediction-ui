# Concrete Compressive Strength Prediction UI

This repository provides an interactive **Streamlit web application** that allows users to input concrete mix parameters and instantly compare the predicted **compressive strengths (in MPa)** of up to three different mixtures.  
It connects to the **FastAPI web service** hosted on Google Cloud Run, which serves predictions from the pre-trained **Random Forest regression model**.

---

## 🌐 Overview

This app serves as the **frontend interface** of the complete concrete strength prediction system.  
It provides an easy-to-use interface for testing and visualizing model predictions.

### Related Repositories
- 🧠 [Concrete Strength Prediction Model Training](https://github.com/ApostolosApostolou/concrete-strength-prediction-model-training) — model development and evaluation  
- ⚙️ [Concrete Strength Prediction API](https://github.com/ApostolosApostolou/concrete-strength-prediction-api) — FastAPI service for model predictions  

---

## 🎨 Features
- Compare up to **three concrete mixes** side-by-side  
- Real-time predictions via **secure API requests**  
- Persistent results for each mix  
- Clean and bright theme with blue accents  
- Secure API key management (via `.env` locally or Hugging Face Secrets)

