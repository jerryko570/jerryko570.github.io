"""
brand_colors.py (v2)
--------------------
키워드별 브랜드 컬러 매핑 + 카테고리별 다양한 fallback 팔레트.

v2 변경 (2026-04-30):
- mcp/skills를 Claude 색에서 분리 (각자 독립된 색)
- shadcn, figjam, v0 등 새 도구 색 추가
- 카테고리별 다양한 팔레트(4-5색) 도입
- 매칭 안 될 때 카테고리 + 제목 해시로 색 결정 → 같은 카테고리 글들도 다양한 색

전략:
1. 글의 tags/title에 브랜드 키워드 매칭 → 그 브랜드 공식 색
2. 매칭 없음 → 카테고리 팔레트에서 제목 해시로 색 선택
3. 카테고리도 없으면 fallback 색

사용법:
    from brand_colors import pick_color
    bg = pick_color(
        tags=["react", "actions"],
        title="...",
        fallback="#3b82f6",
        category="Frontend",
    )
"""
from __future__ import annotations

# ───────────────────────────────────────────────
# 브랜드 공식 컬러
# ───────────────────────────────────────────────
# 키는 소문자, tags나 title에 포함되면 매칭
# dict 순서가 매칭 우선순위 (먼저 정의된 게 이김)
BRAND_COLORS: dict[str, str] = {
    # ===== AI 도구 (각자 다른 색) =====
    # shadcn은 공식 검정/그레이 — Frontend 카드 톤과 다르게 모노톤으로
    "shadcn-ui": "#18181b",
    "shadcn": "#18181b",

    # FigJam은 Figma 보조색 (산호 톤)
    "figjam": "#ff7262",

    # MCP 단독 — 인디고 (프로토콜이라는 추상 개념에 어울리는 톤)
    "mcp": "#6366f1",

    # Skills 단독 — 보라 (학습/스킬셋 느낌)
    "skills": "#8b5cf6",

    # AI 빌더들
    "v0": "#000000",
    "lovable": "#ff5e5b",
    "bolt": "#1389fd",

    # ===== Claude (명시적 키워드만) =====
    "claude": "#ff7847",
    "anthropic": "#ff7847",
    "claude code": "#ff7847",
    "claude desktop": "#ff7847",

    # ===== 다른 LLM =====
    "openai": "#10a37f",
    "gpt": "#10a37f",
    "cursor": "#000000",
    "copilot": "#24292e",
    "huggingface": "#ffd21e",
    "hugging-face": "#ffd21e",

    # ===== 디자인 도구 =====
    "figma": "#a259ff",
    "webflow": "#146ef5",
    "framer": "#0055ff",
    "notion": "#191919",
    "linear": "#5e6ad2",

    # ===== 프레임워크 =====
    "react": "#087ea4",
    "next.js": "#000000",
    "next-js": "#000000",
    "nextjs": "#000000",
    "next": "#000000",
    "vercel": "#000000",
    "vue": "#42b883",
    "svelte": "#ff3e00",
    "astro": "#ff5d01",
    "nuxt": "#00dc82",
    "tailwind": "#06b6d4",
    "vite": "#646cff",
    "remix": "#000000",
    "solid": "#2c4f7c",

    # ===== 언어 =====
    "typescript": "#3178c6",
    "javascript": "#f7df1e",
    "ecmascript": "#f7df1e",
    "python": "#3776ab",
    "rust": "#dea584",
    "go": "#00add8",

    # ===== 한국 기업 =====
    "toss": "#0064ff",
    "tosspayments": "#0064ff",
    "pxd": "#1a1a1a",
    "banksalad": "#26d063",
    "woowahan": "#2ac1bc",
    "kakao": "#fee500",
    "naver": "#03c75a",
    "line": "#06c755",

    # ===== 자동화 / DevOps =====
    "automation": "#34a853",
    "github-actions": "#34a853",
    "ci-cd": "#34a853",
    "ci": "#34a853",
    "workflow": "#34a853",

    "github": "#24292e",
    "git": "#f05033",
    "jetbrains": "#fe2857",
    "supabase": "#3ecf8e",
    "stack-overflow": "#f48024",
    "stackoverflow": "#f48024",
    "docker": "#2496ed",
    "kubernetes": "#326ce5",

    # ===== 디자인 토픽 =====
    "design-system": "#8b5cf6",
    "design-systems": "#8b5cf6",
    "ux": "#ec4899",
    "ui": "#ec4899",
    "accessibility": "#0ea5e9",
    "a11y": "#0ea5e9",
}


