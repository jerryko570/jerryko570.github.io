"""
keyword_extractor.py
--------------------
글의 tags, title, category에서 썸네일에 들어갈 영문 라벨 추출.

추출 우선순위:
1. HIGH_PRIORITY 키워드가 매칭되면 그것을 line1으로
2. MODIFIERS에서 보조 단어가 있으면 line2로 결합
3. 어느 것도 매칭 안 되면 카테고리 기반 폴백

사용법:
    line1, line2 = extract_label(
        tags=["webflow", "claude", "mcp"],
        title="Webflow Claude Connector 공부 정리",
        category="Design",
    )
    # → ("Webflow", "Connector")
"""
from __future__ import annotations

from typing import Optional

# 1순위: 강한 브랜드/기술 이름. (line1, default_line2)
HIGH_PRIORITY: dict[str, tuple[str, Optional[str]]] = {
    # AI / LLM / 에이전트
    "claude": ("Claude", None),
    "anthropic": ("Anthropic", None),
    "openai": ("OpenAI", None),
    "gpt": ("GPT", None),
    "cursor": ("Cursor", None),
    "copilot": ("Copilot", None),
    "mcp": ("MCP", "Connector"),

    # 디자인 도구
    "figma": ("Figma", None),
    "webflow": ("Webflow", None),
    "framer": ("Framer", None),
    "notion": ("Notion", None),
    "linear": ("Linear", None),

    # 프레임워크 / 빌드 도구
    "react": ("React", None),
    "next": ("Next.js", None),
    "nextjs": ("Next.js", None),
    "next-js": ("Next.js", None),
    "vue": ("Vue", None),
    "svelte": ("Svelte", None),
    "astro": ("Astro", None),
    "nuxt": ("Nuxt", None),
    "tailwind": ("Tailwind", None),
    "vite": ("Vite", None),
    "vercel": ("Vercel", None),

    # 언어
    "typescript": ("TypeScript", None),
    "javascript": ("JavaScript", None),

    # 한국 기업
    "toss": ("Toss", "Tech"),
    "tosspayments": ("Toss", "Payments"),
    "pxd": ("PXD", "Story"),
    "banksalad": ("Banksalad", None),
    "woowahan": ("Woowahan", None),

    # 개발자 플랫폼
    "github": ("GitHub", None),
    "jetbrains": ("JetBrains", None),
    "huggingface": ("HuggingFace", None),
    "supabase": ("Supabase", None),
}

# 2순위: 보조 단어 (1순위와 결합 가능)
MODIFIERS: dict[str, str] = {
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
    "v18": "v18",
    "v19": "v19",
    "hooks": "Hooks",
    "actions": "Actions",
    "rsc": "RSC",
    "compiler": "Compiler",
    "server-component": "Server",
    "server-components": "Server",
    "ssr": "SSR",
    "ssg": "SSG",
    "pqc": "PQC",
    "security": "Security",
    "automation": "Automation",
    "workflow": "Workflow",
}

# 3순위: 카테고리별 폴백 라벨
CATEGORY_FALLBACK: dict[str, tuple[str, str]] = {
    "Design": ("Design", "Note"),
    "DesignCraft": ("Product", "Design"),
    "Frontend": ("Frontend", "Note"),
    "DevTools": ("Dev", "Note"),
}


def extract_label(
    tags: list[str],
    title: str,
    category: str,
) -> tuple[str, Optional[str]]:
    """
    Returns (line1, line2_or_None).
    line1만 있으면 한 줄, 둘 다 있으면 두 줄로 표시.
    """
    haystack = " ".join(tags + [title]).lower()

    # 1. 강한 키워드 찾기 (먼저 매칭된 것을 사용)
    primary: Optional[tuple[str, Optional[str]]] = None
    for key, label_pair in HIGH_PRIORITY.items():
        if key in haystack:
            primary = label_pair
            break

    # 2. 보조 단어로 line2 보강
    if primary:
        line1, default_line2 = primary
        for key, label in MODIFIERS.items():
            if key in haystack and label != line1:
                return (line1, label)
        return (line1, default_line2)

    # 3. 폴백 - 카테고리 기반
    return CATEGORY_FALLBACK.get(category, ("Study", "Note"))


if __name__ == "__main__":
    # 간단 테스트
    cases = [
        (["webflow", "claude", "mcp"], "Webflow Claude Connector 공부 정리", "Design"),
        (["claude", "skills"], "Claude Skills 공부 정리", "DevTools"),
        (["react", "actions"], "React 19 Actions 훑어보면서", "Frontend"),
        (["tailwind", "v4"], "Tailwind v4 디자인 토큰", "Frontend"),
        (["toss", "pqc"], "토스페이먼츠 PQC 도입기 공부 정리", "DesignCraft"),
        (["ux"], "어떤 한국 디자인 글", "DesignCraft"),
    ]
    for tags, title, cat in cases:
        result = extract_label(tags, title, cat)
        print(f"  {result}  ← {title[:30]}")