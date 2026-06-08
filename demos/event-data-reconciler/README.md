# Event Data Reconciler

Finds mismatches between registration, judging, and email platforms. Saves 3-5 hours per event cycle.

## What It Does

Compares exports from two platforms (e.g. Cvent and Award Force) and surfaces discrepancies: missing registrants, duplicate entries, field mismatches, and status conflicts.

## Usage

```
python event_data_reconciler.py --source1 data/cvent_export.csv --source2 data/award_force_export.csv --match-on email --output data/reconciliation_report.csv
```

## What Can Go Wrong

- Both files must have a common matching field (email is most reliable)
- Date format differences between platforms can cause false mismatches
- Test with the sample data in examples/ before running on real exports

## Part of

[Fiore3 Automation Demos](https://github.com/aley-fiore3/fiore3-automation-demos)
