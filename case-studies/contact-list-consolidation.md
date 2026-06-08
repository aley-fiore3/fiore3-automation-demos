# Case Study: Contact List Consolidation Across Three Platforms

**Industry:** Nonprofit / Advocacy
**Problem type:** Fragmented contact data, duplicate records, no single source of truth
**Time to build:** ~8 hours across three sessions
**Outcome:** 4,200 records across three platforms collapsed into one clean master list; 840 duplicates identified and resolved; email deliverability improved

---

## Background

An advocacy nonprofit I work with had accumulated contacts across three systems over five years, with no intentional strategy for how they related to each other:

- **Salesforce** — their official CRM, used by the development team for donor tracking and major gift cultivation
- **Mailchimp** — used by the communications team for email campaigns; had been growing independently for three years
- **A Google Sheet** — maintained by the program team, tracking direct service contacts, partner organizations, and "warm leads" that hadn't made it into Salesforce yet

Each system had grown in isolation. The same person might exist in all three, with different email addresses, different name formats, different organization affiliations, and no linking ID across them.

The consequences were real: donors received duplicate solicitations, partners got left off event invitations because they were only in the Sheet, and the development team couldn't trust their Salesforce reports because they knew the data was incomplete.

---

## What I Found When I Embedded

The first thing I asked was: which system is supposed to be the master? Nobody had a clear answer. Each team had a legitimate claim — development owned the donor relationships, comms owned the email list, program owned the partnership contacts. The consolidation problem was downstream of an organizational question nobody had resolved.

I didn't try to resolve it for them. Instead, I reframed the project: rather than picking one system as master and migrating everything into it, I built a **read-only reconciliation layer** — a script that exports from all three, identifies overlapping records, and produces a match report that the teams could review together and use to make their own decisions about what to merge.

This was a deliberate choice to scope the automation appropriately. Merging 4,000 records across three systems without human sign-off is exactly the kind of action that creates more problems than it solves.

---

## What I Built

**Phase 1: Export and normalize**

Each platform exports in a different format. Salesforce gives you a structured CSV with standard field names. Mailchimp exports with its own column schema. The Google Sheet was freeform — columns had been renamed over time, some fields were missing, and one column had been used for two different purposes at different points.

I wrote a normalization layer for each source that maps their native columns to a shared schema: `email`, `first_name`, `last_name`, `org`, `source`, `last_activity_date`.

**Phase 2: Match**

Matching logic ran in priority order:

1. Exact email match → definite duplicate
2. Same first+last name + same org → probable duplicate, flag for review
3. Same first+last name, different org → possible duplicate (name change, job change), flag for human review
4. Email fuzzy match (within edit distance 1) → possible typo, flag for review

Each matched pair got a confidence score (High / Medium / Review). The output was a CSV with one row per matched pair, their source systems, and the confidence level.

**Phase 3: Summary report**

A separate output file summarized the findings:
- Total records per source
- Exact matches (safe to merge)
- Probable matches (recommend review)
- Unique-to-one-system records (possibly missing from others)

---

## The Org Structure Problem That Shaped Everything

About 200 records had organization names that were clearly the same entity but formatted differently: "Notre Dame", "University of Notre Dame", "Univ. of Notre Dame", "ND". Standard dedup on org name alone would have missed all of these.

I added an org normalization step using a manually curated mapping file — a CSV with raw names in column A and canonical names in column B. The teams could add to it over time. For the initial run, I populated it by doing a frequency sort on org names across all three sources, then manually reviewing the top 100 (which covered about 60% of all records).

This is slow work. There's no shortcut that's better than a human reading through a sorted list. But it's also work that only needs to happen once well — after that, the canonical list becomes an organizational asset.

---

## Results

| Metric | Before | After |
|---|---|---|
| Total unique records (estimated) | Unknown | 3,360 (down from 4,200 raw) |
| Definite duplicates identified | 0 (unknown) | 420 (exact email match) |
| Probable duplicates flagged | 0 | 420 (for human review) |
| Records only in one system | Unknown | 1,100 identified for potential cross-enrollment |
| Email deliverability | Declining (duplicate sends) | Improved after list cleaning |
| Development team Salesforce confidence | Low | Higher — gaps now visible and actionable |

---

## What I Did Not Do

I didn't merge anything. That was intentional and important.

The reconciliation report went to a joint meeting of all three teams. They used it to make decisions about which records to merge, which to keep separate, and how to handle the 420 "probable duplicate" cases. Some of those turned out to be the same person at different jobs. Some were different people with similar names. A script couldn't tell the difference — the teams could.

The automation did the hard mechanical work of surfacing the overlaps. The humans made the calls. That's the right division of labor for a project like this.

---

## What I Left Behind

Three export/normalize scripts — one per platform — each with a config file for column mapping. The org normalization CSV with ~150 canonical entries. The matching script with adjustable confidence thresholds. A README explaining how to re-run the reconciliation on a quarterly schedule. And a one-page document explaining what each output file means and how to read the confidence levels.

I also wrote up a one-paragraph recommendation: they should pick one system as master within the next 12 months, or the consolidation problem will return. That decision was outside my scope to make for them, but it was inside my scope to name clearly.

---

*Part of the [Fiore3 Automation Demos](https://github.com/aley-fiore3/fiore3-automation-demos) repository.*
*Built by [Alessandra Desiderio](https://alessandradesiderio.com)*
