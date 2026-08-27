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

Look especially for `client-preference` entries about the named audience (tone/format they've asked for before), `positioning-decision` entries relevant to the message, and any `resource-location` entry that might matter (e.g. a client asset folder to reference). Fold anything relevant into the draft.

## 4. Check this skill's own history

business-manager keeps its own private, per-capability index — same tool as step 3, pointed at a private file instead of the shared one:

```bash
python3 <businessMemoryPath>/scripts/log_tool.py --file <businessMemoryPath>/business-manager/memory/write-email.jsonl search --query "<purpose/audience/campaign>"
```

This is write-email's own record of what it's already written (distinct from the shared judgment in step 3) — skim results so this email doesn't repeat an angle or subject line already used for the same purpose/campaign. The file won't exist on the first run; that's fine, treat it as no prior history.

## 5. Load business-manager's own context

Read `<businessMemoryPath>/business-manager/brand-guide.md` if it exists, for voice/tone. If it doesn't exist yet, proceed with a clear, direct professional tone and note in your output that no brand guide is on file.

## 6. Write the email

- One subject line (plus 1-2 alternates if useful)
- Body matching brand voice, sized to purpose (outreach = short; nurture/launch = can be longer)
- Exactly one clear call to action
- Sender sign-off using `senderName` / `businessName` from config

## 7. Save the output

Save the full email to `<businessMemoryPath>/business-manager/outputs/emails/<short-slug>.md`.

## 8. Update this skill's own index

```bash
python3 <businessMemoryPath>/scripts/log_tool.py --file <businessMemoryPath>/business-manager/memory/write-email.jsonl add \
  --field "sent" --content "<purpose> — <audience> — subject: <subject line>" --tags "<audience-or-client>,<campaign-if-any>"
```

`sent` is this private index's only field — it doesn't need `bm-add-log-field`/schema validation since it's not shared. Include the output path from step 7 in `--content` so a later search surfaces where the full email lives.

## 9. Log to shared business-memory, if warranted

Separate from step 8 — use judgment, don't log routine metadata here. Only log something if the brief or your draft surfaced a fact worth any agent knowing later: a client preference stated for the first time, a positioning/messaging decision, a campaign learning, or a resource location mentioned in passing.

```bash
python3 <businessMemoryPath>/scripts/log_tool.py --file <businessMemoryPath>/log.jsonl add \
  --field "<client-preference|campaign-learning|positioning-decision|resource-location>" --content "<content>" --tags "<comma,separated,tags>"
```

## 10. Return

Show the finished email in the chat, plus the path it was saved to, plus a one-line note if anything was also logged to shared business-memory.
