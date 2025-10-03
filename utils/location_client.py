import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEODB_API_KEY")

def normalize_location(location_name):
    if not api_key:
        print("Missing GEODB_API_KEY in .env")
        return None

    url = f"https://wft-geo-db.p.rapidapi.com/v1/geo/cities?namePrefix={location_name}"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.ok:
            data = response.json()
            if data.get("data"):
                city = data["data"][0]
                return {
                    "city": city["city"],
                    "country": city["country"],
                    "region": city.get("region"),
                    "latitude": city["latitude"],
                    "longitude": city["longitude"]
                }
            else:
                print("No matching city found.")
        else:
            print(f"GeoDB error: {response.status_code} — {response.text[:100]}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    return None