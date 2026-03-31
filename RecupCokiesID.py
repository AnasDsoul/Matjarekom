import requests

session = requests.Session()

# 1. LOGIN
login_url = "https://v1.cathedis.delivery/callback"

login_payload = {
    "username": "Matjarekom",
    "password": "C4z78uvH"
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

login_response = session.post(login_url, data=login_payload, headers=headers)

print("Login status:", login_response.status_code)
print("Cookies:", session.cookies.get_dict())


# 2. APPEL API
url = "https://v1.cathedis.delivery/ws/action"

payload = {
    "action": "delivery.api.my",
    "data": {
        "context": {
            "limit": 40,
            "offset": 0
        }
    }
}

headers = {
    "Content-Type": "application/json"
}

response = session.post(url, json=payload, headers=headers)

print("Status:", response.status_code)
print("Response:", response.text)