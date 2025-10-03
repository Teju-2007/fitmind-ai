import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
SPOONACULAR_KEY = os.getenv("SPOONACULAR_KEY")

# 🔍 Fetch recipes from Spoonacular API
def fetch_recipes(query, number=5):
    if not SPOONACULAR_KEY:
        return {"error": "Missing Spoonacular API key. Check your .env file."}

    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "query": query,
        "number": number,
        "addRecipeInformation": True
    }
    headers = {
        "x-api-key": SPOONACULAR_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("results", [])
        else:
            return {"error": f"{response.status_code} — {response.text[:100]}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

# 🔍 Fetch region-aware recipes from local dataset
def fetch_local_recipes(region, health_keywords):
    try:
        with open("data/meals.json", "r", encoding="utf-8") as f:
            meals = json.load(f)

        region = region.lower().strip()
        keywords = health_keywords.lower().strip().split()
        filtered = []

        for meal in meals:
            meal_region = meal.get("region", "").lower()
            meal_tags = [tag.lower() for tag in meal.get("goal_tags", [])]

            if region in meal_region and any(tag in meal_tags for tag in keywords):
                filtered.append(meal)

        return filtered
    except Exception as e:
        print("❌ Error loading local meals:", e)
        return []