import streamlit as st
import pandas as pd


from utils.csv_helpers import load_csv
from utils.ui_helpers import apply_page_style, render_sidebar, overview_metric_card


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Provider Profile",
    page_icon="🧑‍⚕️",
    layout="wide"
)

apply_page_style()
render_sidebar("Provider Profile")


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
    .metric-shell-red {
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

    .profile-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 14px;
        margin-top: 4px;
    }

    .profile-item {
        background: #F8FAFC;
        border: 1px solid #E5EAF2;
        border-radius: 14px;
        padding: 12px 14px;
    }

    .profile-label {
        color: #5B657A;
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 4px;
    }

    .profile-value {
        color: #243046;
        font-size: 0.97rem;
        font-weight: 600;
    }

    .status-chip {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        color: white;
        font-size: 0.78rem;
        font-weight: 700;
        text-align: center;
        min-width: 100px;
    }

    .status-active {
        background: linear-gradient(135deg, #177E59 0%, #24A16C 100%);
    }

    .status-pending {
        background: linear-gradient(135deg, #A56A00 0%, #D39B22 100%);
    }

    .status-submitted {
        background: linear-gradient(135deg, #2A6EF2 0%, #5A95FF 100%);
    }

    .status-overdue {
        background: linear-gradient(135deg, #B42318 0%, #D84A3A 100%);
    }

    .status-inactive {
        background: linear-gradient(135deg, #64748B 0%, #94A3B8 100%);
    }

    div[data-testid="stDataFrame"],
    div[data-testid="stDataEditor"] {
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
        <div class="hero-title">🧑‍⚕️ Provider Profile</div>
        <div class="hero-subtitle">
            View one provider’s full credentialing picture in one place, including insurance records, licenses, recredentialing, and activity history.
        </div>
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str):
    st.markdown(f'<div class="section-pill">{title}</div>', unsafe_allow_html=True)


def render_profile_item(label: str, value):
    safe_value = "—" if pd.isna(value) or str(value).strip() == "" else str(value)
    st.markdown(
        f"""
        <div class="profile-item">
            <div class="profile-label">{label}</div>
            <div class="profile-value">{safe_value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def status_badge(status):
    text = str(status).strip()

    if text in ["Approved", "Active", "Yes"]:
        return '<span class="status-chip status-active">{}</span>'.format(text)
    if text in ["Pending", "Due Soon"]:
        return '<span class="status-chip status-pending">{}</span>'.format(text)
    if text in ["Submitted"]:
        return '<span class="status-chip status-submitted">{}</span>'.format(text)
    if text in ["Overdue", "Expired", "Denied", "No"]:
        return '<span class="status-chip status-overdue">{}</span>'.format(text)
    return '<span class="status-chip status-inactive">{}</span>'.format(text if text else "—")


def safe_dataframe(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    existing = [c for c in cols if c in df.columns]
    if not existing:
        return pd.DataFrame()
    return df[existing].copy()


# =========================================================
# LOAD DATA
# =========================================================
providers_df = load_csv(providers_file, [
    "ProviderID",
    "Provider Name",
    "First Name",
    "Last Name",
    "NPI",
    "Credentials",
    "Specialty",
    "Start Date",
    "Onboarding Status",
    "Credentialing Status",
    "Provider Status"
])

credentialing_df = load_csv(credentialing_file, [
    "RecordID",
    "ProviderID",
    "Provider Name",
    "Location",
    "Insurance Plan",
    "Application Submitted",
    "Approval Date",
    "Current Status",
    "Next Recredentialing Due"
])

licenses_df = load_csv(licenses_file, [
    "LicenseID",
    "ProviderID",
    "Provider Name",
    "Provider",
    "License Type",
    "License Number",
    "State",
    "Expiration Date",
    "Status"
])

recred_df = load_csv(recred_file, [
    "RecredID",
    "ProviderID",
    "Provider Name",
    "Insurance Plan",
    "Last Credentialed",
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
    "Notes",
    "Follow-Up Needed",
    "Follow-Up Date"
])

if providers_df is None or providers_df.empty:
    providers_df = pd.DataFrame(columns=[
        "ProviderID", "Provider Name", "First Name", "Last Name", "NPI", "Credentials", "Specialty",
        "Start Date", "Onboarding Status", "Credentialing Status", "Provider Status"
    ])

if "First Name" not in providers_df.columns:
    providers_df["First Name"] = ""

if "Last Name" not in providers_df.columns:
    providers_df["Last Name"] = ""

if "Provider Name" not in providers_df.columns:
    providers_df["Provider Name"] = ""

providers_df["Provider Name"] = providers_df["Provider Name"].fillna("").astype(str).str.strip()
missing_provider_name = providers_df["Provider Name"] == ""
providers_df.loc[missing_provider_name, "Provider Name"] = (
    providers_df.loc[missing_provider_name, "First Name"].fillna("").astype(str).str.strip()
    + " "
    + providers_df.loc[missing_provider_name, "Last Name"].fillna("").astype(str).str.strip()
).str.strip()

if credentialing_df is None or credentialing_df.empty:
    credentialing_df = pd.DataFrame(columns=[
        "RecordID", "ProviderID", "Provider Name", "Location", "Insurance Plan",
        "Application Submitted", "Approval Date", "Current Status", "Next Recredentialing Due"
    ])

if licenses_df is None or licenses_df.empty:
    licenses_df = pd.DataFrame(columns=[
        "LicenseID", "ProviderID", "Provider Name", "Provider", "License Type",
        "License Number", "State", "Expiration Date", "Status"
    ])

if recred_df is None or recred_df.empty:
    recred_df = pd.DataFrame(columns=[
        "RecredID", "ProviderID", "Provider Name", "Insurance Plan",
        "Last Credentialed", "Next Due Date", "Status"
    ])

if activity_df is None or activity_df.empty:
    activity_df = pd.DataFrame(columns=[
        "ActivityID", "ProviderID", "Provider Name", "Insurance Plan",
        "Activity Date", "Method", "Action", "Notes",
        "Follow-Up Needed", "Follow-Up Date"
    ])


# =========================================================
# HERO
# =========================================================
render_hero()


# =========================================================
# MAIN
# =========================================================
if providers_df.empty:
    st.warning("No providers found yet. Please add a provider first.")
else:
    providers_df["ProviderID"] = pd.to_numeric(providers_df["ProviderID"], errors="coerce")
    providers_df = providers_df.dropna(subset=["ProviderID"])
    providers_df["ProviderID"] = providers_df["ProviderID"].astype(int)

    provider_options = providers_df.apply(
        lambda row: f"{row['ProviderID']} - {row['Provider Name'] if str(row['Provider Name']).strip() else 'Unnamed Provider'}",
        axis=1,
    ).tolist()

    selected_provider_id_from_home = st.session_state.get("selected_provider_id")
    default_index = 0
    if selected_provider_id_from_home is not None:
        selected_matches = providers_df.index[providers_df["ProviderID"] == selected_provider_id_from_home].tolist()
        if selected_matches:
            default_index = int(selected_matches[0])
        st.session_state.pop("selected_provider_id", None)

    section_header("Select Provider")

    with st.container():
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        selected_provider = st.selectbox("Select a Provider", provider_options, index=default_index)
        selected_provider_id = int(selected_provider.split(" - ")[0])
        st.markdown('</div>', unsafe_allow_html=True)

    provider_row = providers_df[providers_df["ProviderID"] == selected_provider_id].iloc[0]

    selected_provider_name = str(provider_row.get("Provider Name", "")).strip().lower()

    credentialing_by_id = pd.to_numeric(credentialing_df.get("ProviderID", pd.Series(dtype="float64")), errors="coerce") == selected_provider_id
    licenses_by_id = pd.to_numeric(licenses_df.get("ProviderID", pd.Series(dtype="float64")), errors="coerce") == selected_provider_id
    recred_by_id = pd.to_numeric(recred_df.get("ProviderID", pd.Series(dtype="float64")), errors="coerce") == selected_provider_id
    activity_by_id = pd.to_numeric(activity_df.get("ProviderID", pd.Series(dtype="float64")), errors="coerce") == selected_provider_id

    credentialing_by_name = credentialing_df.get("Provider Name", pd.Series(dtype="object")).fillna("").astype(str).str.strip().str.lower() == selected_provider_name
    licenses_by_provider = licenses_df.get("Provider", pd.Series(dtype="object")).fillna("").astype(str).str.strip().str.lower() == selected_provider_name
    licenses_by_name = licenses_df.get("Provider Name", pd.Series(dtype="object")).fillna("").astype(str).str.strip().str.lower() == selected_provider_name
    recred_by_name = recred_df.get("Provider Name", pd.Series(dtype="object")).fillna("").astype(str).str.strip().str.lower() == selected_provider_name
    activity_by_name = activity_df.get("Provider Name", pd.Series(dtype="object")).fillna("").astype(str).str.strip().str.lower() == selected_provider_name

    provider_credentialing = credentialing_df[credentialing_by_id | credentialing_by_name].copy()
    provider_licenses = licenses_df[licenses_by_id | licenses_by_name | licenses_by_provider].copy()
    provider_recred = recred_df[recred_by_id | recred_by_name].copy()
    provider_activity = activity_df[activity_by_id | activity_by_name].copy()

    # =====================================================
    # OVERVIEW METRICS
    # =====================================================
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        overview_metric_card("overview-blue", "🧾", "Insurance Records", str(len(provider_credentialing)), "Payer enrollments")
    with m2:
        overview_metric_card("overview-green", "📄", "License Records", str(len(provider_licenses)), "License and renewal entries")
    with m3:
        overview_metric_card("overview-amber", "🔄", "Recredentialing", str(len(provider_recred)), "Due date tracking records")
    with m4:
        overview_metric_card("overview-rose", "📝", "Activity Entries", str(len(provider_activity)), "Logged credentialing actions")

    # =====================================================
    # PROVIDER OVERVIEW
    # =====================================================
    section_header("Provider Overview")

    with st.container():
        st.markdown('<div class="panel">', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            render_profile_item("Provider ID", provider_row.get("ProviderID", ""))
        with col2:
            render_profile_item("Onboarding Status", provider_row.get("Onboarding Status", ""))
        with col3:
            render_profile_item("Provider Status", provider_row.get("Provider Status", ""))

        st.markdown('<div class="profile-grid">', unsafe_allow_html=True)
        render_profile_item("Provider Name", provider_row.get("Provider Name", ""))
        render_profile_item("NPI", provider_row.get("NPI", ""))
        render_profile_item("Specialty", provider_row.get("Specialty", ""))
        render_profile_item("Start Date", provider_row.get("Start Date", ""))
        render_profile_item("Credentialing Status", provider_row.get("Credentialing Status", ""))
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # =====================================================
    # INSURANCE CREDENTIALING
    # =====================================================
    section_header("Insurance Credentialing")

    with st.container():
        st.markdown('<div class="panel">', unsafe_allow_html=True)

        if provider_credentialing.empty:
            st.info("No insurance credentialing records for this provider.")
        else:
            display_df = provider_credentialing.copy()
            if "Current Status" in display_df.columns:
                display_df["Current Status"] = display_df["Current Status"].apply(status_badge)

            display_df = safe_dataframe(display_df, [
                "Current Status",
                "Insurance Plan",
                "Location",
                "Application Submitted",
                "Approval Date",
                "Next Recredentialing Due"
            ])

            st.markdown(
                display_df.to_html(index=False, escape=False),
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # =====================================================
    # LICENSES AND RENEWALS
    # =====================================================
    section_header("Licenses and Renewals")

    with st.container():
        st.markdown('<div class="panel">', unsafe_allow_html=True)

        if provider_licenses.empty:
            st.info("No license or renewal records for this provider.")
        else:
            display_df = provider_licenses.copy()
            if "Status" in display_df.columns:
                display_df["Status"] = display_df["Status"].apply(status_badge)

            display_df = safe_dataframe(display_df, [
                "Status",
                "License Type",
                "License Number",
                "State",
                "Expiration Date"
            ])

            st.markdown(
                display_df.to_html(index=False, escape=False),
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # =====================================================
    # RECREDENTIALING
    # =====================================================
    section_header("Recredentialing")

    with st.container():
        st.markdown('<div class="panel">', unsafe_allow_html=True)

        if provider_recred.empty:
            st.info("No recredentialing records for this provider.")
        else:
            display_df = provider_recred.copy()
            if "Status" in display_df.columns:
                display_df["Status"] = display_df["Status"].apply(status_badge)

            display_df = safe_dataframe(display_df, [
                "Status",
                "Insurance Plan",
                "Last Credentialed",
                "Next Due Date"
            ])

            st.markdown(
                display_df.to_html(index=False, escape=False),
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # =====================================================
    # ACTIVITY LOG
    # =====================================================
    section_header("Credentialing Activity Log")

    with st.container():
        st.markdown('<div class="panel">', unsafe_allow_html=True)

        if provider_activity.empty:
            st.info("No activity log entries for this provider.")
        else:
            provider_activity["SortDate"] = pd.to_datetime(
                provider_activity["Activity Date"],
                format="%m/%d/%Y",
                errors="coerce"
            )
            provider_activity = provider_activity.sort_values(
                by="SortDate",
                ascending=False
            ).drop(columns=["SortDate"])

            display_df = provider_activity.copy()
            if "Follow-Up Needed" in display_df.columns:
                display_df["Follow-Up Needed"] = display_df["Follow-Up Needed"].apply(status_badge)

            display_df = safe_dataframe(display_df, [
                "Activity Date",
                "Insurance Plan",
                "Method",
                "Action",
                "Follow-Up Needed",
                "Follow-Up Date",
                "Notes"
            ])

            st.markdown(
                display_df.to_html(index=False, escape=False),
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # =====================================================
    # SNAPSHOT SUMMARY
    # =====================================================
    section_header("Snapshot Summary")

    with st.container():
        st.markdown('<div class="panel">', unsafe_allow_html=True)

        left, right = st.columns([1.05, 1])

        with left:
            st.markdown("#### What This Page Shows")
            st.markdown("""
            <div class="logic-row">
                <div class="logic-badge logic-blue">Overview</div>
                <div class="logic-text">Provider identity, onboarding status, provider status, and credentialing status</div>
            </div>

            <div class="logic-row">
                <div class="logic-badge logic-green">Records</div>
                <div class="logic-text">Insurance, license, and recredentialing records tied to the selected provider</div>
            </div>

            <div class="logic-row">
                <div class="logic-badge logic-gold">Activity</div>
                <div class="logic-text">Most recent credentialing actions, follow-ups, and supporting notes</div>
            </div>
            """, unsafe_allow_html=True)

        with right:
            st.markdown("#### Recent Activity Preview")
            if provider_activity.empty:
                st.info("No recent activity available.")
            else:
                recent_preview = provider_activity.copy()
                recent_preview["SortDate"] = pd.to_datetime(
                    recent_preview["Activity Date"],
                    format="%m/%d/%Y",
                    errors="coerce"
                )
                recent_preview = recent_preview.sort_values(
                    by="SortDate",
                    ascending=False
                ).drop(columns=["SortDate"]).head(5)

                preview_df = safe_dataframe(recent_preview, [
                    "Activity Date",
                    "Insurance Plan",
                    "Action"
                ])

                st.dataframe(
                    preview_df,
                    use_container_width=True,
                    hide_index=True
                )

        st.markdown('</div>', unsafe_allow_html=True)