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


def _get_list_emails(api_key: str, list_id: int) -> list[str]:
    """Fetch all contact emails from a Brevo contact list."""
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = api_key
    contacts_api = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(configuration))

    emails = []
    limit = 50
    offset = 0
    while True:
        result = contacts_api.get_contacts_from_list(list_id, limit=limit, offset=offset)
        batch = result.contacts or []
        emails.extend(c["email"] for c in batch if c.get("email"))
        if len(batch) < limit:
            break
        offset += limit
    return emails


def send_report(subject: str, markdown_content: str) -> bool:
    api_key = os.environ.get("BREVO_API_KEY")
    list_id = os.environ.get("BREVO_LIST_ID")
    from_email = os.environ.get("FROM_EMAIL")

    if not all([api_key, list_id, from_email]):
        logger.warning("Brevo env vars not set — skipping email.")
        return False

    recipients = _get_list_emails(api_key, int(list_id))
    if not recipients:
        logger.warning("No contacts found in Brevo list — skipping email.")
        return False

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = api_key
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    html = markdown_to_html(markdown_content)
    success_count = 0
    for recipient_email in recipients:
        email = sib_api_v3_sdk.SendSmtpEmail(
            sender={"email": from_email},
            to=[{"email": recipient_email}],
            subject=subject,
            html_content=html,
        )
        try:
            response = api_instance.send_transac_email(email)
            logger.info(f"Sent to {recipient_email}. Message ID: {response.message_id}")
            success_count += 1
        except ApiException as e:
            logger.error(f"Failed to send to {recipient_email}: {e}")

    logger.info(f"Report sent to {success_count}/{len(recipients)} recipients.")
    return success_count > 0
