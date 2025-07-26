import subprocess
import tempfile

def mux_audio_to_video(video_path, audio_path, output_path=None):
    if not output_path:
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name

    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]

    try:
        subprocess.run(cmd, check=True)
        return output_path
    except subprocess.CalledProcessError as e:
        print("FFmpeg error:", e)
        return None
