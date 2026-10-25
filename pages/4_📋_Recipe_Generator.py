import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.gemini_client import generate_text_response, analyze_food_image, get_gemini_client
from PIL import Image

st.set_page_config(page_title="Recipe Generator · FoodVerse AI", page_icon="📋", layout="wide")

st.markdown("""
<style>
.recipe-card {
    background:linear-gradient(145deg,#1A1A2E,#16213E);
    border:1px solid rgba(255,107,53,0.4); border-radius:16px; padding:1.5rem; margin:1rem 0;
}
.tag {
    display:inline-block; background:rgba(255,107,53,0.15); border:1px solid rgba(255,107,53,0.5);
    border-radius:20px; padding:3px 12px; font-size:0.78rem; color:#FF6B35; margin:2px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("# 📋 Recipe Generator")
st.markdown("**Generate personalized recipes from your ingredients, cuisine preference, or a food image.**")
st.markdown("---")

with st.sidebar:
    st.markdown("## 📋 Recipe Generator")
    st.markdown("Create custom recipes tailored to your needs!")
    st.markdown("---")
    recipe_mode = st.radio("🎯 Recipe Mode", [
        "🧺 From Ingredients",
        "🌍 By Cuisine & Dish",
        "📸 From Food Image",
        "🗓️ Weekly Meal Plan"
    ])
    st.markdown("---")
    num_recipes = st.slider("📄 Number of Recipes", 1, 5, 2)
    difficulty = st.selectbox("⚡ Difficulty", ["Easy (Beginner)", "Medium (Intermediate)", "Hard (Advanced)"])
    cook_time = st.selectbox("⏱️ Max Cook Time", ["15 mins", "30 mins", "45 mins", "1 hour", "Any"])
    st.markdown("---")
    dietary_restrictions = st.multiselect(
        "🌿 Dietary Restrictions",
        ["Vegetarian", "Vegan", "Gluten Free", "Dairy Free", "Nut Free", "Low Carb", "Keto", "Paleo"]
    )

# ── API Key ───────────────────────────────────────────────────────────────────
api_key = os.getenv("GEMINI_API_KEY", "")
try:
    api_key = api_key or st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    pass

if not api_key:
    st.warning("⚠️ Add your **Gemini API Key** in Streamlit secrets as `GEMINI_API_KEY`. [Get it free →](https://aistudio.google.com/)")

# ── Recipe Mode UI ────────────────────────────────────────────────────────────
col_input, col_output = st.columns([1, 1.5])

with col_input:
    st.subheader("⚙️ Recipe Settings")

    diet_str = ", ".join(dietary_restrictions) if dietary_restrictions else "None"
    generate_btn = False

    if "🧺 From Ingredients" in recipe_mode:
        ingredients = st.text_area(
            "🛒 Your Available Ingredients",
            placeholder="e.g. chicken breast, tomatoes, onions, garlic, olive oil, pasta",
            height=150,
            help="List ingredients separated by commas"
        )
        cuisine_hint = st.selectbox("🌍 Preferred Cuisine (optional)",
            ["Any", "Indian", "Italian", "Chinese", "Mexican", "Thai", "Japanese", "Mediterranean", "American"])
        generate_btn = st.button("👨‍🍳 Generate Recipes", type="primary", use_container_width=True,
                                  disabled=not ingredients)

    elif "🌍 By Cuisine & Dish" in recipe_mode:
        cuisine = st.selectbox("🌍 Cuisine", 
            ["Indian", "Italian", "Chinese", "Mexican", "Thai", "Japanese",
             "Mediterranean", "American", "Korean", "French", "Middle Eastern", "Greek"])
        dish_type = st.selectbox("🍽️ Dish Type",
            ["Main Course", "Starter/Appetizer", "Dessert", "Breakfast", "Snack", "Soup", "Salad", "Side Dish"])
        special_request = st.text_input("✨ Special Request (optional)", 
            placeholder="e.g. romantic dinner, comfort food, kids-friendly")
        generate_btn = st.button("👨‍🍳 Generate Recipes", type="primary", use_container_width=True)

    elif "📸 From Food Image" in recipe_mode:
        uploaded = st.file_uploader("Upload a food photo to recreate", type=["jpg","jpeg","png","webp"])
        if uploaded:
            st.image(Image.open(uploaded), use_container_width=True)
        generate_btn = st.button("👨‍🍳 Generate Recipe", type="primary", use_container_width=True,
                                  disabled=not uploaded)

    elif "🗓️ Weekly Meal Plan" in recipe_mode:
        plan_goal = st.selectbox("🎯 Your Goal",
            ["Balanced & Healthy", "Weight Loss", "Muscle Gain", "High Protein", "Budget Friendly", "Quick Meals"])
        num_people = st.number_input("👨‍👩‍👧 Number of People", 1, 10, 2)
        include_snacks = st.checkbox("Include Snacks", value=True)
        generate_btn = st.button("📅 Generate Meal Plan", type="primary", use_container_width=True)

    # ── Quick cuisine buttons ─────────────────────────────────────────────────
    st.markdown("#### 🌍 Popular Cuisines")
    cuisines_quick = ["🍕 Italian", "🍜 Chinese", "🍛 Indian", "🌮 Mexican"]
    qc = st.columns(2)
    for i, cq in enumerate(cuisines_quick):
        with qc[i % 2]:
            st.markdown(f'<span class="tag">{cq}</span>', unsafe_allow_html=True)

with col_output:
    st.subheader("🍳 Generated Recipes")

    if generate_btn:
        # Build appropriate prompt
        base_settings = f"""
Settings:
- Number of recipes: {num_recipes}
- Difficulty: {difficulty}
- Max cook time: {cook_time}
- Dietary restrictions: {diet_str}
"""
        if "🧺 From Ingredients" in recipe_mode:
            prompt = f"""Generate {num_recipes} creative recipe(s) using ONLY or MOSTLY these ingredients:
**Ingredients available**: {ingredients}
**Preferred cuisine**: {cuisine_hint}
{base_settings}

For each recipe provide:
1. 🍽️ **Recipe Name**
2. ⏱️ **Time**: Prep + Cook time
3. 🍽️ **Servings**
4. ⭐ **Difficulty**
5. 🛒 **Ingredients** (with exact quantities)
6. 👨‍🍳 **Step-by-Step Instructions** (numbered)
7. 💡 **Chef's Tips**
8. 🔄 **Possible Substitutions**

Format each recipe clearly with headers and emojis!"""

        elif "🌍 By Cuisine & Dish" in recipe_mode:
            prompt = f"""Generate {num_recipes} authentic {cuisine} {dish_type} recipe(s).
{f"Special request: {special_request}" if special_request else ""}
{base_settings}

For each recipe:
1. 🍽️ **Recipe Name** (authentic name + translation if needed)
2. 🌍 **Origin/Region**
3. ⏱️ **Time**: Prep + Cook
4. 🍽️ **Servings**
5. 🛒 **Ingredients** (with quantities)
6. 👨‍🍳 **Instructions** (step-by-step)
7. 🍷 **Serving Suggestions**
8. 💡 **Authenticity Tips**"""

        elif "📸 From Food Image" in recipe_mode:
            prompt = f"""Look at this food image and create a detailed recipe to recreate it at home.
{base_settings}

Provide:
1. 🍽️ **Dish Identification** — what is this?
2. 🛒 **Ingredients** (with exact quantities for home cooking)
3. 🍳 **Equipment Needed**
4. 👨‍🍳 **Step-by-Step Recipe**
5. 🎨 **Plating Tips** to match the photo
6. 🔄 **Variations** to try"""

        elif "🗓️ Weekly Meal Plan" in recipe_mode:
            prompt = f"""Create a complete 7-day meal plan for {num_people} person(s).
Goal: {plan_goal}
Include snacks: {include_snacks}
{base_settings}

Format as:
**Day 1 - [Day Name]**
- 🌅 Breakfast: [dish + brief description]
- ☀️ Lunch: [dish + brief description]
- 🌙 Dinner: [dish + brief description]
{"- 🍎 Snacks: [options]" if include_snacks else ""}
- 📊 Approx. Calories: [number]

Repeat for all 7 days. End with:
- 🛒 **Master Shopping List** (organized by category)
- 💡 **Meal Prep Tips** for the week"""

        with st.spinner("👨‍🍳 Generating your personalized recipe(s)..."):
            if "📸 From Food Image" in recipe_mode and uploaded:
                image = Image.open(uploaded)
                result = analyze_food_image(image, prompt)
            else:
                result = generate_text_response(prompt)

        st.markdown(f'<div class="recipe-card">{result}</div>', unsafe_allow_html=True)

        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.download_button("📥 Download Recipe", result, "recipe.txt", "text/plain", use_container_width=True)
        with col_dl2:
            st.button("📤 Share Recipe", use_container_width=True, disabled=True, help="Coming soon!")

    else:
        st.markdown("""
        <div style="text-align:center; padding:3rem; opacity:0.6;">
            <div style="font-size:4rem">📋</div>
            <div style="margin-top:1rem; font-size:1rem">Configure your preferences and generate recipes!</div>
        </div>""", unsafe_allow_html=True)

# ── Popular cuisines showcase ─────────────────────────────────────────────────
st.markdown("---")
st.subheader("🌍 Explore World Cuisines")
wc = st.columns(6)
world_cuisines = [("🇮🇳","Indian"),("🇮🇹","Italian"),("🇯🇵","Japanese"),("🇲🇽","Mexican"),("🇨🇳","Chinese"),("🇹🇭","Thai")]
for col, (flag, name) in zip(wc, world_cuisines):
    with col:
        st.markdown(f"""
        <div style="text-align:center; background:rgba(255,107,53,0.1); border-radius:12px; padding:0.8rem;">
            <div style="font-size:2rem">{flag}</div>
            <div style="color:#FF6B35; font-weight:600; font-size:0.85rem; margin-top:0.3rem">{name}</div>
        </div>""", unsafe_allow_html=True)
