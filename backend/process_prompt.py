import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_scene_data(prompt, characters=None):
    # Step 1: If no characters provided, generate them using GPT
    if not characters:
        character_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a character development expert. Based on the given prompt, generate 3 unique fictional characters. "
                        "For each character, provide: name, age, appearance, background, personality."
                    )
                },
                {"role": "user", "content": prompt}
            ]
        )
        character_data = character_response.choices[0].message.content
        characters = character_data

    # Step 2: Generate the scene using the prompt + characters
    enriched_prompt = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a screenwriter. Return the response in JSON format. "
                    "Describe a vivid scene including location, action, mood, and character dialogue."
                ),
            },
            {"role": "user", "content": f"Prompt: {prompt}\nCharacters: {characters}"}
        ]
    )

    return enriched_prompt.choices[0].message.content
