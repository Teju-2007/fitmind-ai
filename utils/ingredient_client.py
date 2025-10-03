import requests

def get_local_ingredients(country):
    url = f"https://world.openfoodfacts.org/country/{country.lower()}.json"

    try:
        response = requests.get(url, timeout=5)
        if response.ok and response.headers.get("Content-Type", "").startswith("application/json"):
            products = response.json().get("products", [])
            return list({p["product_name"].lower() for p in products if "product_name" in p})
        else:
            print(f"OpenFoodFacts error: {response.status_code} — {response.text[:100]}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []