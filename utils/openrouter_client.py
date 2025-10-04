import os
import requests
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_chatbot_reply(user_message):
    if not OPENROUTER_API_KEY:
        return "Missing OpenRouter API key. Please check your .env file."

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-3.5-turbo",  # You can swap this with other supported models
        "messages": [{"role": "user", "content": user_message}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"OpenRouter error {response.status_code}: {response.text[:100]}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}"