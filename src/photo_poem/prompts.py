import random

# ── Styles per language ───────────────────────────────────────────────────────

STYLES_EN: dict[str, str] = {
    "haiku": "a haiku (three lines: 5-7-5 syllables, rooted in a single sensory moment)",
    "sonnet": "a Shakespearean sonnet (14 lines, ABAB CDCD EFEF GG rhyme scheme, volta before the couplet)",
    "free verse": "a free verse poem (no fixed rhyme or metre, shaped by breath and image)",
    "villanelle": "a villanelle (19 lines, two repeating refrains, ABA rhyme scheme throughout)",
    "imagist": "an imagist poem (short, precise, no sentiment — pure image rendered in clear hard language)",
    "ode": "an ode (celebratory and lyrical, at least three stanzas, elevated tone)",
    "elegy": "an elegy (mournful and reflective, honouring the feeling of the moment)",
    "prose poem": "a prose poem (written as a paragraph, lyrical and compressed, no line breaks)",
    "rap": "a rap verse (rhythmic and percussive, internal rhymes, vivid street-level imagery, a punchy 16-bar structure with a hook)",
}

STYLES_ZH: dict[str, str] = {
    "絕句 (Jueju)": (
        "a jueju (絕句) — a classical Chinese quatrain of four lines, each line exactly "
        "5 or 7 characters, with end rhyme on lines 2 and 4, evoking a single vivid scene"
    ),
    "古詩 (Gushi)": (
        "a gushi (古詩) — ancient-style verse with flexible length lines, "
        "no strict tonal rules, allowing natural rhythm to carry the feeling"
    ),
    "詞 (Ci)": (
        "a ci (詞) — lyrical verse with lines of varying length, following the emotional "
        "flow of the image, intimate and musical in tone"
    ),
    "律詩 (Lüshi)": (
        "a lüshi (律詩) — an eight-line regulated verse poem with strict parallelism "
        "in the middle couplets and end rhyme on even lines"
    ),
    "現代詩 (Xinshi)": (
        "a xinshi (現代詩) — modern free verse in the contemporary Chinese tradition, "
        "personal voice, vivid imagery, no classical constraints"
    ),
    "散文詩 (Prose poem)": (
        "a sanwen shi (散文詩) — a prose poem written as flowing paragraphs, "
        "lyrical and impressionistic, blurring the line between prose and verse"
    ),
    "說唱 (Rap)": (
        "a Chinese rap verse (說唱) — rhythmic and punchy, strong internal rhymes "
        "in Mandarin, vivid imagery, a modern 16-bar structure with a hook"
    ),
}

STYLES_YUE: dict[str, str] = {
    "絕句 (Jueju)": (
        "a jueju (絕句) written in Cantonese — a classical quatrain of four lines, "
        "5 or 7 characters each, using Cantonese tones and natural Cantonese rhyme "
        "(Cantonese preserves the original Tang Dynasty sound system)"
    ),
    "古詩 (Gushi)": (
        "a gushi (古詩) in Cantonese — ancient-style verse with flexible lines, "
        "written in the Cantonese classical tradition with its rich tonal palette"
    ),
    "詞 (Ci)": (
        "a ci (詞) in Cantonese — lyrical verse of varying line lengths, "
        "intimate and musical, drawing on Cantonese's expressive tonal range"
    ),
    "粵語白話詩": (
        "a vernacular Cantonese poem (粵語白話詩) — written entirely in spoken Cantonese "
        "using vernacular characters and expressions, authentic to everyday Cantonese speech"
    ),
    "嶺南詩風 (Lingnan style)": (
        "a Lingnan-style poem (嶺南詩風) — drawing on the Southern Chinese poetic school: "
        "vivid local imagery, warm sensory detail, the landscape and light of Guangdong"
    ),
    "現代粵語詩": (
        "a modern Cantonese free verse poem (現代粵語詩) — contemporary, personal, "
        "written in Cantonese with a natural speaking voice and honest emotional directness"
    ),
    "廣東話說唱 (Rap)": (
        "a Cantonese rap verse (廣東話說唱) — rhythmic and percussive, rich with "
        "Cantonese slang and tonal wordplay, vivid imagery, a punchy 16-bar structure "
        "with a hook, in the tradition of HK hip-hop"
    ),
}

STYLES_BY_LANGUAGE: dict[str, dict[str, str]] = {
    "English": STYLES_EN,
    "Mandarin (Simplified)": STYLES_ZH,
    "Mandarin (Traditional)": STYLES_ZH,
    "Cantonese": STYLES_YUE,
}

# ── Poets ─────────────────────────────────────────────────────────────────────

