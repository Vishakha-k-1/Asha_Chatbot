# backend/memory.py
import google.generativeai as genai

def get_chat_model():
    return genai.GenerativeModel("gemini-1.5-pro").start_chat(history=[])
