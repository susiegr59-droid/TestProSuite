import os
import streamlit as st
import pandas as pd


from utils.ui_helpers import apply_page_style, render_sidebar, overview_metric_card
from utils.alert_helpers import get_action_required_items
from utils.email_helpers import send_email_smtp, build_action_required_email
from utils.csv_helpers import load_csv, save_csv


st.set_page_config(page_title="Action Required", page_icon="⚠️", layout="wide")

apply_page_style()
render_sidebar("Action Required")


ACTIVITY_COLUMNS = [
    "ActivityID",
    "ProviderID",
    "Provider Name",
    "Insurance Plan",
    "Activity Date",
    "Method",
    "Action",
    "Notes",
    "Follow-Up Needed",
    "Follow-Up Date",
]


st.markdown(
    """
    <style>
        .ar-hero {
            background: linear-gradient(90deg, #8B1E3F 0%, #C44569 55%, #F4A261 100%);
            padding: 1.6rem 1.8rem;
            border-radius: 22px;
            color: white;
            box-shadow: 0 10px 26px rgba(139, 30, 63, 0.18);
            margin-bottom: 1.4rem;
        }
        .ar-title {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.35rem;
        }
        .ar-subtitle {
            font-size: 1rem;
            opacity: 0.95;
        }
        .section-chip {
            display: inline-block;
            padding: 0.45rem 0.85rem;
            border-radius: 999px;
            font-weight: 700;
            font-size: 0.95rem;
            margin-bottom: 0.8rem;
        }
        .followup-chip {
            background: rgba(47, 115, 217, 0.12);
            color: #2458A6;
        }
        .license-chip {
            background: rgba(244, 162, 97, 0.16);
            color: #A85A12;
        }
        .recred-chip {
            background: rgba(42, 111, 242, 0.12);
            color: #1C57C7;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def format_status(status):
    status = str(status).strip()
    return {
        "Expired": "🔴 Expired",
        "Overdue": "🔴 Overdue",
        "Due Today": "🔵 Due Today",
        "Expiring Soon": "🟡 Expiring Soon",
        "Due Soon": "🟡 Due Soon",
        "Upcoming": "🟠 Upcoming",
        "Due / Overdue": "🟡 Due / Overdue",
    }.get(status, status)


def status_priority(status):
    return {
        "Expired": 1,
        "Overdue": 1,
        "Due Today": 2,
        "Due / Overdue": 2,
        "Expiring Soon": 3,
        "Due Soon": 3,
        "Upcoming": 4,
    }.get(str(status).strip(), 9)


def normalize_alerts(alerts):
    df = pd.DataFrame(alerts)

    if df.empty:
        return pd.DataFrame(columns=["Status", "Category", "Provider", "Item", "Due Date", "Notes"])

    df = df.copy()

    df = df.rename(
        columns={
            "Alert Status": "Status",
            "Alert Date": "Due Date",
            "Alert Type": "Category",
        }
    )

    df = df.loc[:, ~df.columns.duplicated()].copy()

    if "Provider" not in df.columns:
        df["Provider"] = df["Provider Name"] if "Provider Name" in df.columns else ""

    if "Item" not in df.columns:
        df["Item"] = df["Category"] if "Category" in df.columns else ""

    for col in ["Status", "Category", "Provider", "Item", "Due Date", "Notes"]:
        if col not in df.columns:
            df[col] = ""

    df["Category"] = df["Category"].replace(
        {
            "Follow-Up Task": "Follow-Up",
            "Activity Follow-Up": "Follow-Up",
            "License Renewal": "License",
            "Recredentialing": "Recredentialing",
        }
    )

    return df[["Status", "Category", "Provider", "Item", "Due Date", "Notes"]].copy()


def complete_activity_followup(provider, due_date):
    df = load_csv("data/credentialing_activity.csv", ACTIVITY_COLUMNS)

    if df is None or df.empty:
        return False

    match = (
        df["Provider Name"].astype(str).str.strip() == str(provider).strip()
    ) & (
        df["Follow-Up Date"].astype(str).str.strip() == str(due_date).strip()
    )

    if not match.any():
        return False

    df.loc[match, "Follow-Up Needed"] = "No"
    df.loc[match, "Follow-Up Date"] = ""

    save_csv(df, "data/credentialing_activity.csv")
    return True


alerts = get_action_required_items()
alerts_df = normalize_alerts(alerts)


st.markdown(
    """
    <div class="ar-hero">
        <div class="ar-title">⚠️ Action Required</div>
        <div class="ar-subtitle">
            Items needing attention across follow-ups, licenses, and recredentialing.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


if alerts_df.empty:
    st.success("No items currently require action.")

else:
    status_series = alerts_df["Status"].astype(str)

    urgent_count = int(status_series.isin(["Expired", "Overdue"]).sum())
    today_count = int(status_series.isin(["Due Today"]).sum())
    upcoming_count = int(
        status_series.isin(["Expiring Soon", "Due Soon", "Upcoming", "Due / Overdue"]).sum()
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        overview_metric_card("overview-rose", "🚨", "Urgent", str(urgent_count), "Expired or overdue items")

    with c2:
        overview_metric_card("overview-blue", "📅", "Due Today", str(today_count), "Items requiring attention today")

    with c3:
        overview_metric_card("overview-amber", "🕒", "Upcoming / Due Soon", str(upcoming_count), "Items approaching deadline")

    sort_df = alerts_df.copy()
    sort_df["Priority"] = sort_df["Status"].apply(status_priority)
    sort_df["SortDate"] = pd.to_datetime(sort_df["Due Date"], errors="coerce")

    sort_df = sort_df.sort_values(
        by=["Priority", "SortDate", "Provider", "Item"],
        ascending=[True, True, True, True],
        na_position="last",
    ).drop(columns=["Priority", "SortDate"], errors="ignore")

    followups_df = sort_df[sort_df["Category"] == "Follow-Up"].copy()
    licenses_df = sort_df[sort_df["Category"] == "License"].copy()
    recred_df = sort_df[sort_df["Category"] == "Recredentialing"].copy()

    st.markdown("### 🔍 Filter & View All Action Items")

    f1, f2, f3 = st.columns(3)

    with f1:
        selected_category = st.selectbox(
            "Category",
            ["All"] + sorted(sort_df["Category"].dropna().astype(str).unique().tolist()),
        )

    with f2:
        selected_status = st.selectbox(
            "Status",
            ["All"] + sorted(sort_df["Status"].dropna().astype(str).unique().tolist()),
        )

    with f3:
        selected_provider = st.selectbox(
            "Provider",
            ["All"] + sorted(sort_df["Provider"].dropna().astype(str).unique().tolist()),
        )

    filtered_df = sort_df.copy()

    if selected_category != "All":
        filtered_df = filtered_df[filtered_df["Category"] == selected_category]

    if selected_status != "All":
        filtered_df = filtered_df[filtered_df["Status"] == selected_status]

    if selected_provider != "All":
        filtered_df = filtered_df[filtered_df["Provider"] == selected_provider]

    display_all = filtered_df[["Status", "Category", "Provider", "Item", "Due Date", "Notes"]].copy()

    st.markdown("### 🧭 Take Action")

    for i, row in display_all.iterrows():
        item_text = str(row["Item"]).lower()
        provider = row["Provider"]
        due_date = row["Due Date"]
        notes = row["Notes"]

        col1, col2, col3, col4, col5, col6 = st.columns([1.4, 2, 2, 1.5, 1, 1.3])

        with col1:
            st.markdown(format_status(row["Status"]))

        with col2:
            st.write(provider)

        with col3:
            st.write(row["Item"])

        with col4:
            st.write(due_date)

        with col5:
            if "activity" in item_text:
                if st.button("Open", key=f"act_{i}"):
                    st.session_state["ar_provider"] = provider
                    st.session_state["ar_due_date"] = due_date
                    st.session_state["ar_notes"] = notes
                    st.switch_page("pages/05_Credentialing_Activity_Log.py")

            elif row["Category"] == "Follow-Up":
                if st.button("Open", key=f"fu_{i}"):
                    st.switch_page("pages/06_Follow_up_Tasks.py")

            elif row["Category"] == "License":
                if st.button("Open", key=f"lic_{i}"):
                    st.switch_page("pages/07_Licenses_and_Renewals.py")

            elif row["Category"] == "Recredentialing":
                if st.button("Open", key=f"rec_{i}"):
                    st.switch_page("pages/08_Recredentialing.py")

        with col6:
            if "activity" in item_text:
                if st.button("Complete", key=f"done_{i}"):
                    st.session_state[f"confirm_complete_{i}"] = True

                if st.session_state.get(f"confirm_complete_{i}", False):
                    st.warning("Confirm complete?")

                    yes_col, no_col = st.columns(2)

                    with yes_col:
                        if st.button("Yes", key=f"yes_{i}"):
                            completed = complete_activity_followup(provider, due_date)
                            st.session_state[f"confirm_complete_{i}"] = False

                            if completed:
                                st.success("Follow-up marked complete.")
                            else:
                                st.error("Could not find matching follow-up.")

                            st.rerun()

                    with no_col:
                        if st.button("No", key=f"no_{i}"):
                            st.session_state[f"confirm_complete_{i}"] = False
                            st.rerun()

        st.divider()

    st.markdown(
        f"""
        🔴 **Urgent:** {urgent_count} &nbsp;&nbsp;&nbsp;
        🔵 **Due Today:** {today_count} &nbsp;&nbsp;&nbsp;
        🟡 **Upcoming / Due Soon:** {upcoming_count}
        """
    )

    st.divider()

    st.markdown(
        f'<div class="section-chip followup-chip">📞 Follow-Ups ({len(followups_df)})</div>',
        unsafe_allow_html=True,
    )

    if followups_df.empty:
        st.info("No follow-up items currently require action.")
    else:
        display_followups = followups_df[["Status", "Provider", "Item", "Due Date", "Notes"]].copy()
        display_followups["Status"] = display_followups["Status"].apply(format_status)
        st.dataframe(display_followups, use_container_width=True, hide_index=True)

    if st.button("📞 Go To Follow-Ups", use_container_width=True):
        st.switch_page("pages/06_Follow_up_Tasks.py")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f'<div class="section-chip license-chip">📄 Licenses ({len(licenses_df)})</div>',
        unsafe_allow_html=True,
    )

    if licenses_df.empty:
        st.info("No license items currently require action.")
    else:
        display_licenses = licenses_df[["Status", "Provider", "Item", "Due Date", "Notes"]].copy()
        display_licenses["Status"] = display_licenses["Status"].apply(format_status)
        st.dataframe(display_licenses, use_container_width=True, hide_index=True)

    if st.button("📄 Go To Licenses", use_container_width=True):
        st.switch_page("pages/07_Licenses_and_Renewals.py")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f'<div class="section-chip recred-chip">🔄 Recredentialing ({len(recred_df)})</div>',
        unsafe_allow_html=True,
    )

    if recred_df.empty:
        st.info("No recredentialing items currently require action.")
    else:
        display_recred = recred_df[["Status", "Provider", "Item", "Due Date", "Notes"]].copy()
        display_recred["Status"] = display_recred["Status"].apply(format_status)
        st.dataframe(display_recred, use_container_width=True, hide_index=True)

    if st.button("🔄 Go To Recredentialing", use_container_width=True):
        st.switch_page("pages/08_Recredentialing.py")


st.divider()
st.subheader("Email Summary")

default_email = os.getenv("PROSUITE_ALERT_EMAIL", "")
recipient_email = st.text_input("Send Action Required summary to", value=default_email)

if st.button("📧 Send Action Required Summary", use_container_width=True):
    try:
        email_body = build_action_required_email(alerts)
        send_email_smtp(
            subject="ProSuite - Action Required Summary",
            body=email_body,
            to_email=recipient_email.strip(),
        )
        st.success(f"Summary email sent to {recipient_email}")

    except Exception as e:
        st.error(f"Email failed: {e}")