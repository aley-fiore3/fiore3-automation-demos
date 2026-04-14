# Automation ROI Calculator

Use this to estimate whether automating a process is worth the investment.

## The Math

```
Hours spent per cycle:        ___
Cycles per year:              ___
Hourly cost of person doing it: ___
Error rate (% of time it needs rework): ___

ANNUAL COST OF MANUAL PROCESS:
= (Hours × Cycles × Hourly Cost) + (Hours × Cycles × Hourly Cost × Error Rate × 0.5)
= $___

AUTOMATION BUILD COST:
= Hours to build × Builder hourly rate
= $___

ANNUAL COST OF AUTOMATED PROCESS:
= Maintenance hours per year × Hourly cost
= $___

PAYBACK PERIOD:
= Build Cost ÷ (Annual Manual Cost - Annual Automated Cost)
= ___ months
```

## Quick Decision Framework

| Annual Manual Cost | Build Cost | Payback | Decision |
|-------------------|------------|---------|----------|
| > $5,000 | < $2,000 | < 6 months | Automate now |
| > $2,000 | < $3,000 | 6-12 months | Automate if recurring |
| < $1,000 | Any | > 12 months | Probably not worth it |

## Beyond the Math

Some automations are worth it even when the ROI doesn't look great:
- **Error reduction** — if mistakes have downstream consequences (wrong data in a grant report, missed deadline)
- **Sanity preservation** — if the manual task is soul-crushing and causes turnover
- **Speed** — if doing it faster creates opportunities (first to apply, faster turnaround for clients)
- **Scalability** — if you're about to 3x your volume and the manual process won't survive

## Example

**Process:** Cleaning and migrating contact lists between event platforms

| | Manual | Automated |
|-|--------|-----------|
| Time per migration | 6 hours | 15 minutes |
| Migrations per year | 4 | 4 |
| Hourly cost | $50 | $50 |
| Error rate | 15% | 2% |
| Annual cost | $1,380 | $50 + maintenance |
| Build cost | — | $800 (one-time) |
| **Payback** | — | **7 months** |
