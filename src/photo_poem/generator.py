from pathlib import Path

from anthropic.types import TextBlock

from .claude_client import get_client, get_model
from .image_utils import load_image_as_base64, load_uploaded_image_as_base64
from .prompts import STYLES_BY_LANGUAGE, SYSTEM_PROMPT, random_style, user_prompt


def generate_poem_from_path(
    image_path: str | Path,
    style: str | None = None,
    language: str = "English",
    poet: str | None = None,
) -> tuple[str, str]:
    """Generate a poem from a local image file. Returns (poem, style_name)."""
    image_data = load_image_as_base64(image_path)
    return _generate(image_data, style, language, poet)


def generate_poem_from_upload(
    file_bytes: bytes,
    style: str | None = None,
    language: str = "English",
    poet: str | None = None,
) -> tuple[str, str]:
    """Generate a poem from uploaded image bytes. Returns (poem, style_name)."""
    image_data = load_uploaded_image_as_base64(file_bytes)
    return _generate(image_data, style, language, poet)


def _generate(
    image_data: str,
    style: str | None = None,
    language: str = "English",
    poet: str | None = None,
) -> tuple[str, str]:
    styles = STYLES_BY_LANGUAGE.get(language, STYLES_BY_LANGUAGE["English"])
    if style and style in styles:
        style_name, style_description = style, styles[style]
    else:
        style_name, style_description = random_style(language)
    client = get_client()
    model = get_model()

    message = client.messages.create(
        model=model,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": user_prompt(style_description, language, poet, style_name),
                    },
                ],
            }
        ],
    )

    block = message.content[0]
    if not isinstance(block, TextBlock):
        raise ValueError(f"Unexpected response block type: {type(block).__name__}")
    poem = block.text.strip()
    return poem, style_name
