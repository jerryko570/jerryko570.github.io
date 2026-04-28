"""
keyword_extractor.py
--------------------
글의 발행처(source) 이름을 썸네일 라벨로 추출.

전략:
- "어떤 사이트의 글이냐"를 한 단어로 보여주는 게 가장 깔끔.
- candidates.json의 source 필드가 1순위 (Toss Tech, Figma Blog 등).
- source가 없으면 tags/title에서 출처 키워드 매칭 (claude → Claude).
- 마지막 폴백은 카테고리.

반환 시그니처는 기존과 동일 (line1, line2_or_None).
대부분 한 줄(line1)만 채우고 line2는 None — 카드가 단순해짐.
드물게 출처 자체가 길면 두 줄로 쪼갬 (예: 'Stack' / 'Overflow').

사용법:
    line1, line2 = extract_label(
        tags=["webflow", "claude", "mcp"],
        title="Webflow Claude Connector 공부 정리",
        category="Design",
        source="Webflow Blog",   # candidates.json의 source 필드
    )
    # → ("Webflow", None)
"""
from __future__ import annotations

from typing import Optional

# ───────────────────────────────────────────────
# 1. source 필드 → 라벨 매핑 (candidates.json의 source 값 기준)
# ───────────────────────────────────────────────
# 키는 source 문자열에 포함되면 매칭 (소문자 비교)
SOURCE_LABEL: dict[str, tuple[str, Optional[str]]] = {
    # Frontend
    "react blog": ("React", None),
    "vercel": ("Vercel", None),
    "tailwind": ("Tailwind", None),
    "astro": ("Astro", None),
    "svelte": ("Svelte", None),
    "nuxt": ("Nuxt", None),
    "web.dev": ("web.dev", None),
    "vue": ("Vue", None),

    # Design tools
    "figma": ("Figma", None),
    "webflow": ("Webflow", None),
    "framer": ("Framer", None),
    "notion": ("Notion", None),
    "linear": ("Linear", None),
    "sketch": ("Sketch", None),

    # AI / DevTools
    # Claude 관련(Anthropic, MCP, Claude Code 등)은 전부 "Claude"로 통일
    "anthropic": ("Claude", None),
    "claude": ("Claude", None),
    "claude code": ("Claude", None),
    "claude desktop": ("Claude", None),
    "mcp": ("Claude", None),
    "openai": ("OpenAI", None),
    "github blog": ("GitHub", None),
    "jetbrains": ("JetBrains", None),
    "hugging face": ("HuggingFace", None),
    "huggingface": ("HuggingFace", None),
    "stack overflow": ("Stack", "Overflow"),
    "supabase": ("Supabase", None),

    # 한국 기업
    "toss tech": ("Toss", None),
    "tosspayments": ("Toss", None),
    "pxd": ("PXD", None),
    "디지털 인사이트": ("Digital", "Insight"),
    "ditoday": ("Digital", "Insight"),
    "요즘it": ("요즘IT", None),
    "yozm": ("요즘IT", None),
    "wishket": ("요즘IT", None),
    "뱅크샐러드": ("Banksalad", None),
    "banksalad": ("Banksalad", None),
}

# ───────────────────────────────────────────────
# 2. source가 없거나 매칭 실패 시 — tags/title에서 키워드로 추출
# ───────────────────────────────────────────────
KEYWORD_LABEL: dict[str, tuple[str, Optional[str]]] = {
    # AI
    # Claude 관련(Anthropic, MCP, Skills 등)은 전부 "Claude"로 묶음
    "claude": ("Claude", None),
    "anthropic": ("Claude", None),
    "mcp": ("Claude", None),
    "openai": ("OpenAI", None),
    "gpt": ("GPT", None),
    "cursor": ("Cursor", None),
    "copilot": ("Copilot", None),

    # 디자인 도구
    "figma": ("Figma", None),
    "webflow": ("Webflow", None),
    "framer": ("Framer", None),
    "notion": ("Notion", None),
    "linear": ("Linear", None),

    # 프레임워크
    "react": ("React", None),
    "next": ("Next.js", None),
    "nextjs": ("Next.js", None),
    "next-js": ("Next.js", None),
    "vercel": ("Vercel", None),
    "vue": ("Vue", None),
    "svelte": ("Svelte", None),
    "astro": ("Astro", None),
    "nuxt": ("Nuxt", None),
    "tailwind": ("Tailwind", None),
    "vite": ("Vite", None),
    "remix": ("Remix", None),

    # 언어
    "typescript": ("TypeScript", None),
    "javascript": ("JavaScript", None),

    # 브라우저 / 웹 표준
    "chrome": ("Chrome", None),
    "firefox": ("Firefox", None),
    "safari": ("Safari", None),
    "css": ("CSS", None),
    "html": ("HTML", None),
    "baseline": ("Baseline", None),

    # 한국 기업
    "tosspayments": ("Toss", None),
    "toss": ("Toss", None),
    "pxd": ("PXD", None),
    "banksalad": ("Banksalad", None),
    "kakao": ("Kakao", None),
    "naver": ("Naver", None),

    # 개발 플랫폼
    "github": ("GitHub", None),
    "jetbrains": ("JetBrains", None),
    "supabase": ("Supabase", None),
    "docker": ("Docker", None),
}

