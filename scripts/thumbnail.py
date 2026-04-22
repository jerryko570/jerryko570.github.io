"""
thumbnail.py (library)
----------------------
PIL 기반 썸네일 생성 로직.
make_thumbnail.py에서 CLI로 호출됨.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

# 썸네일 규격
WIDTH, HEIGHT = 1200, 630
PADDING = 80

# Ubuntu(GitHub Actions)의 한글 폰트 경로 + 로컬 개발 fallback
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
    """한글 지원 폰트 찾기. NotoSansCJK TTC의 인덱스 1 = 한국어(KR)."""
    for path in FONT_PATHS:
        if not Path(path).exists():
            continue
        try:
            if path.endswith(".ttc"):
                # TTC 순서: 0=JP, 1=KR, 2=SC, 3=TC, 4=HK
                return ImageFont.truetype(path, size=size, index=1)
            return ImageFont.truetype(path, size=size)
        except Exception as e:
            logger.debug(f"폰트 로드 실패 [{path}]: {e}")
            continue
    logger.warning("⚠️ 한글 지원 폰트를 찾지 못했습니다. 기본 폰트로 대체.")
    return ImageFont.load_default()


def _make_gradient(start_hex: str, end_hex: str) -> Image.Image:
    """대각선 방향 그라데이션 이미지 생성"""
    start = _hex_to_rgb(start_hex)
    end = _hex_to_rgb(end_hex)

    img = Image.new("RGB", (WIDTH, HEIGHT))
    pixels = img.load()

    for y in range(HEIGHT):
        for x in range(WIDTH):
            t = (x / WIDTH * 0.5 + y / HEIGHT * 0.5)
            r = int(start[0] + (end[0] - start[0]) * t)
            g = int(start[1] + (end[1] - start[1]) * t)
            b = int(start[2] + (end[2] - start[2]) * t)
            pixels[x, y] = (r, g, b)

    return img


def _draw_dark_overlay(img: Image.Image, opacity: int = 90) -> Image.Image:
    """텍스트 가독성을 위해 어두운 오버레이"""
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, opacity))
    return Image.alpha_composite(img, overlay)


def _wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """제목을 max_width에 맞춰 줄바꿈"""
    lines = []
    current = ""

    tokens = text.split()
    i = 0
    while i < len(tokens):
        token = tokens[i]
        test = (current + " " + token).strip() if current else token
        bbox = font.getbbox(test)
        width = bbox[2] - bbox[0]

        if width <= max_width:
            current = test
            i += 1
        else:
            if current:
                lines.append(current)
                current = ""
            else:
                # 단일 토큰이 너무 길면 글자 단위로 자름
                for ch_idx in range(1, len(token) + 1):
                    sub = token[:ch_idx]
                    bbox = font.getbbox(sub)
                    if bbox[2] - bbox[0] > max_width:
                        lines.append(token[:ch_idx - 1] if ch_idx > 1 else token[:1])
                        tokens[i] = token[ch_idx - 1:] if ch_idx > 1 else token[1:]
                        break
                else:
                    lines.append(token)
                    i += 1

    if current:
        lines.append(current)

    return lines[:4]  # 최대 4줄


def generate_thumbnail(
    title: str,
    category_label: str,
    color_start: str,
    color_end: str,
    output_path: Path,
) -> Path:
    """썸네일 생성 후 저장"""
    # 1. 그라데이션 배경
    img = _make_gradient(color_start, color_end).convert("RGBA")

    # 2. 어두운 오버레이
    img = _draw_dark_overlay(img, opacity=110)
    draw = ImageDraw.Draw(img)

    # 3. 카테고리 라벨 pill (어두운 배경 + 흰 글씨로 대비 확보)
    label_font = _find_font(28)
    label_text = category_label
    label_bbox = draw.textbbox((0, 0), label_text, font=label_font)
    label_w = label_bbox[2] - label_bbox[0]
    label_h = label_bbox[3] - label_bbox[1]
    label_x, label_y = PADDING, PADDING

    # 별도 레이어에서 pill 그리고 합성
    pill_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    pill_draw = ImageDraw.Draw(pill_layer)
    pill_draw.rounded_rectangle(
        [label_x - 20, label_y - 10, label_x + label_w + 20, label_y + label_h + 20],
        radius=28,
        fill=(0, 0, 0, 140),
    )
    img = Image.alpha_composite(img, pill_layer)
    draw = ImageDraw.Draw(img)
    draw.text((label_x, label_y), label_text, font=label_font, fill="white")

    # 4. 제목 (중앙 약간 아래)
    title_font_size = 72 if len(title) < 30 else 58
    title_font = _find_font(title_font_size)

    max_text_width = WIDTH - PADDING * 2
    lines = _wrap_text(title, title_font, max_text_width)

    line_height = int(title_font_size * 1.35)
    total_text_height = line_height * len(lines)
    start_y = (HEIGHT - total_text_height) // 2 + 20

    for idx, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=title_font)
        line_w = bbox[2] - bbox[0]
        x = (WIDTH - line_w) // 2
        y = start_y + idx * line_height
        # 그림자
        draw.text((x + 2, y + 2), line, font=title_font, fill=(0, 0, 0, 180))
        # 본문
        draw.text((x, y), line, font=title_font, fill="white")

    # 5. 하단 우측 브랜드
    brand_font = _find_font(22)
    brand_text = "Jerry's Blog"
    bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
    brand_w = bbox[2] - bbox[0]
    draw.text(
        (WIDTH - PADDING - brand_w, HEIGHT - PADDING - 20),
        brand_text,
        font=brand_font,
        fill=(255, 255, 255, 220),
    )

    # 저장
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(output_path, "PNG", optimize=True)
    logger.info(f"🖼️  썸네일 생성: {output_path.name}")
    return output_path
