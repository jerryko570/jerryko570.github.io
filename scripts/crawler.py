"""
crawler.py (library)
--------------------
RSS 피드 파싱 로직.
prepare.py에서 import해서 사용합니다.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from typing import List

import feedparser
import requests
import yaml
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# 너무 오래된 글은 제외 (최근 14일 이내만)
MAX_AGE_DAYS = 14


@dataclass
class Candidate:
    title: str
    url: str
    summary: str          # 원문 요약/초록
    published: str        # 발행일 ISO
    source: str           # 소스명 (예: "Smashing Magazine")
    category_id: str
    category_label: str   # 한글 카테고리명

    def to_dict(self) -> dict:
        return asdict(self)


def load_sources(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _clean_html(html_text: str) -> str:
    """HTML 태그 제거"""
    if not html_text:
        return ""
    soup = BeautifulSoup(html_text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _parse_date(entry) -> datetime | None:
    for key in ("published_parsed", "updated_parsed"):
        val = getattr(entry, key, None)
        if val:
            try:
                return datetime(*val[:6], tzinfo=timezone.utc)
            except Exception:
                continue
    return None


def fetch_feed(url: str, timeout: int = 15) -> list:
    """RSS 피드에서 엔트리 목록을 가져옵니다. 실패 시 빈 리스트."""
    try:
        resp = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; JerryBlogBot/1.0)",
                "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8",
            },
            timeout=timeout,
        )
        resp.raise_for_status()
        parsed = feedparser.parse(resp.content)
        return parsed.entries or []
    except Exception as e:
        logger.warning(f"  ⚠️ 피드 로딩 실패 [{url}]: {e}")
        return []


def crawl_category(category: dict) -> List[Candidate]:
    """주어진 카테고리의 모든 소스를 크롤링해서 후보 리스트 반환"""
    candidates: List[Candidate] = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)

    for source in category.get("sources", []):
        logger.info(f"  📡 크롤링 중: {source['name']}")
        entries = fetch_feed(source["url"])

        for entry in entries[:20]:  # 소스당 최대 20개
            published = _parse_date(entry)
            if published and published < cutoff:
                continue

            title = getattr(entry, "title", "").strip()
            link = getattr(entry, "link", "").strip()
            if not title or not link:
                continue

            raw_summary = (
                getattr(entry, "summary", "")
                or getattr(entry, "description", "")
                or ""
            )
            summary = _clean_html(raw_summary)
            if len(summary) > 2000:
                summary = summary[:2000] + "..."

            candidates.append(Candidate(
                title=title,
                url=link,
                summary=summary,
                published=published.isoformat() if published else "",
                source=source["name"],
                category_id=category["id"],
                category_label=category["korean_label"],
            ))

    candidates.sort(key=lambda c: c.published, reverse=True)
    logger.info(f"  ✅ 총 {len(candidates)}개 후보 수집됨")
    return candidates
