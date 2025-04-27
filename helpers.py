# backend/utils/helpers.py

import json
import csv
import os
import difflib

def load_herkey_data():
    with open("data/herkey.json", "r", encoding="utf-8") as f:
        return json.load(f)

def search_herkey_content(query, data):
    matches = []
    for item in data:
        text = item.get("title", "") + " " + item.get("description", "")
        if difflib.SequenceMatcher(None, query.lower(), text.lower()).ratio() > 0.4:
            matches.append(text)
    return matches[:5]

def load_job_listings(path="data/job_listings.csv"):
    if not os.path.exists(path):
        return []
    with open(path, encoding='utf-8') as f:
        return list(csv.DictReader(f))

def load_session_details(path="data/session_details.json"):
    if not os.path.exists(path):
        return []
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def load_faqs(path="data/faqs.json"):
    if not os.path.exists(path):
        return []
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def load_mentors(path="data/mentors.json"):
    if not os.path.exists(path):
        return []
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def search_job_listings(query, data):
    return [item for item in data if query.lower() in item['title'].lower()][:3]

def search_sessions(query, data):
    return [item for item in data if query.lower() in item['title'].lower()][:3]

def search_faqs(query, data):
    return [item for item in data if query.lower() in item['question'].lower()][:1]

def search_mentors(query, data):
    return [item for item in data if query.lower() in item['expertise'].lower()][:3]

def filter_response_for_bias(response_text):
    biased_terms = ["only men", "typically male", "not suitable for women"]
    for term in biased_terms:
        if term in response_text.lower():
            return "I'm designed to provide inclusive advice. Let's focus on opportunities for everyone. 😊"
    return response_text
