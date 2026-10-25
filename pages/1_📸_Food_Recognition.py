import streamlit as st
from PIL import Image
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.gemini_client import analyze_food_image, get_gemini_client

st.set_page_config(page_title="Food Recognition · FoodVerse AI", page_icon="📸", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.result-card {
    background: linear-gradient(145deg,#1A1A2E,#16213E);
    border:1px solid rgba(255,107,53,0.4);
    border-radius:16px; padding:1.5rem; margin:1rem 0;
}
.section-title { color:#FF6B35; font-weight:700; font-size:1.1rem; margin-bottom:0.5rem; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 📸 Food Recognition")
st.markdown("**Upload any food photo and let Gemini AI identify it, suggest recipes, and provide culinary insights.**")
st.markdown("---")

# ── Sidebar config ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📸 Food Recognition")
    st.markdown("Upload a photo to identify food, get recipes, and explore culinary details.")
    st.markdown("---")
    analysis_mode = st.selectbox(
        "🎯 Analysis Mode",
        ["Full Analysis", "Quick Identification", "Recipe Focus", "Cultural & History"]
    )
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.info("• Use clear, well-lit photos\n• Single dish works best\n• Works with ingredients too!")

# ── API Key check ─────────────────────────────────────────────────────────────
api_key = os.getenv("GEMINI_API_KEY", "") or st.secrets.get("GEMINI_API_KEY", "") if hasattr(st, 'secrets') else ""
if not api_key:
    st.warning("⚠️ Add your **Gemini API Key** in Streamlit secrets or `.env` file as `GEMINI_API_KEY`")
    st.code("GEMINI_API_KEY=your_key_here", language="bash")
    st.markdown("👉 Get your free key at [Google AI Studio](https://aistudio.google.com/)")

# ── Upload ────────────────────────────────────────────────────────────────────
col_upload, col_result = st.columns([1, 1.5])

with col_upload:
    st.subheader("📤 Upload Food Image")
    uploaded_file = st.file_uploader(
        "Choose a food image...",
        type=["jpg", "jpeg", "png", "webp"],
        help="Supports JPG, PNG, WebP up to 10MB"
    )
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        st.success(f"✅ Image loaded: {uploaded_file.name} ({uploaded_file.size//1024} KB)")

    # ── Example prompts ───────────────────────────────────────────────────────
    st.markdown("#### 🎯 What would you like to know?")
    custom_question = st.text_area(
        "Custom question (optional)",
        placeholder="e.g. Is this dish spicy? Can I make it vegan?",
        height=80
    )

    analyze_btn = st.button("🔍 Analyze Food", type="primary", use_container_width=True, disabled=not uploaded_file)

# ── Analysis ──────────────────────────────────────────────────────────────────
with col_result:
    st.subheader("🤖 AI Analysis Results")

    if analyze_btn and uploaded_file:
        image = Image.open(uploaded_file)

        # Build prompt based on mode
        mode_prompts = {
            "Full Analysis": """Analyze this food image comprehensively:

1. 🍽️ **Food Identification**: Name the dish/ingredients with confidence level
2. 🌍 **Origin & Cuisine**: Cultural background and cuisine type  
3. 📊 **Estimated Nutrition**: Calories, protein, carbs, fats per serving
4. 👨‍🍳 **Recipe**: Step-by-step recipe to make this dish
5. 💡 **Variations**: 3 creative variations or substitutions
6. 🌿 **Dietary Info**: Vegan/vegetarian/gluten-free status, allergens
7. ⭐ **Fun Fact**: An interesting fact about this food

Format with clear sections and emojis.""",

            "Quick Identification": """Quickly identify this food:
1. 🍽️ What is this food/dish?
2. 🌍 What cuisine/origin?
3. 📊 Rough calorie estimate
4. 🌿 Key dietary flags (vegan, gluten-free, etc.)
Keep it brief and punchy!""",

            "Recipe Focus": """Focus on the recipe for this food:
1. 🍽️ Dish name
2. 🛒 Ingredients list (with quantities)
3. 👨‍🍳 Step-by-step cooking instructions
4. ⏱️ Prep & cook time
5. 🍽️ Serving suggestions
6. 💡 Pro tips for perfect results""",

            "Cultural & History": """Tell me the cultural story of this food:
1. 🍽️ Food identification
2. 🌍 Geographic & cultural origin
3. 📜 History and evolution of the dish
4. 🎉 When/how is it traditionally served?
5. 🌐 Regional variations across the world
6. 🤝 Cultural significance"""
        }

        prompt = mode_prompts[analysis_mode]
        if custom_question:
            prompt += f"\n\n7. ❓ **Custom Question**: {custom_question}"

        with st.spinner("🔍 Gemini is analyzing your food image..."):
            result = analyze_food_image(image, prompt)

        st.markdown(f'<div class="result-card">{result}</div>', unsafe_allow_html=True)

        # ── Download result ───────────────────────────────────────────────────
        st.download_button(
            "📥 Download Analysis",
            data=result,
            file_name="foodverse_analysis.txt",
            mime="text/plain"
        )

    elif not uploaded_file:
        st.markdown("""
        <div style="text-align:center; padding:3rem; opacity:0.6;">
            <div style="font-size:4rem">📸</div>
            <div style="font-size:1.1rem; margin-top:1rem">Upload a food image to get started</div>
            <div style="font-size:0.85rem; margin-top:0.5rem">Supports any food, dish, or ingredient photo</div>
        </div>
        """, unsafe_allow_html=True)

# ── Sample gallery ────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("🌟 What FoodVerse AI Can Identify")
g1, g2, g3, g4, g5 = st.columns(5)
foods = [("🍕", "Pizza"), ("🍣", "Sushi"), ("🥘", "Curries"), ("🥗", "Salads"), ("🍰", "Desserts")]
for col, (icon, name) in zip([g1, g2, g3, g4, g5], foods):
    with col:
        st.markdown(f"""
        <div style="text-align:center; background:rgba(255,107,53,0.1); border-radius:12px; padding:1rem;">
            <div style="font-size:2.5rem">{icon}</div>
            <div style="color:#FF6B35; font-weight:600; margin-top:0.3rem">{name}</div>
        </div>""", unsafe_allow_html=True)
