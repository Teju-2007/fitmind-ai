import pandas as pd
import streamlit as st

def load_health_data(csv_path="data/fitness_health_tracking.csv"):
    try:
        df = pd.read_csv(csv_path)

        # Ensure required columns exist
        required_columns = ["mood", "activity_type", "sleep_hours", "meal_suggestion"]
        for col in required_columns:
            if col not in df.columns:
                st.error(f"⚠️ Missing column '{col}' in health tracking dataset.")
                return pd.DataFrame()

        return df
    except Exception as e:
        st.error(f"⚠️ Error loading health data: {e}")
        return pd.DataFrame()

def match_progress(df, mood, activity_type, sleep_hours):
    if df.empty:
        return []

    # Normalize inputs
    mood = str(mood).strip().lower()
    activity_type = str(activity_type).strip().lower()

    # Filter by mood and activity
    matches = df[
        (df["mood"].str.lower() == mood) &
        (df["activity_type"].str.lower() == activity_type)
    ]

    # Optional: filter by sleep range
    if "sleep_hours" in df.columns:
        matches = matches[
            matches["sleep_hours"].apply(lambda x: abs(float(x) - float(sleep_hours)) <= 1)
        ]

    return matches.to_dict(orient="records")

def suggest_meal_if_low(mood, sleep_hours):
    df = load_health_data()
    if df.empty:
        return "Try a balanced meal with greens and protein."

    matches = match_progress(df, mood, "walking", sleep_hours)  # fallback to walking
    if matches:
        return matches[0].get("meal_suggestion", "Try a balanced meal with greens and protein.")
    return "Try a balanced meal with greens and protein."