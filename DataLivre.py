import requests
import os
import json
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd

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

# 2. APPEL API AVEC PAGINATION
url = "https://v1.cathedis.delivery/ws/action"

headers = {
    "Content-Type": "application/json"
}

LIMIT = 1000
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
allProduct = []
for d in all_responses:

    Data = d["data"]

    for Dat in Data:
        all_data = Dat["values"]["deliveries"]
        for l in all_data:
            row = {"city":l["city"],"subject":l["subject"],"returnStatus":l["returnStatus"],
            "createdOn": l["createdOn"],
            "id": l["id"],
            "amount": l["amount"],
            "address": l["address"],"deliveryStatusType": l["deliveryStatusType"],"phone": l["phone"],
            "recipient": l["recipient"],"deliveryStatus": l["deliveryStatus"],"status":l["status"]}
            allProduct.append(row)

df = pd.DataFrame(allProduct)

df.to_excel(
    r"C:\Users\Anas\Desktop\MatjarEkom\Matjarekom.xlsx",
    index=False,
    engine="openpyxl"
)

print("Done — fichier généré.")