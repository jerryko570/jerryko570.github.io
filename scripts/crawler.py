"""
crawler.py (library)
--------------------
RSS 피드 파싱 로직.
prepare.py에서 import해서 사용합니다.
실제 크롤링 일은 crawler.py가 함

v2 변경사항:
- MAX_AGE_DAYS: 14 → 60 (최근 1~2달 이내만)
- 공식 소스만 다루므로 발표 빈도가 낮아서 기간 확대
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
#
# 최근 60일 이내 (1~2달)
MAX_AGE_DAYS = 60


@dataclass
class Candidate:
    title: str
    url: str
    summary: str
    published: str
    source: str
    category_id: str
    category_label: str

    def to_dict(self) -> dict:
        return asdict(self)


def load_sources(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _clean_html(html_text: str) -> str:
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
    """주어진 카테고리의 모든 소스를 크롤링"""
    candidates: List[Candidate] = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)

    for source in category.get("sources", []):
        logger.info(f"  📡 크롤링 중: {source['name']}")
        entries = fetch_feed(source["url"])

        for entry in entries[:20]:
            published = _parse_date(entry)
            # 날짜 없으면 스킵 (공식 소스는 날짜 있어야 함)
            if not published or published < cutoff:
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
    logger.info(f"  ✅ 총 {len(candidates)}개 후보 수집됨 (최근 {MAX_AGE_DAYS}일 이내)")
    return candidates
