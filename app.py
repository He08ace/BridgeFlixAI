
import streamlit as st
from backend.character_db import save_character_reference, load_characters
from backend.process_prompt import generate_scene_data
from backend.generate_scene_assets import generate_full_scene

st.set_page_config(page_title="BridgeFlixAI Studio", layout="wide")
st.title("🎬 BridgeFlixAI Text-to-Video Studio")

# Sidebar: Character Upload
st.sidebar.header("👤 Upload Characters")
uploaded_files = st.sidebar.file_uploader("Upload character images", accept_multiple_files=True, type=["png", "jpg", "jpeg"])
voice_ids = st.sidebar.text_area("Voice IDs (comma separated)").split(",")

if uploaded_files:
    characters = load_characters(uploaded_files, voice_ids)
    st.sidebar.success(f"{len(characters)} character(s) loaded.")
else:
    characters = {}

# Main: Prompt Input
prompt = st.text_area("🎯 Scene Prompt", placeholder="Enter a scene description...")

if st.button("Generate Scene"):
    if not prompt or not characters:
        st.warning("Please upload characters and enter a prompt.")
    else:
        with st.spinner("Generating..."):
            scene_data = generate_scene_data(prompt, characters)
            results = generate_full_scene(scene_data)

        if results:
            for idx, item in enumerate(results):
                st.subheader(f"Scene {idx+1}: {item['character'].capitalize()}")
                st.audio(item["audio"])
                st.video(item["video"])
                st.markdown(f"**Line:** {item['text']}")
        else:
            st.error("No results returned. Please check your inputs.")
