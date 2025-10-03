import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_weekly_summary():
    st.header("📅 Weekly Summary")

    progress_data = st.session_state.get("progress_data", [])
    if not progress_data:
        st.warning("No progress data yet. Check in at least once to see your summary.")
        return

    df = pd.DataFrame(progress_data)
    df["week"] = pd.to_datetime(df["week"])
    recent = df[df["week"] >= pd.Timestamp.now() - pd.Timedelta(days=7)]

    if recent.empty:
        st.info("No check-ins this week. Start tracking to see your summary.")
        return

    # 📊 Weight & Energy Trends
    st.subheader("📊 Weight & Energy Trends")
    st.line_chart(recent.set_index("week")[["weight", "energy"]])

    # 🧠 Mood Overview
    st.subheader("🧠 Mood Overview")
    mood_counts = recent["mood"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(mood_counts, labels=mood_counts.index, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

    # 💡 FitMind AI Suggestions
    st.subheader("💡 FitMind AI Suggestions")
    suggestions = []

    if recent["energy"].mean() < 5:
        suggestions.append("⚡ Your energy levels are low—try iron-rich meals like Palak Dal or Red Rice Fish Curry.")
    if any("low" in mood.lower() for mood in recent["mood"]):
        suggestions.append("🧘 Feeling low? Omega-3 meals like Turnip Mutton Stew or Paneer Salad may help uplift your mood.")
    if recent["weight"].iloc[-1] > recent["weight"].iloc[0]:
        suggestions.append("📉 Weight increased—consider lighter meals like Poha Bowl or Spinach Yogurt Dip.")

    if suggestions:
        for tip in suggestions:
            st.info(tip)
    else:
        st.success("🎉 You're on track! Keep up the great work.")