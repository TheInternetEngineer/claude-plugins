---
name: bm-log
description: Captures a structured entry (client preference, campaign learning, positioning decision, where a business folder/file lives, etc.) into the shared _business-memory log, so it can be recalled later during planning, client work, or content decisions — by this plugin or any other agent reading the same folder. Triggers on "log this client preference", "remember this for future campaigns", "add this to business memory", "log a positioning decision", "this is where our invoices/contracts/assets are", "remember this folder", "point business manager at this folder for X".
---

# Log

Appends one structured entry to the shared, persistent business-memory log. This is the capture step — recall happens later, when other capabilities (from this plugin or any other agent) read the log back.

## 1. Gate-check root

Resolve `<businessMemoryPath>`: check the `BUSINESS_MEMORY_PATH` environment variable first, then `~/.business-memory/root.json`. If neither is set, or the resolved folder is missing `log-schema.json`, stop and tell the user to run `bm-setup` first.

## 2. Distill from conversation

The user typically won't hand you a ready-made entry — they'll think out loud about a client, a campaign result, or a decision, and you extract what's worth remembering from that. Before writing anything:
- **Content** — condense the relevant part into a clear, structured entry (not a verbatim transcript, but don't lose the specifics that make it useful later)
- **Field/type** — what kind of entry this is (e.g. `client-preference`, `campaign-learning`, `positioning-decision`, `resource-location`). Infer it from context when obvious; ask only when genuinely ambiguous between two registered fields
- **Tags** (optional) — free-form keywords for later filtering (e.g. a client name, a campaign name). For `resource-location` entries, always tag with a short handle for the thing itself (e.g. `invoices-folder`) so a later lookup can search by that handle directly.

Show the user the distilled entry (content + field) before writing it, unless they've already confirmed what to log in the same breath. Only append once you have a clear go-ahead.

## 3. Validate the field

Read `<businessMemoryPath>/log-schema.json` — the live, shared schema (not the plugin repo's copy, which is only the first-run seed).

- If the requested field is registered, proceed.
- If it isn't, tell the user it's not a registered field, offer to register it now via `bm-add-log-field`, or suggest the closest existing field if they'd rather not create a new one.

## 4. Add via the script — never hand-append

Do not read the log and rewrite it yourself, and do not compose the JSON line by hand. Use the copy of `log_tool.py` that lives inside the shared folder (not the plugin repo's copy) — this keeps the folder self-contained for other agents:

```bash
python3 <businessMemoryPath>/scripts/log_tool.py --file <businessMemoryPath>/log.jsonl add \
  --field "<field>" --content "<content>" --tags "<comma,separated,tags>"
```

The script fuzzy-matches the new content against existing entries in the same field. Its one-line JSON result tells you what happened:
- `"action": "added"` — genuinely new entry, new `id`
- `"action": "bumped"` — matched an existing entry closely enough that it's treated as a repeat mention; today's date was appended to that entry's `mentions` list instead of creating a duplicate (recurring points are a signal of what actually matters to this business)
- `"action": "already_current"` — matched an existing entry already mentioned today; nothing changed

## 5. Return

One line: what happened (new entry logged under `<field>`, or "already logged — now also mentioned again today" with the matched content) and the entry id.
