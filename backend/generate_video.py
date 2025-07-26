import tempfile
import subprocess

def generate_video_clip(scene_data, base_image=None, base_clip=None):
    print("Generating video with scene data:", scene_data)
    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name

    prompt = scene_data["prompt"]

    try:
        cmd = [
            "python", "scripts/svd_run.py",
            "--prompt", prompt,
            "--output", temp_path
        ]
        subprocess.run(cmd, check=True)
    except Exception as e:
        print("Stable Video Diffusion failed:", e)
        return None

    return temp_path
