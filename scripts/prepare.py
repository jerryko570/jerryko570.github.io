"""
prepare.py (CLI)
----------------
Claude Code Action 실행 전에 돌아가는 스크립트.
1. state.json 읽어서 다음 카테고리 결정
2. 해당 카테고리 RSS 소스들 크롤링
3. 이미 본 URL 제외
4. candidates.json에 결과 저장 (Claude Code가 읽어감)

주의: state.json의 last_category_index는 여기서 건드리지 않음.
     Claude Code가 포스트 생성에 성공하면 그때 업데이트 (실패 시 같은 카테고리 재시도).
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

from crawler import crawl_category, load_sources
from state_manager import StateManager

# 경로
SCRIPT_DIR = Path(__file__).resolve().parent
SOURCES_PATH = SCRIPT_DIR / "sources.yml"
STATE_PATH = SCRIPT_DIR / "state.json"
CANDIDATES_PATH = SCRIPT_DIR / "candidates.json"

# 로깅
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def main() -> int:
    logger.info("🚀 후보 수집 시작\n")

    # 1. 설정 로드
    sources_config = load_sources(str(SOURCES_PATH))
    categories = sources_config["categories"]
    state = StateManager(STATE_PATH)

    # 2. 다음 카테고리 결정
    next_idx = state.next_category_index(len(categories))
    category = categories[next_idx]
    logger.info(f"📂 이번 차례 카테고리: {category['display_name']} ({category['korean_label']})")
    logger.info(f"   (인덱스: {next_idx})\n")

    # 3. 크롤링
    logger.info("🔍 최신 글 크롤링 중...")
    candidates = crawl_category(category)

    # 4. 이미 본 URL 필터링
    fresh = [c for c in candidates if not state.is_seen(c.url)]
    logger.info(f"\n  🆕 새로운 후보: {len(fresh)}개 (전체 {len(candidates)}개 중)\n")

    # 5. candidates.json 저장 (Claude Code가 읽어감)
    # 상위 10개만 전달해서 프롬프트 크기 제어
    top = fresh[:10]
    result = {
        "category": {
            "id": category["id"],
            "display_name": category["display_name"],
            "korean_label": category["korean_label"],
            "color_start": category["color_start"],
            "color_end": category["color_end"],
        },
        "next_category_index": next_idx,
        "candidates": [c.to_dict() for c in top],
    }

    with CANDIDATES_PATH.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    logger.info(f"✅ candidates.json 저장 완료 ({len(top)}개)")

    if not top:
        logger.warning("⚠️ 새로운 후보 없음 - 이번 턴은 생성 스킵")

    # state.json은 Claude Code가 성공적으로 포스트 생성 후 업데이트
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        logger.exception(f"❌ 오류: {e}")
        sys.exit(1)
