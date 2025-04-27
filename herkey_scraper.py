# backend/utils/herkey_scraper.py
import requests
from bs4 import BeautifulSoup
import json
import os

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(data_dir, exist_ok=True)

url = "https://www.herkey.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

programs = soup.find_all('h2', class_='program-title')
mentor_data = [{"name": p.text.strip(), "expertise": "Career Guidance"} for p in programs]

with open(os.path.join(data_dir, "mentors.json"), "w", encoding="utf-8") as f:
    json.dump(mentor_data, f, indent=2)
