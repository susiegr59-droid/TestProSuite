import streamlit as st
import pandas as pd
from datetime import date, datetime


from utils.csv_helpers import load_csv, initialize_csv, save_csv
from utils.ui_helpers import apply_page_style, render_sidebar, overview_metric_card


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Recredentialing",
    page_icon="🔄",
    layout="wide"
)

apply_page_style()
render_sidebar("Recredentialing")


# =========================================================
# PAGE-SPECIFIC STYLING
# =========================================================
st.markdown("""
<style>
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1450px !important;
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
    .metric-shell-gold,
    .metric-shell-red,
    .metric-shell-green {
        border-radius: 18px;
        padding: 14px 16px;
        color: white;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
        min-height: 88px;
    }

    .metric-shell-blue {
        background: linear-gradient(135deg, #2A6EF2 0%, #5A95FF 100%);
    }

    .metric-shell-gold {
        background: linear-gradient(135deg, #A56A00 0%, #D39B22 100%);
    }

    .metric-shell-red {
        background: linear-gradient(135deg, #B42318 0%, #D84A3A 100%);
    }

    .metric-shell-green {
        background: linear-gradient(135deg, #177E59 0%, #24A16C 100%);
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

    div[data-testid="stDataFrame"],
    div[data-testid="stDataEditor"] {
        border: 1px solid #E7EBF3;
        border-radius: 14px;
        overflow: hidden;
    }

    .status-chip {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        color: white;
        font-size: 0.78rem;
        font-weight: 700;
        text-align: center;
        min-width: 88px;
    }

    .status-active {
        background: linear-gradient(135deg, #177E59 0%, #24A16C 100%);
    }

    .status-due {
        background: linear-gradient(135deg, #A56A00 0%, #D39B22 100%);
    }

    .status-overdue {
        background: linear-gradient(135deg, #B42318 0%, #D84A3A 100%);
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
        min-width: 92px;
        text-align: center;
        padding: 6px 12px;
        border-radius: 999px;
        color: white;
        font-size: 0.82rem;
        font-weight: 700;
    }

    .logic-green {
        background: linear-gradient(135deg, #177E59 0%, #24A16C 100%);
    }

    .logic-gold {
        background: linear-gradient(135deg, #A56A00 0%, #D39B22 100%);
    }

    .logic-red {
        background: linear-gradient(135deg, #B42318 0%, #D84A3A 100%);
    }

    .logic-text {
        color: #243046;
        font-size: 0.92rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# CONSTANTS / FILES
# =========================================================
providers_file = "data/providers.csv"
recred_file = "data/recredentialing.csv"

required_columns = [
    "RecredID",
    "ProviderID",
    "Provider Name",
    "Insurance Plan",
    "Last Credentialed",
    "Next Due Date",
    "Status"
]


# =========================================================
# HELPERS
# =========================================================
def section_header(title: str):
    st.markdown(f'<div class="section-pill">{title}</div>', unsafe_allow_html=True)


def render_hero():
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-title">🔄 Recredentialing</div>
        <div class="hero-subtitle">
            Track upcoming insurance recredentialing deadlines and identify records that need action.
        </div>
    </div>
    """, unsafe_allow_html=True)


def calculate_recred_status(next_due_date):
    today = date.today()
    days_left = (next_due_date - today).days

    if days_left < 0:
        return "Overdue"
    elif days_left <= 90:
        return "Due Soon"
    else:
        return "Active"


def status_badge(status):
    status = str(status).strip()

    if status == "Active":
        return '<span class="status-chip status-active">Active</span>'
    elif status == "Due Soon":
        return '<span class="status-chip status-due">Due Soon</span>'
    elif status == "Overdue":
        return '<span class="status-chip status-overdue">Overdue</span>'
    else:
        return status


def parse_date(date_value):
    try:
        return datetime.strptime(str(date_value), "%m/%d/%Y").date()
    except Exception:
        return None


def format_display_date(date_value):
    parsed = parse_date(date_value)
    if parsed:
        return parsed.strftime("%m/%d/%Y")
    return str(date_value) if pd.notna(date_value) else ""


def days_until_due(date_value):
    parsed = parse_date(date_value)
    if not parsed:
        return pd.NA
    return (parsed - date.today()).days


# =========================================================
# INITIALIZE / LOAD DATA
# =========================================================
initialize_csv(recred_file, required_columns)

providers_df = load_csv(
    providers_file,
    ["ProviderID", "Provider Name", "Provider Status"]
)

recred_df = load_csv(recred_file, required_columns)

if providers_df is None or providers_df.empty:
    providers_df = pd.DataFrame(columns=["ProviderID", "Provider Name", "Provider Status"])

if recred_df is None or recred_df.empty:
    recred_df = pd.DataFrame(columns=required_columns)

if "Provider Status" not in providers_df.columns:
    providers_df["Provider Status"] = "Active"

providers_df = providers_df[
    providers_df["Provider Status"].astype(str).str.strip().str.lower() == "active"
].copy()


# =========================================================
# RECALCULATE STATUSES ON LOAD
# =========================================================
if not recred_df.empty:
    for idx, row in recred_df.iterrows():
        due_date = parse_date(row["Next Due Date"])
        if due_date:
            recred_df.at[idx, "Status"] = calculate_recred_status(due_date)

    save_csv(recred_df, recred_file)


