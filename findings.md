# Findings

## RSS Feed Sources (Penguin-related)
- https://feeds.bbci.co.uk/news/science_and_environment/rss.xml — BBC Science & Environment
- https://rss.nytimes.com/services/xml/rss/nyt/Science.xml — NYT Science
- https://www.nationalgeographic.com/animals/rss — Nat Geo Animals (may need verification)
- https://phys.org/rss-feed/biology-news/animals-and-plants/ — Phys.org Biology
- https://www.sciencedaily.com/rss/plants_animals/birds.xml — ScienceDaily Birds
- https://antarcticsun.usap.gov/feed/ — Antarctic Sun (direct penguin habitat news)

## Keywords for filtering
- penguin, penguins, penguin colony, emperor penguin, chinstrap, adelie, macaroni penguin,
  little blue penguin, African penguin, Spheniscidae, Antarctica, sub-Antarctic

## SendGrid
- Free tier: 100 emails/day forever
- SDK: sendgrid Python library
- Requires: verified sender email, API key from sendgrid.com
- HTML or plain text body supported — will send Markdown as HTML (converted inline)

## GitHub Actions
- Cron syntax for 08:00 UTC daily: `0 8 * * *`
- Needs: GITHUB_TOKEN (auto-provided) for committing reports
- Needs secrets: SENDGRID_API_KEY, TO_EMAIL, FROM_EMAIL
- Python setup: actions/setup-python@v5
- Commit step: uses git config + git add + git commit + git push
