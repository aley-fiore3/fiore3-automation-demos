# Document Generator

Auto-generates personalized letters, certificates, or reports from a spreadsheet. Saves 1-2 hours per batch.

## What It Does

Given a CSV of recipients and a template document, this tool generates one personalized output file per row.

## Usage

```
python document_generator.py --template template.docx --data data/recipients.csv --output output/
```

## What Can Go Wrong

- Template placeholders must match column headers exactly (case-sensitive)
- Empty cells in the CSV will produce blank fields in the output
- Output folder must exist before running

## Part of

[Fiore3 Automation Demos](https://github.com/aley-fiore3/fiore3-automation-demos)
