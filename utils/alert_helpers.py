from pathlib import Path
from datetime import date

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

FOLLOW_UP_TASKS_FILE = DATA_DIR / "follow_up_tasks.csv"
ACTIVITY_FILE = DATA_DIR / "credentialing_activity.csv"
LICENSES_FILE = DATA_DIR / "licenses.csv"
RECREDENTIALING_FILE = DATA_DIR / "recredentialing.csv"

LICENSE_EXPIRING_SOON_DAYS = 30
RECREDENTIALING_DUE_SOON_DAYS = 45


def _load_csv(file_path: Path) -> pd.DataFrame:
    if file_path.exists():
        try:
            return pd.read_csv(file_path)
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()


def _parse_date(value):
    if pd.isna(value) or value == "":
        return pd.NaT
    return pd.to_datetime(value, errors="coerce")


def _find_column(df: pd.DataFrame, possible_names):
    for name in possible_names:
        if name in df.columns:
            return name
    return None


def _is_open_status(value):
    if pd.isna(value):
        return True

    value = str(value).strip().lower()

    closed_statuses = [
        "closed",
        "complete",
        "completed",
        "done",
        "resolved",
        "inactive",
        "cancelled",
        "canceled",
    ]

    return value not in closed_statuses


def _clean_alerts(df: pd.DataFrame, alert_type: str, alert_date_col: str, alert_status: str):
    alerts = df.copy()

    alerts["Alert Type"] = alert_type
    alerts["Alert Date"] = alerts[alert_date_col].dt.strftime("%m/%d/%Y")
    alerts["Alert Status"] = alert_status

    if "Provider" not in alerts.columns:
       provider_col = _find_column(alerts, ["Provider Name", "Provider"])
    alerts["Provider"] = alerts[provider_col] if provider_col else ""

    if "Item" not in alerts.columns:
        item_cols = ["Payer", "License Type", "License", "Task", "Subject", "Description"]
        found_item = _find_column(alerts, item_cols)
        alerts["Item"] = alerts[found_item] if found_item else alert_type

    if "Notes" not in alerts.columns:
        note_col = _find_column(alerts, ["Notes", "Note", "Comments", "Comment"])
        alerts["Notes"] = alerts[note_col] if note_col else ""

    return alerts


def get_follow_up_task_alerts() -> pd.DataFrame:
    today = pd.Timestamp(date.today())

    df = _load_csv(FOLLOW_UP_TASKS_FILE)
    if df.empty:
        return pd.DataFrame()

    due_col = _find_column(
        df,
        [
            "Due Date",
            "Follow-Up Date",
            "Follow Up Date",
            "Follow-up Date",
            "Next Follow-Up Date",
            "Next Follow Up Date",
        ],
    )

    status_col = _find_column(df, ["Status", "Task Status", "Current Status"])

    if not due_col:
        return pd.DataFrame()

    df = df.copy()
    df["_DueDate"] = df[due_col].apply(_parse_date)

    mask_due = df["_DueDate"].notna() & (df["_DueDate"] <= today)
    mask_open = df[status_col].apply(_is_open_status) if status_col else True

    alerts = df[mask_due & mask_open].copy()
    if alerts.empty:
        return pd.DataFrame()

    alerts = _clean_alerts(alerts, "Follow-Up Task", "_DueDate", "Due / Overdue")
    return alerts.drop(columns=["_DueDate"], errors="ignore")


def get_activity_follow_up_alerts() -> pd.DataFrame:
    today = pd.Timestamp(date.today())

    df = _load_csv(ACTIVITY_FILE)
    if df.empty:
        return pd.DataFrame()

    follow_up_col = _find_column(
        df,
        [
            "Follow-Up Date",
            "Follow Up Date",
            "Follow-up Date",
            "Next Follow-Up Date",
            "Next Follow Up Date",
            "Due Date",
        ],
    )

    status_col = _find_column(
        df,
        ["Status", "Follow-Up Status", "Follow Up Status", "Task Status", "Current Status"],
    )

    if not follow_up_col:
        return pd.DataFrame()

    df = df.copy()
    df["_FollowUpDate"] = df[follow_up_col].apply(_parse_date)

    mask_due = df["_FollowUpDate"].notna() & (df["_FollowUpDate"] <= today)
    mask_open = df[status_col].apply(_is_open_status) if status_col else True

    alerts = df[mask_due & mask_open].copy()
    if alerts.empty:
        return pd.DataFrame()

    alerts = _clean_alerts(alerts, "Activity Follow-Up", "_FollowUpDate", "Due / Overdue")
    return alerts.drop(columns=["_FollowUpDate"], errors="ignore")


