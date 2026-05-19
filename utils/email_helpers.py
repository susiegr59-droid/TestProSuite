import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()


def send_email_smtp(subject, body, to_email):
    smtp_host = os.getenv("PROSUITE_SMTP_HOST")
    smtp_port = int(os.getenv("PROSUITE_SMTP_PORT", "587"))
    smtp_user = os.getenv("PROSUITE_SMTP_USER")
    smtp_password = os.getenv("PROSUITE_SMTP_PASSWORD")
    from_email = os.getenv("PROSUITE_FROM_EMAIL", smtp_user)

    if not smtp_host or not smtp_user or not smtp_password or not from_email:
        raise ValueError("SMTP settings are missing. Please configure environment variables.")

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, [to_email], msg.as_string())


def build_action_required_email(alerts):
    if not alerts:
        return "No items currently require action."

    lines = []
    lines.append("ProSuite Action Required Summary")
    lines.append("=" * 32)
    lines.append("")

    for item in alerts:
        category = item.get("Category", "")
        provider = item.get("Provider", "")
        alert_item = item.get("Item", "")
        due_date = item.get("Due Date", "")
        status = item.get("Status", "")
        notes = item.get("Notes", "")

        lines.append(f"Category: {category}")
        lines.append(f"Provider: {provider}")
        lines.append(f"Item: {alert_item}")
        lines.append(f"Due Date: {due_date}")
        lines.append(f"Status: {status}")
        if str(notes).strip():
            lines.append(f"Notes: {notes}")
        lines.append("-" * 32)

    return "\n".join(lines)