"""
make_thumbnail.py (CLI) v2
--------------------------
사용법:
  python scripts/make_thumbnail.py <title> <category_label> <color_start> <color_end> <output_path> [keyword]

keyword: 중앙에 크게 표시할 영어 키워드 (예: "Next.js", "Claude", "Self Study")
         생략 시 title을 사용 (한글이면 폰트 크기 자동 축소)
"""

import sys
from pathlib import Path

from thumbnail import generate_thumbnail


def main() -> int:
    if len(sys.argv) < 6:
        print(
            "사용법: python make_thumbnail.py <title> <category_label> <color_start> <color_end> <output_path> [keyword]",
            file=sys.stderr,
        )
        return 1

    title = sys.argv[1]
    category_label = sys.argv[2]
    color_start = sys.argv[3]
    color_end = sys.argv[4]
    output_path = Path(sys.argv[5])
    keyword = sys.argv[6] if len(sys.argv) >= 7 else ""

    result = generate_thumbnail(
        title=title,
        category_label=category_label,
        color_start=color_start,
        color_end=color_end,
        output_path=output_path,
        keyword=keyword,
    )
    print(f"✅ 썸네일 생성 완료: {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
