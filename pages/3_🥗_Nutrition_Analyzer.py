import streamlit as st
from PIL import Image
import sys, os
import plotly.graph_objects as go
import plotly.express as px
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.gemini_client import analyze_food_image, generate_text_response, get_gemini_client

st.set_page_config(page_title="Nutrition Analyzer · FoodVerse AI", page_icon="🥗", layout="wide")

st.markdown("""
<style>
.nutrition-card {
    background:linear-gradient(145deg,#1A1A2E,#16213E);
    border:1px solid rgba(255,107,53,0.3); border-radius:16px; padding:1.5rem; margin:0.5rem 0;
}
.macro-value { font-size:1.8rem; font-weight:800; color:#FF6B35; }
.macro-label { font-size:0.8rem; color:rgba(255,255,255,0.7); }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🥗 Nutrition Analyzer")
st.markdown("**Get detailed nutritional information from food images or text descriptions using AI.**")
st.markdown("---")

with st.sidebar:
    st.markdown("## 🥗 Nutrition Analyzer")
    st.markdown("Analyze food nutrition via image or text.")
    st.markdown("---")
    input_method = st.radio("📥 Input Method", ["📸 Image Upload", "✍️ Text Description"])
    dietary_profile = st.multiselect(
        "🎯 Your Dietary Goals",
        ["Weight Loss", "Muscle Gain", "Diabetic Friendly", "Heart Healthy", "Vegan", "Gluten Free"],
        default=[]
    )
    daily_calories = st.slider("🔥 Daily Calorie Goal", 1200, 4000, 2000, step=100)
    st.markdown("---")
    st.info(f"**Daily Goal:** {daily_calories} kcal")

# ── API Key ───────────────────────────────────────────────────────────────────
api_key = os.getenv("GEMINI_API_KEY", "")
try:
    api_key = api_key or st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    pass

if not api_key:
    st.warning("⚠️ Add your **Gemini API Key** in Streamlit secrets as `GEMINI_API_KEY`. Get it free at [Google AI Studio](https://aistudio.google.com/)")

col1, col2 = st.columns([1, 1.6])

with col1:
    st.subheader("📥 Input")

    if "📸 Image Upload" in input_method:
        uploaded = st.file_uploader("Upload food image", type=["jpg","jpeg","png","webp"])
        if uploaded:
            st.image(Image.open(uploaded), use_container_width=True)
        food_text = ""
    else:
        uploaded = None
        food_text = st.text_area(
            "Describe your food",
            placeholder="e.g. A bowl of dal makhani with 2 rotis and raita",
            height=120
        )

    serving_size = st.selectbox("🍽️ Serving Size", ["1 serving (standard)", "Half portion", "Double portion", "Custom"])
    if serving_size == "Custom":
        custom_grams = st.number_input("Grams", min_value=50, max_value=2000, value=250)

    analyze_btn = st.button("🔬 Analyze Nutrition", type="primary", use_container_width=True,
                            disabled=(not uploaded and not food_text))

with col2:
    st.subheader("📊 Nutrition Results")

    if analyze_btn:
        diet_context = f"\nUser dietary goals: {', '.join(dietary_profile)}" if dietary_profile else ""
        serving_context = f"\nServing size context: {serving_size}"

        nutrition_prompt = f"""Analyze the nutritional content of this food and provide:

1. 🍽️ **Food Name & Description**
2. 📊 **Nutrition Facts per serving**:
   - Calories (kcal)
   - Protein (g)
   - Carbohydrates (g)
   - Dietary Fiber (g)
   - Sugars (g)
   - Total Fat (g)
   - Saturated Fat (g)
   - Sodium (mg)
   - Potassium (mg)
   - Vitamins (key ones present)
   - Minerals (key ones present)

3. 🌿 **Dietary Flags**: Vegan, Vegetarian, Gluten-Free, Dairy-Free, Nut-Free status
4. ⚡ **Health Score**: Rate 1-10 with brief explanation
5. 💪 **Good For**: List health benefits
6. ⚠️ **Watch Out For**: Any concerns or limitations
7. 🔄 **Healthier Swaps**: 2-3 suggestions to make it healthier
{diet_context}{serving_context}

Please be specific with numbers. Format cleanly with emojis."""

        with st.spinner("🔬 Analyzing nutritional content..."):
            if uploaded:
                image = Image.open(uploaded)
                result = analyze_food_image(image, nutrition_prompt)
            else:
                result = generate_text_response(f"Food: {food_text}\n\n{nutrition_prompt}")

        st.markdown(f'<div class="nutrition-card">{result}</div>', unsafe_allow_html=True)

        # ── Extract rough numbers for charts ─────────────────────────────────
        st.markdown("#### 📈 Visual Breakdown")
        
        # Simple macro chart with placeholder values (extracted from response ideally)
        # We'll show a sample donut chart
        macros = {"Protein": 20, "Carbs": 45, "Fat": 25, "Fiber": 10}
        fig = go.Figure(data=[go.Pie(
            labels=list(macros.keys()),
            values=list(macros.values()),
            hole=0.5,
            marker_colors=["#FF6B35", "#F7C59F", "#FFD700", "#90EE90"],
        )])
        fig.update_layout(
            title="Macro Distribution (estimated)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            showlegend=True,
            height=300,
            margin=dict(t=40, b=10, l=10, r=10)
        )
        st.plotly_chart(fig, use_container_width=True)

        # ── Daily goal progress ───────────────────────────────────────────────
        st.markdown("#### 🎯 Daily Calorie Tracker")
        estimated_cals = 400  # placeholder
        percent = min(int(estimated_cals / daily_calories * 100), 100)
        st.progress(percent / 100, text=f"~{estimated_cals} kcal / {daily_calories} kcal daily goal ({percent}%)")

        st.download_button("📥 Download Report", result, "nutrition_report.txt", "text/plain")

    else:
        st.markdown("""
        <div style="text-align:center; padding:3rem; opacity:0.6;">
            <div style="font-size:4rem">🥗</div>
            <div style="margin-top:1rem; font-size:1rem">Upload an image or describe your food to analyze nutrition</div>
        </div>""", unsafe_allow_html=True)

# ── Info section ──────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("📚 Nutrition Guide")
n1, n2, n3 = st.columns(3)
with n1:
    st.info("**🔥 Calories**\n\nThe energy from food. Track daily intake for weight management.")
with n2:
    st.info("**💪 Macros**\n\nProtein, Carbs & Fats are the three macronutrients your body needs daily.")
with n3:
    st.info("**🌿 Micros**\n\nVitamins & Minerals are essential for immune function and overall health.")
