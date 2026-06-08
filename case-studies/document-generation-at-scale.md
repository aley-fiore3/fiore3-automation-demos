# Case Study: Document Generation at Scale

**Industry:** Events / Awards Programs
**Problem type:** Manual document creation, inconsistent formatting, volunteer burnout
**Time to build:** ~3 hours
**Outcome:** 340 personalized award letters generated in 4 minutes; zero formatting errors; staff time freed from 2-day task to 10-minute review

---

## Background

A national awards program I support runs an annual competition with around 300-400 entrants. At the end of the judging cycle, every finalist receives a personalized award letter — formally addressed, with their category, award tier, event details, and a few sentences customized to their submission.

For years, the staff coordinator created these manually. She had a Word document template and a spreadsheet. She would open the template, copy in the name, adjust the category, update the award tier, change the event date, and save a new file. Then do it again. 340 times.

It took two full working days. Every year she asked if there was a better way. Every year it got deprioritized because the deadline was always approaching and there wasn't time to fix the process while also running it.

I came in after the third year of this.

---

## What I Found When I Embedded

The spreadsheet she used was clean. It had been refined over three years of doing this manually — she knew exactly what data she needed because she'd been copying it by hand long enough to feel every inconsistency.

The template was also clean. It had a consistent structure, predictable field placements, and a tone that had been approved by the program director. There was nothing wrong with the inputs. The problem was purely mechanical: a human was acting as the merge engine.

There was one complication. About 40 of the letters had a custom paragraph in addition to the standard text — for "Distinguished Achievement" tier winners, the letter included a brief mention of what made their specific submission noteworthy. These notes were in a column called "Custom Note" that was either populated or blank.

This was the interesting design question: how do you handle optional content in a template without making the template logic complicated?

---

## What I Built

A Python script using `python-docx` to read the Word template and perform field substitutions from the spreadsheet. The template uses `{{field_name}}` placeholders throughout — same pattern as most mail merge tools, familiar to anyone who's used them.

For the custom paragraph problem, I added a conditional block:

```python
# If custom_note exists, insert it after the standard award paragraph.
# If not, skip the block entirely — no blank lines, no placeholder text.
if row['custom_note']:
    insert_paragraph_after(award_para, row['custom_note'])
```

The output is one `.docx` file per recipient, named with their ID and last name for easy sorting. A separate manifest CSV logs every generated file, the field values used, and a checksum — so if a letter ever needs to be re-generated, you know exactly what values were used the first time.

---

## The Part That Almost Went Wrong

After the first test run, the coordinator noticed that three letters had the wrong event city. The city field in the spreadsheet had a formula referencing another tab — and when I read the sheet via the Google Sheets API, formula-resolved values weren't coming through correctly for those three rows. The raw value was returning the formula string instead of the result.

This is a known edge case in the Sheets API that's easy to miss. The fix is a single parameter change: `valueRenderOption=FORMATTED_VALUE` instead of the default. Five minutes to fix once you know what's happening, frustrating to debug if you don't.

I added a validation step to the script that checks every field against an expected type before generating any documents — if a field looks like a formula string (starts with `=`), it flags the row and stops before producing a bad output. It's a guard rail that costs almost nothing to add and prevents exactly this class of error.

---

## Results

| Metric | Before | After |
|---|---|---|
| Time to generate all letters | ~2 full working days | 4 minutes |
| Formatting errors | ~5-8 per year (caught in proofing) | 0 in first run |
| Staff required | 1 coordinator, full attention | 1 coordinator, 10-min review of manifest |
| Custom paragraphs handled | Manual, high error risk | Automatic, conditional on data |
| Re-run capability | Start over from scratch | Re-generate any subset in seconds |

---

## What Made This Worth Doing

The two-day task was the visible cost. The invisible cost was what the coordinator *didn't* do during those two days. She was the same person who managed judge communications, coordinated the awards ceremony, and handled finalist notifications. Every year, those things slipped slightly because she was occupied with mail merge.

Fixing the merge fixed the downstream calendar. That's the kind of second-order impact that's worth surfacing when you're scoping automation — the time saved on the direct task is often less valuable than the time it returns to adjacent work.

---

*Part of the [Fiore3 Automation Demos](https://github.com/aley-fiore3/fiore3-automation-demos) repository.*
*Built by [Alessandra Desiderio](https://alessandradesiderio.com)*
