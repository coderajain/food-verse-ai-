import streamlit as st
import sys, os
import google.generativeai as genai
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.gemini_client import get_gemini_client

st.set_page_config(page_title="AI Food Chat · FoodVerse AI", page_icon="💬", layout="wide")

st.markdown("""
<style>
.chat-header {
    background: linear-gradient(135deg,#FF6B35,#F7C59F);
    border-radius:12px; padding:1rem 1.5rem; margin-bottom:1rem;
    color:white; font-weight:700; font-size:1.3rem;
}
.suggestion-btn {
    background:rgba(255,107,53,0.1); border:1px solid rgba(255,107,53,0.4);
    border-radius:20px; padding:6px 14px; margin:3px;
    cursor:pointer; color:#FF6B35; font-size:0.85rem;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="chat-header">💬 FoodVerse AI Chef — Your Personal Food Intelligence Agent</div>', unsafe_allow_html=True)
st.caption("Ask anything about food, recipes, nutrition, cuisines, cooking techniques, meal planning, and more!")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💬 AI Food Chat")
    st.markdown("Chat with your personal AI chef!")
    st.markdown("---")
    persona = st.selectbox("🧑‍🍳 Chef Persona", [
        "🌍 World Food Expert", "🥗 Nutrition Coach", "👨‍🍳 Professional Chef",
        "🌿 Vegan Specialist", "🍜 Asian Cuisine Expert", "🍕 Italian Maestro"
    ])
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.markdown("### 💡 Sample Topics")
    st.info("• Best Indian dinner recipes\n• Vegan protein sources\n• Italian pasta techniques\n• 30-min weeknight meals")

# ── API Key check ─────────────────────────────────────────────────────────────
api_key = os.getenv("GEMINI_API_KEY", "")
try:
    api_key = api_key or st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    pass

# ── Initialize chat history ───────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = None

# ── Persona system instructions ───────────────────────────────────────────────
persona_instructions = {
    "🌍 World Food Expert": "You are a world food expert with deep knowledge of global cuisines, street food, fine dining, and food culture across all continents.",
    "🥗 Nutrition Coach": "You are a certified nutrition coach. Focus on macros, micros, dietary advice, health benefits, and scientific nutritional information.",
    "👨‍🍳 Professional Chef": "You are a professional chef trained in culinary arts. Provide detailed cooking techniques, professional tips, and restaurant-quality recipes.",
    "🌿 Vegan Specialist": "You are a vegan cuisine specialist. Provide plant-based alternatives, vegan recipes, and advice on meeting nutritional needs on a plant-based diet.",
    "🍜 Asian Cuisine Expert": "You are an expert in Asian cuisines — Chinese, Japanese, Korean, Thai, Indian, Vietnamese, and more. Share authentic recipes and cultural context.",
    "🍕 Italian Maestro": "You are an Italian culinary maestro. Share authentic Italian recipes, regional specialties, pasta techniques, and the philosophy of Italian cooking."
}

def get_chat_session(persona_key):
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            "gemini-1.5-flash",
            system_instruction=f"""You are FoodVerse AI — a multimodal food intelligence agent. 
{persona_instructions[persona_key]}

Always:
- Use emojis to make responses engaging
- Be specific and accurate
- Format with headers when appropriate
- Keep responses helpful and concise
- Offer follow-up suggestions"""
        )
        return model.start_chat(history=[])
    return None

# Initialize or update chat session when persona changes
if "current_persona" not in st.session_state or st.session_state.current_persona != persona:
    st.session_state.current_persona = persona
    st.session_state.chat_session = get_chat_session(persona)
    st.session_state.messages = []

# ── Quick suggestion buttons ──────────────────────────────────────────────────
st.markdown("**💡 Quick Questions:**")
suggestions = [
    "What's a healthy breakfast for weight loss?",
    "Give me a 30-min pasta recipe",
    "Best foods for muscle building",
    "How to meal prep for a week?",
    "What are superfoods and their benefits?",
]
cols = st.columns(len(suggestions))
for i, (col, suggestion) in enumerate(zip(cols, suggestions)):
    with col:
        if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
            st.session_state.pending_message = suggestion

# ── Display chat history ──────────────────────────────────────────────────────
st.markdown("---")
chat_container = st.container()
with chat_container:
    # Welcome message if no history
    if not st.session_state.messages:
        st.markdown(f"""
        <div style="text-align:center; padding:2rem; opacity:0.8;">
            <div style="font-size:3rem">👨‍🍳</div>
            <div style="font-size:1.2rem; font-weight:600; margin-top:0.5rem; color:#FF6B35">
                Hello! I'm your {persona}
            </div>
            <div style="font-size:0.9rem; margin-top:0.5rem; color:rgba(255,255,255,0.7)">
                Ask me anything about food, recipes, nutrition, or cooking!
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑" if message["role"] == "user" else "👨‍🍳"):
            st.markdown(message["content"])

# ── Chat input ────────────────────────────────────────────────────────────────
prompt = st.chat_input("Ask your food question...")

# Handle suggestion button clicks
if "pending_message" in st.session_state and st.session_state.pending_message:
    prompt = st.session_state.pending_message
    st.session_state.pending_message = None

if prompt:
    if not api_key:
        st.warning("⚠️ Please add your **Gemini API Key** to use the chat. Get it free at [Google AI Studio](https://aistudio.google.com/)")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt)

        # Get AI response
        with st.chat_message("assistant", avatar="👨‍🍳"):
            with st.spinner("🤔 Thinking..."):
                try:
                    if st.session_state.chat_session:
                        response = st.session_state.chat_session.send_message(prompt)
                        reply = response.text
                    else:
                        reply = "⚠️ Chat session not initialized. Please check your API key."
                except Exception as e:
                    reply = f"❌ Error: {str(e)}"
            
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
