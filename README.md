# RSSPenguin

Daily penguin news aggregator. Pulls from free RSS feeds, filters for penguin-related content, commits a Markdown report to this repo, and emails it via SendGrid.

## How it works

1. GitHub Actions triggers daily at 08:00 UTC
2. `main.py` fetches articles from RSS feeds in `config/sources.yaml`
3. Articles are filtered by penguin-related keywords
4. A Markdown report is saved to `reports/YYYY-MM-DD.md` and committed
5. The report is emailed to you via SendGrid

## Setup

### 1. Fork / clone this repo to your GitHub account

### 2. Get a SendGrid API key
- Sign up at https://sendgrid.com (free tier: 100 emails/day)
- Go to Settings → API Keys → Create API Key (Full Access)
- Verify your sender email under Settings → Sender Authentication

### 3. Add GitHub Secrets
Go to your repo → Settings → Secrets and variables → Actions → New repository secret

| Secret name | Value |
|---|---|
| `SENDGRID_API_KEY` | Your SendGrid API key |
| `TO_EMAIL` | Email address to receive reports |
| `FROM_EMAIL` | Your verified SendGrid sender email |

### 4. Enable GitHub Actions
Go to the Actions tab and enable workflows if prompted.

### 5. Test manually
Go to Actions → Daily Penguin News Report → Run workflow

## Local development

```bash
pip install -r requirements.txt

# Create a .env file
echo "SENDGRID_API_KEY=your_key" >> .env
echo "TO_EMAIL=you@example.com" >> .env
echo "FROM_EMAIL=verified@example.com" >> .env

python main.py
```

## Customize

- Add/remove RSS feeds: edit `config/sources.yaml`
- Add/remove keywords: edit the `keywords` list in `config/sources.yaml`
- Change schedule: edit the cron expression in `.github/workflows/daily-report.yml`

## Reports

Daily reports are stored in `reports/YYYY-MM-DD.md`.
