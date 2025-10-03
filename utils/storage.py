import json
import os

# File paths
PROFILE_PATH = "data/user_profiles.json"
PROGRESS_PATH = "data/user_progress.json"
CHAT_LOG_PATH = "data/chat_logs.json"

# --- Profile & Progress Storage ---

def save_user_profile(profile):
    profiles = load_json(PROFILE_PATH)
    profiles.append(profile)
    write_json(PROFILE_PATH, profiles)

def save_progress_entry(entry):
    progress = load_json(PROGRESS_PATH)
    progress.append(entry)
    write_json(PROGRESS_PATH, progress)

# --- Generic JSON Utilities ---

def load_json(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# --- Chat History ---

def save_chat_history(history, filename=CHAT_LOG_PATH):
    write_json(filename, history)

def load_chat_history(filename=CHAT_LOG_PATH):
    return load_json(filename)