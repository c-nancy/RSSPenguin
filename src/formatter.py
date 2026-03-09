import re
from datetime import datetime, timezone
from pathlib import Path


REPORTS_DIR = Path(__file__).parent.parent / "reports"

# Curated fallback academic papers shown when no current research is found.
# Add more entries here as needed.
FALLBACK_PAPERS = [
    {
        "title": "Rapid population decline in Adélie penguins linked to climate-driven changes in prey availability",
        "url": "https://doi.org/10.1111/gcb.12382",
        "authors": "Ainley et al.",
        "year": "2014",
        "journal": "Global Change Biology",
        "summary": (
            "A landmark study documenting how shifts in Antarctic sea ice and krill availability "
            "are driving population declines in Adélie penguin colonies along the Antarctic Peninsula."
        ),
    },
    {
        "title": "Tracking the fate of emperor penguin colonies amid sea-ice loss",
        "url": "https://doi.org/10.1038/s41558-022-01323-9",
        "authors": "Fretwell et al.",
        "year": "2022",
        "journal": "Nature Climate Change",
        "summary": (
            "Satellite imagery reveals that four emperor penguin colonies experienced catastrophic "
            "breeding failure in 2022 following unprecedented early sea-ice loss — the first "
            "recorded event of this scale."
        ),
    },
    {
        "title": "African penguin population collapse: causes and conservation priorities",
        "url": "https://doi.org/10.1016/j.biocon.2018.12.010",
        "authors": "Sherley et al.",
        "year": "2018",
        "journal": "Biological Conservation",
        "summary": (
            "Comprehensive analysis of the 70% decline in African penguin numbers since 2000, "
            "attributing the collapse to commercial fisheries competition and climate-driven prey shifts."
        ),
    },
]


def _strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()


def _truncate(text: str, limit: int = 300) -> str:
    return text[:limit - 3] + "..." if len(text) > limit else text


def _render_articles(items: list[dict]) -> list[str]:
    lines = []
    for item in items:
        pub = item["published"].strftime("%b %d, %Y") if item["published"] else "Unknown date"
        lines.append(f"### [{item['title']}]({item['url']})")
        lines.append(f"_{item['source']} — {pub}_")
        lines.append("")
        if item["summary"]:
            summary = _truncate(_strip_html(item["summary"]))
            lines.append(summary)
            lines.append("")
    return lines


def format_report(articles: list[dict], date: datetime | None = None) -> str:
    if date is None:
        date = datetime.now(timezone.utc)
    date_str = date.strftime("%Y-%m-%d")

    news = [a for a in articles if a.get("type", "news") == "news"]
    academic = [a for a in articles if a.get("type") == "academic"]

    lines = [
        f"# Penguin News Report — {date_str}",
        "",
        f"> Generated on {date.strftime('%Y-%m-%d %H:%M UTC')} "
        f"| {len(news)} news articles | {len(academic)} academic items",
        "",
        "---",
        "",
    ]

    # --- News section ---
    lines.append("## News & Media")
    lines.append("")
    if news:
        lines.extend(_render_articles(news))
    else:
        lines.append("_No penguin-related news found today._")
        lines.append("")

    lines.append("---")
    lines.append("")

    # --- Academic section ---
    lines.append("## Academic Research")
    lines.append("")
    if academic:
        lines.extend(_render_articles(academic))
    else:
        lines.append(
            "_No new academic papers matched today. "
            "Here are recommended foundational studies:_"
        )
        lines.append("")
        for paper in FALLBACK_PAPERS:
            lines.append(f"### [{paper['title']}]({paper['url']})")
            lines.append(
                f"_{paper['authors']} ({paper['year']}) — {paper['journal']}_"
            )
            lines.append("")
            lines.append(paper["summary"])
            lines.append("")

    lines.append("---")
    lines.append("")

    return "\n".join(lines)


def save_report(content: str, date: datetime | None = None) -> Path:
    if date is None:
        date = datetime.now(timezone.utc)
    REPORTS_DIR.mkdir(exist_ok=True)
    path = REPORTS_DIR / f"{date.strftime('%Y-%m-%d')}.md"
    path.write_text(content, encoding="utf-8")
    return path
