from collections import defaultdict
from config.region_resolver import resolve_region
from utils.grocery import fetch_local_recipes

def aggregate_grocery(meal_plan):
    grocery_list = defaultdict(lambda: {"quantity": "", "cost": 0})
    for meal in meal_plan:
        for ingredient in meal.get("ingredients", []):
            grocery_list[ingredient]["quantity"] = "1 unit"
            grocery_list[ingredient]["cost"] += 10  # Dummy cost
    return dict(grocery_list)

def score_alignment(meal, liked_tags):
    tags = []
    for ing in meal.get("ingredients", []):
        tags.extend(ing.lower().split())
    return sum(tag in liked_tags for tag in tags)

def recommend_meals(user_profile):
    region = resolve_region(user_profile.get("region", "") or user_profile.get("location_input", ""))
    user_profile["region"] = region
    user_profile["goal"] = user_profile.get("goal", "balanced")
    user_profile["budget"] = user_profile.get("budget", 120)
    user_profile["health_conditions"] = user_profile.get("health_conditions", ["none"])
    user_profile["diet_type"] = user_profile.get("diet_type", "vegetarian")
    liked_tags = user_profile.get("liked_tags", [])

    print(f"🔍 Normalized region: {region}")

    # 🔍 Try local dataset first
    local_matches = fetch_local_recipes(region, user_profile["goal"])
    if local_matches:
        best = local_matches[0]
        meal_plan = best.get("meal_plan", [])
        for meal in meal_plan:
            meal["alignment_score"] = score_alignment(meal, liked_tags)

        top_meals = sorted(meal_plan, key=lambda x: x["alignment_score"], reverse=True)[:5]
        grocery_list = aggregate_grocery(top_meals)
        total_cost = sum(item["cost"] for item in grocery_list.values())

        return {
            "message": "Personalized meal plan from local dataset.",
            "meal_plan": top_meals,
            "grocery_list": grocery_list,
            "total_cost": total_cost,
            "source": "local"
        }
