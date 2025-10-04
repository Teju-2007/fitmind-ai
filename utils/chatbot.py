import streamlit as st
from utils.openrouter_client import get_chatbot_reply

# 🌟 Initialize chat history 


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def show_chatbot():
    if "proxy" not in st.session_state:
        st.session_state.proxy = None
        
    if "chatbot_state" not in st.session_state:
        st.session_state.chatbot_state = {}

    if "messages" not in st.session_state:
        st.session_state.messages = []
    st.title("💬 FitMind AI Chatbot")

    # 👤 Load user profile
    user_data_all = st.session_state.get("user_data_all", {})
    if not user_data_all:
        st.warning("⚠️ No user profiles found. Please complete your profile setup.")
        st.stop()

    selected_user = st.selectbox("🧑 Select user profile", list(user_data_all.keys()))
    user_profile = user_data_all.get(selected_user, {})

    # 🗂️ Display chat history
    st.subheader("📜 Conversation History")
    for sender, message in st.session_state.chat_history:
        if sender.startswith("You"):
            st.markdown(f"<div style='color:#1f77b4'><b>🧑 {sender}:</b> {message}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color:#2ca02c'><b>🤖 {sender}:</b> {message}</div>", unsafe_allow_html=True)

    if st.button("🧹 Clear Chat History"):
        st.session_state.chat_history = []
        st.success("Chat history cleared.")

    st.markdown("---")

    # 💬 Chat input
    st.subheader("📝 Ask FitMind AI")
    user_input = st.text_input("Type your question or request:")
    if st.button("📤 Send"):
        if user_input.strip():
            response = get_chatbot_reply(user_input)
            st.markdown("🤖 **Response:**")
            st.markdown(response)

            # Save to history
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("FitMind AI", response))
        else:
            st.warning("⚠️ Please enter a message before sending.")