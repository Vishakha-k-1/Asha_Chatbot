import streamlit as st

def style_app_ui():
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #fff5f8;
            font-family: 'Segoe UI', sans-serif;
            color: #3b0764;
        }
        .stTextInput > div > div > input {
            background-color: #ffffff;
            border: 2px solid #e879f9;
            border-radius: 10px;
            padding: 0.75rem;
        }
        .stChatInputContainer {
            background-color: #fce7f3;
            padding: 10px;
            border-radius: 12px;
        }
        h1, h2, h3 {
            color: #6b21a8;
        }
        .stButton > button {
            background-color: #9333ea;
            color: white;
            font-weight: bold;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h3 style='color:#6b21a8;'>Empowering Women Through Career Conversations ✨</h3>", unsafe_allow_html=True)