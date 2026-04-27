"""
state_manager.py
----------------
중복 방지 및 카테고리 순환 상태 관리.
prepare.py(읽기 전용)와 update_state.py(쓰기) 양쪽에서 사용.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# 디폴트 state — 두 파일에서 같은 곳을 보도록 한 곳에 모음
DEFAULT_STATE: dict[str, Any] = {
    "last_category_index": -1,  # 첫 실행 시 0번부터 시작
    "seen_url_hashes": [],
    "posts_generated": 0,
    "last_run": None,
    "history": [],
}

# 무한 증가 방지 상한
MAX_SEEN_HASHES = 500
MAX_HISTORY = 50


def _hash_url(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]


def _atomic_write_json(path: Path, data: dict) -> None:
    """원자적 JSON 쓰기. 쓰기 도중 프로세스가 죽어도 부분 파일이 남지 않음."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".state-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)  # 같은 FS 내 원자적 교체
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


class StateManager:
    def __init__(self, state_path: Path):
        self.state_path = Path(state_path)
        self.data = self._load()

    def _load(self) -> dict:
        if not self.state_path.exists():
            return dict(DEFAULT_STATE)
        try:
            with self.state_path.open("r", encoding="utf-8") as f:
                loaded = json.load(f)
        except json.JSONDecodeError:
            # state.json 손상 → 기본값으로 복구 (워크플로우 멈추지 않게)
            return dict(DEFAULT_STATE)
        # 누락된 필드는 기본값으로 보강 (구버전 state.json 호환)
        return {**DEFAULT_STATE, **loaded}

    def save(self) -> None:
        _atomic_write_json(self.state_path, self.data)

    # --- 카테고리 순환 ---
    def next_category_index(self, total_categories: int) -> int:
        return (self.data["last_category_index"] + 1) % total_categories

    def set_category_index(self, idx: int) -> None:
        self.data["last_category_index"] = idx

    # --- 중복 방지 ---
    @staticmethod
    def hash_url(url: str) -> str:
        return _hash_url(url)

    def is_seen(self, url: str) -> bool:
        return _hash_url(url) in self.data["seen_url_hashes"]

    def mark_seen(self, url: str) -> None:
        h = _hash_url(url)
        hashes = self.data["seen_url_hashes"]
        if h not in hashes:
            hashes.append(h)
        if len(hashes) > MAX_SEEN_HASHES:
            self.data["seen_url_hashes"] = hashes[-MAX_SEEN_HASHES:]

    # --- 포스트 발행 기록 (한 번에 처리) ---
    def record_post(
        self,
        category_index: int,
        category_id: str,
        source_url: str,
        post_title: str,
    ) -> None:
        """포스트 생성 성공 시 단일 진입점.
        카테고리 인덱스 갱신 + seen 마킹 + history 추가 + 카운터 + last_run."""
        now = datetime.now(timezone.utc)
        self.set_category_index(category_index)
        self.mark_seen(source_url)
        self.data["posts_generated"] += 1
        self.data["last_run"] = now.isoformat()
        self.data["history"].append({
            "date": now.strftime("%Y-%m-%d"),
            "category": category_id,
            "title": post_title,
            "source_url": source_url,
        })
        if len(self.data["history"]) > MAX_HISTORY:
            self.data["history"] = self.data["history"][-MAX_HISTORY:]