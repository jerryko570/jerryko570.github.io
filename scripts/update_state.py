"""
update_state.py (CLI)
---------------------
포스트 생성 성공 후 state.json을 업데이트하는 CLI.
Claude Code가 subprocess로 호출합니다.

사용법:
  python scripts/update_state.py <category_index> <source_url> <post_title> <category_id>
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 5:
        print(
            "사용법: python update_state.py <category_index> <source_url> <post_title> <category_id>",
            file=sys.stderr,
        )
        return 1

    category_index = int(sys.argv[1])
    source_url = sys.argv[2]
    post_title = sys.argv[3]
    category_id = sys.argv[4]

    state_path = Path(__file__).resolve().parent / "state.json"

    # 기존 상태 로드 (없으면 초기값)
    if state_path.exists():
        with state_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {
            "last_category_index": -1,
            "seen_url_hashes": [],
            "posts_generated": 0,
            "last_run": None,
            "history": [],
        }

    # URL 해시
    url_hash = hashlib.sha256(source_url.encode("utf-8")).hexdigest()[:16]

    # 상태 업데이트
    data["last_category_index"] = category_index
    if url_hash not in data["seen_url_hashes"]:
        data["seen_url_hashes"].append(url_hash)
    # 최근 500개만 유지 (무한 증가 방지)
    if len(data["seen_url_hashes"]) > 500:
        data["seen_url_hashes"] = data["seen_url_hashes"][-500:]

    data["posts_generated"] += 1
    data["last_run"] = datetime.now(timezone.utc).isoformat()
    data["history"].append({
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "category": category_id,
        "title": post_title,
        "source_url": source_url,
    })
    # 최근 50개만 유지
    if len(data["history"]) > 50:
        data["history"] = data["history"][-50:]

    # 저장
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with state_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ state.json 업데이트 완료 (카테고리 인덱스: {category_index}, 총 {data['posts_generated']}개 생성)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
