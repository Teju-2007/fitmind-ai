import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.storage import save_progress_entry
from utils.nutrition import get_nutritionix_data
from config.health_mapper import load_health_data, match_progress, suggest_meal_if_low

def generate_feedback(df, user_profile):
    if df is None or df.empty:
        return ["No progress data available yet."]

    latest = df.iloc[-1]
    previous = df.iloc[-2] if len(df) > 1 else None
    feedback = []

    # Weight trend
    if previous is not None:
        if latest["weight"] < previous["weight"]:
            feedback.append("🎉 Great job! Your weight is trending down.")
        elif latest["weight"] > previous["weight"]:
            feedback.append("📈 Your weight increased—consider lighter meals or more movement.")

    # Energy trend
    if previous is not None:
        if latest["energy"] > previous["energy"]:
            feedback.append("⚡ You're feeling more energetic—keep up the good nutrition!")
        elif latest["energy"] < previous["energy"]:
            feedback.append("😴 Feeling low? Try iron-rich meals or hydration boosters.")

    # Mood-based suggestion
    if "mood" in latest and isinstance(latest["mood"], str):
        if "low" in latest["mood"].lower():
            feedback.append("💡 Feeling low? Try meals with omega-3s and leafy greens for mental clarity.")

    # Nutrient-based suggestions
    if "nutrition" in latest:
        health_map = {
            "anemia": {"nutrients": ["Iron", "Vitamin B12"]},
            "diabetes": {"nutrients": ["Fiber", "Magnesium"]},
            "hypertension": {"nutrients": ["Potassium", "Omega-3"]},
        }
        for condition in user_profile.get("health_conditions", []):
            needed = health_map.get(condition.lower(), {}).get("nutrients", [])
            for nutrient in needed:
                if nutrient.lower() not in latest.get("nutrition_summary", "").lower():
                    feedback.append(f"🧠 For {condition}, try boosting **{nutrient}** intake.")

    return feedback

def show_progress_tracker():
    st.header("📈 Your Progress Tracker")

    # Multi-user support
    user_data_all = st.session_state.get("user_data_all", {})
    if not user_data_all:
        st.warning("⚠️ No user profiles found. Please complete your profile setup.")
        return

    selected_user = st.selectbox("Select user", list(user_data_all.keys()))
    profile = user_data_all.get(selected_user, {})

    # Fallback defaults to prevent KeyError
    mood = profile.get("mood", "Neutral")
    activity = profile.get("activity_type", "Walking")
    sleep = profile.get("sleep_hours", 7)

    # Load health map dataset
    df_health = load_health_data()
    matches = match_progress(df_health, mood, activity, sleep)
    meal_suggestion = suggest_meal_if_low(mood, sleep)

    # Weekly check-in form
    st.subheader("🗓️ Weekly Check-In")
    with st.form("checkin_form"):
        weight = st.number_input("Current weight (kg)", min_value=30.0, max_value=200.0, step=0.5)
        energy = st.slider("Energy level (1–10)", 1, 10)
        mood_input = st.selectbox("Mood", [
            "😊 Happy", "😐 Neutral", "😞 Low", "😠 Frustrated", "😴 Tired",
            "😕 Anxious", "😇 Calm", "🤯 Overwhelmed", "😎 Confident"
        ])
        meals_input = st.text_input("Meals you had today (comma-separated)")
        submitted = st.form_submit_button("Save Check-In")

    if submitted:
        nutrition_data = get_nutritionix_data(meals_input)
        nutrition_summary = ""
        if isinstance(nutrition_data, list):
            for item in nutrition_data:
                nutrition_summary += (
                    f"• {item['food_name'].title()}: {item['nf_calories']} kcal, "
                    f"{item['nf_protein']}g protein, {item['nf_total_fat']}g fat, "
                    f"{item['nf_total_carbohydrate']}g carbs\n"
                )

        new_entry = {
            "week": pd.Timestamp.now().strftime("%Y-%m-%d"),
            "weight": weight,
            "energy": energy,
            "mood": mood_input,
            "nutrition_summary": nutrition_summary,
            "nutrition": nutrition_data
        }

        st.session_state.setdefault("progress_data", []).append(new_entry)
        save_progress_entry(new_entry)
        st.success("✅ Progress saved!")

    # Show progress charts and feedback
    if st.session_state.get("progress_data"):
        df = pd.DataFrame(st.session_state["progress_data"])

        st.subheader("📊 Weight Over Time")
        if "week" in df.columns and "weight" in df.columns:
            st.line_chart(df.set_index("week")["weight"])

        st.subheader("⚡ Energy Levels")
        if "week" in df.columns and "energy" in df.columns:
            st.bar_chart(df.set_index("week")["energy"])

        st.subheader("🧠 Mood Distribution")
        if "mood" in df.columns:
            mood_counts = df["mood"].value_counts()
            fig, ax = plt.subplots()
            ax.pie(mood_counts, labels=mood_counts.index, autopct="%1.1f%%", startangle=90)
            ax.axis("equal")
            st.pyplot(fig)
        else:
            st.warning("⚠️ No mood data available yet.")

        st.subheader("🍽️ Nutrition Summary")
        if "nutrition_summary" in df.columns:
            for entry in df["nutrition_summary"].dropna():
                st.markdown(entry)

        feedback = generate_feedback(df, profile)
        if feedback:
            st.subheader("🧠 FitMind AI Suggestions")
            for f in feedback:
                st.info(f)

        st.subheader("🍛 Mood-Based Meal Suggestion")
        st.success(meal_suggestion)