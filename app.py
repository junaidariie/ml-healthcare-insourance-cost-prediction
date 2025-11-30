from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated, Literal
from prediction_helper import predict
from one_shot_bot import generate_advice
from chatbot_advisor import ask_chatbot

class ModelInput(BaseModel):
    gender: Annotated[Literal["male", "female"], Field(description="Enter your gender")]
    marital_status: Annotated[Literal["married", "unmarried"], Field(description="Enter your marital status")]
    age: Annotated[int, Field(gt=0, lt=110, description="Enter your age")]
    number_of_dependants: Annotated[int, Field(gt=0, lt=8)]
    income_lakhs: Annotated[float, Field(gt=0,description="Enter your annual income in lakhs")]
    genetical_risk: Annotated[int, Field(gt=0, lt=6)]
    insurance_plan: Annotated[Literal['Bronze', 'Silver', 'Gold'], Field(description="Choose one of the given plans")]
    employment_status: Annotated[Literal['Salaried', 'Self-Employed', 'Freelancer'], Field()]
    bmi_category: Annotated[Literal['Normal', 'Obesity', 'Overweight', 'Underweight'], Field()]
    smoking_status: Annotated[Literal['No Smoking', 'Regular', 'Occasional'], Field()]
    region: Annotated[Literal['Northwest', 'Southeast', 'Northeast', 'Southwest'], Field()]
    medical_history: Annotated[
        Literal[
            'No Disease', 'Diabetes', 'High blood pressure', 'Diabetes & High blood pressure',
            'Thyroid', 'Heart disease', 'High blood pressure & Heart disease',
            'Diabetes & Thyroid', 'Diabetes & Heart disease'
        ],
        Field()
    ]

class ModelOutput(BaseModel):
    yearly : float
    monthly : float
    advice : str

class ChatMessage(BaseModel):
    thread_id : str
    message : str
    yearly_cost : float
    monthly_cost : float
    ai_summary : str

app = FastAPI()

@app.get("/plans")
def plans():
    return {
        "Bronze": "Basic coverage, low premium.",
        "Silver": "Balance of premium and coverage.",
        "Gold": "Premium cost with highest benefits."
    }


@app.get("/home")
def home():
    return {"message": "Welcome! The API is live"}

@app.post("/predict", response_model=ModelOutput)
def predict_output(input_data: ModelInput):
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

        return ModelOutput(yearly=yearly_prediction, monthly=monthly, advice=advice)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction Failed: {str(e)}")


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
        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
