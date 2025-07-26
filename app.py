import streamlit as st
from backend.character_db import save_character_reference, load_characters
from backend.process_prompt import generate_scene_data
from backend.generate_scene_assets import generate_full_scene

st.set_page_config(page_title="BridgeFlixAI Studio", layout="wide")

st.title("🎬 BridgeFlixAI Studio")
st.markdown("Create AI-powered voice + video scenes with your custom characters.")

# Upload Section
st.header("1. Upload Characters")
uploaded_files = st.file_uploader("Upload character images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
voice_ids = st.text_area("Enter corresponding ElevenLabs Voice IDs (one per line)", "").splitlines()

if st.button("Load Characters"):
    if uploaded_files:
        characters = load_characters(uploaded_files, voice_ids=voice_ids)
        st.success(f"{len(characters)} character(s) loaded into memory.")
        for key, data in characters.items():
            st.image(data["image"], caption=f'{data["name"]} | Voice ID: {data["voice_id"]}', width=150)
    else:
        st.warning("Please upload at least one character image.")

# Prompt Input
st.header("2. Enter Your Scene Prompt")
prompt = st.text_area("Enter a natural language description of the scene:")
if st.button("Generate Scene Breakdown"):
    if not prompt:
        st.error("Please enter a prompt.")
    else:
        characters = load_characters(uploaded_files, voice_ids=voice_ids)
        scene_data = generate_scene_data(prompt, characters)
        if scene_data:
            st.success("Scene breakdown generated.")
            st.json(scene_data["shots"])
            if st.button("Generate Voice & Video"):
                clips = generate_full_scene(scene_data)
                st.success("Scene assets generated.")
                for idx, clip in enumerate(clips):
                    st.subheader(f"Shot {idx+1}: {clip['character'].capitalize()}")
                    st.audio(clip["audio"])
                    st.video(clip["video"])
        else:
            st.error("Scene generation failed. Check your OpenAI API key or formatting.")
