# scripts/keyword_extractor.py

# 1순위: tag/title에서 즉시 매칭되는 강한 브랜드/기술 이름
HIGH_PRIORITY = {
    # AI / 도구
    "claude": ("Claude", None),
    "anthropic": ("Anthropic", None),
    "openai": ("OpenAI", None),
    "cursor": ("Cursor", None),
    "copilot": ("Copilot", None),
    "mcp": ("MCP", "Connector"),

    # 디자인 도구
    "figma": ("Figma", None),
    "webflow": ("Webflow", None),
    "framer": ("Framer", None),
    "notion": ("Notion", None),

    # 프레임워크
    "react": ("React", None),
    "next": ("Next.js", None),
    "nextjs": ("Next.js", None),
    "vue": ("Vue", None),
    "svelte": ("Svelte", None),
    "astro": ("Astro", None),
    "tailwind": ("Tailwind", None),

    # 언어
    "typescript": ("TypeScript", None),
    "javascript": ("JavaScript", None),

    # 한국 기업
    "toss": ("Toss", "Tech"),
    "pxd": ("PXD", "Story"),
    "banksalad": ("Banksalad", None),
}

# 2순위: 보조 단어 (1순위와 결합 가능)
MODIFIERS = {
    "skills": "Skills",
    "agent": "Agent",
    "agents": "Agents",
    "connector": "Connector",
    "design-system": "Design System",
    "design-tools": "Design Tools",
    "release": "Release",
    "beta": "Beta",
    "v4": "v4",
    "v5": "v5",
    "v19": "v19",
    "hooks": "Hooks",
    "actions": "Actions",
    "rsc": "RSC",
}

# 3순위: 카테고리별 폴백 라벨
CATEGORY_FALLBACK = {
    "Design": ("Design", "Note"),
    "DesignCraft": ("Product", "Design"),
    "Frontend": ("Frontend", "Note"),
    "DevTools": ("Dev", "Note"),
}


def extract_label(tags: list, title: str, category: str) -> tuple[str, str | None]:
    """
    Returns (line1, line2 or None)
    line1만 있으면 한 줄, 둘 다 있으면 두 줄.
    """
    haystack = " ".join(tags + [title]).lower()

    # 1. 강한 키워드 찾기
    primary = None
    for key, (line1, default_line2) in HIGH_PRIORITY.items():
        if key in haystack:
            primary = (line1, default_line2)
            break

    # 2. 보조 단어로 line2 보강
    if primary:
        line1, line2 = primary
        for key, label in MODIFIERS.items():
            if key in haystack and label != line1:
                return (line1, label)
        return (line1, line2)

    # 3. 폴백 - 카테고리 기반
    return CATEGORY_FALLBACK.get(category, ("Study", "Note"))