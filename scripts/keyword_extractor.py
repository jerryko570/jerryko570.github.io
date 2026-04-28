"""
keyword_extractor.py
--------------------
글의 tags, title, category에서 썸네일에 들어갈 영문 라벨 추출.

추출 우선순위:
1. HIGH_PRIORITY 키워드가 매칭되면 그것을 line1으로
2. MODIFIERS에서 보조 단어가 있으면 line2로 결합
3. 어느 것도 매칭 안 되면 카테고리 기반 폴백
"""
from __future__ import annotations

from typing import Optional

# 1순위: 강한 브랜드/기술 이름. (line1, default_line2)
# dict 순서가 매칭 우선순위 — 먼저 정의된 게 이김
HIGH_PRIORITY: dict[str, tuple[str, Optional[str]]] = {
    # ========== AI / LLM / 에이전트 ==========
    "claude": ("Claude", None),
    "anthropic": ("Anthropic", None),
    "openai": ("OpenAI", None),
    "gpt": ("GPT", None),
    "cursor": ("Cursor", None),
    "copilot": ("Copilot", None),
    "mcp": ("MCP", "Connector"),
    "huggingface": ("HuggingFace", None),
    "hugging-face": ("HuggingFace", None),
    "llm": ("LLM", None),

    # ========== 디자인 도구 ==========
    "figma": ("Figma", None),
    "webflow": ("Webflow", None),
    "framer": ("Framer", None),
    "notion": ("Notion", None),
    "linear": ("Linear", None),
    "sketch": ("Sketch", None),
    "protopie": ("ProtoPie", None),

    # ========== 프레임워크 / 빌드 도구 ==========
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
    "remix": ("Remix", None),
    "solid": ("Solid", None),

    # ========== 언어 ==========
    "typescript": ("TypeScript", None),
    "javascript": ("JavaScript", None),
    "ecmascript": ("ECMAScript", None),
    "python": ("Python", None),
    "rust": ("Rust", None),
    "golang": ("Go", None),

    # ========== 웹 플랫폼 / 표준 ==========
    "css": ("CSS", None),
    "html": ("HTML", None),
    "webgl": ("WebGL", None),
    "webgpu": ("WebGPU", None),
    "wasm": ("WASM", None),
    "webassembly": ("WASM", None),
    "baseline": ("Baseline", None),
    "web-platform": ("Web", "Platform"),

    # ========== 브라우저 ==========
    "chrome": ("Chrome", None),
    "chromium": ("Chromium", None),
    "firefox": ("Firefox", None),
    "safari": ("Safari", None),
    "edge": ("Edge", None),
    "webkit": ("WebKit", None),

    # ========== 한국 기업 ==========
    "tosspayments": ("Toss", "Payments"),
    "toss": ("Toss", "Tech"),
    "pxd": ("PXD", "Story"),
    "banksalad": ("Banksalad", None),
    "woowahan": ("Woowahan", None),
    "kakao": ("Kakao", None),
    "naver": ("Naver", None),
    "line": ("Line", None),
    "carrot": ("Carrot", None),
    "danggn": ("Danggeun", None),

    # ========== 개발자 플랫폼 / 도구 ==========
    "github": ("GitHub", None),
    "gitlab": ("GitLab", None),
    "jetbrains": ("JetBrains", None),
    "supabase": ("Supabase", None),
    "stack-overflow": ("Stack", "Overflow"),
    "stackoverflow": ("Stack", "Overflow"),
    "docker": ("Docker", None),
    "kubernetes": ("K8s", None),
    "k8s": ("K8s", None),

    # ========== 자동화 / DevOps ==========
    "github-actions": ("GitHub", "Actions"),
    "gh-actions": ("GitHub", "Actions"),
    "ci-cd": ("CI", "CD"),
    "cicd": ("CI", "CD"),
}

# 2순위: 보조 단어 (1순위와 결합 가능)
MODIFIERS: dict[str, str] = {
    # AI 관련
    "skills": "Skills",
    "agent": "Agent",
    "agents": "Agents",
    "connector": "Connector",
    "prompt": "Prompt",
    "tool-use": "Tools",

    # 디자인 시스템 / UX
    "design-system": "Design System",
    "design-systems": "Design System",
    "design-tools": "Design Tools",
    "design-tokens": "Tokens",
    "tokens": "Tokens",
    "a11y": "A11y",
    "accessibility": "A11y",

    # 릴리스 / 버전
    "release": "Release",
    "beta": "Beta",
    "alpha": "Alpha",
    "rc": "RC",
    "v3": "v3",
    "v4": "v4",
    "v5": "v5",
    "v6": "v6",
    "v18": "v18",
    "v19": "v19",
    "v20": "v20",

    # React / 프론트엔드 개념
    "hooks": "Hooks",
    "actions": "Actions",
    "rsc": "RSC",
    "compiler": "Compiler",
    "server-component": "Server",
    "server-components": "Server",
    "client-component": "Client",
    "ssr": "SSR",
    "ssg": "SSG",
    "isr": "ISR",
    "streaming": "Streaming",

    # 보안 / 인프라
    "pqc": "PQC",
    "security": "Security",
    "auth": "Auth",
    "oauth": "OAuth",
    "encryption": "Crypto",

    # 자동화 / 워크플로우
    "automation": "Automation",
    "workflow": "Workflow",
    "ci": "CI",
    "deploy": "Deploy",
    "deployment": "Deploy",

    # CSS / 스타일링
    "color": "Color",
    "typography": "Typography",
    "layout": "Layout",
    "grid": "Grid",
    "flexbox": "Flex",
    "container-query": "Container",

    # 성능 / 측정
    "performance": "Perf",
    "perf": "Perf",
    "core-web-vitals": "Vitals",
    "lighthouse": "Lighthouse",
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

    # 1. 강한 키워드 찾기 (dict 순서대로 먼저 매칭된 것을 사용)
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
    cases = [
        # 기존 검증
        (["webflow", "claude", "mcp"], "Webflow Claude Connector 공부 정리", "Design"),
        (["claude", "skills"], "Claude Skills 공부 정리", "DevTools"),
        (["react", "actions"], "React 19 Actions 훑어보면서", "Frontend"),
        (["tailwind", "v4"], "Tailwind v4 디자인 토큰", "Frontend"),
        (["toss", "pqc"], "토스페이먼츠 PQC 도입기 공부 정리", "DesignCraft"),
        (["ux"], "어떤 한국 디자인 글", "DesignCraft"),

        # 오늘 발행된 글 (이전엔 'Frontend Note'로 떨어졌음)
        (["chrome", "firefox", "css", "baseline"],
         "4월 웹 플랫폼 업데이트 공부 정리 | contrast-color()가 드디어 됐다",
         "Frontend"),

        # 새로 추가한 키워드들 검증
        (["github-actions", "automation"], "GitHub Actions 자동화 정리", "DevTools"),
        (["css", "container-query"], "CSS Container Query 공부", "Frontend"),
        (["accessibility"], "접근성 공부 정리", "Design"),
        (["performance", "core-web-vitals"], "웹 퍼포먼스 측정 정리", "Frontend"),
        (["docker", "deploy"], "Docker 배포 정리", "DevTools"),
    ]
    for tags, title, cat in cases:
        result = extract_label(tags, title, cat)
        print(f"  {str(result):35s}  ← {title[:38]}")