# ───────────────────────────────────────────────
# 3. 마지막 폴백 — 카테고리 라벨
# ───────────────────────────────────────────────
CATEGORY_FALLBACK: dict[str, tuple[str, Optional[str]]] = {
    "Design": ("Design", None),
    "DesignCraft": ("Design", None),
    "Frontend": ("Frontend", None),
    "DevTools": ("DevTools", None),
}


# Claude 패밀리 키워드 — 출처와 무관하게 무조건 'Claude' 라벨 강제
# 이유: Webflow 사이트가 발행한 Claude 통합 글이라도 "Claude 글"로 분류되는 게
# 시각적으로 더 일관됨. 사용자 룰(2026-04-28).
CLAUDE_KEYWORDS: set[str] = {
    "claude",
    "anthropic",
    "mcp",
    "claude code",
    "claude desktop",
    "claude skills",
}


def extract_label(
    tags: list[str],
    title: str,
    category: str,
    source: str = "",
) -> tuple[str, Optional[str]]:
    """
    Returns (line1, line2_or_None).
    대부분 line1만 채워서 한 줄 라벨로 떨어짐.

    우선순위:
    0. Claude 패밀리 키워드가 본문/태그에 있으면 → "Claude" 강제
    1. source 필드 매칭 (Webflow Blog → Webflow 등)
    2. tags/title 키워드 매칭
    3. 카테고리 폴백
    """
    haystack = " ".join(tags + [title]).lower()

    # 0순위: Claude 패밀리는 출처 무시하고 무조건 Claude
    if any(k in haystack for k in CLAUDE_KEYWORDS):
        return ("Claude", None)

    # 1순위: source 필드 매칭
    if source:
        source_lower = source.lower()
        for key, label in SOURCE_LABEL.items():
            if key in source_lower:
                return label

    # 2순위: tags/title 키워드 매칭
    for key, label in KEYWORD_LABEL.items():
        if key in haystack:
            return label

    # 3순위: 카테고리 폴백
    return CATEGORY_FALLBACK.get(category, ("Study", None))


if __name__ == "__main__":
    # candidates.json 형태에 맞춘 테스트
    cases = [
        # (tags, title, category, source)
        (["webflow", "claude", "mcp"],
         "Webflow Claude Connector 공부 정리", "Design", "Webflow Blog"),
        (["claude", "skills"],
         "Claude Skills 공부 정리", "DevTools", "Anthropic News"),
        (["react", "actions"],
         "React 19 Actions 훑어보면서", "Frontend", "React Blog"),
        (["tailwind", "v4"],
         "Tailwind v4 디자인 토큰", "Frontend", "Tailwind Blog"),
        (["toss", "pqc"],
         "토스페이먼츠 PQC 도입기 공부 정리", "DesignCraft", "Toss Tech"),
        (["chrome", "firefox", "css", "baseline"],
         "4월 웹 플랫폼 업데이트 공부 정리", "Frontend", "web.dev Blog"),

        # source가 없는 경우 (수동 글)
        (["css", "container-query"],
         "CSS Container Query 공부", "Frontend", ""),
        (["accessibility"],
         "접근성 공부 정리", "Design", ""),

        # 매칭 안 되는 글 → 카테고리 폴백
        (["unknown"], "정체불명 글", "Frontend", ""),
    ]
    for tags, title, cat, src in cases:
        result = extract_label(tags, title, cat, src)
        print(f"  {str(result):28s}  ← {title[:30]}  (source: {src or '-'})")