import os
import requests
from dotenv import load_dotenv

load_dotenv()
CALORIE_NINJAS_KEY = os.getenv("CALORIE_NINJAS_KEY")

def get_nutrition_data(ingredient):
    if not CALORIE_NINJAS_KEY:
        return {"error": "Missing CalorieNinjas API key"}

    url = f"https://api.calorieninjas.com/v1/nutrition?query={ingredient}"
    headers = {"X-Api-Key": CALORIE_NINJAS_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("items"):
                return data["items"][0]
            else:
                return {"error": f"No nutrition data found for '{ingredient}'"}
        else:
            return {"error": f"API error: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}