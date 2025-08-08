# frontend.py
import streamlit as st
import requests

st.set_page_config(page_title="Zeeshu AI Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 Zeeshu AI")

if "messages" not in st.session_state:
    st.session_state.messages = []
# Input field
user_input = st.text_input("You:", placeholder="Type your message here...")

# Send button
if st.button("Send"):
    if user_input.strip():
        try:
            # Send request to backend API
            res = requests.post(
                "https://chatbot-backend-wro1.onrender.com/chat/",  # Your FastAPI backend endpoint
                json={"message": user_input}
            )

            if res.status_code == 200:
                data = res.json()
                bot_reply = data.get("Zeeshu AI", "No reply from bot")
                st.session_state.messages.append(("You", user_input))
                st.session_state.messages.append(("Zeeshu AI", bot_reply))
            else:
                st.error(f"Error {res.status_code}: {res.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")

# Display chat history
for sender, text in st.session_state.messages:
    st.markdown(f"**{sender}:** {text}")