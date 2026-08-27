---
name: pa-log
description: Captures a structured entry (idea, task, observation, etc.) into the shared _agent-memory log, so it can be recalled later during planning, scheduling, or decision-making — by this plugin or any other agent reading the same folder. Triggers on "log this idea", "add this to my log", "remember this for planning", "log an idea about X".
---

# Log

Appends one structured entry to the shared, persistent log. This is the capture step — recall happens later, when planning skills (from this plugin or any other agent) read the log back.

## 1. Gate-check root

Resolve `<agentMemoryPath>`: check the `AGENT_MEMORY_PATH` environment variable first, then `~/.agent-memory/root.json`. If neither is set, or the resolved folder is missing `log-schema.json`, stop and tell the user to run `pa-setup` first.

## 2. Distill from conversation

The user typically won't hand you a ready-made entry — they'll think out loud, and you extract what's log-worthy from that. Before writing anything:
- **Content** — condense the relevant part of what they said into a clear, structured entry (not a verbatim transcript, but don't lose specifics that make it useful later — keep it close to their own words and intent)
- **Field/type** — what kind of entry this is (e.g. `idea`). Infer it from context when it's obvious; ask only when genuinely ambiguous between two registered fields
- **Tags** (optional) — free-form keywords for later filtering

Show the user the distilled entry (content + field) before writing it, unless they've already confirmed what to log in the same breath (e.g. "log that as an idea"). Only append once you have a clear go-ahead — don't log speculatively from a stream-of-consciousness message on the assumption they want it captured.

## 3. Validate the field

Read `<agentMemoryPath>/log-schema.json` — the live, shared schema (not the plugin repo's copy, which is only the first-run seed).

- If the requested field is registered, proceed.
- If it isn't, tell the user it's not a registered field, offer to register it now via `pa-add-log-field`, or fall back to `idea` if they'd rather not create a new one.

## 4. Add via the script — never hand-append

Do not read the log and rewrite it yourself, and do not compose the JSON line by hand. As the log grows that costs more tokens and more time on every single entry, and it can't dedupe. Use the copy of `log_tool.py` that lives inside the shared folder (not the plugin repo's copy) — this keeps the folder self-contained for other agents:

```bash
python3 <agentMemoryPath>/scripts/log_tool.py --file <agentMemoryPath>/log.jsonl add \
  --field "<field>" --content "<content>" --tags "<comma,separated,tags>"
```

The script fuzzy-matches the new content against existing entries in the same field and writes the file in place (creating it if it doesn't exist yet). Its one-line JSON result tells you what happened:
- `"action": "added"` — genuinely new entry, new `id`
- `"action": "bumped"` — matched an existing entry closely enough that it's treated as a repeat mention; today's date was appended to that entry's `mentions` list instead of creating a duplicate (this mention history is a future signal for how often an idea recurs, useful when planning)
- `"action": "already_current"` — matched an existing entry already mentioned today; nothing changed

## 5. Return

One line: what happened (new entry logged under `<field>`, or "already logged — now also mentioned again today" with the matched content) and the entry id. No need to restate the full content back.
