# FitMind AI

FitMind AI is a modular, culturally adaptive wellness assistant designed to support users across India and beyond. It combines personalized fitness planning, nutrition-aware recipe generation, mood-based progress tracking, and intelligent chat support—all powered by resilient architecture and region-aware data.

## 🌟 Features

- **🧑‍💼 Profile Builder**  
  Collects user name, location, fitness goals, health conditions, mood, preferred activities, and budget to personalize recommendations.

- **💬 Chatbot**  
  Answers any user query with fallback logic, chat history, and OpenRouter integration for intelligent, emotionally aware responses.

- **📈 Progress Tracker**  
  Logs mood, weight, and meals to analyze trends and offer goal-based suggestions.

- **🥗 Recipe Generator**  
  Creates recipes based on available groceries, complete with nutrition values and cultural relevance.

- **🏋️ Fitness Planner**  
  Generates personalized workout plans based on user goals, preferences, and constraints.

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas, NumPy
- OpenRouter API
- Custom datasets (Kaggle meal plans, health maps, fitness routines)

## 🚀 How to Run Locally

```bash
git clone https://github.com/Teju-2007/fitmind-ai.git
cd fitmind-ai
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
streamlit run chatbot.py