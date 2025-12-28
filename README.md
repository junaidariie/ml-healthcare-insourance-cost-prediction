---

# 🏥 AI-Powered Healthcare Insurance Cost Advisor

<p align="center">
  <img src="https://img.shields.io/badge/Frontend-HTML%20%7C%20CSS%20%7C%20JS-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Backend-FastAPI-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/ML-XGBoost-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/LLM-LangChain%20%2B%20Groq-yellow?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Search-Tavily-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Deployment-Railway%20%7C%20GitHub%20Pages-brightgreen?style=for-the-badge" />
</p>

---

## 🧠 Overview

The **AI-Powered Healthcare Insurance Cost Advisor** is an end-to-end intelligent system that predicts **health insurance premiums** and provides **human-like explanations** using AI.

It combines:

* Predictive machine learning
* Conversational AI
* Speech-to-Text and Text-to-Speech
* Real-time external knowledge retrieval
* A modern web-based frontend

This project closely simulates how **real-world insurtech platforms** operate.

---

## 🚀 Live Application

🌐 **Frontend (Web App)**
https://junaidariie.github.io/cred-risk-model/

⚙️ **Backend (API)**
Hosted using FastAPI on HuggingFace

---

## 🧩 What This System Does

Users provide information such as:

* Age
* Lifestyle habits
* BMI category
* Medical background
* Income range
* Insurance preferences

The system then:

1. Predicts **annual and monthly insurance premiums**
2. Explains the reasoning in **simple, human-friendly language**
3. Allows **follow-up conversations** with memory
4. Supports **voice input (STT)** and **voice responses (TTS)**
5. Uses **live web search** when needed for better context

---

## 🧠 Key Features

✔ AI-powered insurance premium prediction
✔ Natural language explanations (no technical jargon)
✔ Conversational chatbot with memory
✔ Speech-to-Text (STT) for voice input
✔ Text-to-Speech (TTS) for voice responses
✔ Real-time knowledge retrieval using Tavily Search
✔ Clean and responsive frontend (HTML, CSS, JavaScript)
✔ Scalable backend with FastAPI
✔ Cloud deployed and production-ready

---

## 🧪 Dataset Overview

* **Dataset Size:** 50,000 records
* **Key Features:**

  * Age
  * BMI
  * Smoking status
  * Region
  * Income
  * Medical & lifestyle indicators

---

## ⚙️ Model Strategy

### 🔹 Age-Based Segmentation

To improve accuracy, separate models were trained for different age groups:

#### Group 1: Age ≤ 25

* Algorithms tested:

  * Linear Regression
  * Ridge Regression
  * XGBoost
* Final model: **XGBoost Regressor**
* Accuracy: **~98%**

#### Group 2: Age > 25

* Algorithms tested:

  * Linear Regression
  * Ridge Regression
  * XGBoost
* Final model: **XGBoost Regressor**
* Accuracy: **~99%**

✔ Hyperparameter tuning using `RandomizedSearchCV`
✔ Metrics used: `R² Score`, `MAE`, `RMSE`

---

## 📊 Output Format

| Field     | Description                           |
| --------- | ------------------------------------- |
| `yearly`  | Estimated annual insurance premium    |
| `monthly` | Monthly premium breakdown             |
| `advice`  | AI-generated explanation and guidance |

---

## 🧠 Conversational AI Capabilities

The assistant can:

* Explain why a premium is high or low
* Answer follow-up questions contextually
* Suggest plan comparisons
* Help users understand trade-offs
* Respond using voice (TTS)
* Accept spoken input (STT)

It behaves like a **real insurance advisor**, not a chatbot.

---

## 🔍 Intelligent Search (Tavily)

When internal knowledge is insufficient, the system:

* Uses Tavily Search to retrieve reliable, real-time information
* Summarizes results in a user-friendly manner
* Avoids overwhelming or technical explanations

---

## 🧱 System Architecture

| Layer             | Technology                             |
| ----------------- | -------------------------------------- |
| Frontend          | HTML, CSS, JavaScript                  |
| Backend API       | FastAPI                                |
| ML Model          | XGBoost                                |
| Conversational AI | LangChain + Groq                       |
| Search Tool       | Tavily                                 |
| Speech            | STT + TTS                              |
| Deployment        | Railway (API), GitHub Pages (Frontend) |

---

## 🔌 API Endpoints

| Method | Endpoint   | Description                              |
| ------ | ---------- | ---------------------------------------- |
| `POST` | `/predict` | Returns premium prediction + explanation |
| `POST` | `/chat`    | Conversational AI with memory            |
| `GET`  | `/plans`   | Available insurance plans                |
| `GET`  | `/health`  | API health check                         |

---

## 🎯 Why This Project Matters

This project demonstrates:

* Real-world AI system design
* End-to-end ML deployment
* Human-centered AI communication
* Integration of LLMs with structured ML outputs
* Practical use of speech and search tools

It closely mirrors how **modern health-fintech platforms** operate.

---

## 👤 Author

**Junaid**
Data Science & Machine Learning Practitioner
Focused on building explainable, production-ready AI systems for real-world use cases.

---


