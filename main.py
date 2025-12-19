import streamlit as st
import requests
import uuid

# Page configuration
st.set_page_config(
    page_title="HealthGuard AI: Insurance Cost Predictor",
    page_icon="🏥",
    layout="wide"
)

# Initialize session storage
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "show_info" not in st.session_state:
    st.session_state.show_info = False

# ========================= ENHANCED UI STYLING =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
* {
    font-family: 'Montserrat', 'Inter', sans-serif;
}
.main {
    background: linear-gradient(135deg, #212d3b 0%, #223a57 100%);
    padding: 2rem 0;
}
.header-container {
    background: linear-gradient(135deg, #243b55 0%, #141e30 100%);
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(36, 59, 85,0.13);
    margin-bottom: 2rem;
    text-align: center;
}
.header-title {
    color: white;
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    text-shadow: 2px 2px 6px rgba(20,30,48,0.2);
    font-family: 'Montserrat', sans-serif;
}
.header-subtitle {
    color: #aab3cf;
    font-size: 1.1rem;
    margin-top: 0.5rem;
    font-family: 'Montserrat', sans-serif;
}
.section-card {
    background: #25304b;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(36, 59, 85,0.12);
    margin-bottom: 1.5rem;
    border-left: 4px solid #27ae60;
    color: #f3f4fa;
}
.section-title {
    color: #f1f7fc;
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'Montserrat', sans-serif;
}
.info-box {
    background: linear-gradient(135deg, #344667 0%, #27ae60 100%);
    color: #f1f7fc;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    border-left: 4px solid #18aad5;
    animation: slideIn 0.5s ease-out;
}
@keyframes slideIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}
.metric-card {
    background: linear-gradient(135deg, #27ae60 0%, #243b55 100%);
    padding: 1.2rem;
    border-radius: 12px;
    color: #f3f4fa;
    text-align: center;
    box-shadow: 0 4px 15px rgba(39, 174, 96, 0.2);
    transition: transform 0.3s ease;
}
.metric-card:hover {
    transform: translateY(-5px);
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    margin: 0.5rem 0;
    font-family: 'Montserrat', sans-serif;
}
.metric-label {
    font-size: 0.9rem;
    opacity: 0.92;
}
.result-card {
    background: linear-gradient(135deg, #27ae60 0%, #2d375b 100%);
    padding: 2rem;
    border-radius: 16px;
    color: #f4f8ff;
    box-shadow: 0 8px 32px rgba(39, 174, 96, 0.10);
    margin: 1.5rem 0;
}
.result-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-top: 1rem;
}
.result-item {
    background: rgba(25,40,65,0.2);
    padding: 1.5rem;
    border-radius: 12px;
    backdrop-filter: blur(10px);
}
.result-item-label {
    font-size: 0.9rem;
    opacity: 0.9;
    margin-bottom: 0.5rem;
}
.result-item-value {
    font-size: 1.8rem;
    font-weight: 700;
}
.advisor-box {
    background: linear-gradient(135deg, #27ae60 0%, #243b55 100%);
    color: #f5f5fa;
    padding: 1.5rem;
    border-radius: 12px;
    margin-top: 1.5rem;
    border-left: 4px solid #18aad5;
    box-shadow: 0 4px 15px rgba(39, 174, 96, 0.1);
}
.advisor-box h4 {
    color: #f1f7fc;
    margin-top: 0;
}
.chat-container {
    background: #24304e;
    color: #fff;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(36, 48, 78,0.12);
    max-height: 400px;
    overflow-y: auto;
    margin-bottom: 1rem;
}
.chat-bubble-user {
    background: linear-gradient(135deg, #27ae60 0%, #243b55 100%);
    color: white;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0 8px auto;
    max-width: 70%;
    text-align: right;
    box-shadow: 0 2px 8px rgba(39, 174, 96, 0.13);
    animation: slideInRight 0.3s ease-out;
    font-family: 'Montserrat', sans-serif;
}
.chat-bubble-bot {
    background: #20293b;
    border: 2px solid #2a3d6a;
    color: #ebf2f8;
    padding: 12px 18px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px auto 8px 0;
    max-width: 70%;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    animation: slideInLeft 0.3s ease-out;
    font-family: 'Montserrat', sans-serif;
}
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(20px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}
.stButton>button {
    width: 100%;
    background: linear-gradient(135deg, #27ae60 0%, #223a57 100%);
    color: white;
    font-weight: 600;
    border: none;
    border-radius: 10px;
    padding: 0.8rem;
    font-size: 1rem;
    font-family: 'Montserrat', sans-serif;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(39, 174, 96, 0.13);
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(39, 174, 96, 0.20);
}
.stNumberInput>div>div>input,
.stSelectbox>div>div>select,
.stTextInput>div>div>input {
    border-radius: 8px;
    border: 2px solid #233269;
    padding: 0.5rem;
    transition: border-color 0.3s ease;
    background: #2d375b;
    color: #e9ecfa;
    font-family: 'Montserrat', sans-serif;
}
.stNumberInput>div>div>input:focus,
.stSelectbox>div>div>select:focus,
.stTextInput>div>div>input:focus {
    border-color: #27ae60;
    box-shadow: 0 0 0 3px rgba(39, 174, 96, 0.1);
}
.alert-banner {
    background: linear-gradient(135deg, #233269 0%, #27ae60 100%);
    color: #fff;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
    border-left: 4px solid #18aad5;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.chat-container::-webkit-scrollbar {
    width: 8px;
}
.chat-container::-webkit-scrollbar-track {
    background: #1a2336;
    border-radius: 10px;
}
.chat-container::-webkit-scrollbar-thumb {
    background: #27ae60;
    border-radius: 10px;
}
.chat-container::-webkit-scrollbar-thumb:hover {
    background: #229954;
}
</style>
""", unsafe_allow_html=True)

# ========================= HEADER =========================
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🏥 HealthGuard AI</h1>
    <p class="header-subtitle">AI-Powered Health Insurance Cost Prediction Platform</p>
</div>
""", unsafe_allow_html=True)

# Alert Banner
st.markdown("""
<div class="alert-banner">
    ⚠️ <strong>Note:</strong> First request may take up to 30-60 seconds (API cold start).
</div>
""", unsafe_allow_html=True)

# Info Toggle
if st.button("ℹ️ How It Works"):
    st.session_state.show_info = not st.session_state.show_info

if st.session_state.show_info:
    st.markdown("""
    <div class="info-box">
        <h4>📊 About HealthGuard AI</h4>
        <p><strong>What we analyze:</strong></p>
        <ul>
            <li>Personal demographics and health profile</li>
            <li>Lifestyle factors (smoking, BMI category)</li>
            <li>Medical history and genetic risk factors</li>
            <li>Financial capacity and employment status</li>
        </ul>
        <p><strong>Our AI provides:</strong></p>
        <ul>
            <li>Accurate annual premium predictions</li>
            <li>Monthly payment breakdowns</li>
            <li>Personalized health insurance advice</li>
            <li>Interactive Q&A with AI health advisor</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Categorical options
categorical_options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Unmarried', 'Married'],
    'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'Smoking Status': ['No Smoking', 'Regular', 'Occasional'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer'],
    'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'Medical History': [
        'No Disease', 'Diabetes', 'High blood pressure', 'Diabetes & High blood pressure',
        'Thyroid', 'Heart disease', 'High blood pressure & Heart disease',
        'Diabetes & Thyroid', 'Diabetes & Heart disease'
    ],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold']
}

# ========================= INPUT FORM =========================
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👤 Personal Information</div>', unsafe_allow_html=True)
    
    age = st.number_input('Age', min_value=18, max_value=100, value=30, step=1)
    gender = st.selectbox('Gender', categorical_options['Gender'])
    marital_status = st.selectbox('Marital Status', categorical_options['Marital Status'])
    number_of_dependants = st.number_input('Number of Dependants', min_value=0, max_value=7, value=2, step=1)
    region = st.selectbox('Region', categorical_options['Region'])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💼 Financial Details</div>', unsafe_allow_html=True)
    
    income_lakhs = st.number_input('Annual Income (Lakhs)', min_value=1, max_value=200, value=10, step=1)
    employment_status = st.selectbox('Employment Status', categorical_options['Employment Status'])
    insurance_plan = st.selectbox('Insurance Plan', categorical_options['Insurance Plan'])
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🏥 Health Information</div>', unsafe_allow_html=True)
    
    bmi_category = st.selectbox('BMI Category', categorical_options['BMI Category'])
    smoking_status = st.selectbox('Smoking Status', categorical_options['Smoking Status'])
    medical_history = st.selectbox('Medical History', categorical_options['Medical History'])
    genetical_risk = st.number_input('Genetical Risk (1-5)', min_value=1, max_value=5, value=3, step=1)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Risk indicator
    risk_color = "#e74c3c" if genetical_risk >= 4 else "#f39c12" if genetical_risk == 3 else "#27ae60"
    st.markdown(f"""
    <div class="metric-card" style="background: linear-gradient(135deg, {risk_color} 0%, #243b55 100%);">
        <div class="metric-label">Genetic Risk Level</div>
        <div class="metric-value">{genetical_risk}/5</div>
    </div>
    """, unsafe_allow_html=True)

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

# ========================= PREDICTION BUTTON =========================
st.markdown("<br>", unsafe_allow_html=True)

if st.button("💰 Calculate Insurance Premium", use_container_width=True):
    API_URL = st.secrets["API_URL"]
    
    with st.spinner('🤖 Calculating your premium...'):
        try:
            response = requests.post(API_URL, json=input_dict, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                yearly = result['yearly']
                monthly = result['monthly']
                advice = result['advice']
                
                # Display Results
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown('<h3 style="margin-top:0; color:white;">📊 Premium Calculation Results</h3>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="result-grid">
                    <div class="result-item">
                        <div class="result-item-label">Annual Premium</div>
                        <div class="result-item-value">₹ {yearly:,.2f}</div>
                    </div>
                    <div class="result-item">
                        <div class="result-item-label">Monthly Premium</div>
                        <div class="result-item-value">₹ {monthly:,.2f}</div>
                    </div>
                    <div class="result-item">
                        <div class="result-item-label">Insurance Plan</div>
                        <div class="result-item-value">{insurance_plan}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Display advice
                st.markdown(f"""
                <div class="advisor-box">
                    <h4>💡 AI Health Advisor Insights</h4>
                    <p>{advice}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Store results in session state
                st.session_state.yearly_cost = yearly
                st.session_state.monthly_cost = monthly
                st.session_state.ai_summary = advice
                st.session_state.analysis_done = True
                
                st.success("✅ Calculation complete! You can now chat with our AI assistant below.")
            else:
                st.error(f"❌ API Error: {response.status_code}")
                
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. Please try again.")
        except Exception as e:
            st.error(f"❌ Connection error: {str(e)}")

# ========================= CHATBOT =========================
if st.session_state.analysis_done:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💬 Interactive Health Insurance Assistant</div>', unsafe_allow_html=True)
    
    if st.session_state.chat_history:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for role, msg in st.session_state.chat_history:
            bubble = "chat-bubble-user" if role == "user" else "chat-bubble-bot"
            prefix = "You: " if role == "user" else "🤖 Assistant: "
            st.markdown(f"<div class='{bubble}'><strong>{prefix}</strong>{msg}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    user_query = st.text_input("Ask a question about your insurance:", placeholder="e.g., How can I reduce my premium costs?")
    
    col_send, col_clear = st.columns([3, 1])
    with col_send:
        send_button = st.button("📤 Send Message", use_container_width=True)
    with col_clear:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.thread_id = str(uuid.uuid4())
            st.experimental_rerun()
    
    if send_button and user_query.strip():
        CHAT_URL = st.secrets["CHAT_URL"]
        payload = {
            "thread_id": st.session_state.thread_id,
            "message": user_query,
            "yearly_cost": st.session_state.yearly_cost,
            "monthly_cost": st.session_state.monthly_cost,
            "ai_summary": st.session_state.ai_summary
        }
        
        with st.spinner("🤖 Thinking..."):
            try:
                r = requests.post(CHAT_URL, json=payload, timeout=30)
                if r.status_code == 200:
                    reply = r.json()["response"]
                    st.session_state.chat_history.append(("user", user_query))
                    st.session_state.chat_history.append(("bot", reply))
                    st.experimental_rerun()
                else:
                    st.error(f"❌ Chat server error: {r.status_code}")
            except Exception as e:
                st.error(f"❌ Chat failed: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #7f8c8d; font-size: 0.9rem;'>
    <p>🏥 HealthGuard AI © 2025 | Powered by Advanced Machine Learning</p>
    <p style='font-size: 0.8rem;'>For demonstration purposes only. Not medical or financial advice.</p>
</div>
""", unsafe_allow_html=True)

