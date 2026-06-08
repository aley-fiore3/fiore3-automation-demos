# Case Study: Intake Form Routing Automation

**Industry:** Consulting / Professional Services
**Problem type:** Manual email triage, inconsistent response times, staff bottleneck
**Time to build:** ~4 hours
**Outcome:** Eliminated manual sorting; every submission routed to the right person within 60 seconds of receipt

---

## Background

A consulting firm I work with uses a website intake form as the front door for new client inquiries. The form collects basic information: name, company, type of engagement, budget range, timeline, and how they found the firm.

The problem was what happened after submission. Every form response landed in a single shared inbox. Someone — usually whoever happened to check email first — would read it, decide who it was for, forward it, and hope the right person picked it up. There was no consistency. High-value leads sometimes sat for 24-48 hours before a response. Lower-stakes inquiries occasionally went to senior consultants who didn't have bandwidth for them. And nobody had visibility into how many inquiries were coming in, what types, or what the conversion rate looked like.

The operations person who managed the inbox described her job as "reading emails and guessing."

---

## What I Found When I Embedded

The intake form had 7 fields, but the routing decision almost always came down to two: engagement type and budget range. Most routing rules could be expressed as a simple decision tree:

- Strategic advisory at $10k+ → senior partner
- Project execution under $10k → associate team
- "Just exploring" or no budget listed → nurture sequence, not a live person
- Anything mentioning a specific technology (Cvent, AI, automation) → me

The senior partner had never written this down. It lived in her head. When she was out, the routing fell apart completely.

The second thing I noticed: the form responses were going into a Google Sheet automatically via Zapier. The data was already there. Nobody was using it.

---

## What I Built

A Python script that runs on a schedule (every 15 minutes via cron), reads new rows from the Google Sheet, applies a routing ruleset from a config file, and sends a pre-formatted notification email to the right recipient — with the full submission details, a suggested response time, and a one-line context note ("This looks like a Cvent migration project — see similar work at [link]").

The config file is a simple YAML:

```yaml
routes:
  - match:
      engagement_type: "Strategic Advisory"
      budget_min: 10000
    send_to: partner@firm.com
    priority: high
    response_target: "same day"

  - match:
      engagement_type: ["Project Execution", "Implementation"]
      budget_max: 9999
    send_to: associates@firm.com
    priority: normal
    response_target: "48 hours"

  - match:
      budget: null
      timeline: "Just exploring"
    send_to: nurture@firm.com
    priority: low
    response_target: "automated"
```

The config was designed so the senior partner could open it, read it, and change a routing rule without calling me. That was an explicit requirement I built to — not an afterthought.

I also added a weekly summary email: total submissions, breakdown by engagement type and budget band, and a count of how many hit each routing bucket. This turned the shared inbox problem into a visibility asset.

---

## The Edge Cases That Mattered

About 15% of submissions didn't cleanly match any rule — missing fields, unexpected values, combinations the ruleset didn't cover. I deliberately routed these to a "needs human review" bucket rather than trying to infer intent. An unrouted lead that gets a human is better than a mis-routed lead that gets an automated non-answer.

This was a judgment call worth documenting: automation should handle the clear cases and surface the ambiguous ones, not try to resolve everything.

---

## Results

| Metric | Before | After |
|---|---|---|
| Average time to first routing | 2-6 hours | < 60 seconds |
| Routing errors per month | ~4 (estimated) | 0 confirmed in first 90 days |
| Ops coordinator time on triage | ~30 min/day | < 5 min/week (reviewing the summary) |
| Visibility into lead volume | None | Weekly digest with breakdown |
| Senior partner out-of-office failures | Frequent | Eliminated |

---

## What I Left Behind

A YAML config file with comments explaining each field. A one-page runbook. A test mode flag (`--dry-run`) that prints what the script *would* route without sending any emails — useful for testing rule changes before deploying them. And a note that says: *"To add a new route, copy an existing block and change the match conditions. The order matters — first match wins."*

The first three months of routing logs are also saved to a CSV so they could audit decisions and tune the ruleset over time.

---

*Part of the [Fiore3 Automation Demos](https://github.com/aley-fiore3/fiore3-automation-demos) repository.*
*Built by [Alessandra Desiderio](https://alessandradesiderio.com)*
