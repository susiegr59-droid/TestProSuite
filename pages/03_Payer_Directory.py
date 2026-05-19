import streamlit as st
import pandas as pd


from utils.csv_helpers import load_csv, initialize_csv, save_csv
from utils.ui_helpers import apply_page_style, render_sidebar, overview_metric_card


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Payer Directory",
    page_icon="🏦",
    layout="wide"
)

apply_page_style()
render_sidebar("Payer Directory")


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
    .metric-shell-green,
    .metric-shell-gold {
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

    .status-inactive {
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
# FILES / CONSTANTS
# =========================================================
payers_file = "data/payers.csv"

required_columns = [
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
]


# =========================================================
# HELPERS
# =========================================================
def render_hero():
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-title">🏦 Payer Directory</div>
        <div class="hero-subtitle">
            Manage payer names, Medicare contractors, regions, contact details, and recredentialing cycles.
        </div>
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str):
    st.markdown(f'<div class="section-pill">{title}</div>', unsafe_allow_html=True)


def active_badge(value):
    text = str(value).strip().lower()
    if text == "yes":
        return '<span class="status-chip status-active">Active</span>'
    return '<span class="status-chip status-inactive">Inactive</span>'


# =========================================================
# INITIALIZE / LOAD
# =========================================================
initialize_csv(payers_file, required_columns)
payers_df = load_csv(payers_file, required_columns)

if payers_df is None or payers_df.empty:
    payers_df = pd.DataFrame(columns=required_columns)


# =========================================================
# HERO
# =========================================================
render_hero()


# =========================================================
# METRICS
# =========================================================
total_payers = len(payers_df)
active_payers = int((payers_df["Active"].astype(str).str.strip().str.lower() == "yes").sum()) if not payers_df.empty else 0
inactive_payers = max(total_payers - active_payers, 0)

m1, m2, m3 = st.columns(3)
with m1:
    overview_metric_card("overview-blue", "🏦", "Total Payers", str(total_payers), "All payer directory entries")
with m2:
    overview_metric_card("overview-green", "✅", "Active Payers", str(active_payers), "Available for credentialing workflows")
with m3:
    overview_metric_card("overview-slate", "🗂️", "Inactive Payers", str(inactive_payers), "Retained for reference")


# =========================================================
# ADD PAYER
# =========================================================
section_header("Add Payer")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    with st.form("payer_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            payer_name = st.text_input("Payer Name")
            contractor = st.text_input("Contractor")
            state_region = st.text_input("State / Region")
            cycle_years = st.number_input("Cycle Years", min_value=1, max_value=10, value=3, step=1)

        with col2:
            phone = st.text_input("Phone")
            fax = st.text_input("Fax")
            portal = st.text_input("Portal")

        notes = st.text_area("Notes", height=120)

        submitted = st.form_submit_button("Add Payer")

    if submitted:
        if not payer_name.strip():
            st.error("Please enter a payer name.")
        else:
            duplicate_check = payers_df[
                payers_df["Payer Name"].astype(str).str.strip().str.lower() == payer_name.strip().lower()
            ]

            if not duplicate_check.empty:
                st.warning("That payer already exists.")
            else:
                existing_ids = pd.to_numeric(payers_df["PayerID"], errors="coerce").dropna()

                if existing_ids.empty:
                    new_id = 1
                else:
                    new_id = int(existing_ids.max()) + 1

                new_row = pd.DataFrame([{
                    "PayerID": new_id,
                    "Payer Name": payer_name.strip(),
                    "Contractor": contractor.strip(),
                    "State/Region": state_region.strip(),
                    "Cycle Years": int(cycle_years),
                    "Phone": phone.strip(),
                    "Fax": fax.strip(),
                    "Portal": portal.strip(),
                    "Notes": notes.strip(),
                    "Active": "Yes"
                }])

                payers_df = pd.concat([payers_df, new_row], ignore_index=True)
                save_csv(payers_df, payers_file)

                st.success("Payer added successfully.")
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# EDIT EXISTING PAYER
# =========================================================
section_header("Edit Existing Payer")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    if payers_df.empty:
        st.info("No payers available to edit yet.")
    else:
        edit_df = payers_df.copy()
        edit_df["PayerID"] = pd.to_numeric(edit_df["PayerID"], errors="coerce")
        edit_df = edit_df.dropna(subset=["PayerID"])
        edit_df["PayerID"] = edit_df["PayerID"].astype(int)

        if edit_df.empty:
            st.info("No valid payers available to edit.")
        else:
            payer_options = edit_df.apply(
                lambda row: f"{row['PayerID']} - {row['Payer Name']}",
                axis=1
            ).tolist()

            selected_payer = st.selectbox("Choose a Payer to Edit", payer_options)
            selected_payer_id = int(selected_payer.split(" - ")[0])

            selected_row = edit_df[edit_df["PayerID"] == selected_payer_id].iloc[0]

            with st.form("edit_payer_form"):
                col1, col2 = st.columns(2)

                with col1:
                    edit_payer_name = st.text_input("Payer Name", value=str(selected_row["Payer Name"]))
                    edit_contractor = st.text_input("Contractor", value=str(selected_row["Contractor"]))
                    edit_state_region = st.text_input("State / Region", value=str(selected_row["State/Region"]))
                    edit_cycle_years = st.number_input(
                        "Cycle Years",
                        min_value=1,
                        max_value=10,
                        value=int(float(selected_row["Cycle Years"])) if str(selected_row["Cycle Years"]).strip() else 3,
                        step=1
                    )

                with col2:
                    edit_phone = st.text_input("Phone", value=str(selected_row["Phone"]))
                    edit_fax = st.text_input("Fax", value=str(selected_row["Fax"]))
                    edit_portal = st.text_input("Portal", value=str(selected_row["Portal"]))

                    active_options = ["Yes", "No"]
                    current_active = str(selected_row["Active"]).strip()
                    edit_active = st.selectbox(
                        "Active",
                        active_options,
                        index=active_options.index(current_active) if current_active in active_options else 0
                    )

                edit_notes = st.text_area("Notes", value=str(selected_row["Notes"]), height=120)

                save_changes = st.form_submit_button("Save Changes")

            if save_changes:
                match_mask = pd.to_numeric(payers_df["PayerID"], errors="coerce") == selected_payer_id

                payers_df.loc[match_mask, "Payer Name"] = edit_payer_name.strip()
                payers_df.loc[match_mask, "Contractor"] = edit_contractor.strip()
                payers_df.loc[match_mask, "State/Region"] = edit_state_region.strip()
                payers_df.loc[match_mask, "Cycle Years"] = int(edit_cycle_years)
                payers_df.loc[match_mask, "Phone"] = edit_phone.strip()
                payers_df.loc[match_mask, "Fax"] = edit_fax.strip()
                payers_df.loc[match_mask, "Portal"] = edit_portal.strip()
                payers_df.loc[match_mask, "Notes"] = edit_notes.strip()
                payers_df.loc[match_mask, "Active"] = edit_active

                save_csv(payers_df, payers_file)
                st.success("Payer updated successfully.")
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# DELETE PAYER
# =========================================================
section_header("Delete Payer")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    if payers_df.empty:
        st.info("No payers available to delete yet.")
    else:
        delete_df = payers_df.copy()
        delete_df["PayerID"] = pd.to_numeric(delete_df["PayerID"], errors="coerce")
        delete_df = delete_df.dropna(subset=["PayerID"])
        delete_df["PayerID"] = delete_df["PayerID"].astype(int)

        if delete_df.empty:
            st.info("No valid payers available to delete.")
        else:
            delete_options = delete_df.apply(
                lambda row: f"{row['PayerID']} - {row['Payer Name']}",
                axis=1
            ).tolist()

            selected_delete = st.selectbox("Choose a Payer to Delete", delete_options)
            selected_delete_id = int(selected_delete.split(" - ")[0])

            st.warning("Delete this payer only if it was created by mistake.")
            confirm_delete = st.checkbox("I understand this will permanently delete the selected payer.")

            if st.button("Delete Selected Payer"):
                if not confirm_delete:
                    st.error("Please confirm deletion first.")
                else:
                    payers_df = payers_df[
                        pd.to_numeric(payers_df["PayerID"], errors="coerce") != selected_delete_id
                    ]
                    save_csv(payers_df, payers_file)
                    st.success("Payer deleted.")
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# CURRENT PAYERS
# =========================================================
section_header("Current Payers")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    if payers_df.empty:
        st.info("No payers found.")
    else:
        st.markdown(
            f'<div class="small-note">Showing <strong>{len(payers_df)}</strong> record(s).</div>',
            unsafe_allow_html=True
        )

        display_df = payers_df.copy()
        display_df["Active"] = display_df["Active"].apply(active_badge)

        preferred_columns = [
            "Payer Name",
            "Contractor",
            "State/Region",
            "Cycle Years",
            "Phone",
            "Fax",
            "Portal",
            "Notes",
            "Active"
        ]

        existing_columns = [col for col in preferred_columns if col in display_df.columns]
        display_df = display_df[existing_columns]

        st.markdown(
            display_df.to_html(index=False, escape=False),
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# PAYER SUMMARY
# =========================================================
section_header("Payer Summary")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    left, right = st.columns([1.1, 1])

    with left:
        st.markdown("#### Directory Guidance")
        st.markdown("""
        <div class="logic-row">
            <div class="logic-badge logic-blue">Contractor</div>
            <div class="logic-text">Use this for Medicare administrators or payer contractor details when applicable</div>
        </div>

        <div class="logic-row">
            <div class="logic-badge logic-green">Active</div>
            <div class="logic-text">Keep active payers available for provider enrollment and credentialing selection lists</div>
        </div>

        <div class="logic-row">
            <div class="logic-badge logic-gold">Cycle Years</div>
            <div class="logic-text">Store the expected recredentialing cycle to support reminders and tracking</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        active_df = payers_df.copy()
        if not active_df.empty:
            active_df = active_df[active_df["Active"].astype(str).str.strip().str.lower() == "yes"].copy()

        if active_df.empty:
            st.info("No active payers available yet.")
        else:
            st.markdown("#### Active Payer List")
            st.dataframe(
                active_df[["Payer Name", "Contractor", "State/Region", "Cycle Years"]],
                use_container_width=True,
                hide_index=True
            )

    st.markdown('</div>', unsafe_allow_html=True)