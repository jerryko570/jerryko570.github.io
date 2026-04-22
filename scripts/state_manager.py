"""
state_manager.py
----------------
중복 방지 및 카테고리 순환 상태 관리.
prepare.py와 Claude Code 양쪽에서 사용.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


class StateManager:
    def __init__(self, state_path: Path):
        self.state_path = state_path
        self.data = self._load()

    def _load(self) -> dict:
        if self.state_path.exists():
            with self.state_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "last_category_index": -1,  # 첫 실행 시 0번부터 시작
            "seen_url_hashes": [],
            "posts_generated": 0,
            "last_run": None,
            "history": [],
        }

    def save(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        with self.state_path.open("w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def next_category_index(self, total_categories: int) -> int:
        return (self.data["last_category_index"] + 1) % total_categories

    @staticmethod
    def hash_url(url: str) -> str:
        return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]

    def is_seen(self, url: str) -> bool:
        return self.hash_url(url) in self.data["seen_url_hashes"]
