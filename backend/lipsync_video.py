import subprocess
import tempfile

def lipsync_with_wav2lip(face_image, audio_path, output_path=None):
    if not output_path:
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name

    cmd = [
        "python", "Wav2Lip/inference.py",
        "--checkpoint_path", "Wav2Lip/wav2lip.pth",
        "--face", face_image,
        "--audio", audio_path,
        "--outfile", output_path
    ]

    try:
        subprocess.run(cmd, check=True)
        return output_path
    except subprocess.CalledProcessError as e:
        print("Wav2Lip failed:", e)
        return None
