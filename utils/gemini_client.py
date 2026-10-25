import google.generativeai as genai
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def get_gemini_client():
    """Initialize and return Gemini client."""
    api_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai

def get_vision_model():
    """Return Gemini vision model."""
    get_gemini_client()
    return genai.GenerativeModel("gemini-1.5-flash")

def get_chat_model():
    """Return Gemini chat model."""
    get_gemini_client()
    return genai.GenerativeModel(
        "gemini-1.5-flash",
        system_instruction="""You are FoodVerse AI, an expert multimodal food intelligence agent. 
        You specialize in:
        - Identifying foods and ingredients from images
        - Providing detailed nutritional information
        - Generating personalized recipes
        - Offering dietary advice and meal planning
        - Explaining cooking techniques and food science
        
        Always be helpful, accurate, and enthusiastic about food. 
        Format responses with emojis for better readability.
        When analyzing images, be specific and detailed.
        """
    )

def analyze_food_image(image, prompt: str) -> str:
    """Analyze a food image using Gemini Vision."""
    try:
        model = get_vision_model()
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"❌ Error analyzing image: {str(e)}"

def generate_text_response(prompt: str, model=None) -> str:
    """Generate a text response from Gemini."""
    try:
        if model is None:
            model = get_chat_model()
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error generating response: {str(e)}"
