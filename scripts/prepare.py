"""
prepare.py
----------
Claude Code Action 실행 전에 도는 스크립트.

흐름:
1. sources.yml + state.json 로드
2. state 기준 "다음 카테고리"부터 순회
   → 새 글 있으면 채택 / 없으면 자동으로 다음 카테고리로 폴백
3. 채택된 카테고리의 상위 N개를 candidates.json에 저장

state.json은 여기서 안 건드림. 포스트 생성 성공 후 update_state.py가 처리.
"""
from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

from crawler import crawl_category, load_sources
from state_manager import StateManager

SCRIPT_DIR = Path(__file__).resolve().parent
SOURCES_PATH = SCRIPT_DIR / "sources.yml"
STATE_PATH = SCRIPT_DIR / "state.json"
CANDIDATES_PATH = SCRIPT_DIR / "candidates.json"

TOP_N = 10  # Claude에 전달할 후보 최대 개수

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def collect_fresh(category: dict, state: StateManager) -> list:
    """카테고리 크롤링 → seen URL 제거 → fresh 후보 반환.
    크롤링이 터지면 빈 리스트 반환해서 폴백이 동작하도록."""
    try:
        candidates = crawl_category(category)
    except Exception as e:
        logger.warning(f"   ⚠️ 크롤링 실패: {e}")
        return []

    fresh = [c for c in candidates if not state.is_seen(c.url)]
    logger.info(f"   🆕 새 후보 {len(fresh)}개 / 전체 {len(candidates)}개")
    return fresh


def select_category(categories: list, state: StateManager):
    """state 기준 다음 카테고리부터 순회하며 fresh 후보가 있는 첫 카테고리 채택.

    Returns:
        (idx, category, fresh) 또는 None
    """
    n = len(categories)
    start_idx = state.next_category_index(n)

    for offset in range(n):
        idx = (start_idx + offset) % n
        category = categories[idx]
        prefix = "📂" if offset == 0 else "↪️ 폴백"
        logger.info(
            f"{prefix} [{idx}] {category['display_name']} ({category['korean_label']})"
        )

        fresh = collect_fresh(category, state)
        if fresh:
            if offset > 0:
                logger.info(f"   ✅ 폴백 성공 (원래 시작점: {start_idx})")
            return idx, category, fresh
        logger.info("")  # 카테고리 간 줄 띄우기

    return None


def write_candidates(idx: int, category: dict, fresh: list) -> int:
    """candidates.json 저장. Claude Code가 이 파일을 읽음."""
    top = fresh[:TOP_N]
    payload = {
        "category": {
            "id": category["id"],
            "display_name": category["display_name"],
            "korean_label": category["korean_label"],
            "color_start": category["color_start"],
            "color_end": category["color_end"],
        },
        "next_category_index": idx,
        "candidates": [c.to_dict() for c in top],
    }
    with CANDIDATES_PATH.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return len(top)


def main() -> int:
    logger.info("🚀 후보 수집 시작\n")

    sources_config = load_sources(str(SOURCES_PATH))
    categories = sources_config["categories"]
    state = StateManager(STATE_PATH)

    selection = select_category(categories, state)

    if selection is None:
        logger.warning("\n⚠️ 모든 카테고리에서 새 후보 없음 - 이번 턴 스킵")
        # 이전 실행 잔재 청소. 워크플로우의 -f 체크가 정확히 동작하도록.
        CANDIDATES_PATH.unlink(missing_ok=True)
        return 0

    idx, category, fresh = selection
    written = write_candidates(idx, category, fresh)
    logger.info(f"\n✅ candidates.json 저장: {category['display_name']} ({written}개)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        logger.exception(f"❌ 오류: {e}")
        sys.exit(1)
