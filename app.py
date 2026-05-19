import streamlit as st
from pathlib import Path
from datetime import date
import pandas as pd

from utils.csv_helpers import load_csv


st.set_page_config(
    page_title="ProSuite Provider Management Software",
    page_icon="PS",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] {display: none !important;}

    .stApp {
        background:
            radial-gradient(1200px 520px at 90% -10%, rgba(56, 112, 175, 0.16), transparent),
            radial-gradient(900px 420px at -8% 0%, rgba(13, 43, 74, 0.10), transparent),
            linear-gradient(180deg, #eef3f8 0%, #e8eef5 100%);
    }

    .block-container {
        max-width: 1220px;
        padding-top: 1rem;
        padding-bottom: 1.8rem;
        padding-left: 2rem;
        padding-right: 1.6rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #163b63 0%, #1a476f 58%, #2b6f9e 100%);
        border-right: 1px solid rgba(211, 232, 248, 0.22);
        min-width: 220px !important;
        max-width: 220px !important;
    }

    section[data-testid="stSidebar"] > div {
        min-width: 220px !important;
        max-width: 220px !important;
        padding: 0.9rem 0.7rem 1rem 0.7rem;
    }

    .sb-brand {
        display: flex;
        align-items: flex-start;
        gap: 0.55rem;
        margin-bottom: 0.65rem;
        padding-top: 0.05rem;
    }

    .sb-badge {
        width: 32px;
        height: 32px;
        border-radius: 9px;
        background: linear-gradient(180deg, rgba(225, 242, 255, 0.20) 0%, rgba(166, 204, 234, 0.18) 100%);
        border: 1px solid rgba(217, 236, 251, 0.34);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 0.76rem;
        letter-spacing: 0.04em;
        color: #eaf6ff;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.22);
    }

    .sb-title {
        margin: 0;
        color: #ebf6ff;
        font-size: 0.98rem;
        font-weight: 800;
        line-height: 1.1;
    }

    .sb-subtitle {
        margin: 0.08rem 0 0 0;
        color: rgba(229, 245, 255, 0.84);
        font-size: 0.72rem;
        font-weight: 600;
    }

    .sb-divider {
        height: 1px;
        background: rgba(208, 230, 249, 0.24);
        margin: 0.6rem 0 0.8rem 0;
    }

    section[data-testid="stSidebar"] .stButton {
        margin-bottom: 0.5rem;
    }

    section[data-testid="stSidebar"] .stButton > button {
        width: auto;
        min-width: 0;
        max-width: 100%;
        border-radius: 13px;
        border: 1px solid rgba(188, 220, 245, 0.54);
        background: linear-gradient(180deg, rgba(124, 165, 205, 0.30) 0%, rgba(84, 124, 166, 0.26) 100%);
        box-shadow: 0 6px 14px rgba(7, 20, 36, 0.24), inset 0 1px 0 rgba(255, 255, 255, 0.24);
        color: #edf8ff;
        font-weight: 700;
        text-align: left;
        justify-content: flex-start;
        padding: 0.55rem 0.8rem;
        margin-bottom: 0;
        line-height: 1.15;
        transition: background 0.16s ease, border-color 0.16s ease, transform 0.16s ease, box-shadow 0.16s ease;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(180deg, rgba(144, 186, 223, 0.34) 0%, rgba(96, 140, 184, 0.30) 100%);
        border-color: rgba(223, 241, 255, 0.72);
        color: #ffffff;
        transform: translateY(-1px);
        box-shadow: 0 9px 18px rgba(7, 20, 36, 0.28), inset 0 1px 0 rgba(255, 255, 255, 0.28);
    }

    .hero {
        border-radius: 22px;
        padding: 1.25rem 1.45rem;
        margin-bottom: 1rem;
        background: linear-gradient(120deg, #0f2744 0%, #163a62 48%, #245f8e 100%);
        box-shadow: 0 18px 40px rgba(8, 29, 49, 0.25);
        color: #f5f9ff;
    }

    .hero-row {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 1rem;
    }

    .hero-brand {
        display: flex;
        align-items: center;
        gap: 0.85rem;
    }

    .brand-badge {
        width: 54px;
        height: 54px;
        border-radius: 14px;
        background: rgba(232, 244, 255, 0.17);
        border: 1px solid rgba(223, 239, 255, 0.25);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1.05rem;
        letter-spacing: 0.06em;
        color: #eaf6ff;
    }

    .hero-title {
        margin: 0;
        font-size: 2.05rem;
        font-weight: 800;
        letter-spacing: -0.01em;
        color: #f0f8ff;
    }

    .hero-subtitle {
        margin: 0.42rem 0 0 0;
        color: rgba(236, 246, 255, 0.9);
        font-size: 0.98rem;
    }

    .mode-pill {
        border-radius: 999px;
        padding: 0.42rem 0.82rem;
        background: #d6ecff;
        color: #103353;
        font-size: 0.8rem;
        font-weight: 700;
        white-space: nowrap;
        margin-top: 0.2rem;
    }

    .section-label {
        margin: 0.35rem 0 0.6rem 0;
        color: #203b5b;
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.09em;
        text-transform: uppercase;
    }

    div[data-testid="stWidgetLabel"] p {
        font-weight: 800;
        color: #15385d;
        letter-spacing: 0.01em;
    }

    div[data-testid="stSelectbox"] label p {
        font-weight: 800 !important;
        color: #15385d !important;
        letter-spacing: 0.01em;
    }

    div[data-testid="stSelectbox"] > div[data-baseweb="select"] > div {
        border: 2px solid #1a1a1a;
        border-radius: 0;
        background: #ffffff;
        box-shadow: none;
    }

    div[data-testid="stSelectbox"] > div[data-baseweb="select"] > div:focus-within {
        border-color: #15385d;
        box-shadow: 0 0 0 2px rgba(21, 56, 93, 0.12);
    }

    .overview-card {
        border-radius: 18px;
        border: 1px solid #e3eaf4;
        box-shadow: 0 12px 28px rgba(16, 39, 66, 0.08);
        padding: 1.15rem 1rem 1rem 1rem;
        margin-bottom: 1rem;
        min-height: 168px;
        text-align: center;
    }

    .overview-green {
        background: linear-gradient(180deg, #f3fff6 0%, #f8fcff 100%);
    }

    .overview-lilac {
        background: linear-gradient(180deg, #f7f4ff 0%, #fbfcff 100%);
    }

    .overview-amber {
        background: linear-gradient(180deg, #fff8ec 0%, #fffdf8 100%);
    }

    .overview-rose {
        background: linear-gradient(180deg, #fff5f7 0%, #fcfcff 100%);
    }

    .overview-icon {
        font-size: 2.7rem;
        line-height: 1;
        margin-bottom: 0.7rem;
    }

    .overview-title {
        margin: 0;
        color: #112b48;
        font-size: 0.9rem;
        font-weight: 800;
        line-height: 1.2;
    }

    .overview-value {
        margin: 0.42rem 0 0 0;
        color: #163d67;
        font-size: 1.45rem;
        font-weight: 800;
        line-height: 1;
    }

    .overview-subtext {
        margin: 0.38rem 0 0 0;
        color: #5d728a;
        font-size: 0.84rem;
        font-weight: 600;
        line-height: 1.25;
    }

    .table-shell {
        border-radius: 14px;
        border: 1px solid #d7e3f0;
        background: #ffffff;
        padding: 0.5rem;
        box-shadow: 0 8px 20px rgba(16, 39, 66, 0.06);
        margin-bottom: 0.85rem;
    }

    .stButton > button[kind="primary"] {
        width: 100%;
        border-radius: 12px;
        min-height: 56px;
        border: 1px solid #2c6ca3;
        background: linear-gradient(180deg, #2169a8 0%, #175183 100%);
        color: #f3f8ff;
        font-weight: 650;
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(180deg, #2b79be 0%, #1f6197 100%);
        border-color: #4a8cc5;
        color: #ffffff;
        transform: none;
    }

    @media (max-width: 980px) {
        .hero-title { font-size: 1.4rem; }
        .hero-row { flex-direction: column; align-items: flex-start; }
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def parse_date_series(values):
    parsed = pd.to_datetime(values, format="%m/%d/%Y", errors="coerce")
    missing_mask = parsed.isna()
    if missing_mask.any():
        parsed.loc[missing_mask] = pd.to_datetime(values[missing_mask], errors="coerce")
    return parsed


def open_page(page_path: str):
    target_page = Path(__file__).parent / page_path
    if target_page.exists():
        st.switch_page(page_path)
    else:
        st.warning(f"Page is not available yet: {page_path}")


modules = [
    {"title": "Providers", "page": "pages/01_Providers.py", "key": "nav_providers"},
    {"title": "Locations", "page": "pages/02_Locations.py", "key": "nav_locations"},
    {"title": "Payer Directory", "page": "pages/03_Payer_Directory.py", "key": "nav_payers"},
    {"title": "Insurance Credentialing", "page": "pages/04_Insurance_Credentialing.py", "key": "nav_insurance"},
    {"title": "Credentialing Activity Log", "page": "pages/05_Credentialing_Activity_Log.py", "key": "nav_activity"},
    {"title": "Follow-up Tasks", "page": "pages/06_Follow_up_Tasks.py", "key": "nav_followup"},
    {"title": "Licenses and Renewals", "page": "pages/07_Licenses_and_Renewals.py", "key": "nav_licenses"},
    {"title": "Recredentialing", "page": "pages/08_Recredentialing.py", "key": "nav_recred"},
    {"title": "Provider Profile", "page": "pages/09_Provider_Profile.py", "key": "nav_profile"},
    {"title": "Reports", "page": "pages/10_Reports.py", "key": "nav_reports"},
    {"title": "Action Required", "page": "pages/11_Action_Required.py", "key": "nav_action"},
]

with st.sidebar:
    st.markdown(
        """
        <div class="sb-brand">
            <div class="sb-badge">PS</div>
            <div>
                <p class="sb-title">Core Modules</p>
                <p class="sb-subtitle">Quick navigation</p>
            </div>
        </div>
        <div class="sb-divider"></div>
        """,
        unsafe_allow_html=True,
    )

    for module in modules:
        if st.button(module["title"], key=module["key"], type="secondary"):
            open_page(module["page"])


today = pd.Timestamp(date.today())

providers_df = load_csv(
    "data/providers.csv",
    [
        "ProviderID",
        "Provider Name",
        "First Name",
        "Last Name",
        "Provider Status",
        "Onboarding Status",
        "Credentialing Status",
    ],
)

providers_df["Provider Name"] = providers_df["Provider Name"].fillna("").astype(str).str.strip()
missing_name = providers_df["Provider Name"] == ""
providers_df.loc[missing_name, "Provider Name"] = (
    providers_df.loc[missing_name, "First Name"].fillna("").astype(str).str.strip()
    + " "
    + providers_df.loc[missing_name, "Last Name"].fillna("").astype(str).str.strip()
).str.strip()

credentialing_df = load_csv(
    "data/insurance_credentialing.csv",
    ["RecordID", "ProviderID", "Provider Name", "Insurance Plan", "Current Status", "Next Recredentialing Due"],
)

licenses_df = load_csv(
    "data/licenses.csv",
    ["LicenseID", "ProviderID", "Provider Name", "License Type", "Expiration Date", "Status"],
)

recred_df = load_csv(
    "data/recredentialing.csv",
    ["RecredID", "ProviderID", "Provider Name", "Insurance Plan", "Next Due Date", "Status"],
)

activity_df = load_csv(
    "data/credentialing_activity.csv",
    ["ActivityID", "ProviderID", "Provider Name", "Action", "Follow-Up Needed", "Follow-Up Date"],
)

licenses_df["Parsed Expiration"] = parse_date_series(licenses_df["Expiration Date"].astype(str))
recred_df["Parsed Due"] = parse_date_series(recred_df["Next Due Date"].astype(str))
activity_df["Parsed Follow-Up"] = parse_date_series(activity_df["Follow-Up Date"].astype(str))

active_providers = int(providers_df["Provider Status"].astype(str).str.strip().str.lower().eq("active").sum())

pending_statuses = {"submitted", "pending", "not started", "in progress"}
pending_enrollments = int(
    credentialing_df["Current Status"].astype(str).str.strip().str.lower().isin(pending_statuses).sum()
)

license_days = (licenses_df["Parsed Expiration"] - today).dt.days
licenses_expiring_30 = int(((license_days >= 0) & (license_days <= 30)).sum())

recred_days = (recred_df["Parsed Due"] - today).dt.days
recred_due_90 = int(((recred_days >= 0) & (recred_days <= 90)).sum())

follow_up_needed = activity_df["Follow-Up Needed"].astype(str).str.strip().str.lower().eq("yes")
follow_up_days = (activity_df["Parsed Follow-Up"] - today).dt.days
overdue_followups = int((follow_up_needed & ((follow_up_days < 0) | activity_df["Parsed Follow-Up"].isna())).sum())

action_rows = []

expired_slice = licenses_df[license_days < 0]
for _, row in expired_slice.head(20).iterrows():
    action_rows.append(
        {
            "Priority": "Critical",
            "Category": "License Expired",
            "Provider": str(row.get("Provider Name", "")).strip() or "Unknown",
            "Due": str(row.get("Expiration Date", "")),
            "Source": "Licenses and Renewals",
        }
    )

expiring_slice = licenses_df[(license_days >= 0) & (license_days <= 30)]
for _, row in expiring_slice.head(20).iterrows():
    action_rows.append(
        {
            "Priority": "High",
            "Category": "License Expiring Soon",
            "Provider": str(row.get("Provider Name", "")).strip() or "Unknown",
            "Due": str(row.get("Expiration Date", "")),
            "Source": "Licenses and Renewals",
        }
    )

due_slice = recred_df[(recred_days >= 0) & (recred_days <= 90)]
for _, row in due_slice.head(20).iterrows():
    action_rows.append(
        {
            "Priority": "Medium",
            "Category": "Recredentialing Due",
            "Provider": str(row.get("Provider Name", "")).strip() or "Unknown",
            "Due": str(row.get("Next Due Date", "")),
            "Source": "Recredentialing",
        }
    )

follow_slice = activity_df[follow_up_needed & ((follow_up_days < 0) | activity_df["Parsed Follow-Up"].isna())]
for _, row in follow_slice.head(20).iterrows():
    action_rows.append(
        {
            "Priority": "High",
            "Category": "Overdue Follow-Up",
            "Provider": str(row.get("Provider Name", "")).strip() or "Unknown",
            "Due": str(row.get("Follow-Up Date", "")) if str(row.get("Follow-Up Date", "")).strip() else "Missing",
            "Source": "Credentialing Activity Log",
        }
    )

st.markdown(
    """
    <div class="hero">
        <div class="hero-row">
            <div>
                <div class="hero-brand">
                    <div class="brand-badge">PS</div>
                    <h1 class="hero-title">ProSuite Provider Management Software</h1>
                </div>
                <p class="hero-subtitle">Centralized tools for provider data, credentialing workflows, locations, and reporting.</p>
            </div>
            <div class="mode-pill">Testing Mode: Login bypass enabled</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="section-label">Today\'s Overview</p>', unsafe_allow_html=True)
k1, k2, k3, k4, k5 = st.columns(5, gap="large")

with k1:
    st.markdown(
        f'<div class="overview-card overview-green"><div class="overview-icon">✅</div><p class="overview-title">Active<br>Providers</p><p class="overview-value">{active_providers}</p><p class="overview-subtext">Current active roster</p></div>',
        unsafe_allow_html=True,
    )
with k2:
    st.markdown(
        f'<div class="overview-card overview-lilac"><div class="overview-icon">🕒</div><p class="overview-title">Pending<br>Enrollment</p><p class="overview-value">{pending_enrollments}</p><p class="overview-subtext">Submitted or in progress</p></div>',
        unsafe_allow_html=True,
    )
with k3:
    st.markdown(
        f'<div class="overview-card overview-amber"><div class="overview-icon">⚠️</div><p class="overview-title">Licenses<br>Expiring</p><p class="overview-value">{licenses_expiring_30}</p><p class="overview-subtext">Due in next 30 days</p></div>',
        unsafe_allow_html=True,
    )
with k4:
    st.markdown(
        f'<div class="overview-card overview-lilac"><div class="overview-icon">📅</div><p class="overview-title">Recredentialing<br>Due</p><p class="overview-value">{recred_due_90}</p><p class="overview-subtext">Due in next 90 days</p></div>',
        unsafe_allow_html=True,
    )
with k5:
    st.markdown(
        f'<div class="overview-card overview-rose"><div class="overview-icon">🔔</div><p class="overview-title">Overdue<br>Follow-Ups</p><p class="overview-value">{overdue_followups}</p><p class="overview-subtext">Action overdue or missing date</p></div>',
        unsafe_allow_html=True,
    )

st.markdown('<p class="section-label">Quick Actions</p>', unsafe_allow_html=True)
qa1, qa2, qa3, qa4 = st.columns(4, gap="large")
with qa1:
    if st.button("Add Provider", key="qa_add_provider", type="primary"):
        open_page("pages/01_Providers.py")
with qa2:
    if st.button("Start Enrollment", key="qa_start_enrollment", type="primary"):
        open_page("pages/04_Insurance_Credentialing.py")
with qa3:
    if st.button("Add License", key="qa_add_license", type="primary"):
        open_page("pages/07_Licenses_and_Renewals.py")
with qa4:
    if st.button("Log Activity", key="qa_log_activity", type="primary"):
        open_page("pages/05_Credentialing_Activity_Log.py")

provider_names = sorted(
    [name for name in providers_df["Provider Name"].dropna().astype(str).unique().tolist() if name.strip()]
)

search_col, jump_col = st.columns([3, 1], gap="large")
selected_provider_name = ""
with search_col:
    selected_provider_name = st.selectbox(
        "Provider Search",
        provider_names if provider_names else ["No providers available"],
        key="home_provider_search",
    )
with jump_col:
    if st.button("Open Provider Profile", key="qa_open_profile", type="primary"):
        if provider_names:
            selected_id_match = providers_df[
                providers_df["Provider Name"].astype(str).str.strip() == selected_provider_name
            ]
            if not selected_id_match.empty:
                selected_numeric_id = pd.to_numeric(selected_id_match.iloc[0]["ProviderID"], errors="coerce")
                if pd.notna(selected_numeric_id):
                    st.session_state["selected_provider_id"] = int(selected_numeric_id)
            open_page("pages/09_Provider_Profile.py")

st.markdown('<p class="section-label">Live Action Required</p>', unsafe_allow_html=True)
if action_rows:
    priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    actions_df = pd.DataFrame(action_rows)
    actions_df["_order"] = actions_df["Priority"].map(priority_order).fillna(99)
    actions_df = actions_df.sort_values(["_order", "Category", "Provider"]).drop(columns=["_order"]).head(20)
    st.markdown('<div class="table-shell">', unsafe_allow_html=True)
    st.dataframe(actions_df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.success("No urgent items right now. Keep monitoring daily to stay ahead of expirations and follow-ups.")
