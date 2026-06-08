# Deployment Guide

This document explains how to take a demo from this repo and deploy it in a real client environment.

---

## Philosophy

Every automation here was built to be handed off, not maintained forever. The goal is:

1. You run it successfully on your own within 30 minutes
2. You understand what it does well enough to modify it
3. You don't need me to fix it when something changes

---

## Prerequisites

Before deploying any demo:

- Python 3.8+ installed
- pip installed
- Access to the relevant platform (Cvent, Award Force, Google Workspace, etc.)
- A CSV export from your source system

```bash
# Verify your setup
python --version   # Should be 3.8+
pip --version
```

---

## Step-by-Step: Email List Cleaner

**Use case:** You have a contact export with duplicate emails, inconsistent org names, and formatting issues. You need a clean version to import into Cvent or another platform.

```bash
cd demos/email-list-cleaner
pip install -r requirements.txt
python clean_list.py --input your_export.csv --output cleaned.csv
```

**What to check in the output:**
- `cleaned.csv` should have no duplicate emails
- The `org_name` column should be normalized
- The `email_valid` column flags any bad addresses — review these manually before import

---

## Step-by-Step: Event Data Reconciler

**Use case:** You've exported from two platforms (e.g. Award Force and Cvent) and need to find contacts that are in one but not the other.

```bash
cd demos/event-data-reconciler
pip install -r requirements.txt
python reconcile.py --source1 platform_a.csv --source2 platform_b.csv --match-on email
```

**Output files:**
- `matches.csv` — contacts that exist in both platforms
- `only_in_source1.csv` — contacts missing from platform B
- `only_in_source2.csv` — contacts missing from platform A

---

## Step-by-Step: Document Generator

**Use case:** You need to generate 50+ personalized letters, certificates, or reports from a spreadsheet.

```bash
cd demos/document-generator
pip install -r requirements.txt
python generate.py --data your_data.csv --template your_template.docx --output ./output/
```

**Customizing the template:**
- Open `template.docx` and use `{{field_name}}` placeholders
- Column headers in your CSV become the available field names

---

## Step-by-Step: Intake Form Router

**Use case:** You're receiving form submissions and need to route them to different inboxes, spreadsheets, or systems based on rules.

```bash
cd demos/intake-form-router
pip install -r requirements.txt
# Edit config.yaml with your routing rules first
python router.py --config config.yaml --input submissions.csv
```

---

## Common Issues

| Problem | Likely Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: pandas` | pandas not installed | Run `pip install pandas` |
| Empty output file | Input CSV columns don't match expected names | Check the `--help` flag and compare column names |
| Encoding error on CSV open | Non-UTF-8 file from Windows | Add `--encoding latin-1` flag |
| Script runs but no changes | Dedup threshold too high | Adjust `--threshold` or review the config |

---

## Getting Help

If something breaks after I've handed this off:

1. Check the `examples/` folder — there are sample inputs and expected outputs
2. Run the script with `--dry-run` to see what it *would* do without writing files
3. Open an issue on this repo with your input file structure (no real data)
4. Or reach out at [alessandradesiderio.com](https://alessandradesiderio.com)

---

*Built to be owned, not rented.*
