# Case Study: Event Platform Migration

## The Problem

A national academic competition used Award Force for judging and Cvent for registration. After the judging season, the organizer needed to:
- Port 250 contacts (judges, entrants, advisors) from Award Force into Cvent
- Ensure every judge in Award Force was registered in Cvent
- Reconcile entrant data across both platforms
- Clean up email mismatches, duplicate contacts, and role inconsistencies

**Time estimate (manual):** 8-12 hours of spreadsheet work, with high error risk.

## The Solution

Built an automated pipeline:

1. **Export** — Pulled CSV exports from both Award Force and Cvent
2. **Clean** — Normalized emails, split names, standardized organizations
3. **Match** — Cross-referenced both lists on email (primary) and name+org (fallback)
4. **Flag** — Identified 8 judges in Cvent but not Award Force, 3 email mismatches, and 12 registrants in wrong reg types
5. **Output** — Generated a clean import file for Cvent and a "needs review" list for manual spot-checks

## Results

| Metric | Before | After |
|--------|--------|-------|
| Time to reconcile | 8-12 hours | 15 minutes |
| Data errors caught | Unknown (manual review) | 23 specific issues flagged |
| Records processed | 250 | 250 |
| Import format | Manual reformatting | Auto-formatted for Cvent |

## Tools Used

- Python (pandas)
- Email List Cleaner script (in this repo)
- Award Force CSV export
- Cvent CSV export

## Lessons Learned

- Always export from Award Force before the season closes — some data becomes inaccessible
- Match on email first, but always have a name+org fallback for cases where someone used different emails
- Run the reconciliation weekly during active periods, not just once at the end
- The "needs review" output is as valuable as the clean output — it catches the edge cases automation can't resolve
