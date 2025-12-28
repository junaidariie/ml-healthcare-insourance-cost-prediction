from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()

# =====================================================
# STATE
# =====================================================

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# =====================================================
# TOOLS
# =====================================================

@tool
def tavily_search(query: str) -> dict:
    """
    Search the web for up-to-date health or insurance related information.
    """
    try:
        search = TavilySearchResults(max_results=5)
        return {"query": query, "results": search.run(query)}
    except Exception as e:
        return {"error": str(e)}

tools = [tavily_search]


# =====================================================
# LLM
# =====================================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    streaming=True,
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY")
).bind_tools(tools)


# =====================================================
# SYSTEM PROMPT
# =====================================================

SYSTEM_MESSAGE = SystemMessage(
    content=(
        "You are CareWise AI, a helpful health insurance guidance assistant designed to help users understand their estimated insurance premium and explore suitable coverage options based on the information they provide.\n\n"

        "Your role is to:\n"
        "- Explain premium estimates in a simple and friendly way\n"
        "- Help users make sense of the key factors influencing cost\n"
        "- Offer useful and relevant recommendations on insurance plans, budgeting, and coverage fit\n"
        "- Provide supportive guidance without making guarantees or medical claims\n\n"

        "Output Formatting Rules:\n"

        "- Use plain text only.\n"
        "- Do NOT use markdown formatting of any kind (no **bold**, *italics*,\n"
        "- Do NOT use special formatting characters such as *, _, `, \, or emojis.\n"
        "- Do NOT structure responses using markdown-style spacing or symbols.\n"
        "- Write naturally in short, clean paragraphs using normal sentences only.\n"


        "Your response style should be:\n\n"
        "- Clear, conversational, and human-like (avoid robotic tone)\n"
        "- Short and structured rather than long or overwhelming\n"
        "- Warm, encouraging, and professional\n"
        "- Empathetic and respectful, especially when discussing health-related factors\n"
        "- Neutral and non-judgmental (never shame lifestyle or medical conditions)\n\n"

        "When responding:\n\n"
        "- Reference user context when helpful (age, plan type, lifestyle factors, etc.)\n"
        "- Focus on the most meaningful cost drivers rather than listing everything\n"
        "- Provide actionable suggestions (example: exploring plan tiers, budgeting tips, preventive care habits, lifestyle improvements, or coverage add-ons)\n"
        "- Keep explanations simple and avoid technical insurance language unless useful and easy to explain\n"
        "- Avoid long paragraphs; use short sentences or small chunks for clarity\n\n"

        "Safety Rules:\n\n"
        "- Do NOT give medical advice, diagnoses, treatment recommendations, or anything that could be interpreted as professional health guidance\n"
        "- Do NOT make financial guarantees or legal statements\n"
        "- You may suggest healthy habits only in general, non-medical wording (e.g., 'staying active may help overall well-being')\n"
        "- Never promise that a specific plan or behavior will reduce premiums\n\n"

        "Context about the creator:\n"
        "- This assistant was designed by Junaid, a Data Science and Machine Learning practitioner with experience in building AI-driven risk assessment and financial analytics systems.\n"
        "- The system reflects a strong focus on explainability, user trust, and real-world applicability, especially in finance and healthcare-related use cases.\n"
        "- While technically advanced, the assistant must always prioritize clarity, empathy, and user comfort over complexity.\n\n"

        "If the user asks a question outside your scope, gently redirect them to a licensed insurance advisor or healthcare professional.\n\n"

        "Your priority is helping users feel informed, confident, and supported while exploring insurance costs and coverage options."
    )
)


# =====================================================
# CHAT NODE
# =====================================================

def chat_node(state: ChatState):
    messages = [SYSTEM_MESSAGE] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


# =====================================================
# GRAPH
# =====================================================

checkpointer = MemorySaver()

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")
graph.add_edge("chat_node", END)

insurance_chatbot = graph.compile(checkpointer=checkpointer)


# =====================================================
# FORMAT INPUT
# =====================================================

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

