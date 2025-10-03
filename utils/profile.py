import streamlit as st
import os
import requests
from dotenv import load_dotenv
from utils.storage import save_user_profile
from utils.ingredient_client import get_local_ingredients

# Load environment variables
load_dotenv()
GEODB_API_KEY = os.getenv("GEODB_API_KEY")

def get_user_fitness_preferences():
    # In a real app, this could come from user input or stored profile
    return {
        "goal": "strength",          # Options: strength, flexibility, fat loss
        "body_part": "legs",         # Options: legs, arms, core, full body
        "equipment": "dumbbells"     # Options: dumbbells, body weight, resistance band
    }

def normalize_location(location_name):
    if not GEODB_API_KEY:
        print("Missing GEODB_API_KEY in .env")
        return None

    url = f"https://wft-geo-db.p.rapidapi.com/v1/geo/cities?namePrefix={location_name}"
    headers = {
        "X-RapidAPI-Key": GEODB_API_KEY,
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.ok:
            data = response.json()
            if data.get("data"):
                city = data["data"][0]
                return {
                    "city": city["city"],
                    "country": city["country"],
                    "region": city.get("region"),
                    "latitude": city["latitude"],
                    "longitude": city["longitude"]
                }
        else:
            print(f"GeoDB error: {response.status_code} — {response.text[:100]}")
    except requests.exceptions.RequestException as e:
        print(f"Location request failed: {e}")
    return None

def collect_user_profile():
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}

    st.header("👤 Your Health Profile")

    name = st.text_input("Name", value=st.session_state.user_data.get("name", ""))
    location_input = st.text_input("📍 Where do you live?", value=st.session_state.user_data.get("location_input", ""))

    budget = st.number_input("💰 Monthly Grocery Budget (₹)", min_value=500, max_value=10000, step=100)
    health_input = st.text_input("🩺 Health Conditions (comma-separated)")
    goal_input = st.text_input("🎯 Fitness Goals (comma-separated)")

    diet_type = st.radio("🥗 Diet Type", [
        "vegetarian",
        "non-vegetarian",
        "vegan",
        "pescatarian",
        "gluten-free",
        "keto",
        "paleo",
        "diabetic-friendly",
        "low-FODMAP"
    ])

    mood = st.selectbox("🧠 Your usual mood", [
        "😊 Happy",
        "😐 Neutral",
        "😞 Low",
        "😠 Frustrated",
        "😴 Tired",
        "😕 Anxious",
        "😇 Calm",
        "🤯 Overwhelmed",
        "😎 Confident"
    ])

    activity_type = st.selectbox("🏃 Preferred activity", [
        "Walking", "Yoga", "Running", "Gym", "Cycling", "Swimming", "Dance"
    ])

    sleep_hours = st.number_input("😴 Average sleep per night (hours)", min_value=3.0, max_value=12.0, step=0.5)

    health_conditions = [h.strip().lower() for h in health_input.split(",") if h.strip()]
    fitness_goals = [g.strip().lower() for g in goal_input.split(",") if g.strip()]

    location_data = normalize_location(location_input)
    if location_data:
        st.success(f"📍 Detected: {location_data['city']}, {location_data['country']}")
        ingredients = get_local_ingredients(location_data["country"])
    else:
        st.warning("Could not detect location. Try a nearby city.")
        location_data = {}
        ingredients = []

    if st.button("Save Profile"):
        profile = {
            "name": name,
            "monthly_budget": budget,
            "health_conditions": health_conditions,
            "fitness_goals": fitness_goals,
            "diet_type": diet_type,
            "location_input": location_input,
            "location": location_data,
            "regional_ingredients": ingredients,
            "mood": mood,
            "activity_type": activity_type,
            "sleep_hours": sleep_hours
        }

        # Save to single-user session
        st.session_state.user_data = profile

        # Save to multi-user dictionary
        if "user_data_all" not in st.session_state:
            st.session_state["user_data_all"] = {}

        st.session_state["user_data_all"][name] = profile

        save_user_profile(profile)
        st.success("✅ Profile saved successfully!")