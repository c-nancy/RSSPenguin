# RSSPenguin — Task Plan

## Goal
Build a daily penguin news aggregator that:
- Pulls from free RSS feeds
- Runs on GitHub Actions (daily cron)
- Outputs a Markdown report committed to the repo
- Emails the report via SendGrid free tier

---

## Phases

### Phase 1 — Project Scaffold [ ]
- [ ] Create project directory structure
- [ ] Write requirements.txt
- [ ] Write config/sources.yaml (RSS feed list + keywords)
- [ ] Write main.py entry point

### Phase 2 — Core Scripts [ ]
- [ ] src/collector.py — fetch & parse RSS feeds
- [ ] src/filter.py — deduplicate and keyword-filter articles
- [ ] src/formatter.py — render Markdown report
- [ ] src/notifier.py — send report via SendGrid

### Phase 3 — GitHub Actions Workflow [ ]
- [ ] .github/workflows/daily-report.yml
  - Cron: daily at 08:00 UTC
  - Steps: checkout, install deps, run main.py, commit report, send email

### Phase 4 — Documentation & Secrets Guide [ ]
- [ ] README.md with setup instructions
- [ ] Document required GitHub Secrets (SENDGRID_API_KEY, TO_EMAIL, FROM_EMAIL)

---

## Decisions
- Language: Python 3.11+
- RSS parsing: feedparser
- HTTP: requests
- Config: PyYAML
- Email: sendgrid SDK
- Report format: Markdown (.md)
- Scheduling: GitHub Actions cron
- Report storage: committed to reports/ in repo
