# Email Deliverability Cheatsheet

Quick reference for keeping your emails out of spam folders.

## Subject Lines

- **Under 50 characters** — avoids truncation on mobile
- **No ALL CAPS** — triggers spam filters
- **Avoid:** "FREE", "Act Now", "Limited Time", "Click Here", "Congratulations"
- **Personalize:** Use first name merge tags when possible
- **Test:** Send yourself a test before blasting

## Sender Setup

- **Use a real name** as sender, not "noreply@"
- **Reply-to should be monitored** — replies that bounce hurt your reputation
- **Authenticate your domain:** SPF, DKIM, and DMARC records all set up
- **Warm up new domains** — start with small sends, increase gradually over 2-4 weeks

## List Hygiene

- **Remove bounces immediately** — hard bounces damage sender reputation
- **Clean your list quarterly** — run through an email validation tool
- **Sunset unengaged contacts** — no opens in 6+ months = remove or re-engage campaign
- **Never buy lists** — purchased lists have high bounce rates and spam complaints
- **Double opt-in** when possible — better quality, lower complaints

## Content

- **Text-to-image ratio:** at least 60% text, 40% images
- **Always include plain text version** alongside HTML
- **Alt text on every image** — some clients block images by default
- **One clear CTA** — don't compete with yourself
- **Unsubscribe link visible** — legally required (CAN-SPAM) and burying it increases spam reports

## Sending

- **Best times (B2B):** Tuesday-Thursday, 9-11am recipient's timezone
- **Best times (B2C):** Varies — test and measure your own audience
- **Avoid:** Monday mornings, Friday afternoons, holidays
- **Segment:** Smaller, targeted sends outperform mass blasts every time

## Metrics That Matter

| Metric | Good | Concerning | Action |
|--------|------|-----------|--------|
| Open rate | 20%+ | Below 15% | Fix subject lines, sender name, send time |
| Click rate | 2.5%+ | Below 1% | Fix CTA, content relevance, design |
| Bounce rate | Below 2% | Above 5% | Clean your list immediately |
| Unsubscribe rate | Below 0.5% | Above 1% | Frequency too high or content misaligned |
| Spam complaints | Below 0.1% | Above 0.3% | Stop sending until you fix the root cause |

## Emergency: Landed in Spam

1. Check if your domain is blacklisted: mxtoolbox.com/blacklists.aspx
2. Verify SPF/DKIM/DMARC: dmarcanalyzer.com
3. Reduce send volume immediately
4. Remove all unengaged contacts
5. Send only to your most engaged segment for 2-4 weeks
6. Gradually increase volume
