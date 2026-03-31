import requests
import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
SHOPNAME = os.getenv("SHOPNAME")
PASSWORD = os.getenv("PASSWORD")

session = requests.Session()

# 1. LOGIN
login_url = "https://v1.cathedis.delivery/callback"

login_payload = {
    "username": SHOPNAME,
    "password": PASSWORD
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

login_response = session.post(login_url, data=login_payload, headers=headers)

print("Login status:", login_response.status_code)
print("Cookies:", session.cookies.get_dict())


# 2. APPEL API AVEC PAGINATION
url = "https://v1.cathedis.delivery/ws/action"

headers = {
    "Content-Type": "application/json"
}

LIMIT = 40
offset = 0
all_responses = []

while True:
    payload = {
        "action": "delivery.api.my",
        "data": {
            "context": {
                "limit": LIMIT,
                "offset": offset
            }
        }
    }

    response = session.post(url, json=payload, headers=headers)

    print(f"Status (offset={offset}):", response.status_code)
    print("Response:", response.text)

    result = response.json()
    all_responses.append(result)

    # Si la réponse est une liste
    if isinstance(result, list):
        if len(result) < LIMIT:
            break
    # Si la réponse est un dict avec une clé contenant les données
    elif isinstance(result, dict):
        # Cherche la première valeur qui est une liste
        data_list = next((v for v in result.values() if isinstance(v, list)), None)
        if data_list is None or len(data_list) < LIMIT:
            break
    else:
        break

    offset += LIMIT

print(f"\nTotal pages récupérées : {len(all_responses)}")