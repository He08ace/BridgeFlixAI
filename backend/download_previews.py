import requests
import os

ELEVEN_API_KEY = "sk_d58c4c8cf3e18fece726e6664db6f9efae76ed2de3cb893c"

voice_ids = [
    "h2sm0NbeIZXHBzJOMYcQ", "9wYX8b0wRvLUEYtGuzP5", "ewxUvnyvvOehYjKjUVKC",
    "rujGCruvEqncqHTi6l0q", "rdDUoCO1RjwdMmNjmhHV", "6OzrBCQf8cjERkYgzSg8",
    "NySnOmeQIeaUH8egRnrQ", "Z5JpFCNFIz8Nhe4KEikq", "gYr8yTP0q4RkX1HnzQfX",
    "6aDn1KB0hjpdcocrUkmq", "rWyjfFeMZ6PxkHqD3wGC", "xkDz8dF9GIt1kG06c9Of",
    "CVRACyqNcQefTlxMj9bt", "gKDyLTHvXI2M1dVbbuuE", "pGuQKOUQJTbKXVCJWAqL",
    "85DL3i4Z7PIWbcOYSlQl", "FGlwXbxtvHyuRiEubkZg", "4ruSPR79OgfZINYizp0U",
    "zWoalRDt5TZrmW4ROIA7", "2qfp6zPuviqeCOZIE9RZ"
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