POETS: dict[str, str] = {
    # English
    "Emily Dickinson": (
        "in the style of Emily Dickinson — slant rhyme, em-dashes as breath pauses, "
        "compressed imagery, unexpected capitalisations, a quiet fascination with "
        "mortality and the eternal in small things"
    ),
    "Mary Oliver": (
        "in the style of Mary Oliver — unhurried and attentive, present tense, "
        "finding wonder in the ordinary natural world, a gentle questioning voice "
        "that invites the reader to look more carefully"
    ),
    "Walt Whitman": (
        "in the style of Walt Whitman — long expansive lines, catalogues of detail, "
        "a democratic and celebratory 'I', direct address to the reader, "
        "the body and the world treated as equally sacred"
    ),
    "Sylvia Plath": (
        "in the style of Sylvia Plath — intense and confessional, precise dark imagery, "
        "controlled fury beneath the surface, the domestic made strange and charged"
    ),
    "Pablo Neruda": (
        "in the style of Pablo Neruda — sensual and elemental, bold metaphors "
        "that leap between the physical and the cosmic, passionate longing, "
        "the beloved and the world treated as one"
    ),
    "Rumi": (
        "in the style of Rumi — mystical and warm, love as spiritual yearning, "
        "simple language carrying deep wisdom, a conversational intimacy with the divine"
    ),
    # Chinese
    "李白 Li Bai": (
        "in the style of Li Bai (李白) — exuberant and romantic, the moon as constant "
        "companion, nature as mirror of feeling, a sense of freedom and wonder, "
        "imagery that feels effortless and inevitable"
    ),
    "杜甫 Du Fu": (
        "in the style of Du Fu (杜甫) — precise and compassionate observation, "
        "the personal woven into the historical, melancholy held with dignity, "
        "each image carefully placed"
    ),
    "蘇軾 Su Shi": (
        "in the style of Su Shi (蘇軾) — philosophical yet accessible, wit balanced "
        "with feeling, finding acceptance in impermanence, the classical and the "
        "conversational held in easy tension"
    ),
    "席慕蓉 Xi Murong": (
        "in the style of Xi Murong (席慕蓉) — modern and lyrical, gentle nostalgia, "
        "longing for what cannot be recovered, clear and accessible language "
        "that carries deep emotional weight"
    ),
    "余光中 Yu Guangzhong": (
        "in the style of Yu Guangzhong (余光中) — rich cultural resonance, "
        "the tension between homeland and distance, classical allusions woven "
        "into a modern voice, lyrical and precise"
    ),
    "顧城 Gu Cheng": (
        "in the style of Gu Cheng (顧城) — childlike wonder turned strange, "
        "minimalist and surreal, a few simple words opening onto something vast, "
        "the innocent eye that sees what adults have forgotten"
    ),
}

RAPPERS: dict[str, str] = {
    # English
    "Kendrick Lamar": (
        "in the style of Kendrick Lamar — dense internal rhymes, shifting perspectives, "
        "vivid Compton-rooted imagery elevated to the universal, intense introspection "
        "that builds to a moment of reckoning"
    ),
    "Jay-Z": (
        "in the style of Jay-Z — confident and precise, multi-syllable rhyme schemes, "
        "sharp wit and street-smart metaphors, a narrator who observes the world "
        "with cool detachment and hard-won wisdom"
    ),
    "Lauryn Hill": (
        "in the style of Lauryn Hill — soulful and raw, melody woven into the flow, "
        "deeply personal and spiritual, love and loss delivered with unflinching honesty"
    ),
    "Frank Ocean": (
        "in the style of Frank Ocean — intimate and elliptical, non-linear storytelling, "
        "tender vulnerability, sensory details that conjure memory and longing"
    ),
    "MF DOOM": (
        "in the style of MF DOOM — labyrinthine internal rhymes, absurdist imagery "
        "hiding genuine emotion, dense wordplay and unexpected references, "
        "a mask worn over something deeply felt"
    ),
    "Eminem": (
        "in the style of Eminem — rapid-fire syllables, complex multi-rhyme chains, "
        "confessional intensity, dark humour cutting through raw personal pain"
    ),
    # Chinese / Cantonese
    "陳奕迅 Eason Chan": (
        "in the style of Eason Chan (陳奕迅) — emotionally direct Cantonese delivery, "
        "colloquial warmth, vivid everyday imagery, the ache of ordinary life made poetic"
    ),
    "MC仁 (LMF)": (
        "in the style of MC仁 from LMF — raw Cantonese street voice, sharp social commentary, "
        "rapid-fire vernacular flow, unapologetically Hong Kong in attitude and imagery"
    ),
    "GAI (中文说唱)": (
        "in the style of GAI — bold Sichuan-inflected Mandarin rap, classical Chinese "
        "references remixed with modern swagger, vivid regional pride and lyrical density"
    ),
    "Higher Brothers": (
        "in the style of Higher Brothers — bilingual swagger, Chengdu cool, "
        "mixing Mandarin and English slang, laid-back confidence with sharp punchlines"
    ),
}

LANGUAGE_INSTRUCTIONS: dict[str, str] = {
    "English": "",
    "Cantonese": (
        "Write the poem in Cantonese (廣東話), using Traditional Chinese characters. "
        "Use natural Cantonese phrasing and expressions, not translated Mandarin."
    ),
    "Mandarin (Simplified)": (
        "Write the poem in Mandarin Chinese (普通話), using Simplified Chinese characters (简体字)."
    ),
    "Mandarin (Traditional)": (
        "Write the poem in Mandarin Chinese (國語), using Traditional Chinese characters (繁體字)."
    ),
}

SYSTEM_PROMPT = (
    "You are a gifted poet who finds beauty and meaning in photographs. "
    "When given an image you write an evocative poem that captures the feeling "
    "and memory behind the photo — without naming people or giving away obvious "
    "visual details that would make the scene instantly recognisable. "
    "Write only the poem itself, no title, no preamble, no explanation."
)


def random_style(language: str = "English") -> tuple[str, str]:
    """Return (style_name, style_description) for the given language."""
    styles = STYLES_BY_LANGUAGE.get(language, STYLES_EN)
    name = random.choice(list(styles))
    return name, styles[name]


def user_prompt(
    style_description: str,
    language: str = "English",
    poet: str | None = None,
) -> str:
    lang_instruction = LANGUAGE_INSTRUCTIONS.get(language, "")
    all_voices = {**POETS, **RAPPERS}
    poet_instruction = f" Write {all_voices[poet]}." if poet and poet in all_voices else ""
    lang_suffix = f" {lang_instruction}" if lang_instruction else ""
    return (
        f"Please write {style_description} inspired by this photograph. "
        "Capture the mood, the light, the feeling of the moment — "
        "but keep it mysterious enough that someone would have to think "
        f"carefully to guess which memory this is.{poet_instruction}{lang_suffix}"
    )
