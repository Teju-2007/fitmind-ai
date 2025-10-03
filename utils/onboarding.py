import streamlit as st
from utils.storage import load_json, PROFILE_PATH

def show_welcome():
    st.title("👋 Welcome to FitMind AI")
    st.caption("Your dynamic, health-aware nutrition companion")

    profiles = load_json(PROFILE_PATH) or []

    if profiles:
        last_user = profiles[-1]
        name = last_user.get("name", "Friend")
        st.success(f"Welcome back, {name}! 🎉")
        st.write("Ready to plan your meals or track your progress?")
    else:
        st.info("Let's get started by setting up your health profile.")
        if st.button("Start Profile Setup"):
            st.session_state.page = "Profile Setup"