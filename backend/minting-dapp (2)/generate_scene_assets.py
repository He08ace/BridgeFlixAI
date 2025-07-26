from backend.generate_voice import synthesize_dialogue
from backend.generate_video import generate_video_clip
from backend.mux_audio_video import mux_audio_to_video
from backend.lipsync_video import lipsync_with_wav2lip
import os

def generate_full_scene(scene_data):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    video_clips = []
    for idx, shot in enumerate(scene_data["shots"]):
        char_name = shot["character"].lower()
        character_match = next((data for key, data in scene_data["characters"].items()
                               if char_name in data["name"].lower()), None)
        if not character_match:
            print(f"No voice ID found for {char_name}, skipping.")
            continue

        voice_id = character_match.get("voice_id")
        dialogue = shot["dialogue"]

        voice_file = synthesize_dialogue(dialogue, voice_id)
        if not voice_file:
            continue

        USE_LIPSYNC = True

        if USE_LIPSYNC:
            face_image_path = character_match["metadata"].get("face_image_path", "john_face.png")
            video_path = lipsync_with_wav2lip(face_image_path, voice_file)
        else:
            video_path = generate_video_clip(scene_data, base_clip=None)

        if not video_path:
            continue

        final_video = mux_audio_to_video(video_path, voice_file)
        print(f"[{idx+1}] Final video: {final_video}")

        video_clips.append({
            "video": final_video,
            "audio": voice_file,
            "text": dialogue,
            "character": char_name
        })

    return video_clips
