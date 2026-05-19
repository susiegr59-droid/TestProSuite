# ProSuite Testing Guide

## Overview
This guide provides comprehensive test scenarios for all 11 modules of the ProSuite application. The tester should work through each module systematically, testing data entry, validation, and navigation.

**Testing Environment:** Remote Streamlit Cloud deployment  
**Tester:** [Coworker Name]  
**Testing Period:** [Dates]  
**Data:** Real company provider data

---

## Module-by-Module Test Scenarios

### Module 1: Dashboard (Home)
**Purpose:** Overview and provider search

**Test Cases:**
- [ ] **Load Dashboard** — App loads without errors, displays metrics cards (Total Providers, Total Locations, Total Payers, Total Licenses)
- [ ] **Provider Search** — Type provider name or ID, results display correctly
- [ ] **Navigation Sidebar** — Click each module in sidebar, verify correct page loads
- [ ] **Active Page Indicator** — Dashboard should be highlighted when on home page
- [ ] **Page Layout** — No visual glitches, all text readable, styling consistent

**Report Issues:** Screenshot any errors or layout problems

---

### Module 2: Providers
**Purpose:** Manage healthcare providers

**Test Cases:**
- [ ] **Load Page** — Page loads, metric cards display (Total Providers, etc.)
- [ ] **View Providers** — Provider table displays all existing providers
- [ ] **Add Provider** — 
  - Fill in all fields (Name, Specialty, License #, State, Email, Phone)
  - Click "Add Provider"
  - New provider appears in table
  - Data saves correctly
- [ ] **Edit Provider** — 
  - Click edit on existing provider
  - Modify a field (e.g., email)
  - Save changes
  - Changes appear in table
- [ ] **Delete Provider** — 
  - Click delete on a provider
  - Confirm deletion
  - Provider removed from table
- [ ] **Search/Filter** — Can find providers by typing name
- [ ] **Required Fields** — Try to add provider with blank required fields, verify error message
- [ ] **Email Validation** — Try invalid email format, should error or warn

**Report Issues:** Any missing fields, validation gaps, or crashes

---

### Module 3: Locations
**Purpose:** Manage practice locations

**Test Cases:**
- [ ] **Load Page** — Page loads with 🏢 icon, metrics display
- [ ] **View Locations** — All locations display in table
- [ ] **Add Location** — 
  - Fill in all fields (Name, Address, City, State, ZIP, Phone, Manager)
  - Click "Add Location"
  - New location appears in table
- [ ] **Edit Location** — Modify existing location, changes save
- [ ] **Delete Location** — Remove location, verify removal from table
- [ ] **Address Format** — Verify address fields format correctly
- [ ] **Duplicate Check** — Try adding duplicate location name, should warn or prevent

**Report Issues:** Missing validations or data integrity problems

---

### Module 4: Payer Directory
**Purpose:** Manage insurance payers

**Test Cases:**
- [ ] **Load Page** — Page loads, payer metrics display
- [ ] **View Payers** — All payers display in table
- [ ] **Add Payer** — 
  - Fill fields (Payer Name, Contact Name, Email, Phone, Portal URL)
  - Save successfully
- [ ] **Edit Payer** — Modify payer details, changes persist
- [ ] **Delete Payer** — Remove payer, verify deletion
- [ ] **URL Validation** — Try invalid Portal URL, should error or warn
- [ ] **Contact Fields** — Email and phone format validated

**Report Issues:** Validation issues or data save failures

---

### Module 5: Insurance Credentialing
**Purpose:** Track provider enrollment with payers

**Test Cases:**
- [ ] **Load Page** — Page loads, credentialing metrics display
- [ ] **View Credentialing Records** — Table shows all provider-payer enrollments
- [ ] **Add Credentialing Record** —
  - Select Provider (dropdown should show provider names only, not IDs)
  - Select Payer
  - Set Status (e.g., "Pending", "Approved", "Denied")
  - Set Application Date
  - Set Decision Date (if applicable)
  - Set Effective Date
  - Save
- [ ] **Edit Record** — Modify status or dates, changes persist
- [ ] **Delete Record** — Remove record, verify deletion
- [ ] **Provider Dropdown** — Should only show provider names (not numeric IDs)
- [ ] **Date Validation** — Decision Date cannot be before Application Date
- [ ] **Status Transitions** — Verify logical status flow (Pending → Approved → Effective)

**Report Issues:** Provider ID visibility, date validation issues, or data problems

---

### Module 6: Licenses & Renewals
**Purpose:** Track professional licenses and expiration dates

**Test Cases:**
- [ ] **Load Page** — Page loads, license metrics display
- [ ] **View Licenses** — All provider licenses display in table
- [ ] **Add License** —
  - Select Provider
  - Enter License Type (e.g., "MD", "NP", "PA")
  - Enter License Number
  - Select State
  - Set Issue Date
  - Set Expiration Date
  - Set Status (Active, Expired, Pending Renewal)
  - Save
- [ ] **Edit License** — Modify license details, changes persist
- [ ] **Delete License** — Remove license, verify deletion
- [ ] **Expiration Alert** — Licenses expiring soon should be highlighted or flagged
- [ ] **Date Validation** — Issue Date cannot be after Expiration Date
- [ ] **Renewal Tracking** — Status "Pending Renewal" should be trackable

**Report Issues:** Expiration alerts, date validation, status tracking issues

---

### Module 7: Recredentialing
**Purpose:** Manage recredentialing cycles

**Test Cases:**
- [ ] **Load Page** — Page loads, recredentialing metrics display
- [ ] **View Cycles** — All recredentialing cycles display
- [ ] **Add Cycle** —
  - Select Provider
  - Set Cycle Start Date
  - Set Cycle End Date
  - Set Status (e.g., "In Progress", "Complete", "Overdue")
  - Save
- [ ] **Edit Cycle** — Modify dates or status, changes persist
- [ ] **Delete Cycle** — Remove cycle, verify deletion
- [ ] **Date Validation** — Start Date cannot be after End Date
- [ ] **Overdue Detection** — Cycles past End Date should show "Overdue" status option
- [ ] **Last Review Date** — Should auto-populate or allow manual entry

**Report Issues:** Date validation, status tracking, or overdue detection problems

---

### Module 8: Credentialing Activity Log
**Purpose:** Audit trail of all credentialing actions

**Test Cases:**
- [ ] **Load Page** — Page loads, displays activity log
- [ ] **View Log** — All activities display with date, provider, action type, notes
- [ ] **Log Entry Format** — Each entry should show:
  - Date/Time
  - Provider Name
  - Activity Type (Application, Approval, Denial, etc.)
  - Notes
- [ ] **Auto-logging** — When you add/edit/delete items in other modules, are they logged here?
- [ ] **Filter by Provider** — Can filter log by provider name
- [ ] **Filter by Date Range** — Can filter by date range (optional but nice)
- [ ] **Add Manual Entry** — Can manually log an activity
- [ ] **Completeness** — Log should capture all significant actions from other modules

**Report Issues:** Missing activity logs, incomplete entries, or filtering issues

---

### Module 9: Follow-up Tasks
**Purpose:** Task management for pending credentialing items

**Test Cases:**
- [ ] **Load Page** — Page loads, task metrics display
- [ ] **View Tasks** — All tasks display in table with Provider, Description, Due Date, Status, Assigned To, Priority
- [ ] **Add Task** —
  - Select Provider
  - Enter Task Description (e.g., "Submit updated W-9", "Verify DEA license")
  - Set Due Date
  - Set Status (Open, In Progress, Complete)
  - Set Priority (Low, Medium, High)
  - Assign To (person name)
  - Save
- [ ] **Edit Task** — Modify task, changes persist
- [ ] **Complete Task** — Mark task complete, status updates
- [ ] **Delete Task** — Remove task, verify deletion
- [ ] **Overdue Tasks** — Tasks past due date should be highlighted/sorted to top
- [ ] **Priority Sorting** — High priority tasks should appear prominently
- [ ] **Assignment Tracking** — Can see who task is assigned to

**Report Issues:** Overdue highlighting, priority sorting, or task management issues

---

### Module 10: Provider Profiles
**Purpose:** Detailed view of individual provider information

**Test Cases:**
- [ ] **Load Page** — Page loads
- [ ] **Search Provider** — Enter provider name/ID in search box
- [ ] **View Full Profile** —
  - Provider details display (Name, Specialty, Contact Info)
  - Associated licenses display
  - Insurance enrollments display
  - Credentialing history displays
  - Recredentialing status displays
- [ ] **Profile Completeness** — All relevant provider data consolidates on one page
- [ ] **Edit from Profile** — Can edit provider info directly from profile (if feature enabled)
- [ ] **Related Records** — Licenses, credentialing, etc. properly linked to provider

**Report Issues:** Missing data, broken links, or incomplete profile views

---

### Module 11: Reports
**Purpose:** Generate summary reports and analytics

**Test Cases:**
- [ ] **Load Page** — Page loads, report options display
- [ ] **Provider Summary Report** — 
  - Generate report showing all providers, specialties, license status
  - Data accurate and complete
  - Can filter by specialty or state (optional)
- [ ] **Credentialing Status Report** — 
  - Shows all providers, enrollment status by payer
  - Pending, approved, denied counts
- [ ] **License Renewal Report** — 
  - Shows licenses by expiration date
  - Highlight expired or expiring soon (30/60/90 days)
- [ ] **Activity Report** — 
  - Summarize activities by date range
  - Can filter by provider or activity type
- [ ] **Export Capability** — Can export reports to CSV or PDF (if available)
- [ ] **Accuracy** — Verify report numbers match data in actual modules

**Report Issues:** Missing reports, inaccurate data, or export issues

---

### Module 12: Action Required (Dashboard)
**Purpose:** Alert dashboard for items requiring immediate attention

**Test Cases:**
- [ ] **Load Page** — Page loads, displays alert items
- [ ] **Overdue Licenses** — Shows licenses that have expired or are expiring soon
- [ ] **Pending Credentialing** — Shows credentialing applications pending decision
- [ ] **Overdue Tasks** — Shows tasks past due date
- [ ] **Overdue Recredentialing** — Shows cycles past end date
- [ ] **Alert Severity** — Critical items (expired licenses) should be most prominent
- [ ] **Click to Action** — Can click on alert and jump to relevant module to fix
- [ ] **Count Accuracy** — Alert counts match actual data in modules
- [ ] **Auto-refresh** — When you fix an issue in another module, does alert clear?

**Report Issues:** Missing alerts, inaccurate counts, or stale data

---

## Cross-Module Testing

**Workflow Tests:** Test complete end-to-end workflows

### Workflow 1: Add New Provider & Enroll with Payer
1. Go to **Providers** module
2. Add new provider (Name, Specialty, License #, etc.)
3. Go to **Licenses** module
4. Add license for new provider
5. Go to **Insurance Credentialing** module
6. Add credentialing record linking provider to payer
7. Go to **Credentialing Activity Log** — verify new activity logged
8. Go to **Action Required** — verify no new alerts (or expected alerts)

**Verify:** Data flows correctly between modules, activity is logged, no data loss

### Workflow 2: Track License Renewal Cycle
1. Go to **Licenses** module
2. Add license with expiration date 30 days from now
3. Go to **Follow-up Tasks** module
4. Add task "Renew license" with due date 60 days from now
5. Go to **Action Required** — license should appear as "expiring soon"
6. Go back to **Licenses**, update status to "Pending Renewal"
7. Verify task and alert update accordingly

**Verify:** Expiration tracking works, alerts trigger correctly, status flows

### Workflow 3: Provider Credentialing Pipeline
1. Go to **Payer Directory** — verify payers loaded
2. Go to **Insurance Credentialing** — add credentialing for provider + payer combo
3. Set status to "Pending"
4. Go to **Follow-up Tasks** — add task to "Follow up on credentialing application"
5. Go to **Action Required** — should show pending credentialing
6. Go back to **Insurance Credentialing** — mark status as "Approved"
7. Verify **Action Required** no longer shows this credentialing as alert

**Verify:** Status changes propagate, alerts clear correctly

---

## Data Integrity Testing

**Test These Scenarios:**
- [ ] **No Orphaned Data** — If you delete a provider, are all their records (licenses, credentialing) handled correctly?
- [ ] **Duplicate Prevention** — Can you add duplicate providers/payers? Should prevent or warn
- [ ] **Required Fields** — Try submitting forms with blank required fields, should error
- [ ] **Data Type Validation** — Try entering text in a date field, should error
- [ ] **Phone Format** — Phone numbers should format consistently
- [ ] **Email Format** — Invalid emails should be caught
- [ ] **Data Persistence** — Refresh page, data should still be there (no loss on reload)

---

## Performance & Usability Testing

- [ ] **Page Load Time** — Each page loads in under 3 seconds
- [ ] **Responsiveness** — App is usable on desktop browser
- [ ] **Navigation Clarity** — Sidebar buttons clearly indicate current page
- [ ] **Form Usability** — Forms are intuitive, labels are clear
- [ ] **Error Messages** — When errors occur, messages are clear and actionable
- [ ] **Search Performance** — Searching provider list is fast even with many records
- [ ] **Stability** — No crashes when adding/editing/deleting data

---

## Issue Reporting Template

When you encounter an issue, report it with this format:

**Module:** [Module Name]  
**Severity:** [Critical / High / Medium / Low]  
**Issue Description:** [What happened]  
**Steps to Reproduce:** 
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior:** [What should happen]  
**Actual Behavior:** [What actually happened]  
**Screenshots:** [Attach if relevant]  

**Example:**
```
Module: Insurance Credentialing
Severity: High
Issue: Provider dropdown shows numeric IDs instead of names
Steps to Reproduce:
1. Go to Insurance Credentialing
2. Click "Provider" dropdown
3. See IDs like "1 - John Smith" instead of just "John Smith"
Expected: Provider names only
Actual: Provider names with IDs
```

---

## Success Criteria

Testing is considered successful when:
- ✅ All 11 modules load without errors
- ✅ Data can be added, edited, and deleted in each module
- ✅ Data persists after page reload
- ✅ Navigation works correctly
- ✅ No crashes or unexpected behaviors
- ✅ All cross-module workflows complete successfully
- ✅ No critical data integrity issues
- ✅ UI is responsive and professional

---

## Questions for Tester

After completing testing, please answer:
1. Which module felt most intuitive? Which least?
2. What features are missing that would be helpful?
3. Any workflows that felt awkward or confusing?
4. Would you actually use this for your work?
5. What's the top priority fix if you could change one thing?

---

**Testing Start Date:** ___________  
**Testing End Date:** ___________  
**Tester Name:** ___________  
**Total Issues Found:** ___________  
  - Critical: _____
  - High: _____
  - Medium: _____
  - Low: _____
