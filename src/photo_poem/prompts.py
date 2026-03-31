import random

STYLES: dict[str, str] = {
    "haiku": "a haiku (three lines: 5-7-5 syllables)",
    "sonnet": "a Shakespearean sonnet (14 lines, ABAB CDCD EFEF GG rhyme scheme)",
    "free verse": "a free verse poem (no rhyme or metre constraints, but with vivid imagery)",
    "limerick": "a limerick (five lines, AABBA rhyme scheme, playful tone)",
    "ode": "an ode (celebratory, lyrical, at least three stanzas)",
    "cinquain": "a cinquain (five lines: 2-4-6-8-2 syllables)",
    "elegy": "an elegy (mournful, reflective, honouring the moment captured)",
}

LANGUAGE_INSTRUCTIONS: dict[str, str] = {
    "English": "",
    "Cantonese": (
        "Write the poem in Cantonese (廣東話), using Traditional Chinese characters. "
        "Use natural Cantonese phrasing and expressions, not translated Mandarin."
    ),
    "Mandarin": (
        "Write the poem in Mandarin Chinese (普通話), using Simplified Chinese characters."
    ),
}

SYSTEM_PROMPT = (
    "You are a gifted poet who finds beauty and meaning in photographs. "
    "When given an image you write an evocative poem that captures the feeling "
    "and memory behind the photo — without naming people or giving away obvious "
    "visual details that would make the scene instantly recognisable. "
    "Write only the poem itself, no title, no preamble, no explanation."
)


def random_style() -> tuple[str, str]:
    """Return (style_name, style_description)."""
    name = random.choice(list(STYLES))
    return name, STYLES[name]


def user_prompt(style_description: str, language: str = "English") -> str:
    lang_instruction = LANGUAGE_INSTRUCTIONS.get(language, "")
    lang_suffix = f" {lang_instruction}" if lang_instruction else ""
    return (
        f"Please write {style_description} inspired by this photograph. "
        "Capture the mood, the light, the feeling of the moment — "
        "but keep it mysterious enough that someone would have to think "
        f"carefully to guess which memory this is.{lang_suffix}"
    )
