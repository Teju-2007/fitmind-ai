import requests

GEONAMES_USERNAME = "tejaveni"  # 🔁 Replace with your actual GeoNames username

def resolve_region(city_name):
    city = city_name.strip()
    url = f"http://api.geonames.org/searchJSON?q={city}&country=IN&maxRows=1&username={GEONAMES_USERNAME}"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        region = data["geonames"][0]["adminName1"]
        return region.strip().lower()
    except (IndexError, KeyError, requests.RequestException):
        print(f"⚠️ Could not resolve region for city: {city}")
        return city.lower()  # fallback to original input