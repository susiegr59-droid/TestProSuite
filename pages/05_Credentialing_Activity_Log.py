import streamlit as st
import pandas as pd
from datetime import date



from utils.csv_helpers import load_csv, initialize_csv, save_csv
from utils.ui_helpers import apply_page_style, render_sidebar, render_page_hero, section_header, overview_metric_card


st.set_page_config(
    page_title="Credentialing Activity",
    page_icon="📝",
    layout="wide"
)

apply_page_style()
render_sidebar("Credentialing Activity Log")
st.markdown("""
<style>
    .ar-highlight-row {
        background: #FFF3CD !important;
        border-left: 6px solid #F59E0B;
        font-weight: 700;
    }

    .saved-card {
        background: #ffffff;
        border: 1px solid #dbe4f0;
        border-left: 6px solid #2A6EF2;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 20px;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
    }

    .saved-card-title {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 8px;
        color: #173B6C;
    }

    .status-chip {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        color: white;
        font-size: 0.78rem;
        font-weight: 700;
        text-align: center;
        min-width: 110px;
    }

    .status-yes {
        background: linear-gradient(135deg, #A56A00 0%, #D39B22 100%);
    }

    .status-no {
        background: linear-gradient(135deg, #64748B 0%, #94A3B8 100%);
    }

</style>
""", unsafe_allow_html=True)


providers_file = "data/providers.csv"
credentialing_file = "data/insurance_credentialing.csv"
activity_file = "data/credentialing_activity.csv"

required_columns = [
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
]


if "activity_success_message" not in st.session_state:
    st.session_state.activity_success_message = ""

if "recent_activity_id" not in st.session_state:
    st.session_state.recent_activity_id = None


def safe_date(value):
    try:
        return pd.to_datetime(str(value), format="%m/%d/%Y").date()
    except Exception:
        return date.today()


def followup_badge(value):
    text = str(value).strip().lower()
    if text == "yes":
        return '<span class="status-chip status-yes">Yes</span>'
    return '<span class="status-chip status-no">No</span>'


