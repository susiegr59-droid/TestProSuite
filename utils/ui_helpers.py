from pathlib import Path

import streamlit as st


MODULES = [
    {"title": "Dashboard", "page": "app.py", "key": "nav_home"},
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


def _open_page(page_path: str):
    target_page = Path(__file__).resolve().parent.parent / page_path
    if target_page.exists():
        st.switch_page(page_path)
    else:
        st.warning(f"Page is not available yet: {page_path}")


def apply_page_style():
    st.markdown(
        """
        <style>

            /* APP BACKGROUND: align module pages with landing theme */
            .stApp {
                background:
                    radial-gradient(1200px 520px at 90% -10%, rgba(56, 112, 175, 0.16), transparent),
                    radial-gradient(900px 420px at -8% 0%, rgba(13, 43, 74, 0.10), transparent),
                    linear-gradient(180deg, #eef3f8 0%, #e8eef5 100%);
            }

            [data-testid="stSidebarNav"] {
                display: none !important;
            }

            /* PAGE LAYOUT */
            .block-container {
                padding-top: 1.2rem;
                padding-bottom: 2rem;
                max-width: 1450px;
            }

            section[data-testid="stSidebar"] {
                background: linear-gradient(180deg, #163b63 0%, #1a476f 58%, #2b6f9e 100%);
                border-right: 1px solid rgba(211, 232, 248, 0.22);
                min-width: 244px !important;
                max-width: 244px !important;
            }

            section[data-testid="stSidebar"] > div {
                min-width: 244px !important;
                max-width: 244px !important;
                padding: 0.85rem 0.85rem 1rem 0.85rem;
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
                color: #ebf6ff !important;
                font-size: 0.98rem;
                font-weight: 800;
                line-height: 1.1;
            }

            .sb-subtitle {
                margin: 0.08rem 0 0 0;
                color: rgba(229, 245, 255, 0.84) !important;
                font-size: 0.72rem;
                font-weight: 600;
            }

            .sb-divider {
                height: 1px;
                background: rgba(208, 230, 249, 0.24);
                margin: 0.55rem 0 0.7rem 0;
            }

            .sb-section-label {
                margin: 0 0 0.45rem 0;
                color: rgba(233, 246, 255, 0.78) !important;
                font-size: 0.7rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
            }

            .sb-active {
                display: inline-flex;
                align-items: center;
                width: auto;
                max-width: 100%;
                border-radius: 13px;
                border: 1px solid rgba(223, 241, 255, 0.74);
                background: linear-gradient(180deg, rgba(151, 193, 229, 0.42) 0%, rgba(101, 145, 188, 0.34) 100%);
                box-shadow: 0 9px 18px rgba(7, 20, 36, 0.30), inset 0 1px 0 rgba(255, 255, 255, 0.28);
                color: #ffffff !important;
                font-weight: 800;
                text-align: left;
                justify-content: flex-start;
                padding: 0.58rem 0.8rem;
                margin-bottom: 0.42rem;
                line-height: 1.15;
            }

            section[data-testid="stSidebar"] .stButton {
                margin-bottom: 0.42rem;
            }

            section[data-testid="stSidebar"] .stButton > button {
                width: auto;
                min-width: 0;
                max-width: 100%;
                border-radius: 13px;
                border: 1px solid rgba(188, 220, 245, 0.54);
                background: linear-gradient(180deg, rgba(124, 165, 205, 0.30) 0%, rgba(84, 124, 166, 0.26) 100%);
                box-shadow: 0 6px 14px rgba(7, 20, 36, 0.24), inset 0 1px 0 rgba(255, 255, 255, 0.24);
                color: #edf8ff !important;
                font-weight: 700;
                text-align: left;
                justify-content: flex-start;
                padding: 0.52rem 0.8rem;
                margin-bottom: 0;
                line-height: 1.15;
                transition: background 0.16s ease, border-color 0.16s ease, transform 0.16s ease, box-shadow 0.16s ease;
            }

            section[data-testid="stSidebar"] .stButton > button:hover {
                background: linear-gradient(180deg, rgba(144, 186, 223, 0.34) 0%, rgba(96, 140, 184, 0.30) 100%);
                border-color: rgba(223, 241, 255, 0.72);
                color: #ffffff !important;
                transform: translateY(-1px);
                box-shadow: 0 9px 18px rgba(7, 20, 36, 0.28), inset 0 1px 0 rgba(255, 255, 255, 0.28);
            }

            section[data-testid="stSidebar"] .stButton > button * {
                color: #edf8ff !important;
            }

            header[data-testid="stHeader"] {
                background: transparent !important;
            }

            /* HEADINGS */
            h1 {
                color: #173B6C;
                font-weight: 750;
                letter-spacing: -0.02em;
                margin-bottom: 0.25rem;
            }

            h2, h3 {
                color: #173B6C;
                font-weight: 700;
                letter-spacing: -0.01em;
            }

            /* CAPTIONS / SECONDARY TEXT */
            .stCaption, p, label {
                color: #4E5F78;
            }

            /* Stronger form wording */
            [data-testid="stWidgetLabel"] p,
            [data-testid="stWidgetLabel"] label,
            label {
                font-weight: 700 !important;
                color: #2f4763 !important;
                letter-spacing: 0.01em;
            }

            /* REDUCE ACCIDENTAL TEXT HIGHLIGHTING ON DISPLAY ELEMENTS */
            h1, h2, h3, p, .stCaption {
                user-select: none;
                -webkit-user-select: none;
                -ms-user-select: none;
            }

            /* ALL BUTTONS */
            div.stButton > button {
                background: linear-gradient(180deg, #2F73D9 0%, #255FB6 100%);
                color: white !important;
                border: none;
                border-radius: 14px;
                font-weight: 600;
                transition: all 0.15s ease;
                box-shadow: 0 6px 14px rgba(15, 23, 42, 0.10);
            }

            div.stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 8px 18px rgba(15, 23, 42, 0.14);
                color: white !important;
            }

            div.stButton > button:focus {
                color: white !important;
                border: none !important;
                box-shadow: 0 8px 18px rgba(15, 23, 42, 0.14) !important;
            }

            div.stButton > button * {
                color: white !important;
            }

            /* FORM ACTION BUTTONS: use pale yellow for add/save style actions inside forms */
            div[data-testid="stFormSubmitButton"] > button {
                background: linear-gradient(180deg, #fff7cf 0%, #f7e39d 100%) !important;
                color: #5a470f !important;
                border: 1.5px solid #d7b64a !important;
                border-radius: 12px !important;
                font-weight: 700 !important;
                box-shadow: 0 7px 14px rgba(121, 96, 24, 0.16) !important;
            }

            div[data-testid="stFormSubmitButton"] > button:hover {
                background: linear-gradient(180deg, #fffbe0 0%, #f9ebba 100%) !important;
                color: #46370c !important;
                border-color: #c49a29 !important;
                box-shadow: 0 9px 18px rgba(121, 96, 24, 0.20) !important;
            }

            div[data-testid="stFormSubmitButton"] > button:focus {
                color: #46370c !important;
                border: 1.5px solid #c49a29 !important;
                box-shadow: 0 0 0 3px rgba(215, 182, 74, 0.20), 0 9px 18px rgba(121, 96, 24, 0.20) !important;
            }

            div[data-testid="stFormSubmitButton"] > button * {
                color: #5a470f !important;
            }

            /* EXPANDERS */
            .streamlit-expanderHeader {
                background: rgba(255, 255, 255, 0.88);
                border-radius: 12px;
            }

            /* DATAFRAME */
            .stDataFrame {
                background: white;
                border-radius: 16px;
                padding: 0.35rem;
                box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
            }

            /* LIGHT HEADER COLOR FOR TABLES */
            .stDataFrame [role="columnheader"] {
                background-color: #EAF2FF !important;
                color: #173B6C !important;
                font-weight: 700 !important;
            }

            /* METRICS */
            [data-testid="stMetric"] {
                background: rgba(255, 255, 255, 0.92);
                border-radius: 16px;
                padding: 1rem 1.1rem;
                box-shadow: 0 8px 20px rgba(15, 23, 42, 0.05);
            }

            /* INPUTS: make response boxes stand out */
            div[data-baseweb="select"] > div,
            div[data-baseweb="input"] > div,
            textarea {
                border-radius: 12px !important;
                border: 2px solid #9bb2c9 !important;
                background: #f9fcff !important;
                box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.75);
            }

            div[data-baseweb="select"] > div:focus-within,
            div[data-baseweb="input"] > div:focus-within,
            textarea:focus {
                border-color: #2f73d9 !important;
                box-shadow: 0 0 0 3px rgba(47, 115, 217, 0.16) !important;
            }

            input,
            textarea,
            [data-baseweb="select"] {
                font-weight: 600 !important;
                color: #173b6c !important;
            }

            /* DIVIDERS */
            hr {
                border: none;
                height: 1px;
                background: rgba(23, 59, 108, 0.10);
                margin-top: 1.5rem;
                margin-bottom: 1.5rem;
            }

            /* PAGE TOP BUTTON SPACING */
            .back-row {
                margin-bottom: 1.25rem;
            }

            .hero-wrap {
                background: linear-gradient(120deg, #0f2744 0%, #163a62 48%, #245f8e 100%);
                padding: 28px 32px;
                border-radius: 22px;
                margin-bottom: 22px;
                box-shadow: 0 16px 34px rgba(8, 29, 49, 0.20);
            }

            .hero-title {
                color: white !important;
                font-size: 2rem;
                font-weight: 750;
                margin: 0;
                line-height: 1.2;
            }

            .hero-subtitle {
                color: rgba(236, 246, 255, 0.92) !important;
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

            /* Streamlit markdown div wrappers cannot contain widgets.
               Hide empty panel placeholders so they do not render as blank white boxes. */
            .panel:empty {
                display: none !important;
                border: 0 !important;
                padding: 0 !important;
                margin: 0 !important;
                box-shadow: none !important;
                min-height: 0 !important;
            }

            .metric-shell-blue,
            .metric-shell-green,
            .metric-shell-gold,
            .metric-shell-red,
            .metric-shell-slate {
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

            .metric-shell-slate {
                background: linear-gradient(135deg, #475569 0%, #64748B 100%);
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

            .overview-blue {
                background: linear-gradient(180deg, #eef6ff 0%, #fbfdff 100%);
            }

            .overview-slate {
                background: linear-gradient(180deg, #f4f7fb 0%, #fbfcff 100%);
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
            .logic-red { background: linear-gradient(135deg, #B42318 0%, #D84A3A 100%); }

            .logic-text {
                color: #243046;
                font-size: 0.92rem;
                font-weight: 500;
            }

        </style>
        """,
        unsafe_allow_html=True
    )


def render_sidebar(current_page: str):
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
            <p class="sb-section-label">Navigation</p>
            """,
            unsafe_allow_html=True,
        )

        for module in MODULES:
            if module["title"] == current_page:
                st.markdown(f'<div class="sb-active">{module["title"]}</div>', unsafe_allow_html=True)
            else:
                if st.button(module["title"], key=f"shared_{module['key']}", type="secondary"):
                    _open_page(module["page"])


def back_to_dashboard():
    render_sidebar("Dashboard")


def render_page_hero(title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str):
    st.markdown(f'<div class="section-pill">{title}</div>', unsafe_allow_html=True)


def metric_card(color_class: str, label: str, value: str, subtext: str = ""):
    st.markdown(
        f"""
        <div class="{color_class}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-subtext">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def overview_metric_card(color_class: str, icon: str, title: str, value: str, subtext: str = ""):
    st.markdown(
        f"""
        <div class="overview-card {color_class}">
            <div class="overview-icon">{icon}</div>
            <div class="overview-title">{title}</div>
            <div class="overview-value">{value}</div>
            <div class="overview-subtext">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )