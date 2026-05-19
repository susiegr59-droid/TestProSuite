import streamlit as st
import pandas as pd


from utils.csv_helpers import load_csv, initialize_csv, save_csv
from utils.ui_helpers import apply_page_style, render_sidebar, render_page_hero, section_header, overview_metric_card


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Locations",
    page_icon="🏢",
    layout="wide"
)

apply_page_style()
render_sidebar("Locations")


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
locations_file = "data/locations.csv"

required_columns = [
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
]


# =========================================================
# HELPERS
# =========================================================
def render_hero():
    render_page_hero(
        "🏢 Practice Locations",
        "Manage practice locations used for credentialing, payer enrollment, and provider setup.",
    )


def active_badge(value):
    text = str(value).strip().lower()
    if text == "yes":
        return '<span class="status-chip status-active">Active</span>'
    return '<span class="status-chip status-inactive">Inactive</span>'


# =========================================================
# INITIALIZE / LOAD
# =========================================================
initialize_csv(locations_file, required_columns)
locations_df = load_csv(locations_file, required_columns)

if locations_df is None or locations_df.empty:
    locations_df = pd.DataFrame(columns=required_columns)


# =========================================================
# HERO
# =========================================================
render_hero()


# =========================================================
# METRICS
# =========================================================
total_locations = len(locations_df)
active_locations = int((locations_df["Active"].astype(str).str.strip().str.lower() == "yes").sum()) if not locations_df.empty else 0
inactive_locations = max(total_locations - active_locations, 0)

m1, m2, m3 = st.columns(3)
with m1:
    overview_metric_card("overview-blue", "🏢", "Total Locations", str(total_locations), "All saved location records")
with m2:
    overview_metric_card("overview-green", "✅", "Active Locations", str(active_locations), "Currently in use")
with m3:
    overview_metric_card("overview-slate", "🗂️", "Inactive Locations", str(inactive_locations), "Retained for reference")


