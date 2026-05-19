import streamlit as st
import pandas as pd
from datetime import date



from utils.csv_helpers import load_csv, save_csv
from utils.ui_helpers import apply_page_style, render_sidebar, overview_metric_card


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Follow-Up Tasks",
    page_icon="📞",
    layout="wide"
)

apply_page_style()
render_sidebar("Follow-up Tasks")


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
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
    }

    .hero-subtitle {
        color: rgba(255,255,255,0.92);
        font-size: 1rem;
        margin-top: 6px;
        margin-bottom: 0;
    }

    .section-pill {
        display: inline-block;
        background: #163A63;
        color: white;
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

    .status-overdue {
        background: linear-gradient(135deg, #B42318 0%, #D84A3A 100%);
    }

    .status-due {
        background: linear-gradient(135deg, #2A6EF2 0%, #5A95FF 100%);
    }

    .status-upcoming {
        background: linear-gradient(135deg, #A56A00 0%, #D39B22 100%);
    }

    div[data-testid="stDataFrame"],
    div[data-testid="stDataEditor"] {
        border: 1px solid #E7EBF3;
        border-radius: 14px;
        overflow: hidden;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        background: white;
        border-radius: 14px;
        overflow: hidden;
    }

    thead tr {
        background: #EAF2FF;
    }

    th {
        color: #173B6C;
        font-weight: 700;
        text-align: left;
        padding: 12px 14px;
        border-bottom: 1px solid #E5EAF2;
    }

    td {
        padding: 12px 14px;
        border-bottom: 1px solid #EEF2F7;
        color: #243046;
        vertical-align: top;
    }

    tr:last-child td {
        border-bottom: none;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# HELPERS
# =========================================================
FOLLOWUP_PATHS = [
    "data/follow_up_tasks.csv",
    "data/followups.csv",
    "data/activity_log.csv",
    "data/credentialing_activity_log.csv",
]


def section_header(title: str):
    st.markdown(f'<div class="section-pill">{title}</div>', unsafe_allow_html=True)


def coalesce_column(df: pd.DataFrame, candidates: list[str], new_name: str):
    for col in candidates:
        if col in df.columns:
            df = df.rename(columns={col: new_name})
            return df
    if new_name not in df.columns:
        df[new_name] = ""
    return df


def load_first_available_csv(paths: list[str]):
    for path in paths:
        try:
            df = load_csv(path)
            if df is not None:
                return df, path
        except Exception:
            continue
    return pd.DataFrame(), paths[0]


def normalize_followups(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        df = pd.DataFrame()

    df = df.copy()

    df = coalesce_column(df, ["Provider", "Provider Name", "provider_name", "Name"], "Provider")
    df = coalesce_column(df, ["Insurance Plan", "Payer", "Plan", "payer_name"], "Insurance Plan")
    df = coalesce_column(df, ["Follow-Up Date", "Follow Up Date", "FU Date", "f_u_date"], "Follow-Up Date")
    df = coalesce_column(df, ["Notes", "Comment", "Comments"], "Notes")
    df = coalesce_column(df, ["Status", "Task Status", "Follow-Up Status"], "Status")
    df = coalesce_column(df, ["Completed", "Is Complete"], "Completed")

    if "Follow-Up Date" not in df.columns:
        df["Follow-Up Date"] = ""

    if "Completed" not in df.columns:
        df["Completed"] = False

    df["Follow-Up Date"] = pd.to_datetime(df["Follow-Up Date"], errors="coerce")
    df["Completed"] = df["Completed"].astype(str).str.lower().isin(["true", "1", "yes", "y"])

    if "Completed" in df.columns:
        df = df[df["Completed"] == False]

    df = df[df["Follow-Up Date"].notna()].copy()

    today = pd.Timestamp(date.today())

    def calc_status(d):
        if pd.isna(d):
            return "Upcoming"
        days = (d.normalize() - today).days
        if days < 0:
            return "Overdue"
        if days == 0:
            return "Due Today"
        return "Upcoming"

    if "Status" not in df.columns:
        df["Status"] = df["Follow-Up Date"].apply(calc_status)
    else:
        df["Status"] = df.apply(
            lambda row: calc_status(row["Follow-Up Date"]) if not str(row["Status"]).strip() else calc_status(row["Follow-Up Date"]),
            axis=1
        )

    wanted = ["Status", "Provider", "Insurance Plan", "Follow-Up Date", "Notes", "Completed"]
    for col in wanted:
        if col not in df.columns:
            df[col] = ""

    df = df[wanted].copy()
    df = df.sort_values(["Follow-Up Date", "Provider"], ascending=[True, True])

    return df


def save_followups(df: pd.DataFrame, path: str):
    save_df = df.copy()
    if "Follow-Up Date" in save_df.columns:
        save_df["Follow-Up Date"] = save_df["Follow-Up Date"].apply(
            lambda x: x.strftime("%Y-%m-%d") if pd.notna(x) else ""
        )
    save_csv(save_df, path)


def status_badge(status: str) -> str:
    s = str(status).strip().lower()
    if s == "overdue":
        return '<span class="status-chip status-overdue">Overdue</span>'
    if s == "due today":
        return '<span class="status-chip status-due">Due Today</span>'
    return '<span class="status-chip status-upcoming">Upcoming</span>'


# =========================================================
# LOAD DATA
# =========================================================
raw_df, source_path = load_first_available_csv(FOLLOWUP_PATHS)
followups_df = normalize_followups(raw_df)

overdue_count = int((followups_df["Status"].astype(str) == "Overdue").sum())
due_today_count = int((followups_df["Status"].astype(str) == "Due Today").sum())
upcoming_count = int((followups_df["Status"].astype(str) == "Upcoming").sum())


# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero-wrap">
    <div class="hero-title">📞 Follow-Up Tasks</div>
    <div class="hero-subtitle">
        Track credentialing follow-ups generated from the activity log.
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# METRICS
# =========================================================
m1, m2, m3 = st.columns(3)
with m1:
    overview_metric_card("overview-rose", "🚨", "Overdue Follow-Ups", str(overdue_count), "Past due tasks needing attention")
with m2:
    overview_metric_card("overview-blue", "📅", "Due Today", str(due_today_count), "Tasks due today")
with m3:
    overview_metric_card("overview-amber", "🕒", "Upcoming", str(upcoming_count), "Future scheduled follow-ups")


# =========================================================
# STATUS OVERVIEW
# =========================================================
section_header("Follow-Up Status Overview")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns([1.2, 1.2, 1.2, 1.6])

    with c1:
        provider_filter = st.selectbox(
            "Provider",
            ["All"] + sorted([x for x in followups_df["Provider"].dropna().astype(str).unique().tolist() if x.strip()])
        )

    with c2:
        plan_filter = st.selectbox(
            "Insurance Plan",
            ["All"] + sorted([x for x in followups_df["Insurance Plan"].dropna().astype(str).unique().tolist() if x.strip()])
        )

    with c3:
        status_filter = st.selectbox(
            "Status",
            ["All", "Overdue", "Due Today", "Upcoming"]
        )

    with c4:
        search_text = st.text_input("Search", placeholder="Provider, payer, notes...")

    filtered_df = followups_df.copy()

    if provider_filter != "All":
        filtered_df = filtered_df[filtered_df["Provider"].astype(str) == provider_filter]

    if plan_filter != "All":
        filtered_df = filtered_df[filtered_df["Insurance Plan"].astype(str) == plan_filter]

    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["Status"].astype(str) == status_filter]

    if search_text.strip():
        q = search_text.strip().lower()
        filtered_df = filtered_df[
            filtered_df[["Provider", "Insurance Plan", "Notes"]]
            .astype(str)
            .apply(lambda col: col.str.lower().str.contains(q, na=False))
            .any(axis=1)
        ]

    st.markdown(
        f'<div class="small-note">Showing <strong>{len(filtered_df)}</strong> record(s).</div>',
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# FOLLOW-UP TASK LIST
# =========================================================
section_header("Follow-Up Task List")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    if filtered_df.empty:
        st.info("No follow-up tasks found for the current filter view.")
    else:
        display_df = filtered_df[["Status", "Provider", "Insurance Plan", "Follow-Up Date", "Notes"]].copy()
        display_df["Status"] = display_df["Status"].apply(status_badge)
        display_df["Follow-Up Date"] = display_df["Follow-Up Date"].apply(
            lambda x: x.strftime("%m/%d/%Y") if pd.notna(x) else ""
        )

        st.markdown(
            display_df.to_html(index=False, escape=False),
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# MARK COMPLETE
# =========================================================
section_header("Mark Follow-Up Complete")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    if filtered_df.empty:
        st.info("There are no follow-up tasks available to complete.")
    else:
        complete_options = []
        for idx, row in filtered_df.iterrows():
            due_text = row["Follow-Up Date"].strftime("%m/%d/%Y") if pd.notna(row["Follow-Up Date"]) else "No Date"
            label = f'{row["Provider"]} | {row["Insurance Plan"]} | {due_text} | {row["Status"]}'
            complete_options.append((label, idx))

        selected_label = st.selectbox(
            "Select follow-up to mark complete",
            [x[0] for x in complete_options]
        )

        selected_idx = dict(complete_options)[selected_label]

        if st.button("✅ Mark Selected Follow-Up Complete"):
            raw_save_df = raw_df.copy()

            if "Completed" not in raw_save_df.columns:
                raw_save_df["Completed"] = False

            raw_save_df = coalesce_column(
                raw_save_df,
                ["Follow-Up Date", "Follow Up Date", "FU Date", "f_u_date"],
                "Follow-Up Date"
            )
            raw_save_df = coalesce_column(
                raw_save_df,
                ["Provider", "Provider Name", "provider_name", "Name"],
                "Provider"
            )
            raw_save_df = coalesce_column(
                raw_save_df,
                ["Insurance Plan", "Payer", "Plan", "payer_name"],
                "Insurance Plan"
            )

            raw_save_df["Follow-Up Date"] = pd.to_datetime(raw_save_df["Follow-Up Date"], errors="coerce")

            match_row = filtered_df.loc[selected_idx]

            mask = raw_save_df["Follow-Up Date"].eq(match_row["Follow-Up Date"])
            mask = mask & raw_save_df["Provider"].astype(str).eq(str(match_row["Provider"]))
            mask = mask & raw_save_df["Insurance Plan"].astype(str).eq(str(match_row["Insurance Plan"]))

            raw_save_df.loc[mask, "Completed"] = True

            try:
                save_followups(raw_save_df, source_path)
                st.success("Follow-up marked complete.")
                st.rerun()
            except Exception as e:
                st.error(f"Unable to save follow-up completion: {e}")

    st.markdown('</div>', unsafe_allow_html=True)