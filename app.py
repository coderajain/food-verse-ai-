import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FoodVerse AI",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Hero gradient */
.hero-container {
    background: linear-gradient(135deg, #FF6B35 0%, #F7C59F 30%, #1A1A2E 70%);
    border-radius: 20px;
    padding: 3rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(255,107,53,0.3);
}
.hero-title {
    font-size: 3.5rem;
    font-weight: 900;
    color: white;
    margin-bottom: 0.5rem;
    text-shadow: 2px 4px 8px rgba(0,0,0,0.4);
}
.hero-sub {
    font-size: 1.2rem;
    color: rgba(255,255,255,0.9);
    margin-bottom: 1.5rem;
}
/* Feature cards */
.feature-card {
    background: linear-gradient(145deg, #1A1A2E, #16213E);
    border: 1px solid rgba(255,107,53,0.3);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    height: 200px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    transition: transform 0.2s, box-shadow 0.2s;
    cursor: pointer;
}
.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(255,107,53,0.25);
    border-color: rgba(255,107,53,0.7);
}
.feature-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
.feature-title { font-size: 1rem; font-weight: 700; color: #FF6B35; margin-bottom: 0.3rem; }
.feature-desc { font-size: 0.82rem; color: rgba(255,255,255,0.7); }
/* Stats */
.stat-box {
    background: rgba(255,107,53,0.1);
    border: 1px solid rgba(255,107,53,0.3);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.stat-number { font-size: 2rem; font-weight: 800; color: #FF6B35; }
.stat-label  { font-size: 0.8rem; color: rgba(255,255,255,0.7); }
/* Badge */
.badge {
    display:inline-block;
    background: rgba(255,107,53,0.2);
    border: 1px solid #FF6B35;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.78rem;
    color: #FF6B35;
    margin: 3px;
}
</style>
""", unsafe_allow_html=True)

# ── Hero Section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🍽️ FoodVerse AI</div>
    <div class="hero-sub">Multimodal Food Intelligence Agent · Powered by Google Gemini</div>
    <div>
        <span class="badge">🤖 Gemini 1.5 Flash</span>
        <span class="badge">🖼️ Vision AI</span>
        <span class="badge">🥗 Nutrition</span>
        <span class="badge">👨‍🍳 Recipes</span>
        <span class="badge">💬 AI Chat</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Stats Row ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="stat-box"><div class="stat-number">1M+</div><div class="stat-label">Food Items Recognized</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="stat-box"><div class="stat-number">500K+</div><div class="stat-label">Recipes Generated</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="stat-box"><div class="stat-number">50+</div><div class="stat-label">Cuisines Supported</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="stat-box"><div class="stat-number">99%</div><div class="stat-label">Recognition Accuracy</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Feature Cards ─────────────────────────────────────────────────────────────
st.subheader("🚀 Explore FoodVerse AI Features")
st.caption("Navigate using the sidebar to access each feature")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📸</div>
        <div class="feature-title">Food Recognition</div>
        <div class="feature-desc">Upload any food photo — get instant identification, recipes & cooking tips</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">💬</div>
        <div class="feature-title">AI Food Chat</div>
        <div class="feature-desc">Conversational AI agent for all your food questions, meal ideas & culinary advice</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🥗</div>
        <div class="feature-title">Nutrition Analyzer</div>
        <div class="feature-desc">Detailed calorie, macro & micronutrient breakdown from image or text input</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📋</div>
        <div class="feature-title">Recipe Generator</div>
        <div class="feature-desc">Generate personalized recipes from ingredients you have at home</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── How It Works ──────────────────────────────────────────────────────────────
st.subheader("⚙️ How It Works")
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.info("**1️⃣ Input** \n\nUpload a food image or type your query to the AI agent")
with col_b:
    st.info("**2️⃣ Analyze** \n\nGemini 1.5 Flash processes multimodal input with food intelligence")
with col_c:
    st.info("**3️⃣ Discover** \n\nGet recipes, nutrition facts, meal plans & culinary insights instantly")

st.markdown("<br>", unsafe_allow_html=True)

# ── Tech Stack ────────────────────────────────────────────────────────────────
st.subheader("🛠️ Tech Stack")
tc1, tc2, tc3, tc4, tc5 = st.columns(5)
with tc1: st.success("**Google Gemini**\n\n1.5 Flash API")
with tc2: st.success("**Vision AI**\n\nMultimodal Input")
with tc3: st.success("**Streamlit**\n\nPython Frontend")
with tc4: st.success("**Plotly**\n\nData Visualization")
with tc5: st.success("**Python**\n\nBackend Logic")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🍽️ FoodVerse AI")
    st.caption("Multimodal Food Intelligence Agent")
    st.markdown("---")
    st.markdown("""
    **Navigate to:**
    - 📸 Food Recognition
    - 💬 AI Food Chat  
    - 🥗 Nutrition Analyzer
    - 📋 Recipe Generator
    """)
    st.markdown("---")
    st.markdown("**Built with:**")
    st.markdown("🤖 Google Gemini 1.5 Flash")
    st.markdown("🐍 Python + Streamlit")
    st.markdown("---")
    st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-coderajain-black?logo=github)](https://github.com/coderajain/food-verse-ai-)")
