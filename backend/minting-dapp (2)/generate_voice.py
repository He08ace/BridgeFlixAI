import requests
import os
import hashlib

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def synthesize_dialogue(text, character_id, stability=0.5, similarity_boost=0.75):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{character_id}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        voice_hash = hashlib.md5(text.encode()).hexdigest()
        filename = f"voice_{character_id}_{voice_hash}.mp3"
        with open(filename, "wb") as f:
            f.write(response.content)
        return filename
    else:
        print("Failed to synthesize speech:", response.text)
        return None
