import json
from google.cloud import dialogflowcx_v3beta1 as dialogflow
from google.oauth2 import service_account
import os

PROJECT_ID = "your-project-id"
LOCATION = "global"  # or your agent’s region like "us-central1"
AGENT_ID = "your-agent-id"
SESSION_ID = "user-session-id"  # Generate dynamically per session

CREDENTIALS_PATH = "dialogflow_key.json"
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)

def detect_intent_text(user_input):
    client = dialogflow.SessionsClient(credentials=credentials)
    session_path = client.session_path(PROJECT_ID, LOCATION, AGENT_ID, SESSION_ID)

    text_input = dialogflow.TextInput(text=user_input)
    query_input = dialogflow.QueryInput(text=text_input, language_code="en")

    response = client.detect_intent(session=session_path, query_input=query_input)
    return response.query_result.response_messages[0].text.text[0]
