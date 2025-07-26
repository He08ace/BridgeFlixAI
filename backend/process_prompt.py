# backend/process_prompt.py

from openai import OpenAI

# Initialize the OpenAI client (uses environment variable if key is set)
client = OpenAI()

def generate_scene_data(prompt, characters=None):
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
            {"role": "user", "content": prompt}
        ]
    )

    reply = enriched_prompt.choices[0].message.content
    return reply
