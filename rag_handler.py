# backend/utils/rag_handler.py

from vertexai.preview.generative_models import GenerativeModel
import vertexai
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION = "us-central1"  # ✅ Use supported region!

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

def generate_rag_response(prompt):
    model = GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(
        f"Based on the career guidance and HerKey resources, answer this:\n{prompt}"
    )
    return response.text
