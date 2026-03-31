import requests
import pandas as pd
from urllib.parse import urljoin
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

SHOPNAME = os.getenv("SHOPNAME")
PASSWORD = os.getenv("PASSWORD")
BASE_URL = os.getenv("BASE_URL")

# 🔹 Configuration
LOGIN_URL = f"{BASE_URL}/login.jsp"

# 🔹 1. LOGIN
session = requests.Session()

login_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

login_payload = {
    "username": SHOPNAME,
    "password": PASSWORD
}
login_response = session.post(LOGIN_URL, json=login_payload, headers=login_headers)

# Vérification
if login_response.status_code != 200:
    print("❌ Erreur login :", login_response.status_code)
    print(login_response.text)
    exit()

print("✅ Login réussi")

# 🔹 2. Récupération des cookies
cookies = session.cookies.get_dict()

jsessionid = cookies.get("JSESSIONID")

print("JSESSIONID:",jsessionid)


