"""
make_thumbnail.py (CLI) v5
--------------------------
사용법:
  python scripts/make_thumbnail.py \
    <title> \
    <category_label> \
    <color_start> \
    <color_end> \
    <output_path> \
    [keyword] \
    [tags_csv] \
    [source]

예 (Webflow 글):
  python scripts/make_thumbnail.py \
    "Webflow Claude Connector 공부 정리" \
    "Design" \
    "#a855f7" "#ec4899" \
    "assets/img/thumbnail/webflow-claude-connector-study-note.png" \
    "webflow" \
    "webflow,claude,mcp" \
    "Webflow Blog"

v5 변경:
- source 인자 추가 (8번째, 선택)
- candidates.json의 source 값을 그대로 넘기면 됨
- 라벨이 출처 한 단어로 깔끔하게 떨어짐 (Webflow / Toss / React 등)
"""

import sys
from pathlib import Path

from thumbnail import generate_thumbnail


def main() -> int:
    if len(sys.argv) < 6:
        print(
            "사용법: python make_thumbnail.py <title> <category_label> "
            "<color_start> <color_end> <output_path> [keyword] [tags_csv] [source]",
            file=sys.stderr,
        )
        return 1

    title = sys.argv[1]
    category_label = sys.argv[2]
    color_start = sys.argv[3]
    color_end = sys.argv[4]
    output_path = Path(sys.argv[5])
    keyword = sys.argv[6] if len(sys.argv) >= 7 else ""

    # tags_csv (선택)
    tags: list[str] = []
    if len(sys.argv) >= 8 and sys.argv[7]:
        tags = [t.strip() for t in sys.argv[7].split(",") if t.strip()]

    # source (선택, 신규)
    source = sys.argv[8] if len(sys.argv) >= 9 else ""

    result = generate_thumbnail(
        title=title,
        category_label=category_label,
        color_start=color_start,
        color_end=color_end,
        output_path=output_path,
        keyword=keyword,
        tags=tags,
        source=source,
    )
    print(f"✅ 썸네일 생성: {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())