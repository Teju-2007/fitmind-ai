import streamlit as st
from utils.health_map import health_map  # ✅ Import the actual dictionary, not the module
from config.ingredient_tags import ingredient_tags
from utils.nutrition import get_nutritionix_data
from utils.openrouter_client import get_chatbot_reply

def generate_recipe(ingredients, goal, budget):
    matched_tags = []
    for ing in ingredients:
        tags = ingredient_tags.get(ing.strip().lower(), [])
        matched_tags.extend(tags)

    # ✅ Safely access goal tags
    goal_tags = health_map.get(goal.lower(), {}).get("nutrients", [])
    relevant = [tag for tag in matched_tags if tag in goal_tags]

    name = f"{goal.title()} Bowl with " + ", ".join(ingredients[:2])
    explanation = (
        f"This recipe supports your goal of **{goal}** with ingredients rich in: "
        f"{', '.join(relevant) if relevant else 'general nutrients'}."
    )

    return {
        "name": name,
        "ingredients": ingredients,
        "nutrition_tags": relevant,
        "estimated_cost": budget // 10,
        "explanation": explanation
    }

def show_recipe_generator():
    st.header("🍳 AI Recipe Generator")

    ingredients_input = st.text_input("🧂 Enter ingredients (comma-separated):")
    style = st.selectbox("🎨 Choose a style", [
        "Indian", "Mediterranean", "Vegan", "High-Protein", "Low-Carb"
    ])
    goal = st.text_input("🎯 Health Goal (e.g. anemia, weight loss, PCOS)")
    budget = st.number_input("💰 Estimated Budget (₹)", min_value=100, max_value=5000, step=50)

    if st.button("Generate Recipe"):
        if not ingredients_input.strip():
            st.warning("Please enter at least one ingredient.")
            return

        ingredients = [i.strip().lower() for i in ingredients_input.split(",") if i.strip()]
        if not ingredients:
            st.warning("No valid ingredients found.")
            return

        recipe_data = generate_recipe(ingredients, goal, budget)

        # Display structured recipe
        st.subheader(f"🧠 {recipe_data['name']}")
        st.markdown(recipe_data["explanation"])
        st.write(f"💸 Estimated Cost: ₹{recipe_data['estimated_cost']}")
        st.write("🧾 Ingredients:", ", ".join(recipe_data["ingredients"]))

        # AI-enhanced recipe steps
        prompt = (
            f"Create a {style} recipe using: {', '.join(ingredients)}. "
            f"Make it suitable for {goal}. Include steps, cooking time, and a short summary."
        )
        ai_recipe = get_chatbot_reply(prompt)
        st.markdown("### 📝 AI-Generated Instructions")
        st.markdown(ai_recipe)

        # Nutrition analysis using Nutritionix
        st.subheader("🧮 Nutrition Breakdown")
        nutrition = get_nutritionix_data(", ".join(ingredients))
        if isinstance(nutrition, list) and nutrition:
            for item in nutrition:
                st.markdown(
                    f"**{item['food_name'].title()}**: {item['nf_calories']} kcal, "
                    f"{item['nf_protein']}g protein, {item['nf_total_fat']}g fat, "
                    f"{item['nf_total_carbohydrate']}g carbs"
                )
        elif isinstance(nutrition, dict) and "error" in nutrition:
            st.error(f"Nutrition API Error: {nutrition['error']}")
        else:
            st.warning("No nutrition data found for the given ingredients.")

def show_nutrition_summary(ingredient):
    st.header("🔍 Nutrition Summary")
    nutrition = get_nutritionix_data(ingredient)
    if isinstance(nutrition, list) and nutrition:
        item = nutrition[0]
        st.markdown(f"🍽️ **{item['food_name'].title()}**")
        st.write(f"Calories: {item['nf_calories']} kcal")
        st.write(f"Protein: {item['nf_protein']} g")
        st.write(f"Fat: {item['nf_total_fat']} g")
        st.write(f"Carbs: {item['nf_total_carbohydrate']} g")
        st.write(f"Sugar: {item.get('nf_sugars', 'N/A')} g")
    elif isinstance(nutrition, dict) and "error" in nutrition:
        st.error(nutrition["error"])
    else:
        st.warning("No nutrition data found.")