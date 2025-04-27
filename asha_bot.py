# backend/asha_bot.py

import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

from utils.dialogflow_handler import detect_intent_text
from utils.helpers import (
    load_job_listings,
    load_session_details,
    load_faqs,
    load_mentors,
    search_job_listings,
    search_sessions,
    search_faqs,
    search_mentors,
    filter_response_for_bias
)
from utils.rag_handler import generate_rag_response

# ✅ MUST be first
st.set_page_config(page_title="Asha - Career Chatbot", page_icon="👩‍🏫")

# ✅ Title
st.title("👩‍🏫 Asha - Your Career Companion powered by HerKey")

# ✅ Load Environment
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-pro")

# ✅ Load Data
job_data = load_job_listings()
session_data = load_session_details()
faq_data = load_faqs()
mentors_data = load_mentors()

# ✅ Session states
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "cohort" not in st.session_state:
    st.session_state.cohort = None
if "user_name" not in st.session_state:
    st.session_state.user_name = st.text_input("Your name", placeholder="Enter your name")
if "user_gender" not in st.session_state:
    st.session_state.user_gender = st.radio("Gender", ["Prefer not to say", "Female", "Male"])
if "career_interest" not in st.session_state:
    st.session_state.career_interest = None

# ✅ Generate Response
def generate_response(prompt):
    if "your name" in prompt.lower() or "who are you" in prompt.lower() or "what's your name" in prompt.lower():
        return "👩‍🏫 I'm Asha, your career companion powered by HerKey! I'm here to guide and support you on your professional journey. 🚀"

    if "password" in prompt.lower():
        return (
            "🚨 It's extremely important not to share your passwords. "
            "Please change it immediately and use something strong!"
        )

    if any(kw in prompt.lower() for kw in ["career in", "want to become", "interested in"]):
        st.session_state.career_interest = prompt
        return "🌟 Thanks! I've saved your career interest. Let's explore opportunities together!"

    if st.session_state.career_interest and "career" in prompt.lower():
        return f"Earlier you mentioned: *{st.session_state.career_interest}*. Have you taken any steps toward it?"

    if "navigate herkey" in prompt.lower() or "career advice" in prompt.lower() or "herkey" in prompt.lower():
        return generate_rag_response(prompt)

    if st.session_state.cohort:
        prompt = f"You are chatting with a woman categorized as a {st.session_state.cohort}. Help her with:\n{prompt}"

    if "job" in prompt.lower():
        results = search_job_listings(prompt, job_data)
        if results:
            return "💼 Here are some job listings:\n" + "\n".join([f"- {job['title']} in {job['location']}" for job in results])

    if "session" in prompt.lower() or "event" in prompt.lower():
        results = search_sessions(prompt, session_data)
        if results:
            return "📅 Upcoming sessions:\n" + "\n".join([f"- {s['title']} on {s['date']}" for s in results])

    if "faq" in prompt.lower() or "how" in prompt.lower():
        results = search_faqs(prompt, faq_data)
        if results:
            return results[0]['answer']

    if "mentor" in prompt.lower():
        results = search_mentors(prompt, mentors_data)
        if results:
            return "🤝 Potential mentors:\n" + "\n".join([f"- {m['name']} ({m['expertise']})" for m in results])

    try:
        rag_response = detect_intent_text(prompt)
        if rag_response:
            return rag_response
    except Exception as e:
        print("Dialogflow fallback error:", e)

    # Fallback to Gemini LLM
    try:
        gemini_response = model.generate_content(prompt)
        return filter_response_for_bias(gemini_response.text)
    except Exception as e:
        print("Gemini fallback error:", e)
        return "Sorry, I'm facing a technical difficulty. Please try again!"

# ✅ Show Chat Input Box (BOTTOM)
user_input = st.chat_input("Ask me anything about jobs, careers, mentorship...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    if any(cohort in user_input.lower() for cohort in ["starter", "restarter", "riser"]):
        st.session_state.cohort = user_input.lower().strip()
        reply = f"Thanks! I've saved you're a {st.session_state.cohort}. Let's make your journey awesome! 🎯"
    else:
        reply = generate_response(user_input)

    st.session_state.chat_history.append(("asha", reply))

# ✅ Display Chat History
for role, message in st.session_state.chat_history:
    with st.chat_message("user" if role == "user" else "assistant"):
        st.markdown(message)
