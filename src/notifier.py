import os
import re
import logging
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

logger = logging.getLogger(__name__)


def markdown_to_html(md: str) -> str:
    """Minimal Markdown-to-HTML conversion for email."""
    html = md
    html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
    html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"_(.+?)_", r"<em>\1</em>", html)
    html = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', html)
    html = re.sub(r"^> (.+)$", r"<blockquote>\1</blockquote>", html, flags=re.MULTILINE)
    html = html.replace("---", "<hr>")
    paragraphs = html.split("\n\n")
    html = "".join(
        p if p.strip().startswith("<") else f"<p>{p.strip()}</p>"
        for p in paragraphs if p.strip()
    )
    return html


def send_report(subject: str, markdown_content: str) -> bool:
    api_key = os.environ.get("BREVO_API_KEY")
    to_email = os.environ.get("TO_EMAIL")
    from_email = os.environ.get("FROM_EMAIL")

    if not all([api_key, to_email, from_email]):
        logger.warning("Brevo env vars not set — skipping email.")
        return False

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = api_key

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    email = sib_api_v3_sdk.SendSmtpEmail(
        sender={"email": from_email},
        to=[{"email": to_email}],
        subject=subject,
        html_content=markdown_to_html(markdown_content),
    )

    try:
        response = api_instance.send_transac_email(email)
        logger.info(f"Email sent. Message ID: {response.message_id}")
        return True
    except ApiException as e:
        logger.error(f"Failed to send email via Brevo: {e}")
        return False
