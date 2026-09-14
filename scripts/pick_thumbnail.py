"""
pick_thumbnail.py (v1)
----------------------
주제(브랜드)별 **공유 썸네일**을 선택한다.
포스트마다 새 이미지를 만들지 않고, 같은 주제의 글은 항상 같은 PNG 1장을
재사용한다 → 색이 항상 일관되고, 파일이 쌓이지 않음.

기존 로직 재활용:
- keyword_extractor.extract_label() → 주제 라벨 (예: "Toss", "Figma", "Next.js")
- brand_colors.pick_color()         → 브랜드 색
- thumbnail.generate_thumbnail()     → 실제 렌더 (라벨 텍스트 카드)

동작:
1. source/tags/title로 주제 라벨 결정
2. 라벨을 안정적인 slug로 변환 → assets/img/thumbnail/<slug>.png 가 "공유 파일"
3. 그 파일이 이미 있으면 그대로 재사용 (재생성 X → 색 고정)
4. 없으면 브랜드 색 + 라벨로 딱 한 번 생성
5. 표준출력으로 프론트매터용 웹 경로(/assets/img/thumbnail/<slug>.png) 한 줄 출력

사용법:
  python scripts/pick_thumbnail.py <source> <tags_csv> <title> [category]

예:
  python scripts/pick_thumbnail.py "Toss Tech" "toss,qa,frontend" "토스 QA 자동화 공부" "Frontend"
  # → /assets/img/thumbnail/toss.png   (없으면 1회 생성, 있으면 재사용)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from brand_colors import pick_color
from keyword_extractor import extract_label
from thumbnail import generate_thumbnail

# 썸네일 저장 폴더 (레포 루트 기준 상대 경로)
THUMB_DIR = Path("assets/img/thumbnail")


def _slugify(line1: str, line2: str | None) -> str:
    """주제 라벨을 안정적인 파일 slug로 변환.

    "Next.js"        → "next-js"   (기존 next-js.png 와 매칭)
    "React"          → "react"     (기존 react.png 와 매칭)
    ("Design","System") → "design-system"
    같은 라벨은 항상 같은 slug → 같은 파일 재사용.
    """
    raw = line1 if not line2 else f"{line1}-{line2}"
    s = raw.lower().strip()
    s = s.replace(".", "-").replace(" ", "-").replace("_", "-")
    # 안전 문자(영소문자/숫자/한글/하이픈)만 남김
    s = re.sub(r"[^a-z0-9가-힣-]", "", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "study"


def pick_thumbnail(source: str, tags: list[str], title: str, category: str) -> Path:
    """주제 공유 썸네일 경로를 반환. 없으면 1회 생성."""
    line1, line2 = extract_label(tags, title, category, source=source)
    slug = _slugify(line1, line2)
    out = THUMB_DIR / f"{slug}.png"

    if not out.exists():
        # 색은 generate_thumbnail 내부에서도 pick_color로 다시 정하지만,
        # fallback으로 브랜드 색을 넘겨 매칭 실패 시에도 흔들리지 않게 함.
        color = pick_color(tags, title, fallback="#3b82f6", category=category)
        generate_thumbnail(
            title=title,
            category_label=category,
            color_start=color,
            color_end=color,
            output_path=out,
            tags=tags,
            source=source,
        )
    return out


def main() -> int:
    if len(sys.argv) < 4:
        print(
            "사용법: python pick_thumbnail.py <source> <tags_csv> <title> [category]",
            file=sys.stderr,
        )
        return 1

    source = sys.argv[1]
    tags = [t.strip() for t in sys.argv[2].split(",") if t.strip()]
    title = sys.argv[3]
    category = sys.argv[4] if len(sys.argv) >= 5 else ""

    out = pick_thumbnail(source, tags, title, category)
    # 프론트매터 image.path 용 웹 경로 (맨 앞 "/" 붙임)
    print("/" + out.as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
