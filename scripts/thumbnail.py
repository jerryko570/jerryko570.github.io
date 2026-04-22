"""
thumbnail.py v3 (library)
-------------------------
Jerry Figma 스펙:
- Font: Pretendard ExtraBold
- Line height: 0.9
- Letter spacing: 0%
- Alignment: Center
- Fill: #FAFAFA (밝은 배경에서는 #1a1a1a 자동)
- 그림자 없음
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

WIDTH, HEIGHT = 1200, 630

# 폰트 우선순위
FONT_PATHS = [
    # GitHub Actions에서 설치되는 Pretendard
    "/usr/share/fonts/truetype/pretendard/Pretendard-ExtraBold.otf",
    "/usr/share/fonts/opentype/pretendard/Pretendard-ExtraBold.otf",
    # Mac 로컬 (Jerry가 설치했다면)
    str(Path.home() / "Library/Fonts/Pretendard-ExtraBold.otf"),
    # Fallback: Noto (한글+영문 둘다 지원)
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "C:/Windows/Fonts/malgun.ttf",
]


def _hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    hex_code = hex_code.lstrip("#")
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))


def _luminance(rgb: Tuple[int, int, int]) -> float:
    """WCAG 상대 휘도 (0=어두움, 1=밝음)"""
    r, g, b = [c / 255.0 for c in rgb]

    def channel(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def _pick_text_color(bg_start: str, bg_end: str) -> str:
    """배경 평균 휘도로 텍스트 색 결정"""
    start = _hex_to_rgb(bg_start)
    end = _hex_to_rgb(bg_end)
    avg = tuple((s + e) / 2 for s, e in zip(start, end))
    lum = _luminance(avg)

    # 임계값 0.5
    return "#1a1a1a" if lum > 0.5 else "#FAFAFA"


def _find_font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_PATHS:
        if not Path(path).exists():
            continue
        try:
            if path.endswith(".ttc"):
                return ImageFont.truetype(path, size=size, index=1)
            return ImageFont.truetype(path, size=size)
        except Exception as e:
            logger.debug(f"폰트 로드 실패 [{path}]: {e}")
            continue
    logger.warning("⚠️ 폰트 없음 - 기본 폰트 사용")
    return ImageFont.load_default()


def _make_gradient(start_hex: str, end_hex: str) -> Image.Image:
    """대각선 그라데이션"""
    start = _hex_to_rgb(start_hex)
    end = _hex_to_rgb(end_hex)

    img = Image.new("RGB", (WIDTH, HEIGHT))
    pixels = img.load()

    for y in range(HEIGHT):
        for x in range(WIDTH):
            t = (x / WIDTH * 0.4 + y / HEIGHT * 0.6)
            r = int(start[0] + (end[0] - start[0]) * t)
            g = int(start[1] + (end[1] - start[1]) * t)
            b = int(start[2] + (end[2] - start[2]) * t)
            pixels[x, y] = (r, g, b)

    return img


def _get_keyword(keyword: str) -> str:
    """중앙 배치할 영어 키워드 (최대 2단어)"""
    if not keyword:
        return "Study"
    words = keyword.strip().split()
    if len(words) > 2:
        return " ".join(words[:2])
    return keyword.strip()


def generate_thumbnail(
    title: str,
    category_label: str,
    color_start: str,
    color_end: str,
    output_path: Path,
    keyword: str = "",
) -> Path:
    """
    Jerry 스펙 썸네일 생성.

    Args:
        title: 호환용 (사용 안 함)
        category_label: 호환용 (사용 안 함)
        color_start, color_end: 배경 그라데이션
        output_path: 저장 경로
        keyword: 중앙에 크게 쓸 영어 키워드 (예: "Claude", "Next.js")
    """
    # 배경
    img = _make_gradient(color_start, color_end).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 텍스트 색상 (배경 밝기 자동 반영)
    text_color = _pick_text_color(color_start, color_end)

    # 키워드
    display = _get_keyword(keyword or title)

    # 폰트 크기 (텍스트 길이에 따라)
    if len(display) <= 6:
        font_size = 260
    elif len(display) <= 10:
        font_size = 200
    elif len(display) <= 15:
        font_size = 150
    else:
        font_size = 120

    font = _find_font(font_size)

    # 텍스트 크기 측정
    bbox = draw.textbbox((0, 0), display, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # 너무 길면 줄이기
    while text_w > WIDTH - 120 and font_size > 60:
        font_size -= 20
        font = _find_font(font_size)
        bbox = draw.textbbox((0, 0), display, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

    # 중앙 정렬 (bbox offset 보정)
    x = (WIDTH - text_w) // 2 - bbox[0]
    y = (HEIGHT - text_h) // 2 - bbox[1]

    # 단색 텍스트만 (그림자 없음)
    draw.text((x, y), display, font=font, fill=text_color)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG", optimize=True)
    logger.info(f"🖼️ 썸네일: {output_path.name} (키워드: {display}, 색: {text_color})")
    return output_path
