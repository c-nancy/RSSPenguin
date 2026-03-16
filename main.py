import logging
import sys
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

from src.collector import collect_all
from src.filter import filter_articles
from src.formatter import format_report, save_report
from src.notifier import send_report

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def main():
    today = datetime.now(timezone.utc)
    week_start = today - timedelta(days=7)
    logger.info(f"Starting RSSPenguin weekly report for week of {week_start.strftime('%Y-%m-%d')}")

    articles = collect_all()
    logger.info(f"Total articles fetched: {len(articles)}")

    filtered = filter_articles(articles)
    logger.info(f"Articles after filtering: {len(filtered)}")

    report = format_report(filtered, date=today, week_start=week_start)
    path = save_report(report, date=today)
    logger.info(f"Report saved to {path}")

    subject = f"Penguin News — Week of {week_start.strftime('%Y-%m-%d')}"
    send_report(subject, report)


if __name__ == "__main__":
    main()
