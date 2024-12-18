import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv("api.env")

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

# API Key Setup
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY not found. Please check your .env file or environment settings.")
    st.stop()

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Translate roles for Streamlit
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# ChatBot Title
st.title("🤖 Gemini Pro - ChatBot")

# Display Chat History
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input Field
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    if user_prompt.strip() == "":
        st.warning("Input cannot be empty. Please ask a question.")
    else:
        # Display User Message
        st.chat_message("user").markdown(user_prompt)
        
        try:
            # Send and Display Assistant Response
            gemini_response = st.session_state.chat_session.send_message(user_prompt)
            with st.chat_message("assistant"):
                st.markdown(gemini_response.text[:3000])  # Handle large responses
        except Exception as e:
            st.error(f"An error occurred: {e}")
