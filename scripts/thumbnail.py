"""
thumbnail.py v4 (library)
-------------------------
Jerry Figma 스펙:
- Font: Pretendard ExtraBold
- Line height: 0.9 (2줄은 1.05로 살짝 넉넉)
- Letter spacing: 0%
- Alignment: Center
- Fill: #FAFAFA (밝은 배경에서는 #1a1a1a 자동)
- 그림자 없음
- 배경: solid color 기본. color_start == color_end면 단색, 다르면 그라데이션.
- 자동 색상: color_start == "auto" 또는 빈 문자열이면 title 해시로 팔레트에서 픽.
- 멀티라인: keyword에 "\\n" 포함 시 2줄 렌더링.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

WIDTH, HEIGHT = 1200, 630

# 자동 배경 팔레트 — 주제별 수동 PNG(react.png, claude.png 등)에 쓰인 색과 구분되도록
# 선명한 단색 위주로 구성. 텍스트는 #FAFAFA와 자동 대비.
AUTO_PALETTE = [
    "#2DA44E",  # GitHub green (automation)
    "#FF6B35",  # Claude orange
    "#1E88E5",  # blue
    "#7C3AED",  # purple
    "#E53935",  # red
    "#009688",  # teal
    "#EC407A",  # pink
    "#3949AB",  # indigo
    "#F59E0B",  # amber
    "#0F766E",  # deep teal
    "#C2410C",  # burnt orange
    "#4338CA",  # deep indigo
]

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


def _make_background(start_hex: str, end_hex: str) -> Image.Image:
    """start == end면 단색, 아니면 대각선 그라데이션."""
    start = _hex_to_rgb(start_hex)
    end = _hex_to_rgb(end_hex)

    if start == end:
        return Image.new("RGB", (WIDTH, HEIGHT), start)

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


def _pick_auto_color(seed: str) -> str:
    """title 해시로 팔레트에서 결정론적으로 픽 — 같은 제목은 같은 색."""
    digest = hashlib.md5((seed or "default").encode("utf-8")).digest()
    return AUTO_PALETTE[digest[0] % len(AUTO_PALETTE)]


def _resolve_colors(color_start: str, color_end: str, seed: str) -> Tuple[str, str]:
    """'auto'/빈 문자열은 팔레트 자동 선택. end가 비면 start와 동일(단색)."""
    cs = color_start.strip() if color_start else ""
    ce = color_end.strip() if color_end else ""
    if not cs or cs.lower() == "auto":
        cs = _pick_auto_color(seed)
    if not ce or ce.lower() == "auto":
        ce = cs
    return cs, ce


def _prepare_lines(keyword: str) -> list[str]:
    """키워드 → 1~2줄 리스트. '\\n' 포함 시 split, 아니면 단어 수로 판단."""
    if not keyword:
        return ["Study"]
    text = keyword.strip()
    # 명시적 줄바꿈이 있으면 그대로 사용
    if "\n" in text:
        return [ln.strip() for ln in text.split("\n") if ln.strip()][:2]
    # 단어 3개 이상이면 앞 2단어만, 그 외는 한 줄
    words = text.split()
    if len(words) > 2:
        return [" ".join(words[:2])]
    return [text]


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
        font_size = 180
    elif len(display) <= 10:
        font_size = 140
    elif len(display) <= 15:
        font_size = 110
    else:
        font_size = 90

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
