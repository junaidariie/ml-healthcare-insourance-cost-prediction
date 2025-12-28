from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
import os
from one_shot_bot import generate_advice
from prediction_helper import predict
from chatbot_advisor import ask_chatbot
from utility import STT, TTS

app = FastAPI()

# ---------------- CORS ---------------- #
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- MODELS ---------------- #

class HealthInput(BaseModel):
    gender: str
    marital_status: str
    age: int
    number_of_dependants: int
    income_lakhs: float
    genetical_risk: int
    insurance_plan: str
    employment_status: str
    bmi_category: str
    smoking_status: str
    region: str
    medical_history: str


class HealthOutput(BaseModel):
    yearly: float
    monthly: float
    advice: str


class ChatMessage(BaseModel):
    thread_id: str
    message: str
    yearly_cost: float
    monthly_cost: float
    ai_summary: str


class TTSRequest(BaseModel):
    text: str


# ---------------- BASIC ROUTE ---------------- #

@app.get("/")
def home():
    return {"message": "Healthcare AI API is running."}


# ---------------- PREDICTION ---------------- #

@app.post("/predict", response_model=HealthOutput)
def predict_output(input_data: HealthInput):
    try:
        data = input_data.model_dump()

        converted_data = {
            "Gender": data["gender"].title(),
            "Marital Status": data["marital_status"].title(),
            "Age": data["age"],
            "Number of Dependants": data["number_of_dependants"],
            "Income in Lakhs": data["income_lakhs"],
            "Genetical Risk": data["genetical_risk"],
            "Insurance Plan": data["insurance_plan"].title(),
            "Employment Status": data["employment_status"],
            "BMI Category": data["bmi_category"],
            "Smoking Status": data["smoking_status"],
            "Region": data["region"],
            "Medical History": data["medical_history"]
        }

        yearly_prediction = float(predict(converted_data))
        monthly = round(yearly_prediction / 12, 2)

        advice = generate_advice(
            yearly_premium=yearly_prediction,
            monthly_premium=monthly,
            age=input_data.age,
            gender=input_data.gender,
            marital_status=input_data.marital_status,
            dependents=input_data.number_of_dependants,
            bmi_category=input_data.bmi_category,
            smoking_status=input_data.smoking_status,
            medical_history=input_data.medical_history,
            genetic_risk=input_data.genetical_risk,
            region=input_data.region,
            income_lakhs=input_data.income_lakhs,
            employment_status=input_data.employment_status,
            insurance_plan=input_data.insurance_plan
        )

        return HealthOutput(yearly=yearly_prediction, monthly=monthly, advice=advice)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction Failed: {str(e)}")

# ---------------- CHAT STREAM ---------------- #

@app.post('/chat')
def chat(input_data : ChatMessage):
    try:
        yearly_cost = input_data.yearly_cost
        monthly_cost = input_data.monthly_cost
        ai_summary = input_data.ai_summary

        response = ask_chatbot(
            yearly_cost=yearly_cost,
            monthly_cost=monthly_cost,
            ai_summary=ai_summary,
            user_message=input_data.message,
            thread_id=input_data.thread_id
        )
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- TTS ---------------- #

@app.post("/tts")
async def generate_tts(request: TTSRequest):
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text is empty")

        audio_path = await TTS(text=request.text)

        if not os.path.exists(audio_path):
            raise HTTPException(status_code=500, detail="Audio file not created")

        return FileResponse(
            path=audio_path,
            media_type="audio/mpeg",
            filename="speech.mp3"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- STT ---------------- #

@app.post("/stt")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        return await STT(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
