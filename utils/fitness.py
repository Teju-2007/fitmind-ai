# fitness.py
import streamlit as st
import json
import random
from utils.profile import get_user_fitness_preferences 

@st.cache_data
def load_exercises():
        with open("exercises.json", "r") as f:
            return json.load(f)


def show_fitness_dashboard():
    # Load and cache data
    exercises = load_exercises()

    # Get user preferences from profile
    prefs = get_user_fitness_preferences()
    default_body_part = prefs["body_part"]
    default_equipment = prefs["equipment"]
    goal = prefs["goal"]

    # Sidebar filters (can override profile defaults)
    st.sidebar.title("🔍 Filter Exercises")
    body_parts = sorted(set(e["body_part"] for e in exercises))
    equipment_types = sorted(set(e["equipment"] for e in exercises))

    selected_body_part = st.sidebar.selectbox("Body Part", ["All"] + body_parts, index=(body_parts.index(default_body_part) + 1 if default_body_part in body_parts else 0))
    selected_equipment = st.sidebar.selectbox("Equipment", ["All"] + equipment_types, index=(equipment_types.index(default_equipment) + 1 if default_equipment in equipment_types else 0))

    # Filter logic
    def filter_exercises(body_part, equipment):
        filtered = exercises
        if body_part != "All":
            filtered = [e for e in filtered if e["body_part"].lower() == body_part.lower()]
        if equipment != "All":
            filtered = [e for e in filtered if e["equipment"].lower() == equipment.lower()]
        return filtered

    filtered_exercises = filter_exercises(selected_body_part, selected_equipment)

    # Main UI
    st.title("🏋️ FitMind AI: Personalized Exercise Dashboard")
    st.write(f"**Goal:** {goal} | **Focus:** {selected_body_part} | **Equipment:** {selected_equipment}")
    st.write(f"Showing {len(filtered_exercises)} exercises")

    for ex in filtered_exercises:
        st.subheader(ex["name"])
        st.image(ex["gif_url"], width=300)
        st.write(f"**Target Muscle:** {ex['target']}")
        st.write(f"**Equipment:** {ex['equipment']}")
        st.write("---")

    # Workout of the Day
    st.sidebar.markdown("---")
    st.sidebar.title("🎯 Personalized Workout of the Day")
    if st.sidebar.button("Generate"):
        wod = random.sample(filtered_exercises, min(5, len(filtered_exercises)))
        st.sidebar.markdown("Here’s your suggested workout:")
        for i, ex in enumerate(wod, 1):
            st.sidebar.write(f"{i}. {ex['name']} ({ex['body_part']})")