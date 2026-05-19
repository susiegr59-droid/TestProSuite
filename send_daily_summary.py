from dotenv import load_dotenv
load_dotenv()

from utils.alert_helpers import get_action_required_items
from utils.email_helpers import send_email_smtp, build_action_required_email
import os


def main():
    alerts = get_action_required_items()
    recipient = os.getenv("PROSUITE_ALERT_EMAIL", "").strip()

    if not recipient:
        raise ValueError("PROSUITE_ALERT_EMAIL is missing in .env")

    email_body = build_action_required_email(alerts)

    send_email_smtp(
        subject="ProSuite - Daily Action Required Summary",
        body=email_body,
        to_email=recipient
    )

    print(f"Daily summary sent to {recipient}")


if __name__ == "__main__":
    main()