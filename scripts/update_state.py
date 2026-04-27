"""
update_state.py (CLI)
---------------------
포스트 생성 성공 후 state.json 업데이트.
Claude Code가 JSON을 stdin으로 흘려넣어 호출.

사용 예 (권장 - heredoc):
  python scripts/update_state.py <<'JSON'
  {
    "category_index": 1,
    "category_id": "design-craft",
    "source_url": "https://toss.tech/article/...",
    "post_title": "토스가 큰 글씨 모드를 만든 과정"
  }
  JSON

또는 echo 파이프:
  echo '{"category_index":1,"category_id":"...","source_url":"...","post_title":"..."}' \
    | python scripts/update_state.py

필수 키 4개 누락 시 종료 코드 1.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from state_manager import StateManager

REQUIRED_KEYS = {"category_index", "category_id", "source_url", "post_title"}


def _err(msg: str) -> None:
    print(f"❌ {msg}", file=sys.stderr)


def main() -> int:
    # 1. stdin에서 JSON 읽기
    raw = sys.stdin.read()
    if not raw.strip():
        _err("stdin이 비어있습니다. JSON을 파이프로 넘겨주세요.")
        return 1

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        _err(f"stdin JSON 파싱 실패: {e}")
        return 1

    if not isinstance(payload, dict):
        _err("JSON 최상위는 객체여야 합니다.")
        return 1

    # 2. 필수 키 검증
    missing = REQUIRED_KEYS - payload.keys()
    if missing:
        _err(f"필수 키 누락: {', '.join(sorted(missing))}")
        return 1

    # 3. category_index 타입 보정
    try:
        category_index = int(payload["category_index"])
    except (TypeError, ValueError):
        _err("category_index는 정수여야 합니다.")
        return 1

    # 4. state.json 업데이트
    state_path = Path(__file__).resolve().parent / "state.json"
    state = StateManager(state_path)
    state.record_post(
        category_index=category_index,
        category_id=str(payload["category_id"]),
        source_url=str(payload["source_url"]),
        post_title=str(payload["post_title"]),
    )
    state.save()

    print(
        f"✅ state.json 업데이트 완료 "
        f"(카테고리 인덱스: {category_index}, "
        f"누적 {state.data['posts_generated']}개)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())