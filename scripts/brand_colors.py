"""
brand_colors.py
---------------
키워드별 브랜드 컬러 매핑.
글의 tags/title에서 브랜드 키워드가 매칭되면 그 브랜드의 공식 색을 사용.
매칭 안 되면 카테고리 기본 색(sources.yml의 color_start)으로 폴백.

색 톤은 Jerry가 4월 22일에 직접 만든 카드들(automation.png 초록,
claude.png 주황)과 결을 맞춤.

사용법:
    from brand_colors import pick_color
    bg = pick_color(tags=["react", "actions"], title="...", fallback="#3b82f6")
"""
from __future__ import annotations

# 브랜드 공식 컬러 또는 그 브랜드를 떠올리게 하는 색
# 키는 소문자, tags나 title에 포함되면 매칭
# dict 순서가 매칭 우선순위 (먼저 정의된 게 이김)
BRAND_COLORS: dict[str, str] = {
    # ========== AI / LLM / 에이전트 ==========
    # Claude는 사용자 손글씨 카드(claude.png)와 같은 톤
    "claude": "#ff7847",          # Claude 진한 주황
    "anthropic": "#ff7847",
    "mcp": "#ff7847",
    "openai": "#10a37f",          # OpenAI 초록
    "gpt": "#10a37f",
    "cursor": "#000000",          # Cursor 검정
    "copilot": "#24292e",         # GitHub Copilot 다크 그레이
    "huggingface": "#ffd21e",     # HF 노랑
    "hugging-face": "#ffd21e",

    # ========== 디자인 도구 ==========
    "figma": "#a259ff",           # Figma 보라
    "webflow": "#146ef5",         # Webflow 파랑
    "framer": "#0055ff",          # Framer 파랑
    "notion": "#191919",          # Notion 검정
    "linear": "#5e6ad2",          # Linear 보라

    # ========== 프레임워크 / 빌드 도구 ==========
    "react": "#087ea4",           # React 공식 진한 파랑
    "next": "#000000",            # Next.js 검정
    "nextjs": "#000000",
    "next-js": "#000000",
    "vercel": "#000000",
    "vue": "#42b883",             # Vue 초록
    "svelte": "#ff3e00",          # Svelte 주황
    "astro": "#ff5d01",           # Astro 주황
    "nuxt": "#00dc82",            # Nuxt 형광 초록
    "tailwind": "#06b6d4",        # Tailwind 청록
    "vite": "#646cff",            # Vite 보라
    "remix": "#000000",
    "solid": "#2c4f7c",           # SolidJS 파랑

    # ========== 언어 ==========
    "typescript": "#3178c6",      # TS 파랑
    "javascript": "#f7df1e",      # JS 노랑
    "ecmascript": "#f7df1e",
    "python": "#3776ab",          # Python 파랑
    "rust": "#dea584",            # Rust 베이지
    "go": "#00add8",              # Go 청록

    # ========== 한국 기업 ==========
    "toss": "#0064ff",            # Toss 파랑
    "tosspayments": "#0064ff",
    "pxd": "#1a1a1a",             # PXD 다크
    "banksalad": "#26d063",       # 뱅크샐러드 초록
    "woowahan": "#2ac1bc",        # 우아한 청록
    "kakao": "#fee500",           # 카카오 노랑
    "naver": "#03c75a",           # 네이버 초록
    "line": "#06c755",            # 라인 초록

    # ========== 개발자 플랫폼 / 자동화 ==========
    # automation 키워드 = automation.png 초록 톤
    "automation": "#34a853",
    "github-actions": "#34a853",
    "ci-cd": "#34a853",
    "ci": "#34a853",
    "workflow": "#34a853",

    "github": "#24292e",          # GitHub 다크
    "git": "#f05033",             # Git 주황빨강
    "jetbrains": "#fe2857",       # JetBrains 핑크/레드
    "supabase": "#3ecf8e",        # Supabase 초록
    "stack-overflow": "#f48024",
    "stackoverflow": "#f48024",
    "docker": "#2496ed",          # Docker 파랑
    "kubernetes": "#326ce5",      # k8s 파랑

    # ========== 디자인 토픽 ==========
    "design-system": "#8b5cf6",   # 디자인 시스템 = 보라
    "design-systems": "#8b5cf6",
    "ux": "#ec4899",              # UX = 분홍
    "ui": "#ec4899",
    "accessibility": "#0ea5e9",   # 접근성 = 하늘
    "a11y": "#0ea5e9",
}


def pick_color(
    tags: list[str],
    title: str,
    fallback: str,
) -> str:
    """
    매칭되는 브랜드 컬러가 있으면 그 색, 없으면 fallback(카테고리 기본 색).
    매칭 우선순위는 BRAND_COLORS dict의 순서를 따름.
    """
    haystack = " ".join(tags + [title]).lower()
    for key, color in BRAND_COLORS.items():
        if key in haystack:
            return color
    return fallback


if __name__ == "__main__":
    # 간단 테스트
    cases = [
        (["webflow", "claude", "mcp"], "Webflow Claude Connector 공부 정리", "#a855f7"),
        (["react", "actions"], "React 19 Actions 훑어보면서", "#3b82f6"),
        (["tailwind", "v4"], "Tailwind v4 디자인 토큰", "#3b82f6"),
        (["toss", "pqc"], "토스페이먼츠 PQC 도입기", "#f43f5e"),
        (["automation", "github-actions"], "깃 블로그 자동화 세팅", "#f59e0b"),
        (["design-system"], "디자인 시스템 구축기", "#a855f7"),
        (["ux"], "한국 디자인 일반 글", "#f43f5e"),
        (["unknown-keyword"], "매칭 안 되는 글", "#3b82f6"),
    ]
    for tags, title, fallback in cases:
        color = pick_color(tags, title, fallback)
        used = "BRAND" if color != fallback else "FALLBACK"
        print(f"  {color}  [{used:8s}]  ← {title[:34]}")
