# Email List Cleaner

Deduplicates, validates, normalizes, and reformats contact lists for migration between platforms.

## Quick Start

```bash
pip install pandas
python email_list_cleaner.py contacts.csv --format cvent --output ready_for_cvent.csv
```

## What It Does

1. **Validates emails** — flags missing, malformed, typos (.cmo → .com), and disposable addresses
2. **Splits names** — "Dr. Maria Santos Jr." → First: Maria, Last: Santos
3. **Normalizes organizations** — "TAMU", "Texas A & M", "Texas A&M" → "Texas A&M University"
4. **Deduplicates** — matches on email, keeps the most complete record
5. **Reformats** — outputs in Cvent, Constant Contact, or Mailchimp import format

## Output

- `*_cleaned.csv` — ready to import
- `*_needs_review.csv` — flagged records that need a human look

## Custom Organization Mapping

Create a CSV with two columns (variant, standard) to map your org names:

```csv
TAMU,Texas A&M University
Texas A & M,Texas A&M University
CU Boulder,University of Colorado Boulder
```

Then: `python email_list_cleaner.py contacts.csv --org-map org_map.csv`
