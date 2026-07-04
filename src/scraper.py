"""
Fetch and parse articles from the OptiSigns Zendesk Help Center API.

Responsibilities:
- Fetch published articles
- Handle pagination
- Return Article objects
"""
from typing import Any

import requests

from src.config import (
    ARTICLES_API_URL,
    DEFAULT_PAGE_SIZE,
    MAX_PAGES,
    REQUEST_TIMEOUT,
)
from src.models import Article

def fetch_articles() -> list[Article]:
    """Fetch articles from the Help Center."""
    articles: list[Article] = []
    next_page: str | None = ARTICLES_API_URL
    current_page = 0
    with requests.Session() as session:
        while next_page:
            current_page += 1
            response = _fetch_page(session, next_page)
            articles.extend(_parse_articles(response["articles"]))

            if MAX_PAGES > 0 and current_page >= MAX_PAGES:
                break

            next_page = response["next_page"]

    return articles

def _fetch_page(session: requests.Session,url: str) -> dict[str, Any]:
    """Fetch a single page from the Zendesk API."""
    params = {
        "per_page": DEFAULT_PAGE_SIZE
    }
    response = session.get(url,params=params,timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()


def _parse_articles(articles: list[dict[str,Any]]) -> list[Article]:
    """Convert raw API articles into Article objects."""
    return [
        Article(
            id=article["id"],
            title=article["title"],
            body=article["body"],
            html_url=article["html_url"],
            updated_at=article["updated_at"],
        )
        for article in articles
    ]

