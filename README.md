# 🍽️ FoodVerse AI — Multimodal Food Intelligence Agent

<div align="center">

![FoodVerse AI Banner](https://img.shields.io/badge/🍽️%20FoodVerse%20AI-Multimodal%20Food%20Intelligence-FF6B35?style=for-the-badge)

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**A powerful multimodal AI agent for food intelligence — built with Google Gemini 1.5 Flash**

[🚀 Live Demo](https://bo6qsblu3b4qtdohmnoxgw.streamlit.app/) · [📂 GitHub](https://github.com/coderajain/food-verse-ai-) · [📖 Docs](#)

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 📸 **Food Recognition** | Upload any food photo → instant identification, recipes & cultural insights |
| 💬 **AI Food Chat** | Conversational food intelligence agent with customizable chef personas |
| 🥗 **Nutrition Analyzer** | Detailed calorie, macro & micronutrient breakdown from image or text |
| 📋 **Recipe Generator** | Generate recipes from available ingredients, cuisine type, or food photos |

---

## 🎯 Project Overview

**FoodVerse AI** is a multimodal food intelligence agent powered by **Google Gemini 1.5 Flash**. It can process both text and image inputs to deliver intelligent, context-aware food insights — from identifying dishes in photos to generating personalized weekly meal plans.

Built as part of the **Generative AI with Google Cloud** learning path on SkillWallet.

### 🤖 Core AI Capabilities
- **Vision Understanding** — Analyze food images to identify dishes, ingredients & plating styles
- **Recipe Generation** — Create step-by-step recipes tailored to your ingredients & preferences
- **Nutritional Analysis** — Estimate calories, macros & micronutrients from images or descriptions
- **Conversational AI** — Multi-turn chat with persona-based food expert agents
- **Cultural Intelligence** — Understand food history, origins & regional variations

---

## 🛠️ Tech Stack

```
Frontend   → Streamlit (Python UI framework)
AI Model   → Google Gemini 1.5 Flash (Multimodal)
Vision     → Gemini Vision API (image + text understanding)
Charts     → Plotly (interactive data visualization)
Language   → Python 3.9+
Deployment → Streamlit Community Cloud
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- A free **Google Gemini API Key** from [Google AI Studio](https://aistudio.google.com/)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/coderajain/food-verse-ai-.git
cd food-verse-ai-

# 2. Create a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your API key
cp .env.example .env
# Edit .env and add your Gemini API key:
# GEMINI_API_KEY=your_api_key_here

# 5. Run the app
streamlit run app.py
```

### 🌐 Open in Browser
```
http://localhost:8501
```

---

## 🔑 API Key Setup

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Click **"Create API Key"**
3. Copy the key
4. Add to `.env`:
   ```
   GEMINI_API_KEY=your_key_here
   ```

**For Streamlit Cloud deployment**, add `GEMINI_API_KEY` in your app's **Secrets** settings.

---

## 📂 Project Structure

```
food-verse-ai/
├── app.py                          # 🏠 Home page (Streamlit entry point)
├── requirements.txt                # 📦 Python dependencies
├── .env.example                    # 🔑 Environment variables template
├── .streamlit/
│   └── config.toml                 # 🎨 Streamlit theme configuration
├── pages/
│   ├── 1_📸_Food_Recognition.py    # 📸 Visual food identification
│   ├── 2_💬_AI_Food_Chat.py        # 💬 Conversational AI agent
│   ├── 3_🥗_Nutrition_Analyzer.py  # 🥗 Nutritional breakdown
│   └── 4_📋_Recipe_Generator.py    # 📋 Recipe generation
└── utils/
    ├── __init__.py
    └── gemini_client.py            # 🤖 Gemini API client & utilities
```

---

## 🌍 Deployment

### Deploy to Streamlit Community Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"New App"** → Connect your GitHub repo
4. Set **Main file path** to `app.py`
5. Add `GEMINI_API_KEY` in **Advanced Settings → Secrets**:
   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   ```
6. Click **Deploy** 🚀

---

## 📸 Screenshots

### 🏠 Home Dashboard
- Modern dark UI with food-themed orange accents
- Feature cards with hover effects
- Technology stack overview

### 📸 Food Recognition
- Drag-and-drop image upload
- 4 analysis modes (Full, Quick, Recipe, Cultural)
- Detailed AI-powered food insights

### 💬 AI Chat
- Multi-persona chef AI agents
- Real-time streaming responses
- Conversation history management

### 🥗 Nutrition Analyzer
- Image + text input support
- Macro distribution pie charts
- Daily calorie tracker

### 📋 Recipe Generator
- From ingredients / by cuisine / from photo / weekly meal plan
- Adjustable difficulty, time, and dietary filters
- Downloadable recipe cards

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👨‍💻 Author

**Coder Ajain**  
[![GitHub](https://img.shields.io/badge/GitHub-coderajain-black?logo=github)](https://github.com/coderajain)

---

## 🙏 Acknowledgements

- [Google Gemini](https://deepmind.google/technologies/gemini/) — Multimodal AI foundation
- [Streamlit](https://streamlit.io) — Python web app framework
- [Google AI Studio](https://aistudio.google.com/) — Free Gemini API access
- [SkillWallet](https://myskillwallet.ai) — Generative AI with Google Cloud learning path

---

<div align="center">
  Made with ❤️ and 🍕 · FoodVerse AI © 2024
</div>