# =========================================================
# DERIVED DATA
# =========================================================
if not recred_df.empty:
    recred_df["Days Until Due"] = recred_df["Next Due Date"].apply(days_until_due)
else:
    recred_df["Days Until Due"] = pd.Series(dtype="object")

total_records = len(recred_df)
due_soon_count = int((recred_df["Status"] == "Due Soon").sum()) if not recred_df.empty else 0
overdue_count = int((recred_df["Status"] == "Overdue").sum()) if not recred_df.empty else 0
active_count = int((recred_df["Status"] == "Active").sum()) if not recred_df.empty else 0


# =========================================================
# HERO
# =========================================================
render_hero()


# =========================================================
# METRICS
# =========================================================
m1, m2, m3, m4 = st.columns(4)
with m1:
    overview_metric_card("overview-blue", "🔄", "Total Records", str(total_records), "All recredentialing records")
with m2:
    overview_metric_card("overview-green", "✅", "Active", str(active_count), "More than 90 days remaining")
with m3:
    overview_metric_card("overview-amber", "⏳", "Due Soon", str(due_soon_count), "Due within 90 days")
with m4:
    overview_metric_card("overview-rose", "🚨", "Overdue", str(overdue_count), "Past due for recredentialing")


# =========================================================
# ADD RECORD
# =========================================================
section_header("Add Recredentialing Record")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    if providers_df.empty:
        st.warning("Please add an active provider first.")
    else:
        provider_options = providers_df.apply(
            lambda row: f"{row['ProviderID']} - {row['Provider Name']}",
            axis=1
        ).tolist()

        with st.form("recred_form", clear_on_submit=True):
            col1, col2 = st.columns(2)

            with col1:
                selected_provider = st.selectbox("Provider", provider_options)
                insurance_plan = st.text_input("Insurance Plan")

            with col2:
                last_credentialed = st.date_input(
                    "Last Credentialed",
                    value=date.today(),
                    format="MM/DD/YYYY"
                )
                next_due_date = st.date_input(
                    "Next Due Date",
                    value=date.today(),
                    format="MM/DD/YYYY"
                )

            submitted = st.form_submit_button("Add Recredentialing Record")

        if submitted:
            provider_id = int(float(selected_provider.split(" - ")[0]))
            provider_name = selected_provider.split(" - ", 1)[1]

            existing_ids = pd.to_numeric(
                recred_df["RecredID"],
                errors="coerce"
            ).dropna()

            if existing_ids.empty:
                new_id = 1
            else:
                new_id = int(existing_ids.max()) + 1

            auto_status = calculate_recred_status(next_due_date)

            new_row = pd.DataFrame([{
                "RecredID": new_id,
                "ProviderID": provider_id,
                "Provider Name": provider_name,
                "Insurance Plan": insurance_plan.strip(),
                "Last Credentialed": last_credentialed.strftime("%m/%d/%Y"),
                "Next Due Date": next_due_date.strftime("%m/%d/%Y"),
                "Status": auto_status
            }])

            recred_df = pd.concat([recred_df, new_row], ignore_index=True)
            save_csv(recred_df, recred_file)

            st.success(f"Recredentialing record added for {provider_name}.")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# CURRENT RECORDS
# =========================================================
section_header("Current Recredentialing Records")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    if recred_df.empty:
        st.info("No recredentialing records added yet.")
    else:
        display_df = recred_df.copy()
        display_df["Status"] = display_df["Status"].apply(status_badge)

        cols = list(display_df.columns)
        cols.insert(0, cols.pop(cols.index("Status")))
        display_df = display_df[cols]

        if "Days Until Due" in display_df.columns:
            cols = list(display_df.columns)
            cols.insert(cols.index("Next Due Date") + 1, cols.pop(cols.index("Days Until Due")))
            display_df = display_df[cols]

        st.markdown(
            f'<div class="small-note">Showing <strong>{len(display_df)}</strong> record(s).</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            display_df.to_html(index=False, escape=False),
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# STATUS LOGIC / UPCOMING
# =========================================================
section_header("Recredentialing Summary")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    left, right = st.columns([1.1, 1])

    with left:
        st.markdown("#### Status Logic")
        st.markdown("""
        <div class="logic-row">
            <div class="logic-badge logic-green">Active</div>
            <div class="logic-text">More than 90 days remaining before next due date</div>
        </div>

        <div class="logic-row">
            <div class="logic-badge logic-gold">Due Soon</div>
            <div class="logic-text">Due within the next 90 days</div>
        </div>

        <div class="logic-row">
            <div class="logic-badge logic-red">Overdue</div>
            <div class="logic-text">Next due date has already passed</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        if recred_df.empty:
            st.info("No recredentialing due dates available yet.")
        else:
            soonest = recred_df.copy()
            soonest["Parsed Due"] = soonest["Next Due Date"].apply(parse_date)
            soonest = soonest.dropna(subset=["Parsed Due"]).sort_values("Parsed Due").head(5).copy()

            if soonest.empty:
                st.info("No valid due dates available yet.")
            else:
                soonest["Next Due Date"] = soonest["Next Due Date"].apply(format_display_date)
                st.markdown("#### Next 5 Due Dates")
                st.dataframe(
                    soonest[["Provider Name", "Insurance Plan", "Next Due Date", "Status"]],
                    use_container_width=True,
                    hide_index=True
                )

    st.markdown('</div>', unsafe_allow_html=True)