# ───────────────────────────────────────────────
# 카테고리별 팔레트 — 매칭 안 될 때 색 다양화
# ───────────────────────────────────────────────
# 각 카테고리 안에서도 글마다 다른 색이 나오도록 4-5개 색 배열
# 제목 해시로 인덱스를 결정 → 같은 글은 항상 같은 색 (재현 가능)
CATEGORY_PALETTES: dict[str, list[str]] = {
    "Design": [
        "#a855f7",  # 보라
        "#ec4899",  # 핑크
        "#8b5cf6",  # 라일락
        "#d946ef",  # 마젠타
        "#c084fc",  # 라벤더
    ],
    "DesignCraft": [
        "#f43f5e",  # 로즈
        "#fb923c",  # 오렌지
        "#f59e0b",  # 앰버
        "#ef4444",  # 레드
        "#fb7185",  # 살몬
    ],
    "Frontend": [
        "#3b82f6",  # 블루
        "#06b6d4",  # 시안
        "#0ea5e9",  # 스카이
        "#0891b2",  # 틸
        "#2563eb",  # 인디고
    ],
    "DevTools": [
        "#10b981",  # 에메랄드
        "#22c55e",  # 그린
        "#34a853",  # 구글 그린
        "#16a34a",  # 진한 그린
        "#14b8a6",  # 틸 그린
    ],
}


def _palette_color(category: str, title: str) -> str | None:
    """카테고리 팔레트에서 제목 해시로 색을 골라 반환.

    제목이 같으면 항상 같은 색 → 재빌드 시 색이 바뀌지 않음.
    """
    palette = CATEGORY_PALETTES.get(category)
    if not palette:
        return None
    # hash()는 Python 실행마다 결과가 달라질 수 있어서 sum(ord)으로 안정화
    seed = sum(ord(c) for c in title)
    return palette[seed % len(palette)]


def pick_color(
    tags: list[str],
    title: str,
    fallback: str,
    category: str = "",
) -> str:
    """
    매칭 우선순위:
    1. 브랜드 키워드 매칭 → 브랜드 공식 색
    2. 카테고리 팔레트 → 제목 해시로 색 선택 (다양화)
    3. fallback 색 (sources.yml의 카테고리 기본 색)
    """
    haystack = " ".join(tags + [title]).lower()

    # 1순위: 브랜드 키워드 매칭
    for key, color in BRAND_COLORS.items():
        if key in haystack:
            return color

    # 2순위: 카테고리 팔레트
    if category:
        palette_color = _palette_color(category, title)
        if palette_color:
            return palette_color

    # 3순위: 단순 fallback
    return fallback


if __name__ == "__main__":
    # 테스트 — v3 keyword_extractor와 결과 매칭되는지 확인
    cases = [
        # (tags, title, fallback, category)
        # ===== 브랜드 매칭 (1순위) =====
        (["webflow", "claude", "mcp"], "Webflow Claude Connector 공부 정리", "#a855f7", "Design"),
        (["shadcn", "ai", "mcp"], "shadcn CLI v4 공부 정리", "#f43f5e", "DesignCraft"),
        (["figma", "figjam", "mcp"], "FigJam MCP 연동 공부 정리", "#a855f7", "Design"),
        (["react", "actions"], "React 19 Actions 훑어보면서", "#3b82f6", "Frontend"),
        (["toss", "pqc"], "토스페이먼츠 PQC 도입기", "#f43f5e", "DesignCraft"),

        # ===== 카테고리 팔레트 (2순위) — 매칭 안 됨 =====
        (["unknown1"], "정체불명 글 1", "#3b82f6", "Frontend"),
        (["unknown2"], "정체불명 글 2", "#3b82f6", "Frontend"),
        (["unknown3"], "정체불명 글 3", "#3b82f6", "Frontend"),
        (["something"], "Design 카테고리 폴백", "#a855f7", "Design"),
        (["something"], "DesignCraft 카테고리 폴백", "#f43f5e", "DesignCraft"),

        # ===== fallback (3순위) — 카테고리 없음 =====
        (["unknown"], "카테고리 없는 글", "#3b82f6", ""),
    ]
    print(f"{'색':10s}  [{'타입':10s}]  ← 제목 (카테고리)")
    print("-" * 80)
    for tags, title, fallback, category in cases:
        color = pick_color(tags, title, fallback, category)
        if color != fallback:
            # 브랜드 매칭인지 팔레트인지
            haystack = " ".join(tags + [title]).lower()
            is_brand = any(k in haystack for k in BRAND_COLORS)
            tag = "BRAND" if is_brand else "PALETTE"
        else:
            tag = "FALLBACK"
        print(f"  {color}  [{tag:10s}]  ← {title[:32]} ({category})")