# =========================================================
# ADD LOCATION
# =========================================================
section_header("Add Location")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    with st.form("location_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            practice_name = st.text_input("Practice Name", value="Dominion Spine and Pain")
            legal_name = st.text_input("Legal Name", value="Maryland Pain & Regenerative Center, LLC")
            dba_name = st.text_input("DBA Name", value="Dominion Spine and Pain")
            display_name = st.text_input("Display Name", placeholder="Example: Waldorf, MD")
            street = st.text_input("Street Address")

        with col2:
            city = st.text_input("City")
            state = st.text_input("State")
            zip_code = st.text_input("ZIP Code")
            group_npi = st.text_input("Group NPI")

        submitted = st.form_submit_button("Add Location")

    if submitted:
        if not display_name.strip():
            st.error("Please enter a display name.")
        elif not city.strip():
            st.error("Please enter a city.")
        elif not state.strip():
            st.error("Please enter a state.")
        else:
            existing_ids = pd.to_numeric(locations_df["LocationID"], errors="coerce").dropna()

            if existing_ids.empty:
                new_id = 1
            else:
                new_id = int(existing_ids.max()) + 1

            new_row = pd.DataFrame([{
                "LocationID": new_id,
                "Practice Name": practice_name.strip(),
                "Legal Name": legal_name.strip(),
                "DBA Name": dba_name.strip(),
                "Display Name": display_name.strip(),
                "Street Address": street.strip(),
                "City": city.strip(),
                "State": state.strip(),
                "ZIP": zip_code.strip(),
                "Group NPI": group_npi.strip(),
                "Active": "Yes"
            }])

            locations_df = pd.concat([locations_df, new_row], ignore_index=True)
            save_csv(locations_df, locations_file)

            st.success("Location added successfully.")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# EDIT LOCATION
# =========================================================
section_header("Edit Existing Location")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    if locations_df.empty:
        st.info("No locations available to edit yet.")
    else:
        edit_df = locations_df.copy()
        edit_df["LocationID"] = pd.to_numeric(edit_df["LocationID"], errors="coerce")
        edit_df = edit_df.dropna(subset=["LocationID"])
        edit_df["LocationID"] = edit_df["LocationID"].astype(int)

        if edit_df.empty:
            st.info("No valid locations available to edit.")
        else:
            location_options = edit_df.apply(
                lambda row: f"{row['LocationID']} - {row['Display Name']}",
                axis=1
            ).tolist()

            selected_location = st.selectbox("Choose a Location to Edit", location_options)
            selected_location_id = int(selected_location.split(" - ")[0])

            selected_row = edit_df[edit_df["LocationID"] == selected_location_id].iloc[0]

            with st.form("edit_location_form"):
                col1, col2 = st.columns(2)

                with col1:
                    edit_practice_name = st.text_input("Practice Name", value=str(selected_row["Practice Name"]))
                    edit_legal_name = st.text_input("Legal Name", value=str(selected_row["Legal Name"]))
                    edit_dba_name = st.text_input("DBA Name", value=str(selected_row["DBA Name"]))
                    edit_display_name = st.text_input("Display Name", value=str(selected_row["Display Name"]))
                    edit_street = st.text_input("Street Address", value=str(selected_row["Street Address"]))

                with col2:
                    edit_city = st.text_input("City", value=str(selected_row["City"]))
                    edit_state = st.text_input("State", value=str(selected_row["State"]))
                    edit_zip = st.text_input("ZIP Code", value=str(selected_row["ZIP"]))
                    edit_group_npi = st.text_input("Group NPI", value=str(selected_row["Group NPI"]))

                    active_options = ["Yes", "No"]
                    current_active = str(selected_row["Active"]).strip()
                    edit_active = st.selectbox(
                        "Active",
                        active_options,
                        index=active_options.index(current_active) if current_active in active_options else 0
                    )

                save_changes = st.form_submit_button("Save Changes")

            if save_changes:
                match_mask = pd.to_numeric(locations_df["LocationID"], errors="coerce") == selected_location_id

                locations_df.loc[match_mask, "Practice Name"] = edit_practice_name.strip()
                locations_df.loc[match_mask, "Legal Name"] = edit_legal_name.strip()
                locations_df.loc[match_mask, "DBA Name"] = edit_dba_name.strip()
                locations_df.loc[match_mask, "Display Name"] = edit_display_name.strip()
                locations_df.loc[match_mask, "Street Address"] = edit_street.strip()
                locations_df.loc[match_mask, "City"] = edit_city.strip()
                locations_df.loc[match_mask, "State"] = edit_state.strip()
                locations_df.loc[match_mask, "ZIP"] = edit_zip.strip()
                locations_df.loc[match_mask, "Group NPI"] = edit_group_npi.strip()
                locations_df.loc[match_mask, "Active"] = edit_active

                save_csv(locations_df, locations_file)
                st.success("Location updated successfully.")
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# CURRENT LOCATIONS
# =========================================================
section_header("Current Locations")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    if locations_df.empty:
        st.info("No locations found.")
    else:
        st.markdown(
            f'<div class="small-note">Showing <strong>{len(locations_df)}</strong> record(s).</div>',
            unsafe_allow_html=True
        )

        display_df = locations_df.copy()
        display_df["Active"] = display_df["Active"].apply(active_badge)

        preferred_columns = [
            "Display Name",
            "Practice Name",
            "Legal Name",
            "DBA Name",
            "Street Address",
            "City",
            "State",
            "ZIP",
            "Group NPI",
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
# LOCATION SUMMARY
# =========================================================
section_header("Location Summary")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    left, right = st.columns([1.1, 1])

    with left:
        st.markdown("#### Location Guidance")
        st.markdown("""
        <div class="logic-row">
            <div class="logic-badge logic-blue">Display Name</div>
            <div class="logic-text">Use a simple office label like Waldorf, MD for easy reference</div>
        </div>

        <div class="logic-row">
            <div class="logic-badge logic-green">Active</div>
            <div class="logic-text">Mark locations active when they should be used in payer and credentialing workflows</div>
        </div>

        <div class="logic-row">
            <div class="logic-badge logic-gold">Group NPI</div>
            <div class="logic-text">Store the billing or organizational NPI tied to that practice location</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        active_df = locations_df.copy()
        if not active_df.empty:
            active_df = active_df[active_df["Active"].astype(str).str.strip().str.lower() == "yes"].copy()

        if active_df.empty:
            st.info("No active locations available yet.")
        else:
            st.markdown("#### Active Location List")
            st.dataframe(
                active_df[["Display Name", "City", "State", "Group NPI"]],
                use_container_width=True,
                hide_index=True
            )

    st.markdown('</div>', unsafe_allow_html=True)