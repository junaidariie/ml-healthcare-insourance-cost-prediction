
import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="Health Insurance Cost Predictor",
    page_icon="🏥",
    layout="centered"
)

# Custom CSS for clean, compact styling
st.markdown("""
    <style>
    .main {
        max-width: 800px;
        padding: 1rem;
        margin: 0 auto;
    }
    .block-container {
        max-width: 800px;
        padding-left: 2rem;
        padding-right: 2rem;
        margin: 0 auto;
    }
    h1 {
        color: #2c3e50;
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        margin-bottom: 0.3rem !important;
    }
    .subtitle {
        color: #7f8c8d;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }
    .section-divider {
        border-top: 1px solid #e0e0e0;
        margin: 1.5rem 0 1rem 0;
    }
    .section-title {
        color: #34495e;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }
    .stButton>button {
        width: 100%;
        background: #27ae60;
        color: white;
        font-weight: 600;
        padding: 0.6rem;
        border: none;
        border-radius: 6px;
        margin-top: 1rem;
    }
    .stButton>button:hover {
        background: #229954;
    }
    .result-card {
        background: #e8f8f5;
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 1rem;
        border-left: 4px solid #27ae60;
        text-align: center;
    }
    .result-label {
        color: #7f8c8d;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    .result-value {
        color: #27ae60;
        font-size: 2rem;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🏥 Health Insurance Cost Predictor")
st.markdown('<p class="subtitle">Get instant premium estimates based on your profile</p>', unsafe_allow_html=True)

# Categorical options
categorical_options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Unmarried', 'Married'],
    'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'Smoking Status': ['No Smoking', 'Regular', 'Occasional'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer', ''],
    'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'Medical History': [
        'No Disease', 'Diabetes', 'High blood pressure', 'Diabetes & High blood pressure',
        'Thyroid', 'Heart disease', 'High blood pressure & Heart disease', 'Diabetes & Thyroid',
        'Diabetes & Heart disease'
    ],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold']
}

# Personal Information
st.markdown('<div class="section-title">Personal Information</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    age = st.number_input('Age', min_value=18, max_value=100, value=30, step=1)
    gender = st.selectbox('Gender', categorical_options['Gender'])
    marital_status = st.selectbox('Marital Status', categorical_options['Marital Status'])

with col2:
    number_of_dependants = st.number_input('Number of Dependants', min_value=0, max_value=20, value=2, step=1)
    bmi_category = st.selectbox('BMI Category', categorical_options['BMI Category'])
    region = st.selectbox('Region', categorical_options['Region'])

# Financial & Employment
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Financial & Employment Details</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    income_lakhs = st.number_input('Annual Income (Lakhs)', min_value=1, max_value=200, value=10, step=1)

with col4:
    employment_status = st.selectbox('Employment Status', categorical_options['Employment Status'])

# Health Information
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Health Information</div>', unsafe_allow_html=True)

col5, col6 = st.columns(2)
with col5:
    smoking_status = st.selectbox('Smoking Status', categorical_options['Smoking Status'])
    genetical_risk = st.number_input('Genetical Risk (1-5)', min_value=1, max_value=5, value=3, step=1)

with col6:
    medical_history = st.selectbox('Medical History', categorical_options['Medical History'])
    insurance_plan = st.selectbox('Insurance Plan', categorical_options['Insurance Plan'])

# Prepare input dictionary
input_dict = {
    'age': age,
    'number_of_dependants': number_of_dependants,
    'income_lakhs': income_lakhs,
    'genetical_risk': genetical_risk,
    'insurance_plan': insurance_plan,
    'employment_status': employment_status,
    'gender': gender.lower(),
    'marital_status': marital_status.lower(),
    'bmi_category': bmi_category,
    'smoking_status': smoking_status,
    'region': region,
    'medical_history': medical_history
}

# Predict Button
if st.button('💰 Calculate Insurance Cost'):
    API_URL = st.secrets["API_URL"]
    
    with st.spinner('Calculating premium...'):
        try:
            response = requests.post(API_URL, json=input_dict)
            
            if response.status_code == 200:
                prediction = response.json()['prediction']
                
                st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Predicted Premium</div>', unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-label">Estimated Annual Premium</div>
                    <div class="result-value">₹ {prediction:,.2f}</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.success("✅ Calculation completed successfully")
                
            else:
                st.error(f"❌ API Error: {response.status_code}")
                
        except Exception as e:
            st.error(f"❌ Connection error: {str(e)}")

