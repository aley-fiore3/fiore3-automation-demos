# Case Study: Grant Tracking Automation for a CDFI

**Industry:** Nonprofit / Community Development Finance
**Problem type:** Manual deadline tracking, missed alerts, staff dependency
**Time to build:** ~6 hours across two sessions
**Outcome:** Eliminated missed deadlines; staff went from checking a spreadsheet daily to receiving a weekly digest

---

## Background

A community development financial institution (CDFI) I work with manages a rolling portfolio of grant applications, reporting deadlines, and funder relationships. At any given time, they're tracking 15-30 active grants, each with multiple milestone dates: letter of intent, full application, reporting periods, and closeout.

The system they were using: a shared Google Sheet, manually updated by whoever remembered.

The problems were predictable. Deadlines slipped through when the person who "owned" the spreadsheet was out. There was no alert when a deadline was two weeks away. Nobody had a reliable answer to "what's due this month?" without opening the sheet and scanning every row.

When a funder relationship went cold because a required progress report was late, they asked me to fix it.

---

## What I Found When I Embedded

The first thing I did was sit with their operations coordinator for 45 minutes and watch how she actually used the spreadsheet. Not ask — watch. What I noticed:

The sheet had 11 columns but she only looked at 4 of them. The "Status" column was two months stale because updating it felt like overhead with no payoff. The "Notes" column had become a graveyard of context — useful information buried where nobody would find it at the right moment. And the real tracking system was her personal calendar, which meant all institutional knowledge about grant deadlines lived in one person's Google Calendar.

That last point was the real problem. The spreadsheet wasn't the system. It was the backup for the system, and the system was a single point of failure.

---

## What I Built

I didn't replace the spreadsheet. I wired an alert layer on top of it.

The automation runs weekly and does three things:

**1. Deadline digest email.** Every Monday morning, the operations coordinator receives an email listing everything due in the next 30 days, sorted by urgency. No login required, no spreadsheet to open. The email is generated from the same Google Sheet they already maintain, so there's no parallel data entry.

**2. Two-week warning.** Any grant milestone that's exactly 14 days away gets a separate "action required" email to the relevant staff member. This catches things before they become urgent, not after.

**3. Overdue flag log.** A separate tab in the sheet auto-populates with any item whose deadline has passed and whose status column doesn't say "complete" or "submitted." This made the stale "Status" column suddenly worth maintaining, because there was now a consequence for leaving it blank.

The build was straightforward: a Python script that reads the sheet via Google Sheets API, filters and sorts by date, then sends HTML-formatted emails via SMTP. I wrote a config file for them to adjust the lead time thresholds and email recipients without touching the code.

---

## The Conversation That Almost Derailed It

Halfway through the build, their executive director asked if we could also automatically send reminder emails directly to program officers at the funding organizations — essentially having the automation email grantors on their behalf.

I said no.

Not because it was technically hard, but because it was the wrong thing to automate. Funder relationships are relationship capital. An automated email to a program officer at the wrong time, with the wrong tone, or about the wrong grant can do real damage. That risk belongs with a human, not a script.

This is a pattern I've encountered repeatedly: clients initially want to automate the high-stakes touchpoints because they're painful, but the pain is there for a reason. My job in those moments is to scope the automation to the low-stakes, high-volume work — and leave the judgment calls where they belong.

---

## Results

| Metric | Before | After |
|---|---|---|
| Missed deadlines (trailing 6 months) | 3 (one funder relationship affected) | 0 |
| Time spent on deadline tracking per week | ~45 minutes (ops coordinator) | ~5 minutes (review digest, respond if needed) |
| Staff single-point-of-failure risk | High (one person's calendar) | Low (automated, multiple recipients) |
| Spreadsheet data quality | Sporadic | Improved — status column now maintained |

---

## What I Left Behind

A working script with a config file. A one-page setup guide. A `README` explaining what each part does and how to change the lead-time thresholds. And a note in the config file that says: *"If you want to add a new recipient, add their email here. If you want to change the 14-day warning to 21 days, change this number. You do not need a developer to do either of these things."*

That last line matters. The goal of forward deployed work isn't to create a dependency. It's to raise the floor of what the organization can do on its own.

---

*Part of the [Fiore3 Automation Demos](https://github.com/aley-fiore3/fiore3-automation-demos) repository.*
*Built by [Alessandra Desiderio](https://alessandradesiderio.com)*
