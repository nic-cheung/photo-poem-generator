import os

import anthropic
import streamlit as st


def get_client() -> anthropic.Anthropic:
    """Return an Anthropic client, reading the API key from st.secrets first."""
    api_key = _get_secret("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not found. Set it in .streamlit/secrets.toml or .env"
        )
    return anthropic.Anthropic(api_key=api_key)


def get_model() -> str:
    return _get_secret("DEFAULT_MODEL") or "claude-opus-4-6"


def _get_secret(key: str) -> str | None:
    try:
        value = st.secrets.get(key)
        if value:
            return value
    except Exception:
        pass
    return os.getenv(key)
