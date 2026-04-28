# scripts/thumbnail.py
"""
SVG가 아닌 PNG로 생성. Chirpy 카드 톤(첨부 스샷)과 동일.
- 정사각에 가까운 1200x800 비율
- 단색 배경 (그라데이션은 옵션)
- Pretendard ExtraBold + 흰색 + 큰 두 줄
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from keyword_extractor import extract_label

# 카드 크기 — Chirpy 카드 비율에 잘 맞음
WIDTH, HEIGHT = 1200, 800

# 폰트 후보 (워크플로우에서 Pretendard 설치, 없으면 Noto fallback)
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/pretendard/Pretendard-ExtraBold.otf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Black.ttc",
]

# 텍스트 색
TEXT_COLOR = (250, 250, 250)


def _load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    # 최후 폴백
    return ImageFont.load_default()


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def _fit_font_size(draw, text: str, max_width: int, start_size: int = 180) -> int:
    """텍스트가 max_width 안에 들어가는 가장 큰 폰트 크기."""
    size = start_size
    while size > 60:
        font = _load_font(size)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return size
        size -= 8
    return size


def generate_thumbnail(
    title: str,
    category_label: str,
    color_start: str,
    color_end: str,
    output_path: Path,
    keyword: str = "",
    tags: list | None = None,
) -> Path:
    tags = tags or ([keyword] if keyword else [])

    # 라벨 추출 (최대 두 줄, 영문)
    line1, line2 = extract_label(tags, title, category_label)

    # 단색 배경 (color_start 사용 — 첨부 스샷과 동일 톤)
    img = Image.new("RGB", (WIDTH, HEIGHT), _hex_to_rgb(color_start))
    draw = ImageDraw.Draw(img)

    # 폰트 크기 자동 조정
    margin = 100
    max_text_width = WIDTH - margin * 2
    longest = max([line1] + ([line2] if line2 else []), key=len)
    font_size = _fit_font_size(draw, longest, max_text_width)
    font = _load_font(font_size)

    # 두 줄 중앙 배치
    line_height = int(font_size * 1.0)  # line-height 0.9~1.0
    lines = [line1] + ([line2] if line2 else [])
    total_height = line_height * len(lines)
    start_y = (HEIGHT - total_height) // 2

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (WIDTH - text_width) // 2
        y = start_y + i * line_height
        draw.text((x, y), line, font=font, fill=TEXT_COLOR)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG", optimize=True)
    return output_path