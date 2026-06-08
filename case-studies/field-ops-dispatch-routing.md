<!--
Industry: Field Services / SMB
Problem type: Scheduling & dispatch automation
Time to build: ~6 hours
Outcome: Technician utilization up 31%; after-hours emergency calls down 60%
-->

# Field Ops Dispatch Routing

**Industry:** Field Services / Commercial HVAC  
**Problem type:** Manual scheduling, reactive dispatch  
**Time to build:** ~6 hours across two days  
**Outcome:** Technician utilization up 31%; after-hours emergency calls down 60%

---

## Background

A commercial HVAC company with seven technicians was scheduling jobs the way they'd done it for twelve years: the owner opened a whiteboard each morning, looked at the day's service requests in his email inbox, and assigned jobs by memory. He knew roughly where each tech lived, roughly which techs were better at commercial rooftop units vs. residential split systems, and roughly which clients needed to be handled carefully.

The system worked when he was the only one doing it. By the time I embedded with them, he was spending two hours every morning on dispatch and still missing things. A tech would drive forty minutes across town for a job that a tech already in that zip code could have handled. Jobs that came in after 10am got pushed to the next day because he didn't want to re-do the board. Three times in the past month, clients had called back angry because no one showed up — not because a tech forgot, but because the morning email had been miscategorized as a follow-up rather than a new request.

His office manager described the situation plainly: "He keeps the whole thing in his head, and we can't afford for that to break."

---

## What I Found When I Embedded

The first thing I did was sit with the owner for a full dispatch morning. I wasn't looking at his software — I was watching him.

What I noticed: he wasn't actually making dispatch decisions in real time. He was reconstructing state. Every morning, he had to re-derive which techs were available, where they were geographically, and what type of jobs were in queue — information that had been known yesterday but was nowhere written down in a recoverable format.

The whiteboard got erased at the end of each day. The inbox had no tagging system. There was a scheduling app (ServiceTitan lite) that the office manager used to confirm appointments, but the owner didn't trust it and had stopped updating it six months ago, so it had drifted out of sync with reality.

The real problem wasn't that he lacked software. It was that every day started from zero.

What he actually needed was two things: a persistent state of who was available and where, and a way to match incoming jobs to techs without doing it all in his head.

I deliberately did not propose replacing the whiteboard. He trusted the whiteboard. I proposed making it writable once and readable automatically.

---

## What I Built

Three components, all lightweight:

**1. Job intake normalization**

Incoming service requests arrived by email, phone (transcribed by the office manager into a shared Google Sheet), and a web form on the company site. None of these had consistent structure.

I wrote a Python script that pulled from the Google Sheet every 15 minutes and normalized each new row into a standard job object:

```python
def normalize_job(row):
    return {
        "job_id": row["Timestamp"].strftime("%Y%m%d-%H%M"),
        "client": row["Client Name"].strip(),
        "address": row["Service Address"].strip(),
        "zip": extract_zip(row["Service Address"]),
        "type": classify_job_type(row["Description"]),  # "commercial_rooftop", "residential_split", "maintenance", "emergency"
        "priority": "urgent" if any(kw in row["Description"].lower() for kw in ["no heat", "no cool", "down", "emergency", "urgent"]) else "standard",
        "requested_date": parse_date(row["Preferred Date"]),
        "created_at": row["Timestamp"]
    }
```

The `classify_job_type` function used a keyword mapping table rather than ML — fast to build, easy to audit, and the owner could edit it himself in a config file.

**2. Tech availability and skill state**

I created a simple daily check-in form (a Google Form that took 30 seconds to fill out) that techs completed each morning from their phones. Fields: available today (yes/no), starting location (zip code), any equipment limitations (free text).

This fed into a "tech state" sheet that persisted day over day. If a tech didn't fill out the form, the script carried forward yesterday's state and flagged the row yellow.

**3. Dispatch suggestion engine**

Each morning at 7:30am, the script generated a suggested dispatch schedule and wrote it to a new tab in the Google Sheet — one row per unscheduled job, with a suggested technician, estimated drive time (using the Google Maps Distance Matrix API), and a confidence flag.

```python
def score_tech_for_job(tech, job, tech_state):
    score = 0
    # Skill match
    if job["type"] in tech_state[tech]["skills"]:
        score += 10
    # Proximity (closer = higher score)
    drive_minutes = get_drive_time(tech_state[tech]["zip"], job["zip"])
    score += max(0, 30 - drive_minutes)  # max 30 points for 0-min drive
    # Availability
    if not tech_state[tech]["available"]:
        return -1  # exclude
    return score
```

The output wasn't a locked schedule — it was a suggested starting point. The owner still opened the sheet each morning, reviewed the recommendations, and reassigned anything he wanted to change. He could override any suggestion in two clicks. The script never sent anything directly to techs; the owner still did that.

This mattered a lot to him. He wasn't ready to hand dispatch to a computer. What I built was something that got him from zero to 80% done before he sat down.

---

## The Conversation About Priorities

About two weeks in, the owner asked if I could add a "priority override" that would automatically move emergency jobs to the top of the queue and alert the nearest tech by text.

I said I could build that, and asked a few questions first. Who defines what's an emergency? What if the classification is wrong and a "no heat" call turns out to be a thermostat setting? What if the auto-assigned tech is the one tech who has a difficult history with that particular client?

He thought about it and said: "You're right. Let's keep that one manual."

That conversation is the one I think about when someone asks me what it means to be a forward deployed engineer. The technical problem was easy. The judgment call — which parts of the workflow should have a human in the loop, and why — is the actual work.

We added a visual indicator instead: emergency jobs got a red background in the sheet. The owner's eyes went there first. That was enough.

---

## Results

| Metric | Before | After |
|---|---|---|
| Time spent on morning dispatch | ~2 hours | ~25 minutes |
| Technician utilization (billable hrs / available hrs) | 61% | 80% |
| Jobs pushed to next day due to late intake | ~4/week | ~0.5/week |
| After-hours emergency calls | ~5/month | ~2/month |
| Missed appointments (no-show) | 3 in 30 days | 0 in 90 days |
| Owner "starting from zero" each morning | Every day | Never |

The utilization number is the one the owner mentions when he talks about it. A 19-point improvement in technician utilization is revenue. Each tech bills roughly $85/hr and works about 200 hrs/month — closing that gap from 61% to 80% was worth approximately $32K/month in recaptured billable time across the team.

---

## What I Left Behind

- `dispatch_engine.py` — the full normalization and scoring script, with config at the top for easy editing
- `job_types.yaml` — keyword classification table, editable by the office manager without touching code
- `tech_skills.yaml` — per-technician skill and preference configuration
- A one-page operations guide covering: how to add a new technician, how to update job type keywords, what to do if the Google Maps API quota hits its limit
- The daily check-in form and its associated Sheet, with instructions for the office manager on resetting state at the start of each month

The owner runs it himself now. The office manager trained a part-time admin on it in under an hour.
