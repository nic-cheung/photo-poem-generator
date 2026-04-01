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

# ── Poets by style ────────────────────────────────────────────────────────────

POETS_BY_STYLE: dict[str, dict[str, str]] = {
    # ── English ──────────────────────────────────────────────────────────────
    "haiku": {
        "Richard Wright": "in the style of Richard Wright — Blends traditional 5-7-5 syllable structures with stark, visceral observations of the natural world and human suffering. His imagery heavily contrasts seasonal changes with themes of isolation, illness, and fleeting resilience.",
        "Jack Kerouac": "in the style of Jack Kerouac — Abandons strict syllable counts for 'Western haiku' that capture spontaneous, fleeting moments in a conversational rhythm. Focuses on Zen-like observations of everyday American life, prioritizing raw emotional impact and brevity over rigid form.",
        "Sonia Sanchez": "in the style of Sonia Sanchez — Merges strict traditional syllable counting with African American vernacular and blues rhythms. Her lyrical themes center on urban Black life, political struggle, and profound personal vulnerability.",
        "Allen Ginsberg": "in the style of Allen Ginsberg — Employs a compressed, 17-syllable 'American Sentence' structure that captures manic, energetic flashes of modern life. His imagery frequently juxtaposes the sacred and the profane, focusing on urban landscapes and mundane interactions.",
        "Etheridge Knight": "in the style of Etheridge Knight — Utilizes the strict economy of the haiku to convey the claustrophobia and harsh realities of prison life and addiction. The emotional register is deeply raw and rhythmic, integrating street language into precise, focused imagery.",
    },
    "sonnet": {
        "William Shakespeare": "in the style of William Shakespeare — Employs the classic ABAB CDCD EFEF GG rhyme scheme in iambic pentameter, driven by witty conceits and rhetorical questions. Lyrical themes revolve around the destructive power of time, the immortality of verse, and complex romantic entanglements.",
        "John Milton": "in the style of John Milton — Utilizes the Petrarchan form with heavy enjambment, allowing complex syntactical thoughts to flow freely across line breaks. His register is lofty, authoritative, and deeply philosophical, focusing on religious justification, political duty, and personal blindness.",
        "Elizabeth Barrett Browning": "in the style of Elizabeth Barrett Browning — Characterized by highly dramatic, emotionally breathless pacing within strict Petrarchan rhyme schemes. Her imagery is deeply intimate and devoted, exploring the spiritual and physical dimensions of romantic love.",
        "Claude McKay": "in the style of Claude McKay — Adopts traditional Elizabethan sonnet structures to deliver explosive, radical political resistance. The emotional register is fiercely defiant and dignified, contrasting rigid formal mechanics with visceral imagery of racial violence and oppression.",
        "Edna St. Vincent Millay": "in the style of Edna St. Vincent Millay — Blends classical metric precision with modern, cynical psychological realism. Her voice is simultaneously romantic and fiercely independent, using traditional forms to explore fleeting love and female autonomy.",
    },
    "free verse": {
        "Walt Whitman": "in the style of Walt Whitman — Features long, sprawling, unmetered lines built on sweeping anaphora and extensive cataloging. His voice is fiercely democratic and emotionally expansive, utilizing cosmic imagery to connect the individual soul with the broader American landscape.",
        "Langston Hughes": "in the style of Langston Hughes — Integrates the syncopated rhythms of jazz and the repetitive structures of the blues into free verse form. The lyrical voice is highly colloquial and musical, focusing on the joys, sorrows, and daily realities of the African American working class.",
        "Sylvia Plath": "in the style of Sylvia Plath — Defined by jarring enjambment, intense sonic density, and violently striking imagery. Her emotional register is confessional and overwhelmingly claustrophobic, exploring deep psychological trauma through stark, mythic metaphors.",
        "William Carlos Williams": "in the style of William Carlos Williams — Relies on short, sharply enjambed lines that dictate a halting, deliberate visual pace on the page. His technique revolves around 'no ideas but in things,' utilizing completely unadorned, objective imagery of everyday American life.",
        "Mary Oliver": "in the style of Mary Oliver — Characterized by a gentle, conversational flow that guides the reader through precise, quiet observations of the natural world. Her emotional register balances reverent wonder with spiritual questioning, creating a deeply accessible and meditative voice.",
    },
    "villanelle": {
        "Dylan Thomas": "in the style of Dylan Thomas — Maximizes the incantatory power of the villanelle's repeating lines to create a surging, forceful musicality. His imagery is explosively elemental, driving an emotional register of fierce existential defiance against mortality.",
        "Elizabeth Bishop": "in the style of Elizabeth Bishop — Approaches the strict form with deceptive casualness, using subtle, conversational variations in her refrains. Her imagery is meticulously observed and geographically precise, masking profound themes of loss and displacement with quiet emotional restraint.",
        "Sylvia Plath": "in the style of Sylvia Plath — Uses the cyclical nature of the villanelle to convey obsessive, inescapable psychological states. Her repetitions feel inevitable and deeply unsettling, driven by dark, surreal imagery and an atmosphere of creeping dread.",
        "W.H. Auden": "in the style of W.H. Auden — Employs the form for philosophical inquiry and societal observation, utilizing strict formal control to anchor sweeping intellectual ideas. His emotional tone balances ironic detachment with an underlying, melancholy sense of historical crisis.",
        "Theodore Roethke": "in the style of Theodore Roethke — Leans into the hypnotic, dreamlike qualities of the repeated refrains, creating a waltzing, almost nursery-rhyme rhythm. His imagery blends the pastoral with the psychological, exploring the cyclical boundaries between nature, sanity, and madness.",
    },
    "imagist": {
        "Ezra Pound": "in the style of Ezra Pound — Practices extreme linguistic economy, stripping away all decorative adjectives and abstract rhetoric. His technique relies on the sharp juxtaposition of disparate visual images, creating a precise, almost sculptural emotional resonance.",
        "H.D. (Hilda Doolittle)": "in the style of H.D. (Hilda Doolittle) — Merges sharp, intensely tactile sensory details with classical Greek mythological motifs. Her free verse is sparse and crystalline, maintaining a cool, objective presentation while exploring profound psychological depths.",
        "William Carlos Williams": "in the style of William Carlos Williams — Focuses exclusively on the immediate, tangible objects of the American environment, avoiding European classical allusions entirely. His imagery is brightly lit and hyper-focused, presenting mundane items with startling, unadorned clarity.",
        "Amy Lowell": "in the style of Amy Lowell — Blends the concise visual focus of imagism with a slightly more sensuous, musical cadence. Her imagery is heavily dependent on vibrant color contrasts and varied textures, creating a lush but structurally controlled poetic landscape.",
        "Richard Aldington": "in the style of Richard Aldington — Delivers hard, clear, and unsentimental images, often juxtaposing the fragility of the human body with the harsh realities of modernity and war. His emotional register is stoic and deeply restrained, presenting trauma through purely visual phenomena.",
    },
    "ode": {
        "John Keats": "in the style of John Keats — Features a slow-paced, heavily sensuous, and deeply meditative rhythm that luxuriates in linguistic texture. His imagery explores the paradoxes of beauty, melancholy, and mortality, capturing fleeting moments of ecstasy within structurally dense stanzas.",
        "Percy Bysshe Shelley": "in the style of Percy Bysshe Shelley — Driven by sweeping, ecstatic rhythms and passionate rhetorical questioning that builds to visionary climaxes. He frequently uses powerful natural elements like the wind as metaphors for political revolution and intellectual transcendence.",
        "William Wordsworth": "in the style of William Wordsworth — Utilizes irregular Pindaric stanzaic forms to map the shifting movements of human thought and memory. His diction is elevated yet grounded in nature, evoking a profound, nostalgic emotional register centered on the loss of childhood wonder.",
        "Frank O'Hara": "in the style of Frank O'Hara — Subverts the formal ode into a hyper-casual, walking-poem format dubbed 'Personism.' His imagery is a breathless, conversational collage of New York cityscapes, celebrity name-drops, and intimate, spontaneous declarations of affection.",
        "Samuel Taylor Coleridge": "in the style of Samuel Taylor Coleridge — Pioneers the conversational ode, beginning in intimate, colloquial settings before expanding into soaring cosmic and philosophical reflection. His register is frequently melancholic and deeply introspective, weaving personal despair with abstract metaphysical theory.",
    },
    "elegy": {
        "Alfred Lord Tennyson": "in the style of Alfred Lord Tennyson — Characterized by highly musical, hypnotic quatrains that pace a long, grueling journey through grief. His imagery grapples directly with the conflict between religious faith and scientific indifference, maintaining a mournful, agonizingly beautiful emotional tone.",
        "W.H. Auden": "in the style of W.H. Auden — Blends deeply personal mourning with broad historical and political context, maintaining a discursive, subtly ironic distance. His language fluctuates between colloquial accessibility and dense philosophical abstraction, universally diagnosing societal ills through the lens of individual death.",
        "Thomas Gray": "in the style of Thomas Gray — Employs stately, heroic quatrains and Augustan diction to create a landscape of pastoral melancholy. His imagery universalizes death, contrasting the forgotten rural poor with the vain monuments of the wealthy, generating a profoundly soothing yet somber emotional resonance.",
        "Walt Whitman": "in the style of Walt Whitman — Operates on a symphonic scale, weaving together repeating national symbols to construct an expansive narrative of collective mourning. The tone is deeply consoling, integrating the concept of death into the continuous, mystical cycle of life.",
        "Percy Bysshe Shelley": "in the style of Percy Bysshe Shelley — Utilizes complex Spenserian stanzas and deeply entrenched pastoral conventions to mourn a fallen peer. He constructs an elaborate mythological allegory where nature itself weeps, culminating in a fierce, defiant celebration of the poet's immortality.",
    },
    "prose poem": {
        "Russell Edson": "in the style of Russell Edson — Structures the poem as a dark, surrealist fable with a completely matter-of-fact, detached narrative tone. His imagery routinely features absurd bodily distortions and bizarre domestic scenarios, creating a register of unsettling, deadpan comedy.",
        "Gertrude Stein": "in the style of Gertrude Stein — Employs extreme, hypnotic repetition and cubist syntax that completely disrupts standard grammar and logical flow. Her focus is on the sonic and physical qualities of language as an object itself, rather than linear narrative or traditional emotional catharsis.",
        "John Ashbery": "in the style of John Ashbery — Characterized by fluidly shifting pronouns and a highly conversational, yet completely elusive, stream of consciousness. He collages disparate idioms and pop culture imagery using dream logic, evoking an emotional register of mild bemusement and profound ontological uncertainty.",
        "Carolyn Forché": "in the style of Carolyn Forché — Practices the 'poetry of witness,' utilizing tight, journalistically precise prose paragraphs to document extreme political violence. Her imagery is jarringly literal and sharply detailed, creating an emotional tone of horrified, unflinching moral clarity.",
        "Claudia Rankine": "in the style of Claudia Rankine — Blends lyric intensity with clinical essayistic observation, frequently employing the second-person 'you' to force reader implication. Her imagery surgically dissects daily microaggressions and systemic racism, maintaining a register of exhausted, hyper-vigilant emotional restraint.",
    },
    "rap": {
        "Kendrick Lamar": "in the style of Kendrick Lamar — Characterized by complex, syncopated flows with rapid-fire triplet cadences and frequent beat manipulation. Lyrical themes blend dense storytelling, racial politics, and deep introspection using heavy internal rhyme schemes and shifting vocal timbres.",
        "Jay-Z": "in the style of Jay-Z — Master of the laid-back, conversational flow built on effortless rhythmic pocket presence and double entendres. The lyrical register is triumphant yet observational, relying on clever wordplay, entrepreneurial braggadocio, and internal assonance rather than overly dense multisyllabic crowding.",
        "Lauryn Hill": "in the style of Lauryn Hill — A soulful, melodic delivery that seamlessly transitions between reggae-influenced singing and tightly woven, percussive rapping. Lyrically rich in spiritual introspection, female empowerment, and social critique, marked by profound emotional warmth and rhythmic precision.",
        "Frank Ocean": "in the style of Frank Ocean — Employs a free-associative, almost stream-of-consciousness flow that floats over the beat with impressionistic R&B melodicism. Features highly cinematic, nostalgic imagery and nonlinear storytelling, utilizing conversational rhythms and deeply vulnerable emotional registers.",
        "MF DOOM": "in the style of MF DOOM — Defined by abstract, wildly unorthodox flows with incredibly dense, multi-syllabic rhyme schemes that often ignore standard bar lines. The vocabulary is extremely esoteric and comic-book referential, delivered in a detached, raspy monotone that prioritizes rhyme complexity over narrative cohesion.",
        "Eminem": "in the style of Eminem — Features hyper-technical, rapid-fire flow mechanics with relentless multisyllabic and internal rhyme density. The lyrical themes range from visceral anger and dark comedy to complex emotional trauma, utilizing aggressive staccato delivery, precise breath control, and shocking, vivid imagery.",
    },
    # ── Mandarin / Traditional (shared keys) ─────────────────────────────────
    "絕句 (Jueju)": {
        "李白 Li Bai": "in the style of 李白 Li Bai — Characterized by an effortless, flowing musicality that largely ignores strict tonal constraints in favor of transcendent Daoist spontaneity. His imagery is heavily populated by wine, moonlight, and solitary mountains, emitting an emotional register of grand, romantic exaggeration and cosmic loneliness.",
        "王之渙 Wang Zhihuan": "in the style of 王之渙 Wang Zhihuan — Focuses on sweeping, expansive frontier landscapes and the infinite stretch of time. His four lines are robust, highly visual, and heroic, capturing the vastness of the natural world and the fleeting, melancholic nature of human ambition.",
        "杜牧 Du Mu": "in the style of 杜牧 Du Mu — Exhibits a delicate, deeply melancholic late-Tang sensibility, often using historical ruins and subtle landscapes to reflect on dynastic decay. His phrasing is elegant and slightly decadent, carrying an emotional tone of lingering romantic sorrow and historical irony.",
        "王維 Wang Wei": "in the style of 王維 Wang Wei — Masters the concept of 'poetry in painting,' utilizing subtle color contrasts and empty space to evoke profound Zen Buddhist stillness. His emotional register is completely devoid of ego, projecting absolute peace, sensory clarity, and deep integration with nature.",
        "柳宗元 Liu Zongyuan": "in the style of 柳宗元 Liu Zongyuan — Delivers stark, almost monochromatic visual clarity, often depicting frozen, wintry, and utterly desolate landscapes. His poetic voice is profoundly isolated and emotionally numb, reflecting the deep, internalized trauma of political exile.",
    },
    "古詩 (Gushi)": {
        "陶淵明 Tao Yuanming": "in the style of 陶淵明 Tao Yuanming — Pioneered the poetry of rustic simplicity, utilizing completely unadorned, accessible language to reject courtly ambition. His recurring imagery of chrysanthemums and farming life establishes an emotional register of tranquil, philosophical acceptance and quiet joy.",
        "曹操 Cao Cao": "in the style of 曹操 Cao Cao — Utilizes powerful, driving four-character lines to convey majestic political ambition and martial grandeur. Despite his heroic posture, his imagery frequently dwells on human mortality and the passing of time, creating a tone of profound, masculine melancholy.",
        "阮籍 Ruan Ji": "in the style of 阮籍 Ruan Ji — Relies heavily on cryptic, deeply allegorical imagery of mythical birds and supernatural Daoist escapes to mask his intent. His emotional register is one of profound existential dread and political terror, using extreme obscurity as a shield against a murderous regime.",
        "陳子昂 Chen Ziang": "in the style of 陳子昂 Chen Ziang — Restored a muscular, straightforward Han/Wei dynasty style, utilizing sweeping historical perspectives and vast spatial geometries. His voice is fiercely solitary, depicting the lone intellectual standing against the infinite stretch of heaven and earth with tragic dignity.",
        "白居易 Bai Juyi": "in the style of 白居易 Bai Juyi — Prioritizes extreme narrative clarity and accessible language designed to be understood by commoners. His imagery is rooted in stark social realism, driven by an emotional register of deep, compassionate empathy for the poor and profound guilt over official privilege.",
    },
    "詞 (Ci)": {
        "蘇軾 Su Shi": "in the style of 蘇軾 Su Shi — Pioneers the 'Haofang' (heroic and unbound) style, breaking the strict, delicate musical confines of traditional ci. His imagery is expansive and philosophical, blending cosmic observation with daily domestic life to create an emotionally optimistic and resilient voice.",
        "李清照 Li Qingzhao": "in the style of 李清照 Li Qingzhao — The absolute master of the 'Wanyue' (delicate and restrained) style, focusing on exquisite, micro-level emotional details and intimate domestic spaces. Her imagery heavily features autumn wind, fading flowers, and wine, delivering a devastating emotional register of profound grief, displacement, and widowhood.",
        "辛棄疾 Xin Qiji": "in the style of 辛棄疾 Xin Qiji — Combines the ci form with fierce martial imagery and rugged, irregular rhythms. His poetic voice is dominated by patriotic fervor and the bitter, suffocating frustration of a brilliant military mind sidelined by a cowardly government.",
        "柳永 Liu Yong": "in the style of 柳永 Liu Yong — Popularized the extended 'manci' form, using vivid, colloquial language to depict the urban entertainment districts and courtesan culture of the Song dynasty. His emotional tone dwells on lingering, sentimental sorrow, the pain of parting, and the melancholy of traveling musicians.",
        "李煜 Li Yu": "in the style of 李煜 Li Yu — Transitions the ci form from palace entertainment to a vehicle for devastating personal tragedy. His imagery contrasts past royal extravagance with his current reality of captive despair, utilizing naked, highly vulnerable language to universalize the grief of irreversible loss.",
    },
    "律詩 (Lüshi)": {
        "杜甫 Du Fu": "in the style of 杜甫 Du Fu — Executes the strict eight-line regulated verse with flawless, complex tonal parallelism and dense syntactical inversion. His imagery is steeped in gritty historical reality and warfare, carrying a profoundly heavy emotional register of compassionate realism and agonizing concern for the nation.",
        "王維 Wang Wei": "in the style of 王維 Wang Wei — Constructs perfectly balanced, effortless middle couplets that seamlessly integrate human presence into vast, indifferent natural landscapes. His emotional tone is defined by quietism and spiritual retreat, removing the poet's ego entirely from the observation.",
        "李商隱 Li Shangyin": "in the style of 李商隱 Li Shangyin — Renowned for highly ambiguous, intensely sensual imagery and incredibly dense layers of historical and mythological allusion. His lüshi are emotionally labyrinthine, projecting a lush, untranslatable sadness and the lingering ghosts of forbidden romance.",
        "孟浩然 Meng Haoran": "in the style of 孟浩然 Meng Haoran — Maintains a lighter, more conversational flow within the strict regulated parameters, focusing on seasonal changes, river journeys, and the hermit lifestyle. His emotional register is characterized by pastoral ease, gentle disappointment, and a deep appreciation for solitude.",
        "陸游 Lu You": "in the style of 陸游 Lu You — Blends fiercely patriotic, martial intent with the despair of aging and political impotence. His strict couplets frequently contrast fever dreams of northern military conquest with the reality of his failing body and rainy, isolated surroundings.",
    },
    "現代詩 (Xinshi)": {
        "徐志摩 Xu Zhimo": "in the style of 徐志摩 Xu Zhimo — Characterized by highly flowing, musical rhythms that adapt Western Romantic metric structures into vernacular Chinese. His imagery frequently revolves around fleeting clouds, Cambridge landscapes, and ephemeral romance, conveying an emotionally delicate, idealistic, and gently melancholic tone.",
        "戴望舒 Dai Wangshu": "in the style of 戴望舒 Dai Wangshu — Heavily influenced by French Symbolism, utilizing hypnotic musical repetition and hazy, synesthetic imagery. His poetic voice frequently wanders through rainy, claustrophobic alleys, capturing the subtle intersection of classical Chinese grace and modern, existential doubt.",
        "顧城 Gu Cheng": "in the style of 顧城 Gu Cheng — A pioneer of 'Misty Poetry' who uses a stark, extremely simple, almost childlike vocabulary. This innocent, fairy-tale imagery serves as a chilling mask for deep psychological trauma and the devastating ideological betrayals of the Cultural Revolution.",
        "北島 Bei Dao": "in the style of 北島 Bei Dao — Employs deeply fragmented, surreal, and often violently juxtaposed imagery to critique totalitarianism. His voice is stoic, utterly disillusioned, and fiercely defiant, creating a cold, heroic emotional register that refuses to surrender intellectual freedom.",
        "余光中 Yu Guangzhong": "in the style of 余光中 Yu Guangzhong — Exercises tight metric control while blending classical Chinese allusions with sharply modern sensibilities. His imagery is frequently geographical and deeply nostalgic, carrying an emotional tone of profound homesickness and cultural displacement across the Taiwan Strait.",
    },
    "散文詩 (Prose poem)": {
        "魯迅 Lu Xun": "in the style of 魯迅 Lu Xun — Employs a dark, highly allegorical surrealism built on biting social critique and unsettling dreamscapes. His prose paragraphs are dense and rhythmically halting, conveying an emotional register of agonized, solitary awakening and fierce intellectual despair.",
        "冰心 Bing Xin": "in the style of 冰心 Bing Xin — Writes in a gentle, highly accessible vernacular that emphasizes maternal warmth and the philosophical purity of youth. Her imagery centers on stars, oceans, and quiet gardens, projecting a profoundly soothing, idealistic, and pantheistic emotional tone.",
        "郭沫若 Guo Moruo": "in the style of 郭沫若 Guo Moruo — Operates in an explosive, Whitman-esque register, blurring the lines between manic free verse and rushing prose. His imagery is cosmic, violently destructive, and mythic, driven by a tone of pantheistic fury and revolutionary rebirth.",
        "西川 Xi Chuan": "in the style of 西川 Xi Chuan — Constructs dense, rhetorically complex paragraphs that weave deep historical reflection with surreal, modern metaphors. His voice possesses immense intellectual weight, analyzing the burdens of Chinese civilization through a detached, highly analytical, and philosophically rigorous lens.",
        "商禽 Shang Qin": "in the style of 商禽 Shang Qin — Masters a Kafkaesque absurdism, utilizing narrative prose structures to tell deeply unsettling, logic-defying micro-stories. His recurring themes involve bodily distortion, imprisonment, and silent screams, projecting a tone of dark, surrealist humor masking profound political trauma.",
    },
    "說唱 (Rap)": {
        "陳奕迅 Eason Chan": "in the style of 陳奕迅 Eason Chan — While primarily a pop vocalist, his rap and rhythmic deliveries are highly melodic, theatrical, and steeped in everyday conversational rhythms. Lyrical themes focus on melancholic romance and existential modern life, emphasizing emotional resonance, subtle vibrato, and a casual yet emotionally weighted flow.",
        "MC仁 (LMF)": "in the style of MC仁 (LMF) — A pioneer of raw, aggressive street flows characterized by heavy boom-bap rhythmic spacing and unpolished, confrontational delivery. Lyrically focuses on fierce social critique, anti-establishment themes, and working-class struggles, using dense local slang and guttural vocal textures.",
        "GAI (中文说唱)": "in the style of GAI (中文说唱) — Blends traditional Chinese folk melodies with aggressive trap cadences, creating a unique 'Jianghu' (martial arts underworld) flow. The lyrics are deeply rooted in regional pride, brotherhood, and traditional Chinese poetry motifs, delivered with a fierce, arrogant swagger and heavy Sichuanese dialect inflections.",
        "Higher Brothers": "in the style of Higher Brothers — Characterized by high-energy, triplet-heavy trap flows and bouncy, infectious cadences that switch rapidly across bars. Lyrical themes revolve around globalized youth culture, materialism, and braggadocio, utilizing a playful mix of Mandarin, Sichuan dialect, and English slang with dense ad-libs.",
        "蛋堡 Soft Lipa": "in the style of 蛋堡 Soft Lipa — Known for a laid-back, jazzy flow that glides effortlessly over boom-bap and mellow beats with conversational grace. Lyrically highly observational and introspective, capturing the quiet melancholy of urban life through subtle storytelling, smooth internal rhymes, and a comforting, almost whispered vocal register.",
    },
    # ── Cantonese-specific ────────────────────────────────────────────────────
    "粵語白話詩": {
        "梁秉鈞 Leung Ping-kwan": "in the style of 梁秉鈞 Leung Ping-kwan — Highly conversational and intimately tied to Hong Kong's unique spatial geography. He frequently uses imagery of local street food and mundane urban objects to explore complex themes of post-colonial identity, displacement, and the fluidity of cultural borders.",
        "廖偉棠 Liao Weitang": "in the style of 廖偉棠 Liao Weitang — Merges gritty urban realism with striking, almost classical phrasing adapted for modern street Cantonese. His voice is passionately politically engaged, frequently giving voice to marginalized workers and the underclass through stark, violently beautiful urban imagery.",
        "黃霑 James Wong": "in the style of 黃霑 James Wong — Infuses profound literary depth into highly colloquial, unapologetically coarse Cantonese vernacular. His thematic register borrows heavily from Wuxia (martial arts) bravado, emphasizing fierce loyalty, philosophical Daoist detachment, and a raucous, roaring celebration of life.",
        "林夕 Lin Xi": "in the style of 林夕 Lin Xi — Characterized by extreme emotional nuance and the seamless integration of dense Buddhist philosophy into modern urban heartbreak. His imagery is highly concentrated and paradoxical, turning simple everyday objects into devastating metaphors for impermanence and the letting go of attachments.",
        "黃偉文 Wyman Wong": "in the style of 黃偉文 Wyman Wong — Employs a wildly playful, deeply cynical, and fashion-forward vocabulary full of sharp pop-culture references. His emotional register masks deep emotional vulnerability beneath a veneer of biting wit, utilizing high-camp metaphors and distinctly modern Hong Kong sarcasm.",
    },
    "嶺南詩風 (Lingnan style)": {
        "陳獻章 Chen Xianzhang": "in the style of 陳獻章 Chen Xianzhang — Grounded in Neo-Confucian naturalism, stripping away ornate poetic artifice in favor of spontaneous, unadorned expression. He draws profound philosophical and moral truths directly from the quiet observation of local Guangdong landscapes and daily routines.",
        "屈大均 Qu Dajun": "in the style of 屈大均 Qu Dajun — Dominated by the agonizing sorrow of a Ming dynasty loyalist mourning a fallen empire. His poetry is heroic, deeply tragic, and geographically hyper-specific, fiercely cataloging Lingnan flora and local customs as an act of cultural preservation and defiance.",
        "陳恭尹 Chen Gongyin": "in the style of 陳恭尹 Chen Gongyin — Features a remarkably sturdy, rhythmically muscular cadence that projects unyielding moral integrity. His imagery blends the martial vigor of anti-Qing resistance with the sweeping, turbulent natural scenery of the southern coastal regions.",
        "梁佩蘭 Liang Peilan": "in the style of 梁佩蘭 Liang Peilan — Possesses a highly delicate, emotionally resonant voice that focuses intimately on the textures of daily life. Her imagery vividly captures the local customs, fishing villages, and coastal atmospheres of Guangdong with elegant, empathetic precision.",
        "黃遵憲 Huang Zunxian": "in the style of 黃遵憲 Huang Zunxian — Pioneers the early modernization of Chinese poetry by forcefully injecting colloquial vitality and Hakka folk song rhythms into classical forms. His remarkably outward-looking voice tackles themes of global travel, new world technology, and the urgent need for political reform.",
    },
    "現代粵語詩": {
        "飲江 Yam Gong": "in the style of 飲江 Yam Gong — Operates with profound philosophical playfulness, constantly subverting linguistic expectations by crashing high intellectual theory into low local slang. His poems utilize recursive logic and conversational stuttering to explore the absurdity of existence and language itself.",
        "鍾國強 Chung Kwok-keung": "in the style of 鍾國強 Chung Kwok-keung — Defined by an incredibly quiet, patient observation of Hong Kong's urban decay and working-class neighborhoods. His imagery is precise and subdued, conveying an emotional register of deep, understated empathy and a lingering sense of historical loss.",
        "洛謀 Lok Mou": "in the style of 洛謀 Lok Mou — Relies on highly experimental syntax and a fragmented, restless urban consciousness. His imagery violently splices global internet culture with the sweaty, immediate reality of Hong Kong street life, reflecting the chaotic mental state of modern youth.",
        "鄧阿藍 Tang Ah-lam": "in the style of 鄧阿藍 Tang Ah-lam — Writes with completely raw, unfiltered working-class colloquialisms, frequently utilizing phonetic spellings of Cantonese grunts and curses. His emotional register is fiercely aggressive, delivering unapologetic, razor-sharp critiques of capitalist exploitation and poverty.",
        "淮遠 Huai Yuan": "in the style of 淮遠 Huai Yuan — Masters a minimalist, highly narrative form of black comedy. His poems function as biting, deadpan satires of bureaucratic absurdity and the isolating, mechanistic nature of modern city living, ending often on sharp, uncomfortable punchlines.",
    },
    "廣東話說唱 (Rap)": {
        "陳奕迅 Eason Chan": "in the style of 陳奕迅 Eason Chan — While primarily a pop vocalist, his rap and rhythmic deliveries are highly melodic, theatrical, and steeped in everyday conversational rhythms. Lyrical themes focus on melancholic romance and existential modern life, emphasizing emotional resonance, subtle vibrato, and a casual yet emotionally weighted flow.",
        "MC仁 (LMF)": "in the style of MC仁 (LMF) — A pioneer of raw, aggressive street flows characterized by heavy boom-bap rhythmic spacing and unpolished, confrontational delivery. Lyrically focuses on fierce social critique, anti-establishment themes, and working-class struggles, using dense local slang and guttural vocal textures.",
        "MastaMic": "in the style of MastaMic — Renowned for his lightning-fast, chopper-style flow and immaculate breath control over upbeat or freestyle tracks. His lyrics are fiercely independent and politically conscious, marked by extreme syllable density, sharp punchlines, and deeply rooted Hong Kong cultural commentary.",
        "Heyo": "in the style of Heyo — Features a versatile, highly rhythmic flow that bridges old-school boom-bap with modern trap sensibilities. Lyrical content leans heavily into introspective philosophy, local Hong Kong identity, and spiritual grounding, delivered with tight multisyllabic rhymes and a charismatic, energetic vocal tone.",
        "JB": "in the style of JB — Defined by an aggressive, raw, and highly emotive delivery over heavy trap beats with a distinct, husky vocal timbre. His lyrics are brutally honest, reflecting street life, personal struggle, and defiant survival in Hong Kong, utilizing dense Cantonese profanity and sharp, percussive rhyme schemes.",
    },
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
    style_name: str | None = None,
) -> str:
    lang_instruction = LANGUAGE_INSTRUCTIONS.get(language, "")
    style_voices = POETS_BY_STYLE.get(style_name, {}) if style_name else {}
    poet_instruction = f" Write {style_voices[poet]}." if poet and poet in style_voices else ""
    lang_suffix = f" {lang_instruction}" if lang_instruction else ""
    return (
        f"Please write {style_description} inspired by this photograph. "
        "Capture the mood, the light, the feeling of the moment — "
        "but keep it mysterious enough that someone would have to think "
        f"carefully to guess which memory this is.{poet_instruction}{lang_suffix}"
    )
