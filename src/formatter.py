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


def _render_articles(items: list[dict], label: str | None = None) -> list[str]:
    lines = []
    for item in items:
        pub = item["published"].strftime("%b %d, %Y") if item["published"] else "Unknown date"
        lines.append(f"### [{item['title']}]({item['url']})")
        source_line = f"_{item['source']} — {pub}_"
        if label:
            source_line += f" _{label}_"
        lines.append(source_line)
        lines.append("")
        if item["summary"]:
            summary = _truncate(_strip_html(item["summary"]))
            lines.append(summary)
            lines.append("")
    return lines


MIN_ITEMS = 3


def _fill_to_min(current: list[dict], older: list[dict], item_type: str) -> tuple[list[dict], list[dict]]:
    """Return (current, fill) where fill contains older items needed to reach MIN_ITEMS."""
    needed = max(0, MIN_ITEMS - len(current))
    candidates = [a for a in older if a.get("type", "news") == item_type]
    return current, candidates[:needed]


def format_report(
    articles: list[dict],
    older_articles: list[dict] | None = None,
    date: datetime | None = None,
    week_start: datetime | None = None,
) -> str:
    if date is None:
        date = datetime.now(timezone.utc)
    if week_start is None:
        from datetime import timedelta
        week_start = date - timedelta(days=7)
    if older_articles is None:
        older_articles = []

    week_range = f"{week_start.strftime('%Y-%m-%d')} to {date.strftime('%Y-%m-%d')}"

    news = [a for a in articles if a.get("type", "news") == "news"]
    academic = [a for a in articles if a.get("type") == "academic"]

    news, news_fill = _fill_to_min(news, older_articles, "news")
    academic, academic_fill = _fill_to_min(academic, older_articles, "academic")

    lines = [
        f"# Penguin News Report — Week of {week_start.strftime('%Y-%m-%d')}",
        "",
        f"> Generated on {date.strftime('%Y-%m-%d %H:%M UTC')} "
        f"| Covering {week_range} "
        f"| {len(news)} news articles | {len(academic)} academic items",
        "",
        "---",
        "",
    ]

    # --- News section ---
    lines.append("## News & Media")
    lines.append("")
    if news or news_fill:
        lines.extend(_render_articles(news))
        if news_fill:
            lines.append("_Older picks to round out this week's reading:_")
            lines.append("")
            lines.extend(_render_articles(news_fill, label="· older"))
    else:
        lines.append("_No penguin-related news found this week._")
        lines.append("")

    lines.append("---")
    lines.append("")

    # --- Academic section ---
    lines.append("## Academic Research")
    lines.append("")
    if academic or academic_fill:
        lines.extend(_render_articles(academic))
        if academic_fill:
            lines.append("_Older picks to round out this week's reading:_")
            lines.append("")
            lines.extend(_render_articles(academic_fill, label="· older"))
    else:
        lines.append(
            "_No new academic papers matched this week. "
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
