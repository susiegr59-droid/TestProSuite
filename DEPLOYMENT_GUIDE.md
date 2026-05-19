# Deploying ProSuite to Streamlit Cloud

This guide walks you through pushing your ProSuite app to GitHub and deploying it on Streamlit Cloud for remote testing.

---

## Prerequisites

1. **GitHub Account** — [Sign up free](https://github.com/signup)
2. **Streamlit Account** — [Sign up free](https://streamlit.io/cloud)
3. **Git installed** — [Download](https://git-scm.com/)
4. **Code ready** — You have your ProSuite folder with:
   - `app.py`
   - `requirements.txt`
   - `pages/` folder with all modules
   - `utils/` folder with helpers
   - `data/` folder with CSV files
   - `.streamlit/config.toml`
   - `README.md`

---

## Step 1: Create a GitHub Repository

### 1a. On GitHub.com:
1. Go to [github.com](https://github.com) and log in
2. Click **"+"** in top right → **"New repository"**
3. Fill in:
   - **Repository name:** `ProSuite` (or `ProSuite_TESTING`)
   - **Description:** "Provider credentialing management system"
   - **Public** (Streamlit Cloud requires public repos)
   - Check "Add a README file" (optional)
   - Click **"Create repository"**

### 1b. Copy the HTTPS clone URL:
- Click the green **"< > Code"** button
- Click **"HTTPS"** tab
- Copy the URL (should look like: `https://github.com/YOUR-USERNAME/ProSuite.git`)

---

## Step 2: Push Your Code to GitHub

Open PowerShell on your computer and navigate to your ProSuite folder:

```powershell
cd "c:\Users\grube\OneDrive\Desktop\000-ProSuite_Master\ProSuite_TESTING"
```

### Initialize Git (only first time):
```powershell
git init
git add .
git commit -m "Initial commit: ProSuite credentialing app"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/ProSuite.git
git push -u origin main
```

**Replace** `YOUR-USERNAME` with your actual GitHub username.

### For future updates:
```powershell
git add .
git commit -m "Update: [describe changes]"
git push
```

---

## Step 3: Important - Handle Sensitive Data

Before deploying, check for sensitive information in your code:

### Check for secrets in Python files:
- **Email credentials** (if in email_helpers.py)
- **API keys**
- **Database passwords**

**DO NOT commit these to GitHub.** Instead:

1. Create a file `.gitignore` in your ProSuite folder with:
```
.streamlit/secrets.toml
.env
__pycache__
*.pyc
.DS_Store
```

2. Remove secrets from code files (if present):
   - Move email credentials to `.streamlit/secrets.toml` (not committed)
   - Update email_helpers.py to load from secrets instead

3. Example: Instead of hardcoding email password in code:
```python
# BAD (don't do this in code):
# password = "mypassword123"

# GOOD (in .streamlit/secrets.toml):
# email_password = "mypassword123"

# GOOD (in code):
# import streamlit as st
# password = st.secrets["email_password"]
```

4. Commit `.gitignore` but NOT `secrets.toml`:
```powershell
git add .gitignore
git commit -m "Add .gitignore to protect secrets"
git push
```

---

## Step 4: Deploy to Streamlit Cloud

### 4a. Sign in to Streamlit Cloud:
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"Sign in"** (use your GitHub account)
3. Authorize Streamlit to access your GitHub repos

### 4b. Deploy your app:
1. Click **"Create app"** button
2. Fill in:
   - **GitHub repo:** Select `YOUR-USERNAME/ProSuite`
   - **Branch:** `main`
   - **Main file path:** `app.py`
3. Click **"Deploy"**

Streamlit will:
- Clone your repo
- Install requirements from `requirements.txt`
- Start your app
- Give you a public URL (like `your-app-name.streamlit.app`)

**This takes 2-5 minutes.** Watch the deployment logs.

---

## Step 5: Share with Your Tester

Once deployed, you'll see a public URL. Share this with your coworker:

**Example:** `https://prosuite.streamlit.app/`

**Instructions to send her:**
> "Hi [Coworker], 
> 
> ProSuite is ready for testing! Access it here: `https://prosuite.streamlit.app/`
> 
> Please work through the Testing Guide (TESTING_GUIDE.md) and report any issues.
> 
> The app uses your real provider data from our CSV files.
> 
> Thanks!"

---

## Step 6: If She Needs to Import Data

If your `data/` folder isn't auto-loaded, add a setup script:

Create `setup_data.py` in your ProSuite folder:
```python
import os
import pandas as pd
from pathlib import Path

def setup_sample_data():
    """Initialize CSV files if they don't exist"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # This runs once when app starts
    # If files exist, they're used as-is
    # If files don't exist, create empty ones with headers
    
    csv_templates = {
        "providers.csv": ["ProviderID", "Provider Name", "Specialty", "License Number", "License State", "Contact Email", "Phone"],
        "locations.csv": ["LocationID", "Location Name", "Address", "City", "State", "ZIP", "Phone", "Manager"],
        "payers.csv": ["PayerID", "Payer Name", "Contact Name", "Contact Email", "Phone", "Portal URL"],
        # Add others...
    }
    
    for filename, columns in csv_templates.items():
        filepath = data_dir / filename
        if not filepath.exists():
            df = pd.DataFrame(columns=columns)
            df.to_csv(filepath, index=False)

if __name__ == "__main__":
    setup_sample_data()
```

Then call this at the top of `app.py`:
```python
from setup_data import setup_sample_data
setup_data()
```

---

## Step 7: Monitor & Update

### View logs:
- Go to [share.streamlit.io](https://share.streamlit.io)
- Click on your ProSuite app
- Click **"Manage app"** → **"Settings"** to see logs

### Make updates:
1. Edit code locally
2. Commit and push to GitHub:
   ```powershell
   git add .
   git commit -m "Fix: [description]"
   git push
   ```
3. Streamlit Cloud auto-redeploys within seconds

### If deployment fails:
- Check logs in Streamlit Cloud dashboard
- Verify `requirements.txt` has all dependencies
- Ensure `app.py` syntax is correct
- Try running locally first: `streamlit run app.py`

---

## Step 8: Handle Streamlit Secrets (If Needed)

If your app has secrets (email credentials, API keys):

1. In Streamlit Cloud, click **"Manage app"** → **"Secrets"**
2. Add your secrets in TOML format:
   ```toml
   [email]
   smtp_server = "smtp.gmail.com"
   smtp_port = 587
   sender_email = "your-email@gmail.com"
   sender_password = "your-app-password"
   ```
3. In your code, access via:
   ```python
   import streamlit as st
   password = st.secrets["email"]["sender_password"]
   ```

---

## Troubleshooting

### "requirements.txt not found"
- Make sure `requirements.txt` is in the root folder (not in subdirectory)
- Verify the filename is exactly `requirements.txt` (lowercase)

### "ModuleNotFoundError"
- Check that all imports in your code exist in `requirements.txt`
- Example: If you use `pandas`, it must be in requirements.txt

### "CSVs not loading / no data"
- Streamlit Cloud doesn't persist the `data/` folder between deploys
- You have two options:
  1. **Use relative paths** in csv_helpers.py (should already work)
  2. **Upload via cloud storage** (Google Drive, S3, etc.) for persistent data
  3. **Use a database** (SQLite, PostgreSQL) instead of CSV

### "App is slow or timing out"
- Check if data files are too large (>100MB)
- Streamlit Cloud has a 1GB limit
- Consider database migration for large datasets

### "Can't access the deployed app"
- Verify it's set to **Public** (not Private)
- In Streamlit Cloud: Settings → "Sharing" → ensure "Public" is selected

---

## Data Persistence with CSV Files

**Important:** Streamlit Cloud runs your code fresh on each page load/interaction. For persistent CSV data, you need:

### Option 1: Local filesystem (simple, works for testing)
- CSVs stored in `data/` folder
- Data persists as long as you don't redeploy
- **Limitation:** Resets on app redeploy, multiple users overwrite each other

### Option 2: Cloud storage (better for multi-user)
- Store CSVs in Google Drive, AWS S3, or similar
- App reads/writes to cloud storage
- Persists across deployments and multiple users

### Option 3: Database (best for production)
- Use SQLite (lightweight, no setup) or PostgreSQL
- Better for concurrent access, larger datasets
- More complex setup but recommended long-term

**For now (testing phase):** Option 1 is fine. Later, consider Option 2 or 3.

---

## Quick Reference: Common Commands

```powershell
# Check Git status
git status

# Add changes
git add .

# Commit changes
git commit -m "your message"

# Push to GitHub
git push

# View recent commits
git log --oneline

# Check current branch
git branch
```

---

## Next Steps

Once your coworker tests:
1. Review her testing report (TESTING_GUIDE.md)
2. Fix critical issues
3. Push updates to GitHub
4. Streamlit Cloud auto-redeploys
5. Request follow-up testing

---

**Questions?** Refer to:
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [GitHub Quickstart](https://docs.github.com/en/get-started/quickstart)
- [Git Guide](https://git-scm.com/book/en/v2)
