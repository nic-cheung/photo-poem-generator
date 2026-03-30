import io
import random
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from .generator import generate_poem_from_path, generate_poem_from_upload  # noqa: E402

st.set_page_config(
    page_title="Photo Poem Generator",
    page_icon="📷",
    layout="centered",
)

st.title("📷 Photo Poem Generator")
st.caption("A poem from your memories — guess the photo before you peek.")

# ── Sidebar: image source ────────────────────────────────────────────────────
with st.sidebar:
    st.header("Settings")
    source = st.radio(
        "Image source",
        ["Upload photos", "Local folder"],
        help="Use 'Upload photos' when running on Streamlit Community Cloud.",
    )

    if source == "Local folder":
        folder = st.text_input("Folder path", value="~/Pictures")
    else:
        uploaded_files = st.file_uploader(
            "Upload photos",
            type=["jpg", "jpeg", "png", "webp", "heic"],
            accept_multiple_files=True,
        )

# ── Session state ────────────────────────────────────────────────────────────
for key in ("poem", "style", "image_bytes", "image_name", "revealed"):
    if key not in st.session_state:
        st.session_state[key] = None

if "revealed" not in st.session_state:
    st.session_state.revealed = False

# ── Generate button ──────────────────────────────────────────────────────────
if st.button("✨ Generate Poem", use_container_width=True):
    st.session_state.revealed = False
    st.session_state.poem = None
    st.session_state.style = None
    st.session_state.image_bytes = None
    st.session_state.image_name = None

    try:
        if source == "Upload photos":
            if not uploaded_files:
                st.warning("Please upload at least one photo first.")
                st.stop()
            chosen = random.choice(uploaded_files)
            file_bytes = chosen.read()
            with st.spinner("Writing your poem…"):
                poem, style = generate_poem_from_upload(file_bytes)
            st.session_state.poem = poem
            st.session_state.style = style
            st.session_state.image_bytes = file_bytes
            st.session_state.image_name = chosen.name

        else:
            folder_path = Path(folder).expanduser()
            image_files = [
                p
                for p in folder_path.iterdir()
                if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
            ]
            if not image_files:
                st.warning(f"No images found in {folder_path}")
                st.stop()
            chosen_path = random.choice(image_files)
            with st.spinner("Writing your poem…"):
                poem, style = generate_poem_from_path(chosen_path)
            st.session_state.poem = poem
            st.session_state.style = style
            with open(chosen_path, "rb") as f:
                st.session_state.image_bytes = f.read()
            st.session_state.image_name = chosen_path.name

    except Exception as e:
        st.error(f"Something went wrong: {e}")
        st.stop()

# ── Display poem ─────────────────────────────────────────────────────────────
if st.session_state.poem:
    st.markdown(
        f"<div style='text-align:center; margin-bottom:0.25rem;'>"
        f"<span style='background:#e94560; color:#fff; border-radius:12px; "
        f"padding:2px 12px; font-size:0.8rem; letter-spacing:0.05em;'>"
        f"{st.session_state.style.upper()}</span></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div style='font-family:serif; font-size:1.2rem; line-height:1.8; "
        f"white-space:pre-wrap; text-align:center; padding:1.5rem 0;'>"
        f"{st.session_state.poem}</div>",
        unsafe_allow_html=True,
    )

    # ── Read aloud ───────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔊 Read it aloud", use_container_width=True):
            try:
                from gtts import gTTS

                tts = gTTS(text=st.session_state.poem, lang="en", slow=False)
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)
                st.audio(audio_buffer, format="audio/mp3")
            except Exception as e:
                st.error(f"Could not generate audio: {e}")

    with col2:
        if st.button("🔍 Reveal the Photo", use_container_width=True):
            st.session_state.revealed = True

    # ── Reveal ───────────────────────────────────────────────────────────────
    if st.session_state.revealed and st.session_state.image_bytes:
        st.divider()
        st.image(
            st.session_state.image_bytes,
            caption=st.session_state.image_name,
            use_container_width=True,
        )
