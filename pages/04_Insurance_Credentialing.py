import streamlit as st
import pandas as pd
from datetime import date


from utils.csv_helpers import load_csv, initialize_csv, save_csv
from utils.ui_helpers import apply_page_style, render_sidebar, overview_metric_card


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Insurance Credentialing",
    page_icon="👩‍⚕️",
    layout="wide"
)

apply_page_style()
render_sidebar("Insurance Credentialing")


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
    .metric-shell-gray {
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

    .metric-shell-gray {
        background: linear-gradient(135deg, #64748B 0%, #94A3B8 100%);
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
        font-size: 0.92rem;
    }

    td {
        padding: 12px 14px;
        border-bottom: 1px solid #EEF2F7;
        color: #243046;
        vertical-align: top;
        font-size: 0.9rem;
    }

    tr:last-child td {
        border-bottom: none;
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

    .status-approved {
        background: linear-gradient(135deg, #177E59 0%, #24A16C 100%);
    }

    .status-pending {
        background: linear-gradient(135deg, #A56A00 0%, #D39B22 100%);
    }

    .status-submitted {
        background: linear-gradient(135deg, #2A6EF2 0%, #5A95FF 100%);
    }

    .status-denied {
        background: linear-gradient(135deg, #B42318 0%, #D84A3A 100%);
    }

    .status-not-started {
        background: linear-gradient(135deg, #64748B 0%, #94A3B8 100%);
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
        min-width: 110px;
        text-align: center;
        padding: 6px 12px;
        border-radius: 999px;
        color: white;
        font-size: 0.82rem;
        font-weight: 700;
    }

    .logic-green { background: linear-gradient(135deg, #177E59 0%, #24A16C 100%); }
    .logic-gold { background: linear-gradient(135deg, #A56A00 0%, #D39B22 100%); }
    .logic-blue { background: linear-gradient(135deg, #2A6EF2 0%, #5A95FF 100%); }
    .logic-red { background: linear-gradient(135deg, #B42318 0%, #D84A3A 100%); }
    .logic-gray { background: linear-gradient(135deg, #64748B 0%, #94A3B8 100%); }

    .logic-text {
        color: #243046;
        font-size: 0.92rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# FILES / CONSTANTS
# =========================================================
providers_file = "data/providers.csv"
credentialing_file = "data/insurance_credentialing.csv"
taxonomy_file = "data/taxonomy_reference.csv"
locations_file = "data/locations.csv"
payers_file = "data/payers.csv"

required_columns = [
    "RecordID",
    "ProviderID",
    "Provider Name",
    "Location",
    "Insurance Plan",
    "Application Submitted",
    "Approval Date",
    "Payer Provider ID",
    "Primary Taxonomy",
    "Primary Taxonomy Code",
    "Secondary Taxonomy",
    "Secondary Taxonomy Code",
    "Tertiary Taxonomy",
    "Tertiary Taxonomy Code",
    "Next Recredentialing Due",
    "Current Status"
]


# =========================================================
# HELPERS
# =========================================================
def render_hero():
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-title">👩‍⚕️ Insurance Credentialing</div>
        <div class="hero-subtitle">
            Manage payer enrollment, application progress, taxonomy assignments, and recredentialing due dates.
        </div>
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str):
    st.markdown(f'<div class="section-pill">{title}</div>', unsafe_allow_html=True)


def safe_date(value):
    try:
        return pd.to_datetime(str(value), format="%m/%d/%Y").date()
    except Exception:
        return date.today()


def parse_optional_date(value):
    try:
        text = str(value).strip()
        if text == "" or text.lower() == "nan":
            return None
        return pd.to_datetime(text, format="%m/%d/%Y").date()
    except Exception:
        return None


def split_taxonomy_choice(choice):
    if not choice or " - " not in choice:
        return "", ""
    specialty, code = choice.rsplit(" - ", 1)
    return specialty.strip(), code.strip()


def make_taxonomy_value(specialty, code):
    specialty = str(specialty).strip()
    code = str(code).strip()
    if specialty and code:
        return f"{specialty} - {code}"
    return ""


def status_badge(status):
    status = str(status).strip()

    if status == "Approved":
        return '<span class="status-chip status-approved">Approved</span>'
    elif status == "Pending":
        return '<span class="status-chip status-pending">Pending</span>'
    elif status == "Submitted":
        return '<span class="status-chip status-submitted">Submitted</span>'
    elif status == "Denied":
        return '<span class="status-chip status-denied">Denied</span>'
    elif status == "Not Started":
        return '<span class="status-chip status-not-started">Not Started</span>'
    else:
        return status


# =========================================================
# INITIALIZE / LOAD
# =========================================================
initialize_csv(credentialing_file, required_columns)

providers_df = load_csv(providers_file, [
    "ProviderID",
    "Provider Name",
    "NPI",
    "Specialty",
    "Start Date",
    "Onboarding Status",
    "Credentialing Status",
    "Provider Status"
])

locations_df = load_csv(locations_file, [
    "LocationID",
    "Practice Name",
    "Legal Name",
    "DBA Name",
    "Display Name",
    "Street Address",
    "City",
    "State",
    "ZIP",
    "Group NPI",
    "Active"
])

payers_df = load_csv(payers_file, [
    "PayerID",
    "Payer Name",
    "Contractor",
    "State/Region",
    "Cycle Years",
    "Phone",
    "Fax",
    "Portal",
    "Notes",
    "Active"
])

taxonomy_df = load_csv(taxonomy_file, [
    "Category",
    "Specialty",
    "Taxonomy Code"
])

credentialing_df = load_csv(credentialing_file, required_columns)

if providers_df is None or providers_df.empty:
    providers_df = pd.DataFrame(columns=[
        "ProviderID", "Provider Name", "NPI", "Specialty",
        "Start Date", "Onboarding Status", "Credentialing Status", "Provider Status"
    ])

if locations_df is None or locations_df.empty:
    locations_df = pd.DataFrame(columns=[
        "LocationID", "Practice Name", "Legal Name", "DBA Name", "Display Name",
        "Street Address", "City", "State", "ZIP", "Group NPI", "Active"
    ])

if payers_df is None or payers_df.empty:
    payers_df = pd.DataFrame(columns=[
        "PayerID", "Payer Name", "Contractor", "State/Region",
        "Cycle Years", "Phone", "Fax", "Portal", "Notes", "Active"
    ])

if taxonomy_df is None or taxonomy_df.empty:
    taxonomy_df = pd.DataFrame(columns=["Category", "Specialty", "Taxonomy Code"])

if credentialing_df is None or credentialing_df.empty:
    credentialing_df = pd.DataFrame(columns=required_columns)

if "Provider Status" not in providers_df.columns:
    providers_df["Provider Status"] = "Active"

providers_df = providers_df[
    providers_df["Provider Status"].astype(str).str.strip().str.lower() == "active"
].copy()

if "Active" not in locations_df.columns:
    locations_df["Active"] = "Yes"

locations_df = locations_df[
    locations_df["Active"].astype(str).str.strip().str.lower() == "yes"
].copy()

if "Active" not in payers_df.columns:
    payers_df["Active"] = "Yes"

payers_df = payers_df[
    payers_df["Active"].astype(str).str.strip().str.lower() == "yes"
].copy()

taxonomy_options = [""]
if not taxonomy_df.empty:
    taxonomy_options += taxonomy_df.apply(
        lambda row: f"{row['Specialty']} - {row['Taxonomy Code']}",
        axis=1
    ).tolist()


# =========================================================
# HERO
# =========================================================
render_hero()


# =========================================================
# METRICS
# =========================================================
if credentialing_df.empty:
    total_records = 0
    pending_count = 0
    approved_count = 0
    submitted_count = 0
    denied_count = 0
    not_started_count = 0
else:
    total_records = len(credentialing_df)
    pending_count = int((credentialing_df["Current Status"].astype(str) == "Pending").sum())
    approved_count = int((credentialing_df["Current Status"].astype(str) == "Approved").sum())
    submitted_count = int((credentialing_df["Current Status"].astype(str) == "Submitted").sum())
    denied_count = int((credentialing_df["Current Status"].astype(str) == "Denied").sum())
    not_started_count = int((credentialing_df["Current Status"].astype(str) == "Not Started").sum())

m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    overview_metric_card("overview-blue", "📋", "Total Records", str(total_records), "All credentialing records")
with m2:
    overview_metric_card("overview-green", "✅", "Approved", str(approved_count), "Completed approvals")
with m3:
    overview_metric_card("overview-amber", "⏳", "Pending", str(pending_count), "Awaiting payer action")
with m4:
    overview_metric_card("overview-lilac", "📤", "Submitted", str(submitted_count), "Applications sent")
with m5:
    overview_metric_card("overview-rose", "⚠️", "Denied", str(denied_count), "Needs review or follow-up")


# =========================================================
# ADD RECORD
# =========================================================
section_header("Add Insurance Credentialing Record")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    if providers_df.empty:
        st.warning("Please add an active provider first.")
    elif locations_df.empty:
        st.warning("Please add an active location first.")
    elif payers_df.empty:
        st.warning("Please add an active payer first in the Payer Directory.")
    else:
        providers_df["ProviderID"] = pd.to_numeric(providers_df["ProviderID"], errors="coerce")
        providers_df = providers_df.dropna(subset=["ProviderID"])
        providers_df["ProviderID"] = providers_df["ProviderID"].astype(int)

        provider_options = providers_df.apply(
            lambda row: (int(row["ProviderID"]), str(row["Provider Name"]).strip()),
            axis=1
        ).tolist()

        location_options = locations_df["Display Name"].dropna().astype(str).tolist()
        payer_options = payers_df["Payer Name"].dropna().astype(str).tolist()
        payer_options = sorted([payer for payer in payer_options if payer.strip() != ""])

        with st.form("insurance_credentialing_form", clear_on_submit=True):
            row1_col1, row1_col2, row1_col3 = st.columns(3)
            row2_col1, row2_col2, row2_col3 = st.columns(3)
            row3_col1, row3_col2 = st.columns(2)

            with row1_col1:
                selected_provider = st.selectbox(
                    "Provider",
                    provider_options,
                    format_func=lambda option: option[1] if option[1] else "Unnamed Provider",
                )
            with row1_col2:
                location_selected = st.selectbox("Location", location_options)
            with row1_col3:
                insurance_plan = st.selectbox("Insurance Plan", payer_options)

            with row2_col1:
                application_submitted = st.date_input(
                    "Application Submitted",
                    value=date.today(),
                    format="MM/DD/YYYY"
                )
            with row2_col2:
                approval_date_blank = st.checkbox("Approval Date not entered yet", value=True)
                if approval_date_blank:
                    approval_date = None
                else:
                    approval_date = st.date_input(
                        "Approval Date",
                        value=date.today(),
                        format="MM/DD/YYYY"
                    )
            with row2_col3:
                payer_provider_id = st.text_input("Payer Provider ID")

            with row3_col1:
                primary_taxonomy_choice = st.selectbox("Primary Taxonomy", taxonomy_options)
                secondary_taxonomy_choice = st.selectbox("Secondary Taxonomy", taxonomy_options)
                tertiary_taxonomy_choice = st.selectbox("Tertiary Taxonomy", taxonomy_options)

            with row3_col2:
                next_recred_blank = st.checkbox("Next Recredentialing Due not entered yet", value=True)
                if next_recred_blank:
                    next_recred_due = None
                else:
                    next_recred_due = st.date_input(
                        "Next Recredentialing Due",
                        value=date.today(),
                        format="MM/DD/YYYY"
                    )

                current_status = st.selectbox(
                    "Current Status",
                    ["Not Started", "Submitted", "Pending", "Approved", "Denied"]
                )

            submitted = st.form_submit_button("Add Credentialing Record")

        if submitted:
            provider_id, provider_name = selected_provider

            duplicate_check = credentialing_df[
                (pd.to_numeric(credentialing_df["ProviderID"], errors="coerce") == provider_id) &
                (credentialing_df["Insurance Plan"].astype(str).str.strip().str.lower() == insurance_plan.strip().lower()) &
                (credentialing_df["Location"].astype(str).str.strip() == location_selected)
            ]

            if not duplicate_check.empty:
                st.warning("This provider already has a record for that insurance plan at that location.")
            else:
                existing_ids = pd.to_numeric(credentialing_df["RecordID"], errors="coerce").dropna()
                new_id = 1 if existing_ids.empty else int(existing_ids.max()) + 1

                primary_taxonomy, primary_taxonomy_code = split_taxonomy_choice(primary_taxonomy_choice)
                secondary_taxonomy, secondary_taxonomy_code = split_taxonomy_choice(secondary_taxonomy_choice)
                tertiary_taxonomy, tertiary_taxonomy_code = split_taxonomy_choice(tertiary_taxonomy_choice)

                new_record = pd.DataFrame([{
                    "RecordID": new_id,
                    "ProviderID": provider_id,
                    "Provider Name": provider_name,
                    "Location": location_selected,
                    "Insurance Plan": insurance_plan.strip(),
                    "Application Submitted": application_submitted.strftime("%m/%d/%Y"),
                    "Approval Date": "" if approval_date is None else approval_date.strftime("%m/%d/%Y"),
                    "Payer Provider ID": payer_provider_id.strip(),
                    "Primary Taxonomy": primary_taxonomy,
                    "Primary Taxonomy Code": primary_taxonomy_code,
                    "Secondary Taxonomy": secondary_taxonomy,
                    "Secondary Taxonomy Code": secondary_taxonomy_code,
                    "Tertiary Taxonomy": tertiary_taxonomy,
                    "Tertiary Taxonomy Code": tertiary_taxonomy_code,
                    "Next Recredentialing Due": "" if next_recred_due is None else next_recred_due.strftime("%m/%d/%Y"),
                    "Current Status": current_status
                }])

                credentialing_df = pd.concat([credentialing_df, new_record], ignore_index=True)
                save_csv(credentialing_df, credentialing_file)
                st.success("Credentialing record added successfully.")
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# EDIT RECORD
# =========================================================
section_header("Edit Existing Credentialing Record")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    if credentialing_df.empty:
        st.info("No credentialing records available to edit yet.")
    else:
        edit_df = credentialing_df.copy()
        edit_df["RecordID"] = pd.to_numeric(edit_df["RecordID"], errors="coerce")
        edit_df = edit_df.dropna(subset=["RecordID"])
        edit_df["RecordID"] = edit_df["RecordID"].astype(int)

        record_options = edit_df.apply(
            lambda row: f"{row['RecordID']} - {row['Provider Name']} - {row['Insurance Plan']} - {row['Location']}",
            axis=1
        ).tolist()

        selected_record = st.selectbox("Choose a Credentialing Record to Edit", record_options)
        selected_record_id = int(selected_record.split(" - ")[0])

        selected_row = edit_df[edit_df["RecordID"] == selected_record_id].iloc[0]

        default_app_date = safe_date(selected_row["Application Submitted"])

        approval_date_text = str(selected_row["Approval Date"]).strip()
        has_approval_date = approval_date_text != "" and approval_date_text.lower() != "nan"
        default_approval_date = safe_date(selected_row["Approval Date"]) if has_approval_date else date.today()

        next_recred_text = str(selected_row["Next Recredentialing Due"]).strip()
        has_next_recred = next_recred_text != "" and next_recred_text.lower() != "nan"
        default_next_recred = safe_date(selected_row["Next Recredentialing Due"]) if has_next_recred else date.today()

        current_primary_value = make_taxonomy_value(
            selected_row["Primary Taxonomy"],
            selected_row["Primary Taxonomy Code"]
        )
        current_secondary_value = make_taxonomy_value(
            selected_row["Secondary Taxonomy"],
            selected_row["Secondary Taxonomy Code"]
        )
        current_tertiary_value = make_taxonomy_value(
            selected_row["Tertiary Taxonomy"],
            selected_row["Tertiary Taxonomy Code"]
        )

        status_options = ["Not Started", "Submitted", "Pending", "Approved", "Denied"]
        current_status_value = str(selected_row["Current Status"])

        location_options = locations_df["Display Name"].dropna().astype(str).tolist()
        current_location_value = str(selected_row["Location"]).strip()

        payer_options = payers_df["Payer Name"].dropna().astype(str).tolist()
        payer_options = sorted([payer for payer in payer_options if payer.strip() != ""])
        current_insurance_plan = str(selected_row["Insurance Plan"]).strip()

        with st.form("edit_credentialing_form"):
            row1_col1, row1_col2, row1_col3 = st.columns(3)
            row2_col1, row2_col2, row2_col3 = st.columns(3)
            row3_col1, row3_col2 = st.columns(2)

            with row1_col1:
                edit_location = st.selectbox(
                    "Location",
                    location_options,
                    index=location_options.index(current_location_value) if current_location_value in location_options else 0
                )

            with row1_col2:
                edit_insurance_plan = st.selectbox(
                    "Insurance Plan",
                    payer_options,
                    index=payer_options.index(current_insurance_plan) if current_insurance_plan in payer_options else 0
                )

            with row1_col3:
                edit_status = st.selectbox(
                    "Current Status",
                    status_options,
                    index=status_options.index(current_status_value) if current_status_value in status_options else 0
                )

            with row2_col1:
                edit_application_submitted = st.date_input(
                    "Application Submitted",
                    value=default_app_date,
                    format="MM/DD/YYYY"
                )

            with row2_col2:
                edit_approval_blank = st.checkbox(
                    "Approval Date not entered yet",
                    value=not has_approval_date
                )

                if edit_approval_blank:
                    edit_approval_date = None
                else:
                    edit_approval_date = st.date_input(
                        "Approval Date",
                        value=default_approval_date,
                        format="MM/DD/YYYY"
                    )

            with row2_col3:
                edit_payer_provider_id = st.text_input(
                    "Payer Provider ID",
                    value=str(selected_row["Payer Provider ID"])
                )

            with row3_col1:
                edit_primary_taxonomy_choice = st.selectbox(
                    "Primary Taxonomy",
                    taxonomy_options,
                    index=taxonomy_options.index(current_primary_value) if current_primary_value in taxonomy_options else 0
                )
                edit_secondary_taxonomy_choice = st.selectbox(
                    "Secondary Taxonomy",
                    taxonomy_options,
                    index=taxonomy_options.index(current_secondary_value) if current_secondary_value in taxonomy_options else 0
                )
                edit_tertiary_taxonomy_choice = st.selectbox(
                    "Tertiary Taxonomy",
                    taxonomy_options,
                    index=taxonomy_options.index(current_tertiary_value) if current_tertiary_value in taxonomy_options else 0
                )

            with row3_col2:
                edit_next_recred_blank = st.checkbox(
                    "Next Recredentialing Due not entered yet",
                    value=not has_next_recred
                )

                if edit_next_recred_blank:
                    edit_next_recred_due = None
                else:
                    edit_next_recred_due = st.date_input(
                        "Next Recredentialing Due",
                        value=default_next_recred,
                        format="MM/DD/YYYY"
                    )

            save_changes = st.form_submit_button("Save Changes")

        if save_changes:
            match_mask = pd.to_numeric(credentialing_df["RecordID"], errors="coerce") == selected_record_id

            edit_primary_taxonomy, edit_primary_taxonomy_code = split_taxonomy_choice(edit_primary_taxonomy_choice)
            edit_secondary_taxonomy, edit_secondary_taxonomy_code = split_taxonomy_choice(edit_secondary_taxonomy_choice)
            edit_tertiary_taxonomy, edit_tertiary_taxonomy_code = split_taxonomy_choice(edit_tertiary_taxonomy_choice)

            credentialing_df.loc[match_mask, "Location"] = edit_location
            credentialing_df.loc[match_mask, "Insurance Plan"] = edit_insurance_plan.strip()
            credentialing_df.loc[match_mask, "Application Submitted"] = edit_application_submitted.strftime("%m/%d/%Y")
            credentialing_df.loc[match_mask, "Approval Date"] = "" if edit_approval_date is None else edit_approval_date.strftime("%m/%d/%Y")
            credentialing_df.loc[match_mask, "Payer Provider ID"] = edit_payer_provider_id.strip()
            credentialing_df.loc[match_mask, "Primary Taxonomy"] = edit_primary_taxonomy
            credentialing_df.loc[match_mask, "Primary Taxonomy Code"] = edit_primary_taxonomy_code
            credentialing_df.loc[match_mask, "Secondary Taxonomy"] = edit_secondary_taxonomy
            credentialing_df.loc[match_mask, "Secondary Taxonomy Code"] = edit_secondary_taxonomy_code
            credentialing_df.loc[match_mask, "Tertiary Taxonomy"] = edit_tertiary_taxonomy
            credentialing_df.loc[match_mask, "Tertiary Taxonomy Code"] = edit_tertiary_taxonomy_code
            credentialing_df.loc[match_mask, "Next Recredentialing Due"] = "" if edit_next_recred_due is None else edit_next_recred_due.strftime("%m/%d/%Y")
            credentialing_df.loc[match_mask, "Current Status"] = edit_status

            save_csv(credentialing_df, credentialing_file)
            st.success("Credentialing record updated successfully.")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# CURRENT RECORDS
# =========================================================
section_header("Current Insurance Credentialing Records")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    if credentialing_df.empty:
        st.info("No insurance credentialing records have been added yet.")
    else:
        st.markdown(
            f'<div class="small-note">Showing <strong>{len(credentialing_df)}</strong> record(s).</div>',
            unsafe_allow_html=True
        )

        display_df = credentialing_df.copy()
        display_df["Current Status"] = display_df["Current Status"].apply(status_badge)

        preferred_columns = [
            "Current Status",
            "Provider Name",
            "Location",
            "Insurance Plan",
            "Application Submitted",
            "Approval Date",
            "Payer Provider ID",
            "Next Recredentialing Due",
            "Primary Taxonomy",
            "Primary Taxonomy Code",
            "Secondary Taxonomy",
            "Secondary Taxonomy Code",
            "Tertiary Taxonomy",
            "Tertiary Taxonomy Code"
        ]

        existing_columns = [col for col in preferred_columns if col in display_df.columns]
        display_df = display_df[existing_columns]

        st.markdown(
            display_df.to_html(index=False, escape=False),
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# STATUS SUMMARY
# =========================================================
section_header("Credentialing Status Summary")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    left, right = st.columns([1.1, 1])

    with left:
        st.markdown("#### Status Logic")
        st.markdown("""
        <div class="logic-row">
            <div class="logic-badge logic-green">Approved</div>
            <div class="logic-text">Enrollment completed and approved by the payer</div>
        </div>

        <div class="logic-row">
            <div class="logic-badge logic-gold">Pending</div>
            <div class="logic-text">Application is under review or awaiting payer action</div>
        </div>

        <div class="logic-row">
            <div class="logic-badge logic-blue">Submitted</div>
            <div class="logic-text">Application has been sent but not yet moved to pending or approved</div>
        </div>

        <div class="logic-row">
            <div class="logic-badge logic-red">Denied</div>
            <div class="logic-text">Application was denied and needs correction or follow-up</div>
        </div>

        <div class="logic-row">
            <div class="logic-badge logic-gray">Not Started</div>
            <div class="logic-text">Credentialing process has not begun yet</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        next_due_df = credentialing_df.copy()
        if "Next Recredentialing Due" in next_due_df.columns:
            next_due_df["Parsed Due"] = next_due_df["Next Recredentialing Due"].apply(parse_optional_date)
            next_due_df = next_due_df.dropna(subset=["Parsed Due"]).sort_values("Parsed Due").head(5).copy()

            if next_due_df.empty:
                st.info("No upcoming recredentialing due dates entered yet.")
            else:
                next_due_df["Current Status"] = next_due_df["Current Status"].apply(
                    lambda x: str(x)
                )
                st.markdown("#### Next 5 Recredentialing Due Dates")
                st.dataframe(
                    next_due_df[["Provider Name", "Insurance Plan", "Location", "Next Recredentialing Due", "Current Status"]],
                    use_container_width=True,
                    hide_index=True
                )
        else:
            st.info("No upcoming recredentialing due dates entered yet.")

    st.markdown('</div>', unsafe_allow_html=True)