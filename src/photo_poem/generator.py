from pathlib import Path

from .claude_client import get_client, get_model
from .image_utils import load_image_as_base64, load_uploaded_image_as_base64
from .prompts import STYLES, SYSTEM_PROMPT, random_style, user_prompt


def generate_poem_from_path(
    image_path: str | Path, style: str | None = None, language: str = "English"
) -> tuple[str, str]:
    """Generate a poem from a local image file. Returns (poem, style_name)."""
    image_data = load_image_as_base64(image_path)
    return _generate(image_data, style, language)


def generate_poem_from_upload(
    file_bytes: bytes, style: str | None = None, language: str = "English"
) -> tuple[str, str]:
    """Generate a poem from uploaded image bytes. Returns (poem, style_name)."""
    image_data = load_uploaded_image_as_base64(file_bytes)
    return _generate(image_data, style, language)


def _generate(image_data: str, style: str | None = None, language: str = "English") -> tuple[str, str]:
    if style:
        style_name, style_description = style, STYLES[style]
    else:
        style_name, style_description = random_style()
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
                        "text": user_prompt(style_description, language),
                    },
                ],
            }
        ],
    )

    poem = message.content[0].text.strip()
    return poem, style_name
