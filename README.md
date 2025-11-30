***

# 🏥 AI-Powered Healthcare Insurance Cost Advisor

🏥 AI-Powered Healthcare Insurance Cost Advisor
<p align="center"> <img src="https://img.shields.io/badge/Streamlit-Frontend-blue?style=for-the-badge" /> <img src="https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge" /> <img src="https://img.shields.io/badge/Railway-Hosting-purple?style=for-the-badge" /> <img src="https://img.shields.io/badge/XGBoost-ML%20Model-orange?style=for-the-badge" /> <img src="https://img.shields.io/badge/LangChain-AI%20Chatbot-yellow?style=for-the-badge" /> </p>

A complete end-to-end healthcare insurance intelligence system that predicts insurance premiums based on user lifestyle, demographics, medical background, and risk factors. The platform also includes an AI-powered advisory chatbot that explains the prediction in natural language and answers follow-up questions.
This project combines:

- A trained ML model that predicts **yearly and monthly insurance premium**
- A **FastAPI backend** serving predictions and chatbot responses
- A modern **Streamlit UI**
- A **conversational assistant** powered by LLM (Groq + LangChain)
- Full deployment on a cloud infrastructure

***

### 🔗 Live Application  
🚀 **Launch the App:**  
[https://ml-healthcare-insourance-cost-prediction-qbmwupheyvejgcf6mpmv8.streamlit.app/](https://ml-healthcare-insourance-cost-prediction-qbmwupheyvejgcf6mpmv8.streamlit.app/)

***

## 🧠 Project Overview

This project is designed to provide accurate healthcare insurance cost predictions using advanced machine learning models. It includes

- EDA and insightful data visualization
- Segmented model training for different age groups
- XGBoost and regression-based models with hyperparameter tuning
- Seamless deployment using FastAPI, Docker, and Streamlit Cloud

***

## 📊 Dataset

- **Dataset size:** 50,000 rows
- **Features:** age, sex, BMI, children, smoker, region, charges
- **Important features:** Age, BMI, Risk Factors, Smoking, Plan Tier, Region, Income  

***

## ⚙️ Model Strategy

### 🔹 Age-Based Segmentation

To improve prediction accuracy:[12]

- **Group 1:** Age ≤ 25
    - Algorithms tested: `Linear Regression`, `Ridge Regression`, `XGBoost`
    - **Final Model:** `XGBoost Regressor` with hyperparameter tuning via `RandomizedSearchCV`
    - **Accuracy:** **98%**
- **Group 2:** Age > 25
    - Algorithms tested: `Linear Regression`, `Ridge Regression`, `XGBoost`
    - **Final Model:** `XGBoost Regressor` with `RandomizedSearchCV`
    - **Accuracy:** **99%**

***

## 📈 Model Performance

| Group | Model | Accuracy |
| --- | --- | --- |
| Age ≤ 25 | XGBoost Regressor | 98% |
| Age > 25 | XGBoost Regressor | 99% |

- Hyperparameter tuning done via `RandomizedSearchCV`
- Metrics used: `R² Score`, `MAE`, `RMSE`

***

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

***

## 📦 Features

✔ Health Insurance Premium Prediction  
✔ FastAPI-Powered ML Inference Endpoint  
✔ Streamlit Frontend with Modern UX  
✔ AI-Generated Personalized Guidance  
✔ Conversation-Capable Assistant with Context Memory  
✔ Deployed on Cloud (FastAPI on Railway + Streamlit Cloud)

***

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

***

## 📊 Dataset & Model Output

### Output includes:

| Output Field | Meaning |
|-------------|----------|
| `yearly` | Estimated annual premium |
| `monthly` | Monthly cost breakdown |
| `advice` | AI-generated explanation & guidance |

***

## 🏗️ System Architecture

### Components:

| Layer | Technology |
|-------|-----------|
| Machine Learning Model | XGBoost |
| API Backend | FastAPI |
| Frontend | Streamlit Cloud |
| Hosting | Railway (API) + Streamlit Cloud |
| LLM Assistant | LangChain+Groq |
| Persistence | Optional Thread Memory |

***

## ⚙️ API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/predict` | Returns yearly, monthly cost + AI summary |
| `POST` | `/chat` | Conversational follow-up with context |
| `GET` | `/plans` | Returns available insurance plan info |
| `GET` | `/home` | Status check |

***

depth/)



