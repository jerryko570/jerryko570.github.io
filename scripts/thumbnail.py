"""
thumbnail.py v2 (library)
-------------------------
Jerry 스타일 썸네일: 영어 키워드 하나만 크게 중앙정렬

특징:
- 영어 키워드 1~2개만 크게
- 중앙정렬
- 깔끔한 그라데이션 배경
- 라벨/워터마크 없음
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

# 썸네일 규격
WIDTH, HEIGHT = 1200, 630

FONT_PATHS = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
    "/System/Library/Fonts/AppleSDGothicNeo.ttc",
    "C:/Windows/Fonts/malgun.ttf",
]


def _hex_to_rgb(hex_code: str) -> Tuple[int, int, int]:
    hex_code = hex_code.lstrip("#")
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))


def _find_font(size: int) -> ImageFont.FreeTypeFont:
    """한글+영문 지원 폰트 찾기"""
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
    logger.warning("⚠️ 한글 지원 폰트를 찾지 못했습니다.")
    return ImageFont.load_default()


def _make_gradient(start_hex: str, end_hex: str) -> Image.Image:
    """대각선 방향 그라데이션"""
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
    """표시할 영어 키워드 (최대 2단어)"""
    if not keyword:
        return "Study"
    # 너무 길면 앞 1~2 단어만
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
    썸네일 생성.

    Args:
        title: (사용 안 함, 호환용)
        category_label: (사용 안 함, 호환용)
        color_start, color_end: 배경 그라데이션
        output_path: 저장 경로
        keyword: 중앙에 크게 표시할 영어 키워드 (예: "Next.js", "Self Study", "Claude")
    """
    # 배경 그라데이션
    img = _make_gradient(color_start, color_end).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 중앙에 표시할 키워드
    display = _get_keyword(keyword or title)

    # 키워드 길이에 따라 폰트 크기 동적 조정
    if len(display) <= 6:
        font_size = 220
    elif len(display) <= 10:
        font_size = 170
    elif len(display) <= 15:
        font_size = 130
    else:
        font_size = 100

    font = _find_font(font_size)

    # 텍스트 크기 측정
    bbox = draw.textbbox((0, 0), display, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # 너무 길면 폰트 한번 더 줄이기
    while text_w > WIDTH - 120 and font_size > 60:
        font_size -= 20
        font = _find_font(font_size)
        bbox = draw.textbbox((0, 0), display, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

    # 정확한 중앙 위치 계산 (bbox offset 고려)
    x = (WIDTH - text_w) // 2 - bbox[0]
    y = (HEIGHT - text_h) // 2 - bbox[1]

    # 살짝 그림자
    draw.text((x + 3, y + 3), display, font=font, fill=(0, 0, 0, 100))
    # 본문 (흰색)
    draw.text((x, y), display, font=font, fill="white")

    # 저장
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG", optimize=True)
    logger.info(f"🖼️  썸네일 생성: {output_path.name} (키워드: {display})")
    return output_path
