import requests
import os

ELEVEN_API_KEY = "sk_c08a7983b49a092b308bcc595d84f17ae0ff3ff5527525db"

voice_ids = [
    "h2sm0NbeIZXHBzJOMYcQ", "9wYX8b0wRvLUEYtGuzP5", "ewxUvnyvvOehYjKjUVKC"
]

sample_text = "Welcome to BridgeFlix AI. Your voice has power."

headers = {
    "xi-api-key": ELEVEN_API_KEY,
    "Content-Type": "application/json"
}

os.makedirs("voice_previews", exist_ok=True)

for i, vid in enumerate(voice_ids):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{vid}"
    payload = {
        "text": sample_text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        filename = f"voice_previews/voice_{i+1}.mp3"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Saved {filename}")
    else:
        print(f"❌ Error with Voice ID {vid}: {response.status_code} - {response.text}")
