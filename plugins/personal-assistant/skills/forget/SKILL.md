---
name: forget
description: Removes an entry from the shared memory log — because it was logged by mistake, is no longer relevant, or has been superseded. Triggers on "forget that", "remove that from the log", "delete that idea", "that's not relevant anymore, take it out", "unlog X".
---

# Forget

Removes an entry from `log.jsonl` — by marking it forgotten, never by erasing the line, so nothing is silently lost and the removal itself has a date.

## 1. Gate-check root

Resolve `<agentMemoryPath>`: check the `AGENT_MEMORY_PATH` environment variable first, then `~/.agent-memory/root.json`. If neither is set, or the resolved folder is missing `log-schema.json`, stop and tell the user to run `setup` first.

## 2. Find the entry

If the user gave you an exact id, use it directly. Otherwise, run:
```bash
python3 <agentMemoryPath>/scripts/log_tool.py --file <agentMemoryPath>/log.jsonl search --query "<what they described>"
```
- **Exactly one strong match:** confirm it with the user in one line ("this one — '<content>', logged <first_seen>?") before removing it. Don't skip confirmation just because there's only one result — removal isn't reversible from the user's perspective even though it's a soft delete.
- **Multiple candidates:** show them (content + id) and ask which one.
- **No match:** say so; don't guess or fall back to forgetting something unrelated.

## 3. Remove it

Once confirmed:
```bash
python3 <agentMemoryPath>/scripts/log_tool.py --file <agentMemoryPath>/log.jsonl forget --id "<id>"
```
This marks the entry `forgotten: true` with a `forgotten_at` date — it stops appearing in normal `search` results and won't be matched for dedupe by `log` anymore, but the line itself stays in the file. Never hand-edit `log.jsonl` to delete a line directly.

## 4. Return

One line: confirm what was forgotten (its content) and its id. If the user later wants to log the same idea again, it will be treated as new, not resurrected.
