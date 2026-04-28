"""
make_thumbnail.py (CLI) v4
--------------------------
사용법:
  python scripts/make_thumbnail.py <title> <category_label> <color_start> <color_end> <output_path> [keyword] [tags_csv]

예:
  python scripts/make_thumbnail.py \
    "Webflow Claude Connector 공부 정리" \
    "Design" \
    "#a855f7" "#ec4899" \
    "assets/img/thumbnail/webflow-claude-connector-study-note.png" \
    "webflow" \
    "webflow,claude,mcp"

v4 변경:
- thumbnail.py 단색 카드 (Pretendard ExtraBold + 흰색 텍스트)
- keyword_extractor로 라벨 자동 추출
- tags_csv 인자 추가 (선택, 없으면 keyword만 사용)
"""

import sys
from pathlib import Path

from thumbnail import generate_thumbnail


def main() -> int:
    if len(sys.argv) < 6:
        print(
            "사용법: python make_thumbnail.py <title> <category_label> "
            "<color_start> <color_end> <output_path> [keyword] [tags_csv]",
            file=sys.stderr,
        )
        return 1

    title = sys.argv[1]
    category_label = sys.argv[2]
    color_start = sys.argv[3]
    color_end = sys.argv[4]
    output_path = Path(sys.argv[5])
    keyword = sys.argv[6] if len(sys.argv) >= 7 else ""

    # tags_csv가 있으면 쪼개서 list로
    tags: list[str] = []
    if len(sys.argv) >= 8 and sys.argv[7]:
        tags = [t.strip() for t in sys.argv[7].split(",") if t.strip()]

    result = generate_thumbnail(
        title=title,
        category_label=category_label,
        color_start=color_start,
        color_end=color_end,
        output_path=output_path,
        keyword=keyword,
        tags=tags,
    )
    print(f"✅ 썸네일 생성: {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())