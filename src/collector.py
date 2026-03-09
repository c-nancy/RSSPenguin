import feedparser
import yaml
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

CONFIG_PATH = Path(__file__).parent.parent / "config" / "sources.yaml"


def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def fetch_feed(feed: dict) -> list[dict]:
    """Fetch and parse a single RSS feed. Returns list of article dicts."""
    articles = []
    try:
        parsed = feedparser.parse(feed["url"])
        for entry in parsed.entries:
            published = entry.get("published_parsed") or entry.get("updated_parsed")
            articles.append({
                "source": feed["name"],
                "type": feed.get("type", "news"),
                "title": entry.get("title", "").strip(),
                "url": entry.get("link", ""),
                "summary": entry.get("summary", "").strip(),
                "published": datetime(*published[:6], tzinfo=timezone.utc) if published else None,
            })
        logger.info(f"Fetched {len(articles)} articles from {feed['name']}")
    except Exception as e:
        logger.warning(f"Failed to fetch {feed['name']}: {e}")
    return articles


def collect_all() -> list[dict]:
    """Fetch articles from all configured RSS feeds."""
    config = load_config()
    all_articles = []
    for feed in config["feeds"]:
        all_articles.extend(fetch_feed(feed))
    return all_articles
