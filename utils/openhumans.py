import requests

def fetch_public_data():
    url = "https://www.openhumans.org/api/public-data/"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            print(f"OpenHumans error: {response.status_code} — {response.text[:100]}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

def get_mood_logs():
    data = fetch_public_data()
    return [entry for entry in data if "mood" in entry.get("metadata", {}).get("tags", [])]

def get_sleep_logs():
    data = fetch_public_data()
    return [entry for entry in data if "sleep" in entry.get("metadata", {}).get("tags", [])]