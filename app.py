import streamlit as st

# Core modules
from utils.profile import collect_user_profile
from utils.onboarding import show_welcome
from utils.recipe_generator import show_recipe_generator
from utils.chatbot import show_chatbot 
from utils.progress import show_progress_tracker
from utils.weekly_summary import show_weekly_summary
from utils.fitness import show_fitness_dashboard  # ✅ Added fitness module

# Page config
st.set_page_config(page_title="FitMind AI", layout="wide")

# App header
st.title("🧠 FitMind AI")
st.caption("Your dynamic, health-aware nutrition companion")

# Sidebar navigation
page = st.sidebar.radio("📂 Navigation", [
    "Welcome", "Profile Setup",
    "Chatbot", "Progress Tracker",
    "Weekly Summary", "Fitness Dashboard",
    "Recipe Generator"
])

# Page routing
pages = {
    "Welcome": show_welcome,
    "Profile Setup": collect_user_profile,
    "Chatbot": show_chatbot,
    "Progress Tracker": show_progress_tracker,
    "Weekly Summary": show_weekly_summary,
    "Fitness Dashboard": show_fitness_dashboard,  # ✅ Routing added
    "Recipe Generator": show_recipe_generator,
}

# Render selected page
pages[page]()