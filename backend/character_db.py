from PIL import Image
from io import BytesIO
import hashlib

CHARACTER_DB = {}

def save_character_reference(upload, voice_id=None, metadata=None):
    image_bytes = upload.read()
    image_hash = hashlib.md5(image_bytes).hexdigest()
    CHARACTER_DB[image_hash] = {
        "name": upload.name,
        "image": Image.open(BytesIO(image_bytes)),
        "voice_id": voice_id,
        "metadata": metadata or {}
    }
    return image_hash

def load_characters(uploaded_files, voice_ids=None):
    if not uploaded_files:
        return {}
    for idx, file in enumerate(uploaded_files):
        vid = voice_ids[idx] if voice_ids and idx < len(voice_ids) else None
        save_character_reference(file, voice_id=vid)
    return CHARACTER_DB

def match_characters(prompt, character_db):
    matched = {}
    for key, data in character_db.items():
        if data["name"].split(".")[0].lower() in prompt.lower():
            matched[key] = data
    return matched
