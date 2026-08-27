# _agent-memory

A shared, plugin-agnostic memory folder. Any agent that can read files and run Python can use it — nothing here requires a specific plugin to be installed.

## log.jsonl

One JSON object per line. Append-only; existing lines are only ever updated to add a mention date (see below) — never delete or reorder lines by hand.

Fields per entry:
- `id` — short unique id (8 hex chars)
- `field` — the entry's category/type, one of the names registered in `log-schema.json`
- `content` — the entry text
- `tags` — optional list of free-form keywords
- `first_seen` — ISO date (`YYYY-MM-DD`) the entry was first logged
- `mentions` — list of ISO dates the same idea was logged again; more mentions means it came up more often — a useful signal when planning or prioritizing

## log-schema.json

The registry of valid `field` values, each with a one-line `description`. Add new fields here directly, or through the `add-log-field` skill if you're an agent running the personal-assistant plugin.

## scripts/log_tool.py

Stdlib-only Python, no install step. Handles adding entries with fuzzy dedupe (a repeated idea bumps `mentions` instead of creating a duplicate) and searching. Usage:

```bash
python3 scripts/log_tool.py --file log.jsonl add --field idea --content "..." --tags "a,b"
python3 scripts/log_tool.py --file log.jsonl search --query "..."
```

Always go through this script to add or search entries — hand-editing the file skips deduping.

## context.json

`{"instructionsFile": "<relative path or null>"}` — if the working folder (the parent of this one) has a `CLAUDE.md`, `AGENTS.md`, or `README.md` describing how the broader system/folder is organized, its path is recorded here so any agent can find it without re-discovering it.

## Ownership convention

Any file or folder here **not** prefixed with a plugin's name (e.g. `personal-assistant.config.json`, `personal-assistant/`) is shared, plugin-agnostic data — safe for any agent to read and, for `log.jsonl`/`log-schema.json`, to extend through the script above. Plugin-prefixed files are that plugin's own private bookkeeping — leave them alone unless you are that plugin.
