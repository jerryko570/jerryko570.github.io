"""
crawler.py (library)
--------------------
RSS/Atom 피드 파싱.
prepare.py에서 import해서 사용.
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from typing import List, Optional

import feedparser
import requests
import yaml
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# 최근 60일 이내 글만 수집 (공식 소스 발표 빈도 고려)
MAX_AGE_DAYS = 60

# 소스당 최대로 살펴볼 entry 수 (피드 후행 노이즈 방지)
MAX_ENTRIES_PER_SOURCE = 20

# summary 글자 수 상한 (Claude 프롬프트 크기 제어)
SUMMARY_MAX_CHARS = 2000


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
    return re.sub(r"\s+", " ", text).strip()


def _parse_date(entry) -> Optional[datetime]:
    for key in ("published_parsed", "updated_parsed"):
        val = getattr(entry, key, None)
        if val:
            try:
                return datetime(*val[:6], tzinfo=timezone.utc)
            except (TypeError, ValueError):
                continue
    return None


def _extract_summary(entry) -> str:
    """feedparser에서 본문/요약 추출. RSS와 Atom 모두 대응."""
    # 1순위: summary, description (RSS 표준)
    for key in ("summary", "description"):
        val = getattr(entry, key, None)
        if val:
            return val
    # 2순위: content[0].value (Atom 표준 — Vercel atom 등이 사용)
    content_list = getattr(entry, "content", None)
    if content_list:
        try:
            value = content_list[0].get("value")
            if value:
                return value
        except (IndexError, AttributeError, TypeError):
            pass
    return ""


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
        logger.warning(f"   ⚠️ 피드 로딩 실패 [{url}]: {e}")
        return []


def crawl_category(category: dict) -> List[Candidate]:
    """카테고리에 묶인 모든 소스를 크롤링해서 발행일 내림차순으로 반환."""
    candidates: List[Candidate] = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)

    for source in category.get("sources", []):
        logger.info(f"   📡 크롤링: {source['name']}")
        entries = fetch_feed(source["url"])

        for entry in entries[:MAX_ENTRIES_PER_SOURCE]:
            published = _parse_date(entry)
            # 날짜 없거나 cutoff 이전이면 스킵
            if not published or published < cutoff:
                continue

            title = (getattr(entry, "title", "") or "").strip()
            link = (getattr(entry, "link", "") or "").strip()
            if not title or not link:
                continue

            summary = _clean_html(_extract_summary(entry))
            if len(summary) > SUMMARY_MAX_CHARS:
                summary = summary[:SUMMARY_MAX_CHARS] + "..."

            candidates.append(Candidate(
                title=title,
                url=link,
                summary=summary,
                published=published.isoformat(),
                source=source["name"],
                category_id=category["id"],
                category_label=category["korean_label"],
            ))

    candidates.sort(key=lambda c: c.published, reverse=True)
    logger.info(
        f"   ✅ 총 {len(candidates)}개 후보 (최근 {MAX_AGE_DAYS}일 이내)"
    )
    return candidates