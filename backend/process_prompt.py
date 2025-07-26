from backend.character_db import match_characters
import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def generate_scene_data(prompt, character_db):
    matched_characters = match_characters(prompt, character_db)

    # Build character context
    character_descriptions = []
    for data in matched_characters.values():
        personality = data["metadata"].get("personality", "")
        backstory = data["metadata"].get("backstory", "")
        style = data["metadata"].get("style", "")
        char_summary = f"{data['name'].split('.')[0]} is {personality}. {backstory} Speaks like: {style}"
        character_descriptions.append(char_summary)

    system_message = (
        "You are a screenwriter assistant. Break prompts into structured scenes. "
        "Output a JSON list of shots with keys: character, dialogue, action, location, mood."
    )

    user_prompt = f"""
    Prompt: "{prompt}"

    Characters:
    {chr(10).join(character_descriptions)}

    Return JSON like:
    [
      {{
        "character": "Alex",
        "dialogue": "Let's get out of here!",
        "action": "Alex grabs the bag and runs.",
        "location": "Abandoned warehouse",
        "mood": "tense"
      }}
    ]
    """

    enriched_prompt = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ]
    )

    content = enriched_prompt.choices[0].message.content

    log_path = os.path.join(LOG_DIR, f"scene_log_{hash(prompt)}.json")
    with open(log_path, "w") as f:
        json.dump({"original": prompt, "enriched": content}, f, indent=2)

    try:
        shot_data = json.loads(content)
    except json.JSONDecodeError:
        print("Failed to parse GPT JSON. Content was:")
        print(content)
        return None

    scene_data = {
        "prompt": prompt,
        "characters": matched_characters,
        "shots": shot_data
    }
    return scene_data
# process_prompt.py logic placeholder
