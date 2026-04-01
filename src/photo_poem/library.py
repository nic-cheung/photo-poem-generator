import os

import streamlit as st
from supabase import create_client, Client

BUCKET = "cards"


@st.cache_resource
def get_supabase() -> Client:
    url = _secret("SUPABASE_URL")
    key = _secret("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in secrets or .env")
    return create_client(url, key)


def save_entry(poem: str, style: str, image_name: str, card_bytes: bytes) -> str:
    """Insert poem record and upload card image. Returns the new row id."""
    client = get_supabase()
    result = (
        client.table("poems")
        .insert({"poem": poem, "style": style, "image_name": image_name})
        .execute()
    )
    poem_id = str(result.data[0]["id"])  # type: ignore[index, call-overload]
    client.storage.from_(BUCKET).upload(
        path=f"{poem_id}.jpg",
        file=card_bytes,
        file_options={"content-type": "image/jpeg"},
    )
    return poem_id


def load_entries() -> list[dict]:
    """Return all poems ordered newest first."""
    client = get_supabase()
    result = (
        client.table("poems")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    return result.data  # type: ignore[return-value]


def get_card_bytes(poem_id: str) -> bytes:
    """Download card image bytes directly from storage."""
    client = get_supabase()
    return bytes(client.storage.from_(BUCKET).download(f"{poem_id}.jpg"))


def delete_entry(poem_id: str) -> None:
    client = get_supabase()
    client.storage.from_(BUCKET).remove([f"{poem_id}.jpg"])
    client.table("poems").delete().eq("id", poem_id).execute()


def _secret(key: str) -> str | None:
    try:
        val = st.secrets.get(key)
        if val:
            return str(val)
    except Exception:
        pass
    return os.getenv(key)
