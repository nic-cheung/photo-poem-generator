import base64
import io
import json
import random
import sys
import textwrap
from datetime import datetime
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

CSS = """
<style>
/* ── Chrome ─────────────────────────────────────────────────────────────── */
#MainMenu, footer { visibility: hidden; }
header { visibility: hidden; }

/* ── Page ────────────────────────────────────────────────────────────────── */
.stApp { background: #09090f; }
.block-container {
    padding-top: 2.5rem !important;
    padding-bottom: 4rem !important;
    max-width: 660px;
}

/* ── Header ──────────────────────────────────────────────────────────────── */
.app-header { text-align: center; margin-bottom: 2rem; }
.app-header .ornament { color: #e94560; font-size: 1.1rem; display: block; margin-bottom: 0.5rem; }
.app-header .title {
    font-family: Georgia, serif;
    font-size: 1.55rem;
    font-weight: normal;
    letter-spacing: 0.14em;
    color: #e8e0d0;
    text-transform: uppercase;
}
.app-header .subtitle {
    font-size: 0.78rem;
    color: #484858;
    letter-spacing: 0.06em;
    margin-top: 0.5rem;
}

/* ── Tabs ────────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    border-bottom: 1px solid #151520;
    gap: 0;
    margin-bottom: 1.5rem;
    background: transparent !important;
}
.stTabs [data-baseweb="tab"] {
    padding: 0.6rem 2rem !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase;
    color: #404055 !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #e8e0d0 !important;
    border-bottom: 2px solid #e94560 !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── Buttons ─────────────────────────────────────────────────────────────── */
.stButton > button {
    font-family: Georgia, serif !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.05em !important;
    border-radius: 9px !important;
    border: 1px solid #252535 !important;
    background: #111120 !important;
    color: #c8c0b0 !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.18s ease !important;
    width: 100%;
}
.stButton > button:hover {
    border-color: #e94560 !important;
    color: #e8e0d0 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(233, 69, 96, 0.15) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Generate button — accent filled */
div[data-testid="element-container"]:has(button[kind="primary"]) button {
    background: #e94560 !important;
    border-color: #e94560 !important;
    color: white !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1.2rem !important;
}

/* ── File uploader ───────────────────────────────────────────────────────── */
[data-testid="stFileUploaderDropzone"] {
    border: 1.5px dashed #1e1e2e !important;
    border-radius: 12px !important;
    background: #0c0c18 !important;
    transition: border-color 0.2s;
}
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #e94560 !important;
}

/* ── Poem card ───────────────────────────────────────────────────────────── */
.poem-card {
    background: #0d0d1c;
    border: 1px solid #1a1a2c;
    border-radius: 18px;
    padding: 2.8rem 2.4rem 2.4rem;
    margin: 1.6rem 0 1rem;
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
    animation: fadeUp 0.5s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.poem-card .badge {
    display: block;
    text-align: center;
    font-family: -apple-system, sans-serif;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    color: #e94560;
    margin-bottom: 1.8rem;
    text-transform: uppercase;
}
.poem-card .poem-text {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 1.08rem;
    line-height: 2;
    text-align: center;
    color: #d8d0bc;
    white-space: pre-wrap;
}

/* ── Reveal ──────────────────────────────────────────────────────────────── */
.reveal-label {
    text-align: center;
    font-family: -apple-system, sans-serif;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    color: #363646;
    text-transform: uppercase;
    margin: 2rem 0 0.8rem;
}
.stImage { border-radius: 12px; overflow: hidden; }

/* ── Library card ────────────────────────────────────────────────────────── */
.lib-caption {
    font-family: -apple-system, sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.06em;
    color: #404055;
    margin: 0.4rem 0 1.2rem;
    text-align: center;
}
.lib-caption .lib-style { color: #e94560; }
.library-empty {
    text-align: center;
    color: #2a2a3a;
    font-size: 0.88rem;
    padding: 5rem 0;
    letter-spacing: 0.04em;
    font-family: Georgia, serif;
}

/* ── Sidebar ─────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] { background: #080810 !important; border-right: 1px solid #111120 !important; }
[data-testid="stSidebar"] label { font-size: 0.82rem !important; color: #888 !important; }
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stRadio > div { font-size: 0.85rem !important; }

/* ── Misc ────────────────────────────────────────────────────────────────── */
hr { border-color: #111120 !important; margin: 1.2rem 0 !important; }
.stSuccess > div { border-radius: 10px !important; font-size: 0.85rem !important; }
.stWarning > div { border-radius: 10px !important; font-size: 0.85rem !important; }
audio { width: 100%; border-radius: 8px; margin-top: 0.5rem; }

/* ── Scrollbar ───────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #09090f; }
::-webkit-scrollbar-thumb { background: #1e1e2e; border-radius: 4px; }
</style>
"""


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
st.set_page_config(page_title="Photo & Poem", page_icon="✦", layout="centered")
st.markdown(CSS, unsafe_allow_html=True)

