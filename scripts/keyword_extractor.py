"""
keyword_extractor.py (v3)
--------------------------
글의 발행처(source) 이름을 썸네일 라벨로 추출.

v3 변경 (2026-04-30):
- CLAUDE 룰 좁힘: claude/anthropic이 명시적으로 있을 때만 Claude로 분류.
  → mcp, skills는 단독으로는 Claude 라벨을 트리거하지 않음.
- 새 키워드 추가: shadcn, figjam, MCP(단독), Skills(단독), v0, lovable 등.
- fallback 강화: 매칭 안 되면 첫 태그를 라벨로 사용 (이름이 너무 길지 않을 때).

전략:
- "어떤 사이트/도구의 글이냐"를 한 단어로 보여주는 게 가장 깔끔.
- candidates.json의 source 필드가 1순위 (Toss Tech, Figma Blog 등).
- source가 없으면 tags/title에서 출처 키워드 매칭.
- 마지막 폴백은 첫 태그 → 카테고리.

사용법:
    line1, line2 = extract_label(
        tags=["webflow", "claude", "mcp"],
        title="Webflow Claude Connector 공부 정리",
        category="Design",
        source="Webflow Blog",
    )
    # → ("Claude", None)  (claude 태그가 명시적으로 있으니 Claude)

    line1, line2 = extract_label(
        tags=["shadcn", "ai", "mcp"],
        title="shadcn CLI v4 공부 정리",
        category="DesignCraft",
        source="pxd",
    )
    # → ("shadcn", None)  (claude 태그 없음 + shadcn 매칭)
"""
from __future__ import annotations

from typing import Optional

# ───────────────────────────────────────────────
# 1. source 필드 → 라벨 매핑 (candidates.json의 source 값 기준)
# ───────────────────────────────────────────────
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
    # 명시적 Claude만 통합
    "anthropic": ("Claude", None),
    "claude code": ("Claude", None),
    "claude desktop": ("Claude", None),
    "claude": ("Claude", None),
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
# 2. tags/title 키워드 매칭 (순서가 우선순위)
# ───────────────────────────────────────────────
# v3 — 더 구체적인 키워드를 먼저 매칭하도록 순서 정렬
KEYWORD_LABEL: dict[str, tuple[str, Optional[str]]] = {
    # ===== AI 도구 (Claude와 분리) =====
    # shadcn/ui, figjam 같은 구체적인 도구명 먼저
    "shadcn-ui": ("shadcn", None),
    "shadcn": ("shadcn", None),
    "figjam": ("FigJam", None),
    "v0": ("v0", None),
    "lovable": ("Lovable", None),
    "bolt": ("Bolt", None),

    # ===== Claude (명시적 키워드만) =====
    "claude": ("Claude", None),
    "anthropic": ("Claude", None),

    # ===== 일반 AI 컨셉 (Claude 다음에) =====
    # mcp/skills는 단독으로 매칭되면 자체 라벨
    "mcp": ("MCP", None),
    "skills": ("Skills", None),

    # ===== 다른 LLM/도구 =====
    "openai": ("OpenAI", None),
    "gpt": ("GPT", None),
    "cursor": ("Cursor", None),
    "copilot": ("Copilot", None),

    # ===== 디자인 도구 =====
    "figma": ("Figma", None),
    "webflow": ("Webflow", None),
    "framer": ("Framer", None),
    "notion": ("Notion", None),
    "linear": ("Linear", None),

    # ===== 프레임워크 =====
    "react": ("React", None),
    "next.js": ("Next.js", None),
    "next-js": ("Next.js", None),
    "nextjs": ("Next.js", None),
    "next": ("Next.js", None),
    "vercel": ("Vercel", None),
    "vue": ("Vue", None),
    "svelte": ("Svelte", None),
    "astro": ("Astro", None),
    "nuxt": ("Nuxt", None),
    "tailwind": ("Tailwind", None),
    "vite": ("Vite", None),
    "remix": ("Remix", None),

    # ===== 언어 =====
    "typescript": ("TypeScript", None),
    "javascript": ("JavaScript", None),

    # ===== 브라우저 / 웹 표준 =====
    "chrome": ("Chrome", None),
    "firefox": ("Firefox", None),
    "safari": ("Safari", None),
    "css": ("CSS", None),
    "html": ("HTML", None),
    "baseline": ("Baseline", None),

    # ===== 디자인 토픽 =====
    "design-system": ("Design", "System"),
    "design-systems": ("Design", "System"),
    "accessibility": ("A11Y", None),
    "a11y": ("A11Y", None),

    # ===== 한국 기업 =====
    "tosspayments": ("Toss", None),
    "toss": ("Toss", None),
    "pxd": ("PXD", None),
    "banksalad": ("Banksalad", None),
    "kakao": ("Kakao", None),
    "naver": ("Naver", None),

    # ===== 개발 플랫폼 =====
    "github-actions": ("Actions", None),
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
    "DesignCraft": ("Design", "Craft"),
    "Frontend": ("Frontend", None),
    "DevTools": ("DevTools", None),
}


