import base64
import io
from pathlib import Path

from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

MAX_DIMENSION = 2048


def load_image_as_base64(path: str | Path) -> str:
    """Load an image file, resize to max 2048px, convert to RGB, return base64 JPEG."""
    img = Image.open(path).convert("RGB")
    img = _resize(img)
    return _to_base64_jpeg(img)


def load_uploaded_image_as_base64(file_bytes: bytes) -> str:
    """Load image bytes (from st.file_uploader), resize and return base64 JPEG."""
    img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    img = _resize(img)
    return _to_base64_jpeg(img)


def _resize(img: Image.Image) -> Image.Image:
    if max(img.size) > MAX_DIMENSION:
        img.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.LANCZOS)
    return img


def _to_base64_jpeg(img: Image.Image) -> str:
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
