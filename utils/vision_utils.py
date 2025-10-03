from PIL import Image
import pytesseract

def extract_text_from_image(img_file):
    image = Image.open(img_file)
    return pytesseract.image_to_string(image).strip()

def get_nutrition_summary(text):
    from utils.nutrition import get_nutritionix_data
    return get_nutritionix_data(text)

def check_health_safety(nutrition, user_profile):
    issues = []
    conditions = user_profile.get("health_conditions", [])
    for item in nutrition:
        if "diabetes" in conditions and item.get("nf_sugars", 0) > 10:
            issues.append(f"{item['food_name']} has high sugar")
        if "hypertension" in conditions and item.get("nf_sodium", 0) > 500:
            issues.append(f"{item['food_name']} has high sodium")
    return issues

def generate_chatbot_prompt(text, issues, nutrition):
    if issues:
        return f"I scanned {text}. Nutrition data shows risks: {', '.join(issues)}. What should I do?"
    else:
        return f"I scanned {text}. Nutrition looks safe. Can you suggest a recipe or usage?"