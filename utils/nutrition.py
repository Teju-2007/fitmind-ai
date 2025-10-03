import os
import requests
from dotenv import load_dotenv

load_dotenv()
APP_ID = os.getenv("NUTRITIONIX_APP_ID")
APP_KEY = os.getenv("NUTRITIONIX_APP_KEY")

def get_nutritionix_data(query):
    if not APP_ID or not APP_KEY:
        return {"error": "Missing Nutritionix API credentials. Check your .env file."}

    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": APP_ID,
        "x-app-key": APP_KEY,
        "Content-Type": "application/json"
    }
    payload = {"query": query}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        if response.status_code == 200:
            return response.json().get("foods", [])
        else:
            return {"error": f"Nutritionix error {response.status_code}: {response.text[:100]}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}