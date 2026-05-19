# ProSuite Provider Management Software

A comprehensive Streamlit-based application for managing healthcare provider credentialing, licensing, and compliance.

## Overview

ProSuite is a desktop/web application designed to streamline provider management workflows including:
- **Provider Management** — Add, edit, and search healthcare providers
- **Location Management** — Manage practice locations and facilities
- **Payer Directory** — Track insurance payers and networks
- **Insurance Credentialing** — Manage provider enrollment with insurance plans
- **Licensing & Renewals** — Track professional licenses and renewal dates
- **Recredentialing** — Manage recredentialing cycles and deadlines
- **Credentialing Activity Log** — Audit trail of all credentialing actions
- **Follow-up Tasks** — Task management for pending credentialing items
- **Provider Profiles** — Detailed provider information and credentials
- **Reports** — Generate summary reports and analytics
- **Action Required** — Alert dashboard for items requiring immediate attention

## System Requirements

- **Python:** 3.9 or higher
- **OS:** Windows, macOS, or Linux
- **Browser:** Modern browser (Chrome, Firefox, Safari, Edge)

## Installation

1. **Clone or download** the ProSuite repository:
   ```bash
   git clone <repository-url>
   cd ProSuite_TESTING
   ```

2. **Create a Python virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`.

**Configuration:**
- Modify `.streamlit/config.toml` to adjust ports, logging, or other Streamlit settings
- Edit CSS styling in `utils/ui_helpers.py` for visual customization

## Project Structure

```
ProSuite_TESTING/
├── app.py                          # Home dashboard / entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── data/                           # CSV data storage
│   ├── providers.csv
│   ├── locations.csv
│   ├── payers.csv
│   ├── insurance_credentialing.csv
│   ├── licenses.csv
│   ├── recredentialing.csv
│   ├── credentialing_activity.csv
│   ├── payer_directory.csv
│   └── taxonomy_reference.csv
├── pages/                          # Individual module pages
│   ├── 01_Providers.py
│   ├── 02_Locations.py
│   ├── 03_Payer_Directory.py
│   ├── 04_Insurance_Credentialing.py
│   ├── 05_Credentialing_Activity_Log.py
│   ├── 06_Follow_up_Tasks.py
│   ├── 07_Licenses_and_Renewals.py
│   ├── 08_Recredentialing.py
│   ├── 09_Provider_Profile.py
│   ├── 10_Reports.py
│   └── 11_Action_Required.py
├── utils/                          # Shared utility modules
│   ├── __init__.py
│   ├── ui_helpers.py               # UI styling & shared navigation
│   ├── csv_helpers.py              # CSV I/O operations
│   ├── alert_helpers.py            # Alert/notification logic
│   ├── email_helpers.py            # Email functionality
│   └── database.py                 # Database operations (future)
├── assets/                         # Images, icons, etc.
└── send_daily_summary.py           # Email digest job (optional)
```

## Data Management

### Current Setup (CSV-Based)
- Data is stored in CSV files in the `data/` directory
- Each module loads/saves data through `utils/csv_helpers.py`
- No database required for initial deployment

### CSV Schema

**providers.csv**
- ProviderID, Provider Name, Specialty, License Number, License State, Contact Email, Phone

**locations.csv**
- LocationID, Location Name, Address, City, State, ZIP, Phone, Manager

**payers.csv**
- PayerID, Payer Name, Contact Name, Contact Email, Phone, Portal URL

**insurance_credentialing.csv**
- CredentialingID, ProviderID, PayerID, Status, Application Date, Decision Date, Effective Date

**licenses.csv**
- LicenseID, ProviderID, License Type, License Number, State, Issue Date, Expiration Date, Status

**recredentialing.csv**
- RecredentialingID, ProviderID, Cycle Start Date, Cycle End Date, Status, Last Review Date

**credentialing_activity.csv**
- ActivityID, ProviderID, Activity Type, Date, Notes, Completed By

**follow_up_tasks.csv**
- TaskID, ProviderID, Task Description, Due Date, Status, Assigned To, Priority

## Key Features

### Navigation
- **Home Dashboard** (`app.py`) — Overview metrics and provider search
- **Sidebar Navigation** — Quick access to all 11 modules (rendered via `render_sidebar()` in `ui_helpers.py`)
- **Active Page Highlighting** — Visual indicator for current module

### Data Entry
- **Forms** — Add, edit, and delete providers, locations, payers, licenses, etc.
- **CSV Uploads** — Bulk operations on data (optional feature)
- **Validation** — Data validation on entry to maintain data integrity

### Reporting
- **Summary Metrics** — Dashboard cards showing key statistics
- **Reports Page** — Custom report generation
- **Activity Log** — Audit trail of all changes
- **Action Required** — Alert dashboard for overdue items

### Styling
- **Responsive Design** — Works on desktop and tablet screens
- **Custom Theme** — Blue gradient theme with professional styling
- **Accessibility** — Streamlit-compliant contrast and sizing

## Architecture Notes

### Module Pattern
Each page in `pages/` follows this pattern:
1. Import dependencies (streamlit, pandas, utils)
2. Configure page (title, icon, layout)
3. Apply styling with `apply_page_style()`
4. Render sidebar with `render_sidebar("Module Name")`
5. Load data via `load_csv()`
6. Display UI components
7. Save data via `save_csv()`

### Shared UI System
- **`apply_page_style()`** — Apply global CSS styling
- **`render_sidebar(current_page)`** — Render navigation sidebar with active page highlighting
- **`render_page_hero(title, icon)`** — Render page header
- **`section_header(text)`** — Render section dividers
- **`overview_metric_card(label, value, icon)`** — Render metric cards

### CSS Customization
Global styling in `utils/ui_helpers.py` includes:
- Sidebar styling (navigation pills, active states)
- Form button styling (submit buttons, delete buttons)
- Metric cards and containers
- Color scheme (blue gradients, text colors)

## Deployment Considerations

### For Local/Network Deployment
1. Ensure Python 3.9+ is installed on the host machine
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `streamlit run app.py`
4. Access via: `http://<host-ip>:8501`
5. Configure `.streamlit/config.toml` for network access if needed

