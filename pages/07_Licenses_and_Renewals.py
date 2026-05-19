import streamlit as st
import pandas as pd
from datetime import date
import time

from utils.csv_helpers import load_csv, save_csv
from utils.ui_helpers import apply_page_style, render_sidebar, render_page_hero, section_header, overview_metric_card


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Licenses and Renewals",
    page_icon="📜",
    layout="wide"
)

apply_page_style()
render_sidebar("Licenses and Renewals")


# =========================================================
# PAGE-SPECIFIC STYLING
# =========================================================
st.markdown("""
<style>
    .stDownloadButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

    /* Darker table grid lines for the license editor */
    div[data-testid="stDataFrame"] [role="grid"] {
        border: 1px solid #7f8893 !important;
    }

    div[data-testid="stDataFrame"] [role="columnheader"],
    div[data-testid="stDataFrame"] [role="gridcell"] {
        border-right: 1px solid #8e97a3 !important;
        border-bottom: 1px solid #8e97a3 !important;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# HELPERS
# =========================================================
DATA_PATH = "data/licenses.csv"


def coalesce_column(df: pd.DataFrame, candidates: list[str], new_name: str):
    for col in candidates:
        if col in df.columns:
            df = df.rename(columns={col: new_name})
            return df
    if new_name not in df.columns:
        df[new_name] = ""
    return df


def normalize_license_df(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        df = pd.DataFrame()

    df = df.copy()

    df = coalesce_column(df, ["Provider", "Provider Name", "provider_name", "Name"], "Provider")
    df = coalesce_column(df, ["License Type", "Type", "license_type"], "License Type")
    df = coalesce_column(df, ["License Number", "Number", "license_number"], "License Number")
    df = coalesce_column(df, ["State", "Jurisdiction", "License State"], "State")
    df = coalesce_column(df, ["Issue Date", "Issued", "issue_date"], "Issue Date")
    df = coalesce_column(df, ["Expiration Date", "Expires", "expiry_date", "expiration_date"], "Expiration Date")
    df = coalesce_column(df, ["Renewal Submitted", "Submitted", "renewal_submitted"], "Renewal Submitted")
    df = coalesce_column(df, ["Status", "License Status", "status"], "Status")
    df = coalesce_column(df, ["Notes", "Comments"], "Notes")

    required_order = [
        "Provider",
        "License Type",
        "License Number",
        "State",
        "Issue Date",
        "Expiration Date",
        "Renewal Submitted",
        "Status",
        "Notes",
    ]

    for col in required_order:
        if col not in df.columns:
            df[col] = ""

    df = df[required_order]

    for date_col in ["Issue Date", "Expiration Date", "Renewal Submitted"]:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    return df


def calculate_status(expiration_date, existing_status=""):
    if pd.isna(expiration_date):
        return existing_status if str(existing_status).strip() else "Missing Date"

    today = pd.Timestamp(date.today())
    days_left = (expiration_date.normalize() - today).days

    if days_left < 0:
        return "Expired"
    if days_left <= 30:
        return "Urgent"
    if days_left <= 60:
        return "Due Soon"
    return "Active"


def add_calculated_fields(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["Calculated Status"] = df.apply(
        lambda row: calculate_status(row["Expiration Date"], row.get("Status", "")),
        axis=1
    )

    today = pd.Timestamp(date.today())
    df["Days Remaining"] = df["Expiration Date"].apply(
        lambda x: (x.normalize() - today).days if pd.notna(x) else pd.NA
    )

    return df


def safe_date_display(series):
    return series.apply(lambda x: x.date() if pd.notna(x) else None)


def format_export_df(df: pd.DataFrame) -> pd.DataFrame:
    export_df = df.copy()
    for col in ["Issue Date", "Expiration Date", "Renewal Submitted"]:
        if col in export_df.columns:
            export_df[col] = export_df[col].apply(
                lambda x: x.strftime("%Y-%m-%d") if pd.notna(x) else ""
            )
    if "Days Remaining" in export_df.columns:
        export_df["Days Remaining"] = export_df["Days Remaining"].fillna("")
    return export_df


# =========================================================
# LOAD DATA
# =========================================================
PROVIDERS_COLUMNS = [
    "Provider Name",
    "First Name",
    "Last Name",
    "Credentials",
    "NPI",
    "Taxonomy",
]

try:
    raw_df = load_csv(DATA_PATH)
except Exception:
    raw_df = pd.DataFrame()

licenses_df = normalize_license_df(raw_df)
licenses_df = add_calculated_fields(licenses_df)

providers_df = load_csv("data/providers.csv", PROVIDERS_COLUMNS)

if providers_df is None or providers_df.empty:
    providers_df = pd.DataFrame(columns=PROVIDERS_COLUMNS)

# =========================================================
# PROVIDER COMPATIBILITY
# =========================================================
if "Provider Name" not in providers_df.columns:
    providers_df["Provider Name"] = ""

if "First Name" not in providers_df.columns:
    providers_df["First Name"] = ""

if "Last Name" not in providers_df.columns:
    providers_df["Last Name"] = ""

if "Credentials" not in providers_df.columns:
    if "Specialty" in providers_df.columns:
        providers_df["Credentials"] = providers_df["Specialty"]
    else:
        providers_df["Credentials"] = ""

providers_df["Provider Name"] = (
    providers_df["Provider Name"]
    .fillna("")
    .astype(str)
    .str.strip()
)

missing_name = providers_df["Provider Name"] == ""

providers_df.loc[missing_name, "Provider Name"] = (
    providers_df.loc[missing_name, "First Name"].fillna("").astype(str).str.strip()
    + " "
    + providers_df.loc[missing_name, "Last Name"].fillna("").astype(str).str.strip()
).str.strip()

provider_options = sorted(
    [
        x for x in providers_df["Provider Name"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
        if x.strip()
    ]
)


# =========================================================
# HEADER
# =========================================================
render_page_hero(
    "📜 Licenses and Renewals",
    "Track expiration dates, renewal status, and upcoming license actions across providers.",
)


# =========================================================
# METRICS
# =========================================================
total_licenses = len(licenses_df)
expired_count = int((licenses_df["Calculated Status"] == "Expired").sum())
urgent_count = int((licenses_df["Calculated Status"] == "Urgent").sum())
due_soon_count = int((licenses_df["Calculated Status"] == "Due Soon").sum())
active_count = max(total_licenses - expired_count - urgent_count - due_soon_count, 0)
due_total = urgent_count + due_soon_count

m1, m2, m3, m4 = st.columns(4)

with m1:
    overview_metric_card("overview-blue", "📄", "Total Licenses", str(total_licenses), "All tracked license records")

with m2:
    overview_metric_card("overview-green", "✅", "Active / Stable", str(active_count), "More than 60 days remaining")

with m3:
    overview_metric_card("overview-amber", "⚠️", "Due in 60 Days", str(due_total), "Upcoming renewals")

with m4:
    overview_metric_card("overview-rose", "🚨", "Expired", str(expired_count), "Needs immediate attention")


# =========================================================
# FILTERS
# =========================================================
section_header("Filters")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns([1.4, 1.2, 1.1, 1.3])

    provider_filter_options = ["All"] + provider_options

    state_options = ["All"] + sorted(
        [
            x for x in licenses_df["State"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
            if x.strip()
        ]
    )

    status_options = [
        "All",
        "Active",
        "Due Soon",
        "Urgent",
        "Expired",
        "Missing Date",
    ]

    with c1:
        provider_filter = st.selectbox(
            "Provider",
            provider_filter_options,
            index=0
        )

    with c2:
        state_filter = st.selectbox(
            "State",
            state_options,
            index=0
        )

    with c3:
        status_filter = st.selectbox(
            "Status",
            status_options,
            index=0
        )

    with c4:
        search_text = st.text_input(
            "Search",
            placeholder="License type, number, notes..."
        )

    filtered_df = licenses_df.copy()

    if provider_filter != "All":
        filtered_df = filtered_df[
            filtered_df["Provider"].astype(str) == provider_filter
        ]

    if state_filter != "All":
        filtered_df = filtered_df[
            filtered_df["State"].astype(str) == state_filter
        ]

    if status_filter != "All":
        filtered_df = filtered_df[
            filtered_df["Calculated Status"] == status_filter
        ]

    if search_text.strip():
        q = search_text.strip().lower()

        filtered_df = filtered_df[
            filtered_df.astype(str).apply(
                lambda row: row.str.lower().str.contains(q, na=False)
            ).any(axis=1)
        ]

    st.markdown(
        f'<div class="small-note">Showing <strong>{len(filtered_df)}</strong> record(s).</div>',
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# PRIORITY RENEWALS
# =========================================================
section_header("Priority Renewals")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    priority_df = filtered_df[
        filtered_df["Calculated Status"].isin(
            ["Expired", "Urgent", "Due Soon"]
        )
    ].copy()

    priority_df = priority_df.sort_values(
        by=["Days Remaining", "Provider"],
        ascending=[True, True],
        na_position="last"
    )

    if priority_df.empty:
        st.success(
            "No urgent or upcoming renewals in the current filtered view."
        )

    else:
        display_priority = priority_df[
            [
                "Provider",
                "License Type",
                "State",
                "Expiration Date",
                "Days Remaining",
                "Calculated Status",
                "Notes",
            ]
        ].copy()

        display_priority["Expiration Date"] = safe_date_display(
            display_priority["Expiration Date"]
        )

        st.dataframe(
            display_priority,
            use_container_width=True,
            hide_index=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# LICENSE MANAGER
# =========================================================
section_header("License Manager")

with st.container():
    st.markdown('<div style="border: 4px solid #205080; border-radius: 16px; padding: 1.5rem 1rem 0.5rem 1rem; margin-bottom: 1.2rem; box-shadow: 0 0 0 4px #eaf3ff;">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #205080; font-weight: 900; margin-bottom: 0.7rem; letter-spacing: 0.5px;">📝 ADD OR EDIT LICENSES BELOW</h3>', unsafe_allow_html=True)
    st.markdown('<div style="font-weight: 800; font-size: 1rem; color: #102a43; margin-bottom: 0.6rem;">Edit records directly in the table below, then click Save Changes.</div>', unsafe_allow_html=True)

    editor_df = filtered_df[
        [
            "Provider",
            "License Type",
            "License Number",
            "State",
            "Issue Date",
            "Expiration Date",
            "Renewal Submitted",
            "Status",
            "Notes",
        ]
    ].copy()

    edited_df = st.data_editor(
        editor_df,
        use_container_width=True,
        hide_index=True,
        num_rows="dynamic",
        key="licenses_editor",
        column_config={
            "Provider": st.column_config.SelectboxColumn(
                "Provider",
                options=provider_options,
                required=True,
                width="medium",
            ),

            "License Type": st.column_config.TextColumn(
                "License Type",
                width="medium",
                required=True,
            ),

            "License Number": st.column_config.TextColumn(
                "License Number",
                width="medium",
            ),

            "State": st.column_config.TextColumn(
                "State",
                width="small",
            ),

            "Issue Date": st.column_config.DateColumn(
                "Issue Date",
                format="MM/DD/YYYY",
                width="small",
            ),

            "Expiration Date": st.column_config.DateColumn(
                "Expiration Date",
                format="MM/DD/YYYY",
                width="small",
                required=True,
            ),

            "Renewal Submitted": st.column_config.DateColumn(
                "Renewal Submitted",
                format="MM/DD/YYYY",
                width="small",
            ),

            "Status": st.column_config.SelectboxColumn(
                "Manual Status",
                width="small",
                options=[
                    "",
                    "Active",
                    "Due Soon",
                    "Urgent",
                    "Expired",
                    "Pending",
                    "Submitted",
                    "Complete",
                ],
            ),

            "Notes": st.column_config.TextColumn(
                "Notes",
                width="large",
            ),
        },
    )

    b1, b2, _ = st.columns([1, 1, 3])

    with b1:
        save_clicked = st.button("💾 Save Changes", use_container_width=True)
        if save_clicked:
            save_df = edited_df.copy()
            for col in [
                "Issue Date",
                "Expiration Date",
                "Renewal Submitted",
            ]:
                save_df[col] = pd.to_datetime(
                    save_df[col],
                    errors="coerce"
                )
            export_df = format_export_df(save_df)
            try:
                save_csv(export_df, DATA_PATH)
                st.session_state["licenses_saved_at"] = time.time()
                st.rerun()
            except Exception as e:
                st.error(f"Unable to save licenses file: {e}")

    with b2:
        csv_download_df = add_calculated_fields(
            edited_df.copy()
        )

        csv_download_df = format_export_df(
            csv_download_df
        )

        st.download_button(
            "⬇️ Export CSV",
            data=csv_download_df.to_csv(index=False).encode("utf-8"),
            file_name="licenses_and_renewals.csv",
            mime="text/csv",
            use_container_width=True,
        )

    if "licenses_saved_at" in st.session_state:
        seconds_since_save = time.time() - st.session_state["licenses_saved_at"]
        if seconds_since_save <= 4:
            st.success("Licenses file saved successfully.", icon="✅")
        else:
            del st.session_state["licenses_saved_at"]

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# RENEWAL SUMMARY
# =========================================================
section_header("Renewal Summary")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    left, right = st.columns([1.2, 1])

    with left:
        st.markdown("#### Status Logic")

        st.markdown("""
        <div class="logic-row">
            <div class="logic-badge logic-red">Expired</div>
            <div class="logic-text">Expiration date already passed</div>
        </div>

        <div class="logic-row">
            <div class="logic-badge logic-gold">Urgent</div>
            <div class="logic-text">Expires within 30 days</div>
        </div>

        <div class="logic-row">
            <div class="logic-badge logic-gold">Due Soon</div>
            <div class="logic-text">Expires within 31 to 60 days</div>
        </div>

        <div class="logic-row">
            <div class="logic-badge logic-green">Active</div>
            <div class="logic-text">More than 60 days remaining</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        soonest = licenses_df.dropna(
            subset=["Expiration Date"]
        ).sort_values(
            "Expiration Date"
        ).head(5).copy()

        if not soonest.empty:
            soonest["Expiration Date"] = safe_date_display(
                soonest["Expiration Date"]
            )

            st.markdown("#### Next 5 Expiring")

            st.dataframe(
                soonest[
                    [
                        "Provider",
                        "License Type",
                        "State",
                        "Expiration Date",
                    ]
                ],
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.info("No expiration dates available yet.")

    st.markdown('</div>', unsafe_allow_html=True)