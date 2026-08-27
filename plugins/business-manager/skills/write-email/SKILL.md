---
name: write-email
description: Writes a single email for a specific purpose — outreach, nurture, launch, follow-up, or one step of a campaign. Use when a single email needs to be drafted, not a full sequence. Triggers on requests like "write an email to...", "draft a follow-up email", "write the day 3 email for...".
---

# Write Email

Produces one finished, on-brand email for a given purpose and audience.

## 1. Gate-check config

Read `<Drive business root>/_business-manager/config.json`.

- If `senderName` or `businessName` is missing, stop and tell the user exactly which field is missing and that it's set via the `setup` command. Do not draft a placeholder email.

## 2. Gather inputs

From the request (ask only if genuinely missing):

- **Purpose/angle** — e.g. cold outreach, re-engagement, launch announcement, day-N of a campaign
- **Audience** — who's receiving it
- **Key message / CTA** — the one thing this email must accomplish
- **Tone override** (optional) — defaults to the brand voice below

## 3. Load context

- Read `<Drive business root>/_business-manager/brand-guide.md` if it exists, for voice/tone. If it doesn't exist yet, proceed with a clear, direct professional tone and note in your output that no brand guide is on file.
- Read `<Drive business root>/_business-manager/memory/emails.md` if it exists — skim for prior angles/subject lines on the same purpose or campaign so this email doesn't repeat one already sent.

## 4. Write the email

- One subject line (plus 1-2 alternates if useful)
- Body matching brand voice, sized to purpose (outreach = short; nurture/launch = can be longer)
- Exactly one clear call to action
- Sender sign-off using `senderName` / `businessName` from config

## 5. Save and log

- Save the email to `<Drive business root>/_business-manager/outputs/emails/<short-slug>.md`
- Append one line to `<Drive business root>/_business-manager/memory/emails.md`: date, purpose, audience, subject line, output path — so future invocations (any session, any surface) know this angle has been used
- Create `memory/emails.md` with a one-line header if it doesn't exist yet

## 6. Return

Show the finished email in the chat, plus the Drive path it was saved to.
