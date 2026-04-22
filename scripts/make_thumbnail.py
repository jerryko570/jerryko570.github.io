"""
make_thumbnail.py (CLI)
-----------------------
Claude Code가 subprocess로 호출하는 썸네일 생성 CLI.

사용법:
  python scripts/make_thumbnail.py "한글 제목" "카테고리 라벨" "#hexstart" "#hexend" "출력경로.png"
"""

import sys
from pathlib import Path

from thumbnail import generate_thumbnail


def main() -> int:
    if len(sys.argv) != 6:
        print(
            "사용법: python make_thumbnail.py <title> <category_label> <color_start> <color_end> <output_path>",
            file=sys.stderr,
        )
        return 1

    title = sys.argv[1]
    category_label = sys.argv[2]
    color_start = sys.argv[3]
    color_end = sys.argv[4]
    output_path = Path(sys.argv[5])

    result = generate_thumbnail(
        title=title,
        category_label=category_label,
        color_start=color_start,
        color_end=color_end,
        output_path=output_path,
    )
    print(f"✅ 썸네일 생성 완료: {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
