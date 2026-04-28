"""
thumbnail.py (v2)
-----------------
단색 배경 + 큰 흰색 텍스트 (1~2줄) 형태의 PNG 썸네일 생성.

배경색 결정 우선순위:
1. brand_colors.py에 매칭되는 브랜드 키워드 → 브랜드 공식 색
2. 매칭 없음 → sources.yml의 카테고리 color_start 사용

스타일:
- 단색 배경
- Pretendard ExtraBold (없으면 Noto Sans CJK Black fallback)
- 흰색 텍스트, line-height 1.0
- 자동 폰트 사이즈 조정 (라벨 길이에 맞춰)
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont

from brand_colors import pick_color
from keyword_extractor import extract_label

# 카드 크기 — Chirpy 카드 비율과 잘 맞음
WIDTH, HEIGHT = 1200, 800

# 텍스트 색 — Figma 사양(#FFFFFF) 그대로 순백
TEXT_COLOR = (255, 255, 255)

# Line height — Figma 사양 90% (폰트 사이즈의 0.9배)
LINE_HEIGHT_RATIO = 0.9

# 폰트 후보 (워크플로우에서 Pretendard 설치, 없으면 Noto fallback)
# macOS 로컬에서도 동작하도록 시스템 폰트 경로 다수 포함
FONT_CANDIDATES = [
    # 1. 워크플로우에서 설치하는 Pretendard (Linux)
    "/usr/share/fonts/truetype/pretendard/Pretendard-ExtraBold.otf",

    # 2. Linux Noto (워크플로우 fallback)
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Black.ttc",

    # 3. macOS 한글 지원 굵은 폰트들
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "/System/Library/Fonts/Supplemental/AppleSDGothicNeo.ttc",
    "/Library/Fonts/AppleSDGothicNeo.ttc",
    "/System/Library/Fonts/PingFang.ttc",                    # 한자도 가능
    "/System/Library/Fonts/Helvetica.ttc",                   # 한글 못 그리지만 영문 라벨엔 OK
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
]


def _load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    # 시스템 폰트를 못 찾은 경우 — default font는 매우 작은 비트맵이라
    # 카드에 글씨가 거의 안 보이게 됨. 사용자가 알 수 있도록 경고.
    import sys
    print(
        "⚠️  시스템에서 사용 가능한 폰트를 찾지 못했습니다. "
        "PIL default font를 사용하므로 텍스트가 매우 작게 나옵니다.\n"
        "    macOS: AppleSDGothicNeo가 보통 /System/Library/Fonts/에 있습니다.\n"
        "    Linux: fonts-noto-cjk 패키지를 설치하세요.",
        file=sys.stderr,
    )
    return ImageFont.load_default()


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _fit_font_size(
    draw: ImageDraw.ImageDraw,
    text: str,
    max_width: int,
    start_size: int = 200,
    min_size: int = 80,
) -> int:
    """텍스트가 max_width 안에 들어가는 가장 큰 폰트 크기를 반환."""
    size = start_size
    while size > min_size:
        font = _load_font(size)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return size
        size -= 8
    return min_size


def generate_thumbnail(
    title: str,
    category_label: str,
    color_start: str,
    color_end: str,  # 인터페이스 호환용 (단색 모드라 미사용)
    output_path: Path,
    keyword: str = "",
    tags: Optional[list[str]] = None,
    source: str = "",
) -> Path:
    """단색 배경 + 큰 흰 텍스트 PNG 생성. output_path 반환."""
    tags = tags or ([keyword] if keyword else [])

    # 1. 라벨 추출 — source가 있으면 그게 1순위, 없으면 tags/title 매칭
    line1, line2 = extract_label(tags, title, category_label, source=source)
    lines = [line1] + ([line2] if line2 else [])

    # 2. 배경색 결정 — 브랜드 매칭 우선, 없으면 카테고리 기본 색
    bg_hex = pick_color(tags, title, fallback=color_start)
    img = Image.new("RGB", (WIDTH, HEIGHT), _hex_to_rgb(bg_hex))
    draw = ImageDraw.Draw(img)

    # 3. 가장 긴 줄에 맞춰 폰트 사이즈 자동 조정
    margin = 100
    max_text_width = WIDTH - margin * 2
    longest = max(lines, key=len)
    font_size = _fit_font_size(draw, longest, max_text_width)
    font = _load_font(font_size)

    # 4. 두 줄 중앙 정렬 — line-height 90% (Figma 사양)
    line_height = int(font_size * LINE_HEIGHT_RATIO)
    total_height = line_height * len(lines)
    start_y = (HEIGHT - total_height) // 2

    # 한글 폰트 baseline 보정 — ascent가 커서 살짝 위로 올라감
    start_y -= int(font_size * 0.08)

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (WIDTH - text_width) // 2
        y = start_y + i * line_height
        draw.text((x, y), line, font=font, fill=TEXT_COLOR)

    # 5. 저장
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG", optimize=True)
    return output_path


if __name__ == "__main__":
    # 로컬 테스트: tmp 폴더에 샘플 4장 만들기
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        cases = [
            ("webflow", ["webflow", "claude", "mcp"],
             "Webflow Claude Connector 공부 정리", "Design",
             "#a855f7", "#ec4899"),
            ("claude-skills", ["claude", "skills"],
             "Claude Skills 공부 정리", "DevTools",
             "#f59e0b", "#ea580c"),
            ("react", ["react", "actions"],
             "React 19 Actions 훑어보면서", "Frontend",
             "#3b82f6", "#06b6d4"),
            ("toss", ["toss", "pqc"],
             "토스페이먼츠 PQC 도입기 공부 정리", "DesignCraft",
             "#f43f5e", "#fb923c"),
        ]
        for slug, tags, title, cat, c1, c2 in cases:
            out = tmp_dir / f"{slug}.png"
            generate_thumbnail(title, cat, c1, c2, out, tags=tags)
            print(f"  ✅ {out}")