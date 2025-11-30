# 🏥 AI-Powered Healthcare Insurance Cost Advisor

![Streamlit App](https://img.shields.io/badge/Streamlit-Frontend-red?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge)
![Railway](https://img.shields.io/badge/Hosted%20on-Railway-blue?style=for-the-badge)
![Machine Learning](https://img.shields.io/badge/ML-Regression%20%7C%20XGBoost-orange?style=for-the-badge)

A complete **end-to-end intelligent insurance premium prediction system** that not only estimates healthcare insurance cost using Machine Learning, but also provides **personalized guidance** using an **LLM-powered advisory chatbot**.

This project combines:

- A trained ML model that predicts **yearly and monthly insurance premium**
- A **FastAPI backend** serving predictions and chatbot responses
- A modern **Streamlit UI**
- A **conversational assistant** powered by LLM (Groq + LangChain)
- Full deployment on a cloud infrastructure

---

### 🔗 Live Application  
🚀 **Launch the App:**  
https://ml-healthcare-insourance-cost-prediction-qbmwupheyvejgcf6mpmv8.streamlit.app/

---

## 🧠 What This App Does

Users provide details such as:

- Age  
- Lifestyle and BMI category  
- Medical history  
- Smoking status  
- Region  
- Income level  
- Insurance plan selection  

The system then:

1. Predicts the **estimated annual and monthly insurance premium**
2. Generates a **human-like explanation** of why the cost is what it is
3. Allows follow-up questions through a **chatbot** that remembers context and behaves like a personalized financial assistant

---

## 📦 Features

✔ Health Insurance Premium Prediction  
✔ AI-Generated Personalized Guidance  
✔ FastAPI-Powered ML Inference Endpoint  
✔ Conversation-Capable Assistant with Context Memory  
✔ Streamlit Frontend with Modern UX  
✔ Deployed on Cloud (FastAPI on Railway + Streamlit Cloud)

---

## 📊 Dataset & Model

- **Dataset size:** ~50K records  
- **Important features:** Age, BMI, Risk Factors, Smoking, Plan Tier, Region, Income  
- **Model Type:** Regression  
- **Algorithm:** **XGBoost Regressor**  
- **Optimization:** Hyperparameter tuning with RandomizedSearchCV  

### Output includes:

| Output Field | Meaning |
|-------------|----------|
| `yearly` | Estimated annual premium |
| `monthly` | Monthly cost breakdown |
| `advice` | AI-generated explanation & guidance |

---
### Components:

| Layer | Technology |
|-------|-----------|
| Machine Learning Model | XGBoost |
| API Backend | FastAPI |
| Frontend | Streamlit Cloud |
| Hosting | Railway (API) + Streamlit Cloud |
| LLM Assistant | LangChain+Groq |
| Persistence | Optional Thread Memory |

---


## 🧰 Tech Stack

| Category | Tools |
|---------|-------|
| Language | Python |
| ML | Scikit-learn, XGBoost, Pandas, NumPy |
| Backend | FastAPI |
| Frontend | Streamlit |
| LLM | LangChain, Groq |
| Deployment | Railway + Streamlit Cloud |
| Others | Requests, Pydantic, Docker (optional) |

---


## ⚙️ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/predict` | Returns yearly, monthly cost + AI summary |
| `POST` | `/chat` | Conversational follow-up with context |
| `GET` | `/plans` | Returns available insurance plan info |
| `GET` | `/home` | Status check |

---

