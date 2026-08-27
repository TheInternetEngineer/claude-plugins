---
name: write-email
description: Writes a single email for a specific purpose — outreach, nurture, launch, follow-up, or one step of a campaign. Use when a single email needs to be drafted, not a full sequence. Triggers on requests like "write an email to...", "draft a follow-up email", "write the day 3 email for...".
---

# Write Email

Produces one finished, on-brand email for a given purpose and audience.

## 1. Gate-check config

Resolve `<businessMemoryPath>`: check the `BUSINESS_MEMORY_PATH` environment variable first, then `~/.business-memory/root.json`. Read `<businessMemoryPath>/business-manager.config.json`.

- If `senderName` or `businessName` is missing, stop and tell the user exactly which field is missing and that it's set via `bm-setup`. Do not draft a placeholder email.
- If `<businessMemoryPath>` doesn't resolve at all, tell the user to run `bm-setup` first.

## 2. Gather inputs

From the request (ask only if genuinely missing):

- **Purpose/angle** — e.g. cold outreach, re-engagement, launch announcement, day-N of a campaign
- **Audience** — who's receiving it (a named client/segment, if any)
- **Key message / CTA** — the one thing this email must accomplish
- **Tone override** (optional) — defaults to the brand voice below

## 3. Check shared business-memory before drafting

Search `<businessMemoryPath>/log.jsonl` for anything relevant before writing a word:

```bash
python3 <businessMemoryPath>/scripts/log_tool.py --file <businessMemoryPath>/log.jsonl search --query "<audience/client name or topic>"
```

Look especially for `client-preference` entries about the named audience (tone/format they've asked for before) and `positioning-decision` entries relevant to the message. Fold anything relevant into the draft.

## 4. Load business-manager's own context

- Read `<businessMemoryPath>/business-manager/brand-guide.md` if it exists, for voice/tone. If it doesn't exist yet, proceed with a clear, direct professional tone and note in your output that no brand guide is on file.
- Read `<businessMemoryPath>/business-manager/memory/emails.md` if it exists — skim for prior angles/subject lines on the same purpose or campaign so this email doesn't repeat one already sent. (This is business-manager's own record of what it's written, distinct from the shared `log.jsonl` checked in step 3.)

## 5. Write the email

- One subject line (plus 1-2 alternates if useful)
- Body matching brand voice, sized to purpose (outreach = short; nurture/launch = can be longer)
- Exactly one clear call to action
- Sender sign-off using `senderName` / `businessName` from config

## 6. Save and log — own memory

- Save the email to `<businessMemoryPath>/business-manager/outputs/emails/<short-slug>.md`
- Append one line to `<businessMemoryPath>/business-manager/memory/emails.md`: date, purpose, audience, subject line, output path — so future invocations (any session, any surface) know this angle has been used
- Create `business-manager/memory/emails.md` with a one-line header if it doesn't exist yet

## 7. Log to shared business-memory, if warranted

Use judgment — don't log routine email metadata (that's step 6's job). Only log something here if the brief or your draft surfaced a fact worth any agent knowing later: a client preference stated for the first time, a positioning/messaging decision, a campaign learning.

```bash
python3 <businessMemoryPath>/scripts/log_tool.py --file <businessMemoryPath>/log.jsonl add \
  --field "<client-preference|campaign-learning|positioning-decision>" --content "<content>" --tags "<comma,separated,tags>"
```

If the field isn't registered yet, mention that to the user rather than guessing at a new one — `bm-add-log-field` handles that.

## 8. Return

Show the finished email in the chat, plus the path it was saved to, plus a one-line note if anything was also logged to shared business-memory.