def get_license_alerts() -> pd.DataFrame:
    today = pd.Timestamp(date.today())
    soon_date = today + pd.Timedelta(days=LICENSE_EXPIRING_SOON_DAYS)

    df = _load_csv(LICENSES_FILE)
    if df.empty:
        return pd.DataFrame()

    exp_col = _find_column(
        df,
        [
            "Expiration Date",
            "Expiration",
            "License Expiration",
            "Renewal Date",
            "Renewal Due Date",
            "Expires",
        ],
    )

    status_col = _find_column(df, ["Status", "License Status", "Current Status"])

    if not exp_col:
        return pd.DataFrame()

    df = df.copy()
    df["_ExpirationDate"] = df[exp_col].apply(_parse_date)

    mask_date = df["_ExpirationDate"].notna() & (df["_ExpirationDate"] <= soon_date)
    mask_open = df[status_col].apply(_is_open_status) if status_col else True

    alerts = df[mask_date & mask_open].copy()
    if alerts.empty:
        return pd.DataFrame()

    alerts["AlertStatusTemp"] = alerts["_ExpirationDate"].apply(
        lambda x: "Expired" if x < today else "Expiring Soon"
    )

    final_alerts = []
    for status_value, group in alerts.groupby("AlertStatusTemp"):
        cleaned = _clean_alerts(group, "License Renewal", "_ExpirationDate", status_value)
        final_alerts.append(cleaned)

    return pd.concat(final_alerts, ignore_index=True).drop(
        columns=["_ExpirationDate", "AlertStatusTemp"], errors="ignore"
    )


def get_recredentialing_alerts() -> pd.DataFrame:
    today = pd.Timestamp(date.today())
    soon_date = today + pd.Timedelta(days=RECREDENTIALING_DUE_SOON_DAYS)

    df = _load_csv(RECREDENTIALING_FILE)
    if df.empty:
        return pd.DataFrame()

    due_col = _find_column(
        df,
        [
            "Next Recredentialing Due",
            "Recredentialing Due Date",
            "Due Date",
            "Next Due Date",
            "Expiration Date",
        ],
    )

    status_col = _find_column(df, ["Status", "Recredentialing Status", "Current Status"])

    if not due_col:
        return pd.DataFrame()

    df = df.copy()
    df["_DueDate"] = df[due_col].apply(_parse_date)

    mask_date = df["_DueDate"].notna() & (df["_DueDate"] <= soon_date)
    mask_open = df[status_col].apply(_is_open_status) if status_col else True

    alerts = df[mask_date & mask_open].copy()
    if alerts.empty:
        return pd.DataFrame()

    alerts["AlertStatusTemp"] = alerts["_DueDate"].apply(
        lambda x: "Overdue" if x < today else "Due Soon"
    )

    final_alerts = []
    for status_value, group in alerts.groupby("AlertStatusTemp"):
        cleaned = _clean_alerts(group, "Recredentialing", "_DueDate", status_value)
        final_alerts.append(cleaned)

    return pd.concat(final_alerts, ignore_index=True).drop(
        columns=["_DueDate", "AlertStatusTemp"], errors="ignore"
    )


def get_action_required_items() -> pd.DataFrame:
    alert_frames = [
        get_follow_up_task_alerts(),
        get_activity_follow_up_alerts(),
        get_license_alerts(),
        get_recredentialing_alerts(),
    ]

    alert_frames = [df for df in alert_frames if df is not None and not df.empty]

    if not alert_frames:
        return pd.DataFrame(
            columns=["Alert Type", "Alert Date", "Alert Status", "Provider", "Item", "Notes"]
        )

    combined = pd.concat(alert_frames, ignore_index=True, sort=False)

    if "Alert Date" in combined.columns:
        combined["_SortDate"] = pd.to_datetime(
            combined["Alert Date"],
            errors="coerce",
            format="%m/%d/%Y",
        )
        combined = combined.sort_values(
            by=["_SortDate", "Alert Type"],
            ascending=[True, True],
            na_position="last",
        )
        combined = combined.drop(columns=["_SortDate"], errors="ignore")

    return combined


def get_action_required_count() -> int:
    df = get_action_required_items()
    return int(len(df)) if df is not None else 0


def get_alert_items() -> pd.DataFrame:
    return get_action_required_items()


def get_alert_count() -> int:
    return get_action_required_count()