def show_recent_activity_card(df, activity_id):
    if not activity_id:
        return

    temp_df = df.copy()
    temp_df["ActivityID"] = pd.to_numeric(temp_df["ActivityID"], errors="coerce")
    match = temp_df[temp_df["ActivityID"] == activity_id]

    if match.empty:
        return

    row = match.iloc[0]
    followup_text = "Yes" if str(row["Follow-Up Needed"]).strip().lower() == "yes" else "No"
    followup_date = str(row["Follow-Up Date"]).strip()
    if followup_date.lower() == "nan":
        followup_date = ""

    notes_text = str(row["Notes"]).strip()
    notes_text = notes_text.replace(chr(10), "<br>") if notes_text else "—"

    st.markdown("### Recently Saved Entry")
    st.markdown(
        f"""
        <div class="saved-card">
            <div class="saved-card-title">{row['Provider Name']} • {row['Insurance Plan']}</div>
            <div><strong>Activity Date:</strong> {row['Activity Date']}</div>
            <div><strong>Method:</strong> {row['Method']}</div>
            <div><strong>Action:</strong> {row['Action']}</div>
            <div><strong>Follow-Up Needed:</strong> {followup_text}</div>
            <div><strong>Follow-Up Date:</strong> {followup_date if followup_date else "—"}</div>
            <div style="margin-top:10px;"><strong>Notes:</strong><br>{notes_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_activity_table(display_df, existing_columns, ar_provider, ar_due_date):
    html = """
    <table>
        <thead>
            <tr>
    """

    for col in existing_columns:
        html += f"<th>{col}</th>"
    html += """
            </tr>
        </thead>
        <tbody>
    """

    for _, row in display_df.iterrows():
        provider_match = str(row.get("Provider Name", "")).strip() == str(ar_provider).strip()
        date_match = str(row.get("Follow-Up Date", "")).strip() == str(ar_due_date).strip()

        row_class = "ar-highlight-row" if provider_match and date_match else ""

        html += f'<tr class="{row_class}">'

        for col in existing_columns:
            value = row.get(col, "")
            if col == "Follow-Up Needed":
                value = followup_badge(value)

            if pd.isna(value):
                value = ""

            html += f"<td>{value}</td>"

        html += "</tr>"

    html += """
        </tbody>
    </table>
    """

    st.markdown(html, unsafe_allow_html=True)


initialize_csv(activity_file, required_columns)

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

credentialing_df = load_csv(credentialing_file, [
    "RecordID",
    "ProviderID",
    "Provider Name",
    "Insurance Plan",
    "Application Submitted",
    "Approval Date",
    "Current Status"
])

activity_df = load_csv(activity_file, required_columns)

if providers_df is None or providers_df.empty:
    providers_df = pd.DataFrame(columns=[
        "ProviderID", "Provider Name", "NPI", "Specialty",
        "Start Date", "Onboarding Status", "Credentialing Status", "Provider Status"
    ])

if credentialing_df is None or credentialing_df.empty:
    credentialing_df = pd.DataFrame(columns=[
        "RecordID", "ProviderID", "Provider Name", "Insurance Plan",
        "Application Submitted", "Approval Date", "Current Status"
    ])

if activity_df is None or activity_df.empty:
    activity_df = pd.DataFrame(columns=required_columns)

if st.session_state.activity_success_message:
    st.success(st.session_state.activity_success_message)
    show_recent_activity_card(activity_df, st.session_state.recent_activity_id)
    st.session_state.activity_success_message = ""
    st.session_state.recent_activity_id = None

if "Provider Status" not in providers_df.columns:
    providers_df["Provider Status"] = "Active"

providers_df = providers_df[
    providers_df["Provider Status"].astype(str).str.strip().str.lower() == "active"
].copy()


ar_provider = st.session_state.get("ar_provider", "")
ar_due_date = st.session_state.get("ar_due_date", "")
ar_notes = st.session_state.get("ar_notes", "")
opened_from_action_required = bool(ar_provider or ar_due_date or ar_notes)


render_page_hero(
    "📝 Credentialing Activity Log",
    "Document calls, faxes, emails, status checks, follow-ups, and other credentialing activity.",
)


if activity_df.empty:
    total_entries = 0
    followups_needed = 0
    phone_calls = 0
else:
    total_entries = len(activity_df)
    followups_needed = int((activity_df["Follow-Up Needed"].astype(str).str.strip().str.lower() == "yes").sum())
    phone_calls = int((activity_df["Method"].astype(str).str.strip().str.lower() == "phone").sum())

m1, m2, m3 = st.columns(3)

with m1:
    overview_metric_card("overview-blue", "🗂️", "Total Activity<br>Entries", str(total_entries), "All logged activity")

with m2:
    overview_metric_card("overview-amber", "🔔", "Follow-Ups<br>Needed", str(followups_needed), "Entries requiring follow-up")

with m3:
    overview_metric_card("overview-green", "📞", "Phone Calls<br>Logged", str(phone_calls), "Call activity recorded")


if opened_from_action_required:
    st.warning(
        f"Opened from Action Required. Review/edit the matching follow-up below.\n\n"
        f"Provider: {ar_provider if ar_provider else '—'}\n\n"
        f"Follow-Up Date: {ar_due_date if ar_due_date else '—'}\n\n"
        f"Notes: {ar_notes if ar_notes else '—'}"
    )


# =========================================================
# ADD ACTIVITY ENTRY — HIDDEN WHEN OPENED FROM ACTION REQUIRED
# =========================================================
if not opened_from_action_required:
    section_header("Add Activity Entry")

    with st.container():
        st.markdown('<div class="panel">', unsafe_allow_html=True)

        if providers_df.empty:
            st.warning("Please add an active provider first.")
        else:
            providers_df["ProviderID"] = pd.to_numeric(providers_df["ProviderID"], errors="coerce")
            providers_df = providers_df.dropna(subset=["ProviderID"])
            providers_df["ProviderID"] = providers_df["ProviderID"].astype(int)

            provider_options = providers_df.apply(
                lambda row: f"{row['ProviderID']} - {row['Provider Name']}",
                axis=1
            ).tolist()

            with st.form("activity_form", clear_on_submit=True):
                col1, col2 = st.columns(2)

                with col1:
                    selected_provider = st.selectbox("Provider", provider_options)
                    selected_provider_id = int(selected_provider.split(" - ")[0])
                    selected_provider_name = selected_provider.split(" - ", 1)[1]

                    provider_insurance_options = credentialing_df[
                        pd.to_numeric(credentialing_df["ProviderID"], errors="coerce") == selected_provider_id
                    ]["Insurance Plan"].dropna().astype(str).unique().tolist()

                    if provider_insurance_options:
                        insurance_plan = st.selectbox("Insurance Plan", provider_insurance_options)
                    else:
                        insurance_plan = st.text_input("Insurance Plan")

                    activity_date = st.date_input(
                        "Activity Date",
                        value=date.today(),
                        format="MM/DD/YYYY"
                    )

                with col2:
                    method_options = ["Phone", "Fax", "Email", "Portal", "Mail", "Other"]
                    action_options = [
                        "Application Submitted",
                        "Follow-Up",
                        "Documents Requested",
                        "Documents Sent",
                        "Status Check",
                        "Approval Received",
                        "Denial Received",
                        "Spoke with Representative",
                        "Left Voicemail",
                        "Other"
                    ]

                    method = st.selectbox("Method", method_options)
                    action = st.selectbox("Action", action_options)

                    follow_up_needed = st.checkbox("Follow-Up Needed")

                    follow_up_date = st.date_input(
                        "Follow-Up Date",
                        value=date.today(),
                        format="MM/DD/YYYY",
                        help="This date will only be saved if Follow-Up Needed is checked."
                    )

                notes = st.text_area("Notes", height=140)
                submitted = st.form_submit_button("Add Activity")

            if submitted:
                if not str(insurance_plan).strip():
                    st.error("Please enter or select an insurance plan.")
                else:
                    existing_ids = pd.to_numeric(activity_df["ActivityID"], errors="coerce").dropna()
                    new_id = 1 if existing_ids.empty else int(existing_ids.max()) + 1

                    new_activity = pd.DataFrame([{
                        "ActivityID": new_id,
                        "ProviderID": selected_provider_id,
                        "Provider Name": selected_provider_name,
                        "Insurance Plan": str(insurance_plan).strip(),
                        "Activity Date": activity_date.strftime("%m/%d/%Y"),
                        "Method": method,
                        "Action": action,
                        "Notes": notes.strip(),
                        "Follow-Up Needed": "Yes" if follow_up_needed else "No",
                        "Follow-Up Date": follow_up_date.strftime("%m/%d/%Y") if follow_up_needed else ""
                    }])

                    activity_df = pd.concat([activity_df, new_activity], ignore_index=True)
                    save_csv(activity_df, activity_file)

                    st.session_state.activity_success_message = f"Activity added for {selected_provider_name} - {insurance_plan}"
                    st.session_state.recent_activity_id = new_id
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# EDIT EXISTING ENTRY
# =========================================================
section_header("Edit Existing Activity Entry")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    if activity_df.empty:
        st.info("No activity entries available to edit yet.")
    else:
        display_df = activity_df.copy()
        display_df["ActivityID"] = pd.to_numeric(display_df["ActivityID"], errors="coerce")
        display_df = display_df.dropna(subset=["ActivityID"])
        display_df["ActivityID"] = display_df["ActivityID"].astype(int)

        if display_df.empty:
            st.info("No valid activity entries available to edit.")
        else:
            activity_options = display_df.apply(
                lambda row: f"{row['ActivityID']} - {row['Provider Name']} - {row['Insurance Plan']} - {row['Action']}",
                axis=1
            ).tolist()

            default_index = 0

            if opened_from_action_required:
                for idx, (_, row) in enumerate(display_df.iterrows()):
                    provider_match = str(row["Provider Name"]).strip() == str(ar_provider).strip()
                    date_match = str(row["Follow-Up Date"]).strip() == str(ar_due_date).strip()

                    if provider_match and date_match:
                        default_index = idx
                        break

            selected_activity = st.selectbox(
                "Choose an Activity Entry to Edit",
                activity_options,
                index=default_index
            )

            selected_activity_id = int(selected_activity.split(" - ")[0])
            selected_row = display_df[display_df["ActivityID"] == selected_activity_id].iloc[0]

            default_activity_date = safe_date(selected_row["Activity Date"])

            followup_needed_value = str(selected_row["Follow-Up Needed"]).strip().lower() == "yes"
            followup_date_text = str(selected_row["Follow-Up Date"]).strip()
            has_followup_date = followup_date_text != "" and followup_date_text.lower() != "nan"
            default_followup_date = safe_date(selected_row["Follow-Up Date"]) if has_followup_date else date.today()

            method_options = ["Phone", "Fax", "Email", "Portal", "Mail", "Other"]
            action_options = [
                "Application Submitted",
                "Follow-Up",
                "Documents Requested",
                "Documents Sent",
                "Status Check",
                "Approval Received",
                "Denial Received",
                "Spoke with Representative",
                "Left Voicemail",
                "Other"
            ]

            current_method = str(selected_row["Method"])
            current_action = str(selected_row["Action"])

            with st.form("edit_activity_form"):
                col1, col2 = st.columns(2)

                with col1:
                    edit_insurance_plan = st.text_input("Insurance Plan", value=str(selected_row["Insurance Plan"]))
                    edit_activity_date = st.date_input(
                        "Activity Date",
                        value=default_activity_date,
                        format="MM/DD/YYYY"
                    )
                    edit_method = st.selectbox(
                        "Method",
                        method_options,
                        index=method_options.index(current_method) if current_method in method_options else 0
                    )

                with col2:
                    edit_action = st.selectbox(
                        "Action",
                        action_options,
                        index=action_options.index(current_action) if current_action in action_options else 0
                    )
                    edit_followup_needed = st.checkbox("Follow-Up Needed", value=followup_needed_value)
                    edit_followup_date = st.date_input(
                        "Follow-Up Date",
                        value=default_followup_date,
                        format="MM/DD/YYYY",
                        help="This date will only be saved if Follow-Up Needed is checked."
                    )

                existing_notes = str(selected_row["Notes"]).strip()
                st.text_area("Existing Notes", value=existing_notes, height=150, disabled=True)
                new_note = st.text_area("Add New Note", height=120)

                save_changes = st.form_submit_button("Save Changes")

            if save_changes:
                match_mask = pd.to_numeric(activity_df["ActivityID"], errors="coerce") == selected_activity_id

                activity_df.loc[match_mask, "Insurance Plan"] = edit_insurance_plan.strip()
                activity_df.loc[match_mask, "Activity Date"] = edit_activity_date.strftime("%m/%d/%Y")
                activity_df.loc[match_mask, "Method"] = edit_method
                activity_df.loc[match_mask, "Action"] = edit_action

                existing_notes = str(selected_row["Notes"]).strip()
                new_note_text = new_note.strip()

                if new_note_text:
                    note_stamp = edit_activity_date.strftime("%m/%d/%Y")
                    if existing_notes:
                        appended_note = f"{existing_notes}\n\n[{note_stamp}] {new_note_text}"
                    else:
                        appended_note = f"[{note_stamp}] {new_note_text}"
                else:
                    appended_note = existing_notes

                activity_df.loc[match_mask, "Notes"] = appended_note
                activity_df.loc[match_mask, "Follow-Up Needed"] = "Yes" if edit_followup_needed else "No"
                activity_df.loc[match_mask, "Follow-Up Date"] = edit_followup_date.strftime("%m/%d/%Y") if edit_followup_needed else ""

                save_csv(activity_df, activity_file)
                st.session_state.activity_success_message = "Activity entry updated successfully."
                st.session_state.recent_activity_id = selected_activity_id

                for key in ["ar_provider", "ar_due_date", "ar_notes"]:
                    if key in st.session_state:
                        del st.session_state[key]

                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# DELETE ENTRY
# =========================================================
section_header("Delete Activity Entry")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    if activity_df.empty:
        st.info("No activity entries available to delete yet.")
    else:
        delete_df = activity_df.copy()
        delete_df["ActivityID"] = pd.to_numeric(delete_df["ActivityID"], errors="coerce")
        delete_df = delete_df.dropna(subset=["ActivityID"])
        delete_df["ActivityID"] = delete_df["ActivityID"].astype(int)

        if delete_df.empty:
            st.info("No valid activity entries available to delete.")
        else:
            delete_options = delete_df.apply(
                lambda row: f"{row['ActivityID']} - {row['Provider Name']} - {row['Insurance Plan']} - {row['Action']}",
                axis=1
            ).tolist()

            selected_delete = st.selectbox("Choose an Activity Entry to Delete", delete_options)
            selected_delete_id = int(selected_delete.split(" - ")[0])

            confirm_delete = st.checkbox("I understand this will permanently delete the selected activity entry.")

            if st.button("Delete Selected Activity Entry"):
                if not confirm_delete:
                    st.error("Please confirm deletion first.")
                else:
                    activity_df = activity_df[
                        pd.to_numeric(activity_df["ActivityID"], errors="coerce") != selected_delete_id
                    ]
                    save_csv(activity_df, activity_file)
                    st.session_state.activity_success_message = "Activity entry deleted."
                    st.session_state.recent_activity_id = None
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# ACTIVITY LOG
# =========================================================
section_header("Activity Log")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    if activity_df.empty:
        st.info("No activity entries have been added yet.")
    else:
        filter_col1, filter_col2 = st.columns(2)

        with filter_col1:
            provider_filter_options = ["All Providers"] + sorted(
                activity_df["Provider Name"].dropna().astype(str).unique().tolist()
            )

            default_provider = ar_provider if ar_provider in provider_filter_options else "All Providers"

            selected_provider_filter = st.selectbox(
                "Filter by Provider",
                provider_filter_options,
                index=provider_filter_options.index(default_provider)
            )

        with filter_col2:
            insurance_filter_options = ["All Insurance Plans"] + sorted(
                activity_df["Insurance Plan"].dropna().astype(str).unique().tolist()
            )

            selected_insurance_filter = st.selectbox(
                "Filter by Insurance Plan",
                insurance_filter_options
            )

        filtered_df = activity_df.copy()

        if selected_provider_filter != "All Providers":
            filtered_df = filtered_df[
                filtered_df["Provider Name"].astype(str) == selected_provider_filter
            ]

        if selected_insurance_filter != "All Insurance Plans":
            filtered_df = filtered_df[
                filtered_df["Insurance Plan"].astype(str) == selected_insurance_filter
            ]

        filtered_df["SortDate"] = pd.to_datetime(
            filtered_df["Activity Date"],
            format="%m/%d/%Y",
            errors="coerce"
        )
        filtered_df = filtered_df.sort_values(by="SortDate", ascending=False).drop(columns=["SortDate"])

        st.markdown(
            f'<div class="small-note">Showing <strong>{len(filtered_df)}</strong> record(s).</div>',
            unsafe_allow_html=True
        )

        display_df = filtered_df.copy()

        preferred_columns = [
            "Provider Name",
            "Insurance Plan",
            "Activity Date",
            "Method",
            "Action",
            "Follow-Up Needed",
            "Follow-Up Date",
            "Notes"
        ]

        existing_columns = [col for col in preferred_columns if col in display_df.columns]
        display_df = display_df[existing_columns]

        render_activity_table(display_df, existing_columns, ar_provider, ar_due_date)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# SUMMARY
# =========================================================
section_header("Activity Summary")

with st.container():
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    left, right = st.columns([1.1, 1])

    with left:
        st.markdown("#### Log Guidance")
        st.markdown("""
        <div class="logic-row">
            <div class="logic-badge logic-blue">Activity Date</div>
            <div class="logic-text">Use the actual date the outreach or action occurred</div>
        </div>

        <div class="logic-row">
            <div class="logic-badge logic-gold">Follow-Up</div>
            <div class="logic-text">Mark follow-up needed when another action is required later</div>
        </div>

        <div class="logic-row">
            <div class="logic-badge logic-green">Notes</div>
            <div class="logic-text">Add outcome details, names, reference numbers, or next steps</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        if activity_df.empty:
            st.info("No activity data available yet.")
        else:
            recent_df = activity_df.copy()
            recent_df["SortDate"] = pd.to_datetime(
                recent_df["Activity Date"],
                format="%m/%d/%Y",
                errors="coerce"
            )
            recent_df = recent_df.sort_values(by="SortDate", ascending=False).drop(columns=["SortDate"]).head(5)

            st.markdown("#### Most Recent Entries")
            st.dataframe(
                recent_df[["Provider Name", "Insurance Plan", "Activity Date", "Action"]],
                use_container_width=True,
                hide_index=True
            )

    st.markdown('</div>', unsafe_allow_html=True)