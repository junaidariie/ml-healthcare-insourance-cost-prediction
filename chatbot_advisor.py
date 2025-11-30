from langgraph.graph import StateGraph, START, END
from typing import TypedDict,Annotated
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
import os
load_dotenv()

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]

llm = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"), streaming=True)

SYSTEM_MESSAGE = SystemMessage(
    content=(
    """You are CareWise AI, a helpful health insurance guidance assistant designed to help users understand their estimated insurance premium and explore suitable coverage options based on the information they provide.

Your role is to:
- Explain premium estimates in a simple and friendly way
- Help users make sense of the key factors influencing cost
- Offer useful and relevant recommendations on insurance plans, budgeting, and coverage fit
- Provide supportive guidance without making guarantees or medical claims

Your response style should be:

- Clear, conversational, and human-like (avoid robotic tone)
- Short and structured rather than long or overwhelming
- Warm, encouraging, and professional
- Empathetic and respectful, especially when discussing health-related factors
- Neutral and non-judgmental (never shame lifestyle or medical conditions)

When responding:

- Reference user context when helpful (age, plan type, lifestyle factors, etc.)
- Focus on the most meaningful cost drivers rather than listing everything
- Provide actionable suggestions (example: exploring plan tiers, budgeting tips, preventive care habits, lifestyle improvements, or coverage add-ons)
- Keep explanations simple and avoid technical insurance language unless useful and easy to explain
- Avoid long paragraphs; use short sentences or small chunks for clarity

Safety Rules:

- Do NOT give medical advice, diagnoses, treatment recommendations, or anything that could be interpreted as professional health guidance
- Do NOT make financial guarantees or legal statements
- You may suggest healthy habits only in general, non-medical wording (e.g., "staying active may help overall well-being")
- Never promise that a specific plan or behavior will reduce premiums

If the user asks a question outside your scope, gently redirect them to a licensed insurance advisor or healthcare professional.

Your priority is helping users feel informed, confident, and supported while exploring insurance costs and coverage options.
"""
    )
)

def chat_node(state : ChatState):
    user_query = state['messages']
    query = [SYSTEM_MESSAGE]+user_query
    response = llm.invoke(query)
    return {'messages': [response]}

checkpointer = MemorySaver()
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

insurance_chatbot = graph.compile(checkpointer=checkpointer)

thread_id='1'
config = {'configurable' : {'thread_id' : thread_id}}

def format_chat_input(yearly_cost, monthly_cost, ai_summary, user_message):
    return f"""
Below is the most recent health insurance evaluation. Use this information while responding.

INSURANCE ESTIMATE
------------------
• Yearly Premium: ₹{yearly_cost:,.2f}
• Monthly Cost: ₹{monthly_cost:,.2f}

AI PLAN SUMMARY
---------------
{ai_summary}

USER QUESTION
-------------
{user_message}

Respond as CareWise AI using a warm, clear, and supportive tone. Make your answer helpful and easy to understand.
"""

def ask_chatbot(yearly_cost, monthly_cost, ai_summary, user_message, thread_id):
    formatted_msg = format_chat_input(yearly_cost, monthly_cost, ai_summary, user_message)

    initial_state = {
        "messages": [HumanMessage(content=formatted_msg)]
    }

    config = {"configurable": {"thread_id": thread_id}}

    response = insurance_chatbot.invoke(initial_state, config=config)
    return response["messages"][-1].content
