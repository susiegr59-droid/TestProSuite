import streamlit as st
import pandas as pd
from datetime import date

from utils.csv_helpers import load_csv, initialize_csv, save_csv
from utils.ui_helpers import apply_page_style, render_sidebar, render_page_hero, section_header, overview_metric_card


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Providers",
    page_icon="👩‍⚕️",
    layout="wide"
)

apply_page_style()
render_sidebar("Providers")


# =========================================================
# FILES / CONSTANTS
# =========================================================
providers_file = "data/providers.csv"

required_columns = [
    "ProviderID",
    "First Name",
    "Last Name",
    "DOB",
    "SSN (Last 4)",
    "NPI",
    "Taxonomy",
    "Credentials",
    "Specialty",
    "Address",
    "City",
    "State",
    "Zip",
    "Phone",
    "Email",
    "Start Date",
    "Onboarding Status",
    "Credentialing Status",
    "Provider Status",
    "Notes",
]


# =========================================================
# INITIALIZE / LOAD
# =========================================================
initialize_csv(providers_file, required_columns)
providers_df = load_csv(providers_file, required_columns)

if providers_df is None or providers_df.empty:
    providers_df = pd.DataFrame(columns=required_columns)

# Keep compatibility with older versions that used Specialty only.
if "Credentials" not in providers_df.columns:
    providers_df["Credentials"] = providers_df.get("Specialty", "")

if "Specialty" not in providers_df.columns:
    providers_df["Specialty"] = providers_df.get("Credentials", "")


# =========================================================
# HERO
# =========================================================
render_page_hero(
    "👩‍⚕️ Provider Operations",
    "Add, track, and maintain provider records used across credentialing and payer workflows.",
)


# =========================================================
# METRICS
# =========================================================
total_providers = len(providers_df)
active_providers = (
    int((providers_df["Provider Status"].astype(str).str.strip().str.lower() == "active").sum())
    if not providers_df.empty
    else 0
)
in_progress = (
    int((providers_df["Credentialing Status"].astype(str).str.strip().str.lower() == "in progress").sum())
    if not providers_df.empty
    else 0
)

m1, m2, m3 = st.columns(3)
with m1:
    overview_metric_card("overview-blue", "🧑‍⚕️", "Total<br>Providers", str(total_providers), "All saved records")
with m2:
    overview_metric_card("overview-green", "✅", "Active<br>Providers", str(active_providers), "Currently active")
with m3:
    overview_metric_card("overview-amber", "🕒", "Credentialing<br>In Progress", str(in_progress), "Needs follow-up")


# =========================================================
# ADD PROVIDER
# =========================================================
section_header("Add New Provider")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    with st.form("add_provider", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)

        with c1:
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            dob = st.date_input(
                "Date of Birth",
                value=date(1980, 1, 1),
                min_value=date(1940, 1, 1),
                max_value=date.today(),
                format="MM/DD/YYYY",
            )
            ssn_last4 = st.text_input("SSN (Last 4)", placeholder="1234")

        with c2:
            npi = st.text_input("NPI")
            taxonomy = st.text_input("Taxonomy")
            credentials = st.text_input("Credentials", placeholder="MD, DO, NP, PA-C")
            phone = st.text_input("Phone")

        with c3:
            email = st.text_input("Email")
            address = st.text_input("Address")
            city = st.text_input("City")
            state = st.text_input("State")
            zip_code = st.text_input("Zip")

        c4, c5, c6 = st.columns(3)
        with c4:
            start_date = st.date_input(
                "Start Date",
                value=date.today(),
                min_value=date(1940, 1, 1),
                max_value=date(2100, 12, 31),
                format="MM/DD/YYYY",
            )
        with c5:
            onboarding_status = st.selectbox("Onboarding Status", ["Not Started", "In Progress", "Complete"])
        with c6:
            credentialing_status = st.selectbox("Credentialing Status", ["Not Started", "In Progress", "Complete"])

        provider_status = st.selectbox("Provider Status", ["Active", "Inactive"])
        notes = st.text_area("Notes", height=90)

        submitted = st.form_submit_button("Save Provider")

    if submitted:
        if not first_name.strip() or not last_name.strip():
            st.error("Please enter both first and last name.")
        else:
            existing_ids = pd.to_numeric(providers_df["ProviderID"], errors="coerce").dropna()
            new_id = 1 if existing_ids.empty else int(existing_ids.max()) + 1

            new_row = pd.DataFrame(
                [
                    {
                        "ProviderID": new_id,
                        "First Name": first_name.strip(),
                        "Last Name": last_name.strip(),
                        "DOB": dob.strftime("%m/%d/%Y"),
                        "SSN (Last 4)": ssn_last4.strip(),
                        "NPI": npi.strip(),
                        "Taxonomy": taxonomy.strip(),
                        "Credentials": credentials.strip(),
                        "Specialty": taxonomy.strip(),
                        "Address": address.strip(),
                        "City": city.strip(),
                        "State": state.strip(),
                        "Zip": zip_code.strip(),
                        "Phone": phone.strip(),
                        "Email": email.strip(),
                        "Start Date": start_date.strftime("%m/%d/%Y"),
                        "Onboarding Status": onboarding_status,
                        "Credentialing Status": credentialing_status,
                        "Provider Status": provider_status,
                        "Notes": notes.strip(),
                    }
                ]
            )

            providers_df = pd.concat([providers_df, new_row], ignore_index=True)
            save_csv(providers_df, providers_file)

            st.success(f"{first_name.strip()} {last_name.strip()} added successfully.")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# CURRENT PROVIDERS
# =========================================================
section_header("Provider Roster")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    if providers_df.empty:
        st.info("No providers found.")
    else:
        display_df = providers_df.copy()
        display_df["Full Name"] = (
            display_df["First Name"].astype(str).str.strip() + " " + display_df["Last Name"].astype(str).str.strip()
        )

        display_columns = [
            "ProviderID",
            "Full Name",
            "NPI",
            "Credentials",
            "Phone",
            "Email",
            "City",
            "State",
            "Onboarding Status",
            "Credentialing Status",
            "Provider Status",
        ]

        safe_columns = [col for col in display_columns if col in display_df.columns]

        st.markdown(
            f'<div class="small-note">Showing <strong>{len(display_df)}</strong> provider record(s).</div>',
            unsafe_allow_html=True,
        )
        st.dataframe(display_df[safe_columns], use_container_width=True, hide_index=True)

    st.markdown("</div>", unsafe_allow_html=True)
