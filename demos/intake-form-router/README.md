# Intake Form Router

Processes form submissions and routes them to the right team or system based on configurable rules. Eliminates ongoing manual triage.

## What It Does

Reads form submissions (CSV or JSON), applies routing rules (by type, region, keyword, or value), and outputs separate files per routing destination.

## Usage

```
python intake_form_router.py --input data/submissions.csv --rules config/routing_rules.yaml --output output/
```

## What Can Go Wrong

- Routing rules must be defined in the config file before running
- Submissions that match no rule go to an unmatched/ folder for manual review
- Test routing rules with sample data before deploying on live submissions

## Part of

[Fiore3 Automation Demos](https://github.com/aley-fiore3/fiore3-automation-demos)