# v3 — 명시적 Claude 키워드만 (mcp, skills는 제외)
# 이 키워드들은 0순위로 무조건 "Claude" 라벨로 강제됨.
# Webflow가 발행한 Claude 통합 글 같은 경우, 출처보다 Claude 정체성이 더 중요.
# 단, 단순히 "MCP"만 언급되는 글은 Claude로 묶지 않음 (너무 광범위).
CLAUDE_KEYWORDS: set[str] = {
    "claude",
    "anthropic",
}


def _tag_to_label(tag: str) -> Optional[str]:
    """첫 태그를 사람이 읽을 수 있는 라벨로 변환.

    예: "design-system" → "Design System", "next-js" → "Next Js"
    너무 길거나 너무 짧으면 None 반환.
    """
    if not tag:
        return None
    cleaned = tag.replace("-", " ").replace("_", " ").strip()
    if not cleaned:
        return None
    # 너무 짧거나 너무 길면 패스
    if len(cleaned) > 14 or len(cleaned) < 2:
        return None
    # 단어 첫글자만 대문자로
    return " ".join(w.capitalize() for w in cleaned.split())


def extract_label(
    tags: list[str],
    title: str,
    category: str,
    source: str = "",
) -> tuple[str, Optional[str]]:
    """
    Returns (line1, line2_or_None).

    우선순위:
    0. claude/anthropic이 본문/태그에 명시적으로 있으면 → "Claude" 강제
    1. source 필드 매칭 (Webflow Blog → Webflow 등)
    2. tags/title 키워드 매칭 (shadcn → shadcn 등)
    3. 첫 태그를 라벨로 (design-system → "Design System")
    4. 카테고리 폴백
    """
    haystack = " ".join(tags + [title]).lower()

    # 0순위: 명시적 Claude만 (v3에서 mcp/skills 제외)
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

    # 3순위: 첫 태그를 라벨로 사용 (v3 신규)
    if tags:
        label = _tag_to_label(tags[0])
        if label:
            return (label, None)

    # 4순위: 카테고리 폴백
    return CATEGORY_FALLBACK.get(category, ("Study", None))


if __name__ == "__main__":
    # candidates.json 형태에 맞춘 테스트
    cases = [
        # (tags, title, category, source)
        # ===== Claude 매칭 (claude/anthropic 있음) =====
        (["webflow", "claude", "mcp"],
         "Webflow Claude Connector 공부 정리", "Design", "Webflow Blog"),
        (["claude", "skills"],
         "Claude Skills 공부 정리", "DevTools", "Anthropic News"),

        # ===== Claude 매칭 안 됨 (mcp만 있음) — v3 변경점 =====
        (["shadcn", "ai", "mcp", "cli"],
         "shadcn CLI v4 공부 정리", "DesignCraft", "pxd"),
        (["figma", "figjam", "mcp"],
         "FigJam MCP 연동 공부 정리", "Design", "Figma Blog"),
        (["mcp", "automation"],
         "MCP 서버 만들어보기", "DevTools", ""),

        # ===== 다른 매칭들 =====
        (["react", "actions"],
         "React 19 Actions 훑어보면서", "Frontend", "React Blog"),
        (["toss", "pqc"],
         "토스페이먼츠 PQC 도입기", "DesignCraft", "Toss Tech"),

        # ===== 첫 태그 라벨 폴백 (v3 신규) =====
        (["design-system"],
         "디자인 시스템 토큰 구축기", "Design", ""),
        (["accessibility"],
         "접근성 공부 정리", "Design", ""),

        # ===== 매칭 전혀 안 됨 → 카테고리 폴백 =====
        ([], "정체불명 글", "Frontend", ""),
    ]
    print(f"{'결과':28s}  ← 제목  (source)")
    print("-" * 80)
    for tags, title, cat, src in cases:
        result = extract_label(tags, title, cat, src)
        print(f"  {str(result):28s}  ← {title[:30]}  ({src or '-'})")