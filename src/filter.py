import re
import yaml
from datetime import datetime, timezone, timedelta
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config" / "sources.yaml"


def load_keywords() -> list[str]:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return [kw.lower() for kw in config.get("keywords", [])]


def matches_keywords(article: dict, keywords: list[str]) -> bool:
    text = f"{article['title']} {article['summary']}".lower()
    return any(kw in text for kw in keywords)


def deduplicate(articles: list[dict]) -> list[dict]:
    seen_urls = set()
    seen_titles = set()
    unique = []
    for article in articles:
        url = article["url"]
        # Normalize title for fuzzy dedup
        title_key = re.sub(r"\W+", " ", article["title"].lower()).strip()
        if url not in seen_urls and title_key not in seen_titles:
            seen_urls.add(url)
            seen_titles.add(title_key)
            unique.append(article)
    return unique


def filter_articles(articles: list[dict]) -> list[dict]:
    keywords = load_keywords()
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    recent = [a for a in articles if a["published"] is None or a["published"] >= cutoff]
    matched = [a for a in recent if matches_keywords(a, keywords)]
    return deduplicate(matched)


def filter_articles_older(articles: list[dict], exclude: list[dict]) -> list[dict]:
    """Return keyword-matched articles older than 7 days, excluding already-selected ones."""
    keywords = load_keywords()
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    exclude_urls = {a["url"] for a in exclude}
    older = [
        a for a in articles
        if a["published"] is not None and a["published"] < cutoff
        and matches_keywords(a, keywords)
        and a["url"] not in exclude_urls
    ]
    # Sort by most recent first so we pick the closest-to-now older articles
    older.sort(key=lambda a: a["published"], reverse=True)
    return deduplicate(older)
