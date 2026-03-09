import re
import yaml
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
    matched = [a for a in articles if matches_keywords(a, keywords)]
    return deduplicate(matched)