### For Cloud Deployment (Streamlit Cloud, Docker, AWS/Azure/GCP)
1. Create `.streamlit/config.toml` with production settings
2. Add secret management (API keys, email credentials) via Streamlit secrets
3. Consider database migration from CSV (SQLite, PostgreSQL) for multi-user scenarios
4. Implement authentication layer for license validation
5. Set up scheduled jobs (email digests, license renewal alerts)

### Future Enhancements
- **Database**: Migrate from CSV to PostgreSQL/SQLite for better concurrent access and scalability
- **Authentication**: Add user login system with role-based access control
- **License Management**: Implement license key validation and expiration tracking
- **Email Integration**: Automated emails for license renewals, credentialing updates, follow-ups
- **Bulk Operations**: CSV import/export, bulk provider updates
- **API**: REST API for third-party integrations
- **Mobile**: Responsive mobile interface

## Maintenance & Updates

### For the Development Team
- **Code Standards**: All Python files should follow PEP 8 conventions
- **Comments**: Key functions should have docstrings explaining purpose, inputs, outputs
- **Testing**: Test new features locally before deployment
- **Backups**: Regularly backup CSV data files
- **Version Control**: Use Git to track all changes

### Common Tasks
- **Adding a new module**: Create new file in `pages/` following the module pattern, add to MODULES list in `ui_helpers.py`
- **Adding a field to data**: Add column to CSV, update relevant load_csv() calls with new column name
- **Changing styling**: Edit `.sb-*` CSS classes in `ui_helpers.py`
- **Fixing bugs**: Locate issue in appropriate `pages/*.py` or `utils/*.py` file, test, commit

## Support & Contact

For questions or issues, contact the development team.

---

**Version:** 1.0  
**Last Updated:** May 2026  
**License:** [Specify your license here]
