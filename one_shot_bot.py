from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"), streaming=True)

prompt = PromptTemplate.from_template("""
You are a friendly but professional insurance assistant.

Write a short, conversational explanation of the premium. 
Keep it human, warm, and simple — avoid sounding like a report or policy document.

Response Format:
1) One-line casual greeting.
2) State the premium clearly.
3) A short, natural explanation (2–4 sentences max) of why the cost is what it is, based on the user's data. Mention only the most meaningful factors, not a full list.
4) Give 1–2 helpful suggestions (upgrade recommendation, lifestyle tip, or policy fit).
5) End with a short invitation to continue with the chatbot, like know more about healthcare insourence planes and their cost

Tone rules:
- No long paragraphs.
- No medical diagnosis or guarantees.
- Avoid corporate insurance jargon.
- Keep under 10 total sentences.

User + Model Data:
yearly_premium: ₹{yearly_premium}
monthly_premium : ₹{monthly_premium} 
Age: {age}, Gender: {gender}, Marital Status: {marital_status}, Dependents: {dependents}
BMI: {bmi_category}, Smoking: {smoking_status}, Medical History: {medical_history}, Genetics: Risk {genetic_risk}
Region: {region}, Income: {income_lakhs} lakhs, Employment: {employment_status}, Plan: {insurance_plan}

Now generate the response.


""")

def generate_advice(yearly_premium, monthly_premium, age, gender, marital_status, dependents, bmi_category, smoking_status,
                    medical_history, genetic_risk, region, income_lakhs, employment_status, insurance_plan):
    formatted_prompt = prompt.format(
        yearly_premium=yearly_premium,
        monthly_premium=monthly_premium,
        age=age,
        gender=gender,
        marital_status=marital_status,
        dependents=dependents,
        bmi_category=bmi_category,
        smoking_status=smoking_status,
        medical_history=medical_history,
        genetic_risk=genetic_risk,
        region=region,
        income_lakhs=income_lakhs,
        employment_status=employment_status,
        insurance_plan=insurance_plan
        )

    result = llm.invoke(formatted_prompt)
    return result.content

"""print(generate_advice(
    predicted_premium=7621,
    age=30,
    gender="Male",
    marital_status="Unmarried",
    dependents=2,
    bmi_category="Normal",
    smoking_status="No Smoking",
    medical_history="No Disease",
    genetic_risk=3,
    region="Northwest",
    income_lakhs=10,
    employment_status="Salaried",
    insurance_plan="Bronze"))"""