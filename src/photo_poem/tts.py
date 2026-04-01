import io

from .claude_client import _get_secret

# ── gTTS language config (fallback) ──────────────────────────────────────────

GTTS_ACCENTS: dict[str, tuple[str, str]] = {
    "English": ("en", "com"),
    "Mandarin (Simplified)": ("zh-CN", "com"),
    "Mandarin (Traditional)": ("zh-TW", "com"),
    "Cantonese": ("zh-TW", "com.hk"),
}

# ── ElevenLabs voice IDs ──────────────────────────────────────────────────────

_EL_VOICE_POEM = "21m00Tcm4TlvDq8ikWAM"  # Rachel — warm, expressive narrator
_EL_VOICE_RAP = "pNInz6obpgDQGcFmaJgB"   # Adam — deep, energetic

_EL_MODEL_EN = "eleven_turbo_v2_5"
_EL_MODEL_MULTILINGUAL = "eleven_multilingual_v2"

_RAP_STYLES = {"rap", "說唱 (Rap)", "廣東話說唱 (Rap)"}

# ── OpenAI voice IDs ──────────────────────────────────────────────────────────

_OAI_VOICE_POEM = "nova"   # warm, clear
_OAI_VOICE_RAP = "onyx"    # deep, strong


def generate_audio(text: str, language: str = "English", style: str = "") -> tuple[bytes, str]:
    """Generate audio via ElevenLabs → OpenAI → gTTS fallback chain.

    Returns (mp3_bytes, engine_name).
    """
    is_rap = style in _RAP_STYLES
    is_chinese = language in ("Mandarin (Simplified)", "Mandarin (Traditional)", "Cantonese")

    audio = _try_elevenlabs(text, is_rap, is_chinese)
    if audio is not None:
        return audio, "ElevenLabs"

    audio = _try_openai(text, is_rap)
    if audio is not None:
        return audio, "OpenAI"

    return _gtts_fallback(text, language), "gTTS"


def _try_elevenlabs(text: str, is_rap: bool, is_chinese: bool) -> bytes | None:
    api_key = _get_secret("ELEVENLABS_API_KEY")
    if not api_key:
        return None
    try:
        from elevenlabs import ElevenLabs

        client = ElevenLabs(api_key=api_key)
        voice_id = _EL_VOICE_RAP if is_rap else _EL_VOICE_POEM
        model_id = _EL_MODEL_MULTILINGUAL if is_chinese else _EL_MODEL_EN

        chunks = client.text_to_speech.convert(
            voice_id,
            text=text,
            model_id=model_id,
            output_format="mp3_44100_128",
        )
        return b"".join(chunks)
    except Exception as e:
        # Fall through on quota exhaustion or any API failure
        _is_quota_error = (
            hasattr(e, "status_code") and e.status_code == 429
        ) or "quota" in str(e).lower() or "limit" in str(e).lower()
        if not _is_quota_error:
            # Unexpected error — still fall through but could log here
            pass
        return None


def _try_openai(text: str, is_rap: bool) -> bytes | None:
    api_key = _get_secret("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        voice = _OAI_VOICE_RAP if is_rap else _OAI_VOICE_POEM
        response = client.audio.speech.create(
            model="tts-1-hd",
            voice=voice,
            input=text,
            response_format="mp3",
        )
        return response.content
    except Exception:
        return None


def _gtts_fallback(text: str, language: str) -> bytes:
    from gtts import gTTS

    lang, tld = GTTS_ACCENTS.get(language, ("en", "com"))
    tts = gTTS(text=text, lang=lang, tld=tld, slow=False)
    buffer = io.BytesIO()
    tts.write_to_fp(buffer)
    return buffer.getvalue()
