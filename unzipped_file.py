import pandas as pd
import json

# Load the CSV file
df = pd.read_csv("fitness_exercises.csv")  # Make sure the filename matches

# Select and rename relevant columns
df_clean = df[["name", "bodyPart", "equipment", "target", "gifUrl"]].copy()
df_clean.columns = ["name", "body_part", "equipment", "target", "gif_url"]

# Fill missing values
df_clean.fillna("N/A", inplace=True)

# Convert to list of dictionaries
exercise_list = df_clean.to_dict(orient="records")

# Save to JSON
with open("exercises.json", "w") as f:
    json.dump(exercise_list, f, indent=2)

print(f"✅ Saved {len(exercise_list)} exercises to exercises.json")