st.markdown("""
<div class="app-header">
  <span class="ornament">✦</span>
  <div class="title">Photo &amp; Poem</div>
  <div class="subtitle">a poem from memory &mdash; guess the photo before you peek</div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_generate, tab_library = st.tabs(["Generate", "Library"])

# ══════════════════════════════════════════════════════════════════════════════
# GENERATE TAB
# ══════════════════════════════════════════════════════════════════════════════
with tab_generate:

    _on_cloud = not Path("~/Library").expanduser().exists()

    if _on_cloud:
        source = "Upload photos"
        uploaded_files = st.file_uploader(
            "Choose photos from your camera roll",
            type=["jpg", "jpeg", "png", "webp", "heic"],
            accept_multiple_files=True,
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

    # ── Generate ──────────────────────────────────────────────────────────────
    if st.button("✦  Generate Poem", type="primary", width="stretch"):
        st.session_state.update(
            revealed=False, saved=False, poem=None, style=None,
            image_bytes=None, image_name=None, audio_bytes=None,
        )
        try:
            if source == "Upload photos":
                if not uploaded_files:
                    st.warning("Upload at least one photo first.")
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

    # ── Poem display ──────────────────────────────────────────────────────────
    if st.session_state.poem:
        st.markdown(
            f"<div class='poem-card'>"
            f"<span class='badge'>{st.session_state.style}</span>"
            f"<div class='poem-text'>{st.session_state.poem}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

        # Regenerate
        if st.button("↺  Regenerate", width="stretch"):
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

        # Read aloud + Reveal
        col1, col2 = st.columns(2)
        with col1:
            if voice_engine == "gTTS (accents)":
                if st.button("♪  Read Aloud", width="stretch"):
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
            if st.button("◎  Reveal Photo", width="stretch"):
                st.session_state.revealed = True

        # Audio
        if voice_engine == "gTTS (accents)" and st.session_state.audio_bytes:
            audio_b64 = base64.b64encode(st.session_state.audio_bytes).decode()
            st.markdown(
                f'<audio controls>'
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
                    background: #0d0d1c; color: #c8c0b0;
                    border: 1px solid #252535; border-radius: 8px; font-size: 0.85rem;
                  }}
                  button {{
                    width: 100%; padding: 10px; background: #111120; color: #c8c0b0;
                    border: 1px solid #252535; border-radius: 8px; cursor: pointer;
                    font-family: Georgia, serif; font-size: 0.9rem; letter-spacing: 0.04em;
                    transition: all 0.18s;
                  }}
                  button:hover {{ border-color: #e94560; color: #e8e0d0; }}
                  #status {{ font-size:0.72rem; color:#404055; margin-top:5px; text-align:center; }}
                </style>
                <select id="voice-select"><option>Loading voices…</option></select>
                <button onclick="speak()">♪  Read Aloud</button>
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

        # Reveal
        if st.session_state.revealed and st.session_state.image_bytes:
            st.markdown('<div class="reveal-label">The Memory</div>', unsafe_allow_html=True)
            st.image(st.session_state.image_bytes, width="stretch")

        # Save
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        if st.session_state.saved:
            st.success("Saved to library.")
        else:
            if st.button("+ Save to Library", width="stretch"):
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
    if st.button("↺  Refresh", key="refresh_library"):
        st.rerun()

    try:
        entries = load_entries()
    except Exception as e:
        st.error(f"Could not load library: {e}")
        entries = []

    if not entries:
        st.markdown(
            "<div class='library-empty'>No poems saved yet.<br>Generate one and save it to start your library.</div>",
            unsafe_allow_html=True,
        )
    else:
        cols = st.columns(2, gap="medium")
        for i, entry in enumerate(entries):
            with cols[i % 2]:
                try:
                    card_data = get_card_bytes(entry["id"])
                    st.image(card_data, width="stretch")
                except Exception:
                    st.markdown(
                        "<div style='background:#0d0d1c;border:1px solid #1a1a2c;"
                        "border-radius:12px;padding:2rem;text-align:center;"
                        "color:#2a2a3a;font-size:0.8rem;'>Image unavailable</div>",
                        unsafe_allow_html=True,
                    )
                dt = datetime.fromisoformat(entry["created_at"].replace("Z", "+00:00"))
                st.markdown(
                    f"<div class='lib-caption'>"
                    f"<span class='lib-style'>{entry['style'].upper()}</span>"
                    f" · {dt.strftime('%d %b %Y')}</div>",
                    unsafe_allow_html=True,
                )
                if st.button("Delete", key=f"del_{entry['id']}"):
                    delete_entry(entry["id"])
                    st.rerun()
