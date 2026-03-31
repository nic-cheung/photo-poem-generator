import base64
import io
import json
import random
import sys
import textwrap
from pathlib import Path

# Allow running directly with `streamlit run src/photo_poem/app.py`
sys.path.insert(0, str(Path(__file__).parent.parent))

from PIL import Image, ImageOps
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

load_dotenv()

from photo_poem.generator import generate_poem_from_path, generate_poem_from_upload  # noqa: E402
from photo_poem.prompts import STYLES  # noqa: E402
from photo_poem.library import save_entry, load_entries, get_card_bytes, delete_entry  # noqa: E402

GTTS_ACCENTS = {
    "🇺🇸 US English": "com",
    "🇬🇧 UK English": "co.uk",
    "🇦🇺 Australian": "com.au",
    "🇮🇳 Indian": "co.in",
    "🇨🇦 Canadian": "ca",
}


def _fix_orientation(file_bytes: bytes) -> bytes:
    img = ImageOps.exif_transpose(Image.open(io.BytesIO(file_bytes))).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return buf.getvalue()


def _make_card(poem: str, style: str, image_bytes: bytes) -> bytes:
    from PIL import ImageDraw, ImageFont

    HALF_W, CARD_H = 600, 700
    CARD_W = HALF_W * 2
    PADDING = 52
    BG = (15, 15, 26)
    TEXT_COLOR = (235, 228, 210)
    ACCENT = (233, 69, 96)

    photo = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    ratio = photo.width / photo.height
    target = HALF_W / CARD_H
    if ratio > target:
        new_h, new_w = CARD_H, int(photo.width * CARD_H / photo.height)
    else:
        new_w, new_h = HALF_W, int(photo.height * HALF_W / photo.width)
    photo = photo.resize((new_w, new_h), Image.LANCZOS)
    cx, cy = (new_w - HALF_W) // 2, (new_h - CARD_H) // 2
    photo = photo.crop((cx, cy, cx + HALF_W, cy + CARD_H))

    card = Image.new("RGB", (CARD_W, CARD_H), color=BG)
    card.paste(photo, (HALF_W, 0))
    draw = ImageDraw.Draw(card)
    draw.line([(HALF_W, 0), (HALF_W, CARD_H)], fill=ACCENT, width=3)

    _font_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
    ]

    def _load(size):
        for path in _font_candidates:
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                pass
        return ImageFont.load_default()

    available_h = CARD_H - PADDING * 2 - 50
    for font_size in (22, 19, 16, 13):
        poem_font = _load(font_size)
        line_h = draw.textbbox((0, 0), "Ay", font=poem_font)[3] + 6
        char_w = max(1, draw.textlength("m", font=poem_font))
        chars = max(20, int((HALF_W - PADDING * 2) / char_w))
        lines = []
        for para in poem.split("\n"):
            lines.extend(textwrap.wrap(para, width=chars) if para.strip() else [""])
        if len(lines) * line_h <= available_h:
            break

    badge_font = _load(13)
    badge_text = style.upper()
    bx0, by0, bx1, by1 = draw.textbbox((0, 0), badge_text, font=badge_font)
    bw, bh = bx1 - bx0 + 24, by1 - by0 + 12
    badge_x = (HALF_W - bw) // 2
    badge_y = PADDING - 10
    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + bw, badge_y + bh], radius=8, fill=ACCENT
    )
    draw.text((badge_x + 12, badge_y + 6), badge_text, font=badge_font, fill=(255, 255, 255))

    total_h = len(lines) * line_h
    text_y = badge_y + bh + max(16, (available_h - total_h) // 2)
    for line in lines:
        if line:
            lw = draw.textlength(line, font=poem_font)
            draw.text(((HALF_W - lw) // 2, text_y), line, font=poem_font, fill=TEXT_COLOR)
        text_y += line_h

    buf = io.BytesIO()
    card.save(buf, format="JPEG", quality=92)
    return buf.getvalue()


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Photo Poem Generator",
    page_icon="📷",
    layout="centered",
)

st.title("📷 Photo Poem Generator")
st.caption("A poem from your memories — guess the photo before you peek.")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_generate, tab_library = st.tabs(["Generate", "Library"])

# ══════════════════════════════════════════════════════════════════════════════
# GENERATE TAB
# ══════════════════════════════════════════════════════════════════════════════
with tab_generate:

    # ── Settings & uploader ───────────────────────────────────────────────────
    _on_cloud = not Path("~/Library").expanduser().exists()

    if _on_cloud:
        source = "Upload photos"
        uploaded_files = st.file_uploader(
            "Choose photos from your camera roll",
            type=["jpg", "jpeg", "png", "webp", "heic"],
            accept_multiple_files=True,
            label_visibility="visible",
        )
    else:
        with st.sidebar:
            st.header("Settings")
            source = st.radio("Image source", ["Upload photos", "Local folder"])
            if source == "Local folder":
                folder = st.text_input(
                    "Folder path",
                    value="~/Library/Mobile Documents/com~apple~CloudDocs/Poems",
                )
            else:
                uploaded_files = st.file_uploader(
                    "Upload photos",
                    type=["jpg", "jpeg", "png", "webp", "heic"],
                    accept_multiple_files=True,
                )

    with st.sidebar:
        st.subheader("Poem style")
        style_choice = st.selectbox(
            "Style",
            ["Random"] + list(STYLES.keys()),
            format_func=lambda s: s.capitalize(),
        )
        selected_style = None if style_choice == "Random" else style_choice

        st.subheader("Voice")
        voice_engine = st.radio("Engine", ["gTTS (accents)", "Browser (device voices)"])
        if voice_engine == "gTTS (accents)":
            accent_label = st.selectbox("Accent", list(GTTS_ACCENTS.keys()))

    # ── Session state ─────────────────────────────────────────────────────────
    for key in ("poem", "style", "image_bytes", "image_name", "revealed", "audio_bytes", "saved"):
        if key not in st.session_state:
            st.session_state[key] = None
    if "revealed" not in st.session_state:
        st.session_state.revealed = False
    if "saved" not in st.session_state:
        st.session_state.saved = False

    # ── Generate button ───────────────────────────────────────────────────────
    if st.button("✨ Generate Poem", width="stretch"):
        st.session_state.revealed = False
        st.session_state.saved = False
        st.session_state.poem = None
        st.session_state.style = None
        st.session_state.image_bytes = None
        st.session_state.image_name = None
        st.session_state.audio_bytes = None

        try:
            if source == "Upload photos":
                if not uploaded_files:
                    st.warning("Please upload at least one photo first.")
                    st.stop()
                chosen = random.choice(uploaded_files)
                file_bytes = chosen.read()
                with st.spinner("Writing your poem…"):
                    poem, style = generate_poem_from_upload(file_bytes, selected_style)
                st.session_state.poem = poem
                st.session_state.style = style
                st.session_state.image_bytes = _fix_orientation(file_bytes)
                st.session_state.image_name = chosen.name

            else:
                folder_path = Path(folder).expanduser()
                image_files = [
                    p for p in folder_path.iterdir()
                    if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
                ]
                if not image_files:
                    st.warning(f"No images found in {folder_path}")
                    st.stop()
                chosen_path = random.choice(image_files)
                with st.spinner("Writing your poem…"):
                    poem, style = generate_poem_from_path(chosen_path, selected_style)
                st.session_state.poem = poem
                st.session_state.style = style
                with open(chosen_path, "rb") as f:
                    st.session_state.image_bytes = _fix_orientation(f.read())
                st.session_state.image_name = chosen_path.name

        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.stop()

    # ── Display poem ──────────────────────────────────────────────────────────
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

        # ── Regenerate ───────────────────────────────────────────────────────
        if st.button("🔄 Regenerate poem", width="stretch"):
            with st.spinner("Writing a new poem…"):
                try:
                    poem, style = generate_poem_from_upload(
                        st.session_state.image_bytes, selected_style
                    )
                    st.session_state.poem = poem
                    st.session_state.style = style
                    st.session_state.audio_bytes = None
                    st.session_state.saved = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

        # ── Read aloud ────────────────────────────────────────────────────────
        col1, col2 = st.columns(2)
        with col1:
            if voice_engine == "gTTS (accents)":
                if st.button("🔊 Read it aloud", width="stretch"):
                    try:
                        from gtts import gTTS
                        tts = gTTS(
                            text=st.session_state.poem,
                            lang="en",
                            tld=GTTS_ACCENTS[accent_label],
                            slow=False,
                        )
                        audio_buffer = io.BytesIO()
                        tts.write_to_fp(audio_buffer)
                        st.session_state.audio_bytes = audio_buffer.getvalue()
                    except Exception as e:
                        st.error(f"Could not generate audio: {e}")
            else:
                st.session_state.audio_bytes = None

        with col2:
            if st.button("🔍 Reveal the Photo", width="stretch"):
                st.session_state.revealed = True

        if voice_engine == "gTTS (accents)" and st.session_state.audio_bytes:
            audio_b64 = base64.b64encode(st.session_state.audio_bytes).decode()
            st.markdown(
                f'<audio controls style="width:100%">'
                f'<source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">'
                f'</audio>',
                unsafe_allow_html=True,
            )

        if voice_engine == "Browser (device voices)":
            poem_json = json.dumps(st.session_state.poem)
            components.html(
                f"""
                <style>
                  body {{ margin:0; font-family: sans-serif; }}
                  select {{
                    width: 100%; padding: 6px 8px; margin-bottom: 8px;
                    background: #1a1a2e; color: #fff;
                    border: 1px solid #444; border-radius: 6px; font-size: 0.9rem;
                  }}
                  button {{
                    width: 100%; padding: 8px; background: #e94560; color: #fff;
                    border: none; border-radius: 6px; cursor: pointer; font-size: 1rem;
                  }}
                  button:hover {{ background: #c73652; }}
                  #status {{ font-size:0.8rem; color:#aaa; margin-top:4px; }}
                </style>
                <select id="voice-select"><option>Loading voices…</option></select>
                <button onclick="speak()">🔊 Read it aloud</button>
                <div id="status"></div>
                <script>
                  const text = {poem_json};
                  const sel = document.getElementById('voice-select');
                  const status = document.getElementById('status');
                  function loadVoices() {{
                    const voices = window.speechSynthesis.getVoices().filter(v => v.lang.startsWith('en'));
                    if (!voices.length) return false;
                    sel.innerHTML = '';
                    voices.forEach((v, i) => {{
                      const opt = document.createElement('option');
                      opt.value = i;
                      opt.textContent = v.name + ' (' + v.lang + ')';
                      sel.appendChild(opt);
                    }});
                    status.textContent = voices.length + ' voices available';
                    return true;
                  }}
                  if (!loadVoices()) {{
                    const poll = setInterval(() => {{ if (loadVoices()) clearInterval(poll); }}, 100);
                    window.speechSynthesis.onvoiceschanged = () => {{ loadVoices(); clearInterval(poll); }};
                  }}
                  function speak() {{
                    window.speechSynthesis.cancel();
                    const voices = window.speechSynthesis.getVoices().filter(v => v.lang.startsWith('en'));
                    const utt = new SpeechSynthesisUtterance(text);
                    utt.voice = voices[parseInt(sel.value)] || null;
                    utt.rate = 0.9;
                    window.speechSynthesis.speak(utt);
                  }}
                </script>
                """,
                height=120,
            )

        # ── Reveal ────────────────────────────────────────────────────────────
        if st.session_state.revealed and st.session_state.image_bytes:
            st.divider()
            st.image(
                st.session_state.image_bytes,
                caption=st.session_state.image_name,
                width="stretch",
            )

        # ── Save to library ───────────────────────────────────────────────────
        if st.session_state.image_bytes:
            st.divider()
            if st.session_state.saved:
                st.success("Saved to library.")
            else:
                if st.button("📚 Save to Library", width="stretch"):
                    with st.spinner("Saving…"):
                        try:
                            card_bytes = _make_card(
                                st.session_state.poem,
                                st.session_state.style,
                                st.session_state.image_bytes,
                            )
                            save_entry(
                                poem=st.session_state.poem,
                                style=st.session_state.style,
                                image_name=st.session_state.image_name or "",
                                card_bytes=card_bytes,
                            )
                            st.session_state.saved = True
                            st.rerun()
                        except Exception as e:
                            st.error(f"Could not save: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# LIBRARY TAB
# ══════════════════════════════════════════════════════════════════════════════
with tab_library:
    if st.button("Refresh", key="refresh_library"):
        st.rerun()

    try:
        entries = load_entries()
    except Exception as e:
        st.error(f"Could not load library: {e}")
        entries = []

    if not entries:
        st.info("No poems saved yet. Generate one and click 'Save to Library'.")
    else:
        for entry in entries:
            try:
                card_data = get_card_bytes(entry["id"])
                st.image(card_data, width="stretch")
            except Exception:
                st.warning(f"Could not load image for entry {entry['id'][:8]}…")
            col_meta, col_del = st.columns([4, 1])
            with col_meta:
                from datetime import datetime, timezone
                dt = datetime.fromisoformat(entry["created_at"].replace("Z", "+00:00"))
                st.caption(
                    f"{entry['style'].upper()} · {entry['image_name']} · "
                    f"{dt.strftime('%d %b %Y')}"
                )
            with col_del:
                if st.button("Delete", key=f"del_{entry['id']}"):
                    delete_entry(entry["id"])
                    st.rerun()
            st.divider()
