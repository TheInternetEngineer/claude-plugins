---
name: forget
description: Removes an entry from the shared business-memory log — because it was logged by mistake, is outdated, or has been superseded (a client preference changed, a decision was reversed). Triggers on "forget that", "remove that from business memory", "that preference isn't true anymore, take it out", "unlog X".
---

# Forget

Removes an entry from `log.jsonl` — by marking it forgotten, never by erasing the line, so nothing is silently lost and the removal itself has a date.

## 1. Gate-check root

Resolve `<businessMemoryPath>`: check the `BUSINESS_MEMORY_PATH` environment variable first, then `~/.business-memory/root.json`. If neither is set, or the resolved folder is missing `log-schema.json`, stop and tell the user to run `setup` first.

## 2. Find the entry

If the user gave you an exact id, use it directly. Otherwise, run:
```bash
python3 <businessMemoryPath>/scripts/log_tool.py --file <businessMemoryPath>/log.jsonl search --query "<what they described>"
```
- **Exactly one strong match:** confirm it with the user in one line ("this one — '<content>', logged <first_seen>?") before removing it.
- **Multiple candidates:** show them (content + id) and ask which one.
- **No match:** say so; don't guess.

## 3. Remove it

Once confirmed:
```bash
python3 <businessMemoryPath>/scripts/log_tool.py --file <businessMemoryPath>/log.jsonl forget --id "<id>"
```
This marks the entry `forgotten: true` with a `forgotten_at` date — it stops appearing in normal `search` results and won't be matched for dedupe by `log` anymore, but the line itself stays in the file. Never hand-edit `log.jsonl` to delete a line directly.

## 4. Return

One line: confirm what was forgotten (its content) and its id.
