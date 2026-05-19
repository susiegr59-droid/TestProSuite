import streamlit as st
import pandas as pd
from datetime import date


from utils.csv_helpers import load_csv
from utils.ui_helpers import apply_page_style, render_sidebar, overview_metric_card


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Reports",
    page_icon="📊",
    layout="wide"
)

apply_page_style()
render_sidebar("Reports")


# =========================================================
# PAGE-SPECIFIC STYLING
# =========================================================
st.markdown("""
<style>
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1500px !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    .hero-wrap {
        background: linear-gradient(135deg, #173A63 0%, #2A6EF2 100%);
        padding: 28px 32px;
        border-radius: 22px;
        margin-bottom: 22px;
        box-shadow: 0 10px 28px rgba(23, 58, 99, 0.18);
    }

    .hero-title {
        color: white !important;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }

    .hero-subtitle {
        color: rgba(255,255,255,0.92) !important;
        font-size: 1rem;
        margin-top: 6px;
        margin-bottom: 0;
    }

    .section-pill {
        display: inline-block;
        background: #163A63;
        color: white !important;
        padding: 10px 18px;
        border-radius: 999px;
        font-size: 0.95rem;
        font-weight: 700;
        margin: 6px 0 12px 0;
    }

    .panel {
        background: white;
        border-radius: 20px;
        padding: 20px 20px 16px 20px;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
        border: 1px solid #E8ECF3;
        margin-bottom: 18px;
    }

    .metric-shell-blue,
    .metric-shell-green,
    .metric-shell-gold,
    .metric-shell-red,
    .metric-shell-slate {
        border-radius: 18px;
        padding: 14px 16px;
        color: white;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
        min-height: 88px;
    }

    .metric-shell-blue {
        background: linear-gradient(135deg, #2A6EF2 0%, #5A95FF 100%);
    }

    .metric-shell-green {
        background: linear-gradient(135deg, #177E59 0%, #24A16C 100%);
    }

    .metric-shell-gold {
        background: linear-gradient(135deg, #A56A00 0%, #D39B22 100%);
    }

    .metric-shell-red {
        background: linear-gradient(135deg, #B42318 0%, #D84A3A 100%);
    }

    .metric-shell-slate {
        background: linear-gradient(135deg, #475569 0%, #64748B 100%);
    }

    .metric-label {
        font-size: 0.86rem;
        opacity: 0.92;
        margin-bottom: 8px;
        font-weight: 600;
        color: white !important;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 6px;
        color: white !important;
    }

    .metric-subtext {
        font-size: 0.82rem;
        opacity: 0.92;
        color: white !important;
    }

    .small-note {
        color: #5B657A;
        font-size: 0.88rem;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #E7EBF3;
        border-radius: 14px;
        overflow: hidden;
    }

    .logic-row {
        display: flex;
        align-items: center;
        gap: 12px;
        background: #F8FAFC;
        border: 1px solid #E5EAF2;
        border-radius: 14px;
        padding: 10px 14px;
        margin-bottom: 10px;
    }

    .logic-badge {
        min-width: 120px;
        text-align: center;
        padding: 6px 12px;
        border-radius: 999px;
        color: white;
        font-size: 0.82rem;
        font-weight: 700;
    }

    .logic-blue { background: linear-gradient(135deg, #2A6EF2 0%, #5A95FF 100%); }
    .logic-green { background: linear-gradient(135deg, #177E59 0%, #24A16C 100%); }
    .logic-gold { background: linear-gradient(135deg, #A56A00 0%, #D39B22 100%); }

    .logic-text {
        color: #243046;
        font-size: 0.92rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# FILES
# =========================================================
providers_file = "data/providers.csv"
credentialing_file = "data/insurance_credentialing.csv"
licenses_file = "data/licenses.csv"
recred_file = "data/recredentialing.csv"
activity_file = "data/credentialing_activity.csv"


# =========================================================
# HELPERS
# =========================================================
def render_hero():
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-title">📊 Reports</div>
        <div class="hero-subtitle">
            Summary reporting for onboarding, credentialing progress, renewals, and activity across ProSuite.
        </div>
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str):
    st.markdown(f'<div class="section-pill">{title}</div>', unsafe_allow_html=True)


def safe_df(df, columns):
    if df is None or df.empty:
        return pd.DataFrame(columns=columns)
    for col in columns:
        if col not in df.columns:
            df[col] = ""
    return df[columns].copy()


def parse_mmddyyyy(value):
    try:
        return pd.to_datetime(str(value), format="%m/%d/%Y", errors="coerce")
    except Exception:
        return pd.NaT


# =========================================================
# LOAD DATA
# =========================================================
providers_df = load_csv(providers_file, [
    "ProviderID",
    "Provider Name",
    "Onboarding Status",
    "Credentialing Status",
    "Provider Status"
])

credentialing_df = load_csv(credentialing_file, [
    "RecordID",
    "ProviderID",
    "Provider Name",
    "Insurance Plan",
    "Current Status",
    "Next Recredentialing Due"
])

licenses_df = load_csv(licenses_file, [
    "ProviderID",
    "Provider Name",
    "License Type",
    "Expiration Date",
    "Status"
])

recred_df = load_csv(recred_file, [
    "ProviderID",
    "Provider Name",
    "Insurance Plan",
    "Next Due Date",
    "Status"
])

activity_df = load_csv(activity_file, [
    "ActivityID",
    "ProviderID",
    "Provider Name",
    "Insurance Plan",
    "Activity Date",
    "Method",
    "Action",
    "Follow-Up Needed",
    "Follow-Up Date"
])

providers_df = safe_df(providers_df, [
    "ProviderID", "Provider Name", "Onboarding Status", "Credentialing Status", "Provider Status"
])

credentialing_df = safe_df(credentialing_df, [
    "RecordID", "ProviderID", "Provider Name", "Insurance Plan", "Current Status", "Next Recredentialing Due"
])

licenses_df = safe_df(licenses_df, [
    "ProviderID", "Provider Name", "License Type", "Expiration Date", "Status"
])

recred_df = safe_df(recred_df, [
    "ProviderID", "Provider Name", "Insurance Plan", "Next Due Date", "Status"
])

activity_df = safe_df(activity_df, [
    "ActivityID", "ProviderID", "Provider Name", "Insurance Plan", "Activity Date", "Method", "Action",
    "Follow-Up Needed", "Follow-Up Date"
])


# =========================================================
# CALCULATIONS
# =========================================================
today = pd.Timestamp(date.today())

total_providers = len(providers_df)

providers_onboarding = int(
    providers_df["Onboarding Status"].astype(str).str.strip().str.lower().isin(
        ["in progress", "pending", "onboarding", "started"]
    ).sum()
)

credentialing_in_progress = int(
    credentialing_df["Current Status"].astype(str).str.strip().str.lower().isin(
        ["submitted", "pending", "not started"]
    ).sum()
)

recred_df["Parsed Next Due"] = pd.to_datetime(
    recred_df["Next Due Date"].astype(str),
    format="%m/%d/%Y",
    errors="coerce"
)
recred_days_remaining = (recred_df["Parsed Next Due"] - today).dt.days
recredentialing_due = int(
    (
        recred_df["Parsed Next Due"].notna() &
        (recred_days_remaining <= 90) &
        (recred_days_remaining >= 0)
    ).sum()
)

licenses_df["Parsed Expiration"] = pd.to_datetime(
    licenses_df["Expiration Date"].astype(str),
    format="%m/%d/%Y",
    errors="coerce"
)
license_days_remaining = (licenses_df["Parsed Expiration"] - today).dt.days
licenses_expiring = int(
    (
        licenses_df["Parsed Expiration"].notna() &
        (license_days_remaining <= 60) &
        (license_days_remaining >= 0)
    ).sum()
)

followups_needed = int(
    activity_df["Follow-Up Needed"].astype(str).str.strip().str.lower().eq("yes").sum()
)

summary_df = pd.DataFrame({
    "Category": [
        "Total Providers",
        "Providers Onboarding",
        "Credentialing In Progress",
        "Recredentialing Due",
        "Licenses Expiring",
        "Follow-Ups Needed"
    ],
    "Count": [
        total_providers,
        providers_onboarding,
        credentialing_in_progress,
        recredentialing_due,
        licenses_expiring,
        followups_needed
    ]
})


# =========================================================
# HERO
# =========================================================
render_hero()


# =========================================================
# METRICS
# =========================================================
c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    overview_metric_card("overview-blue", "👥", "Providers", str(total_providers), "Total active records")
with c2:
    overview_metric_card("overview-amber", "🧭", "Onboarding", str(providers_onboarding), "Still in onboarding")
with c3:
    overview_metric_card("overview-lilac", "📋", "Credentialing", str(credentialing_in_progress), "In progress")
with c4:
    overview_metric_card("overview-rose", "🔄", "Recred Due", str(recredentialing_due), "Due within 90 days")
with c5:
    overview_metric_card("overview-rose", "📄", "Licenses Expiring", str(licenses_expiring), "Due within 60 days")
with c6:
    overview_metric_card("overview-slate", "📞", "Follow-Ups", str(followups_needed), "Open follow-up items")


# =========================================================
# REPORT SUMMARY
# =========================================================
section_header("Report Summary")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown(
        f'<div class="small-note">Showing <strong>{len(summary_df)}</strong> summary metric(s).</div>',
        unsafe_allow_html=True
    )

    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# DETAIL SNAPSHOTS
# =========================================================
section_header("Detail Snapshots")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown("#### Upcoming Recredentialing")
        upcoming_recred = recred_df.copy()
        upcoming_recred = upcoming_recred[upcoming_recred["Parsed Next Due"].notna()].copy()
        upcoming_recred = upcoming_recred.sort_values("Parsed Next Due").head(5)

        if upcoming_recred.empty:
            st.info("No recredentialing due dates available.")
        else:
            st.dataframe(
                upcoming_recred[["Provider Name", "Insurance Plan", "Next Due Date", "Status"]],
                use_container_width=True,
                hide_index=True
            )

    with right:
        st.markdown("#### Expiring Licenses")
        expiring_licenses = licenses_df.copy()
        expiring_licenses = expiring_licenses[expiring_licenses["Parsed Expiration"].notna()].copy()
        expiring_licenses = expiring_licenses.sort_values("Parsed Expiration").head(5)

        if expiring_licenses.empty:
            st.info("No license expiration dates available.")
        else:
            st.dataframe(
                expiring_licenses[["Provider Name", "License Type", "Expiration Date", "Status"]],
                use_container_width=True,
                hide_index=True
            )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# REPORT NOTES
# =========================================================
section_header("Report Notes")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    left, right = st.columns([1.05, 1])

    with left:
        st.markdown("#### How Counts Are Calculated")
        st.markdown("""
        <div class="logic-row">
            <div class="logic-badge logic-blue">Credentialing</div>
            <div class="logic-text">Counts records with statuses like Submitted, Pending, or Not Started as in progress</div>
        </div>

        <div class="logic-row">
            <div class="logic-badge logic-green">Renewals</div>
            <div class="logic-text">Recredentialing due counts include records with due dates in the next 90 days</div>
        </div>

        <div class="logic-row">
            <div class="logic-badge logic-gold">Licenses</div>
            <div class="logic-text">License expiring counts include expiration dates within the next 60 days</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("#### Future Enhancements")
        st.info("This page is ready for future charts, filters, exports, and downloadable reports.")

    st.markdown('</div>', unsafe_allow_html=True)