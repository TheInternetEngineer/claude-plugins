# _business-memory

This is the business's own running record of recurring context and judgment — client preferences, what's worked or hasn't in campaigns, positioning decisions, content angles already used. It is deliberately **not** a store of raw operational records: contracts, invoices, and financial statements stay wherever they already live, not here. An agent that reads this folder gains the accumulated judgment calls of running this business, not its paperwork.

It's shared and plugin-agnostic on purpose: any agent that can read files and run Python can use it — nothing here requires business-manager specifically to be installed.

**Finding this folder:** the `BUSINESS_MEMORY_PATH` environment variable points here. Any agent — Claude-based or not — should check that first. `~/.business-memory/root.json` (`{"businessMemoryPath": "..."}`) is a same-session fallback for tools that can't see a freshly-set env var yet.

**Across machines:** if this folder lives inside a Drive/Dropbox/iCloud-synced directory, the same memory is available on every machine with that sync client signed in — just re-run `bm-setup` there to point that machine's `BUSINESS_MEMORY_PATH` at the local sync path. The data itself is only as secure as that sync account (2FA recommended); this folder should never be committed to a public git repo.

## log.jsonl

One JSON object per line. Append-only; existing lines are only ever updated to add a mention date or a forgotten flag (see below) — never delete or reorder lines by hand.

Fields per entry:
- `id` — short unique id (8 hex chars)
- `field` — the entry's category/type, one of the names registered in `log-schema.json`
- `content` — the entry text
- `tags` — optional list of free-form keywords
- `first_seen` — ISO date (`YYYY-MM-DD`) the entry was first logged
- `mentions` — list of ISO dates the same point recurred; more mentions means it came up more often — a useful signal for what actually matters to this business
- `forgotten` / `forgotten_at` — present only once an entry has been removed via `bm-forget`. The line stays for audit purposes but is excluded from normal reads.

## log-schema.json

The registry of valid `field` values, each with a one-line `description`. Seeded with fields that fit running a business (`client-preference`, `campaign-learning`, `positioning-decision`) — add more here directly, or through the `bm-add-log-field` skill if you're an agent running business-manager.

## scripts/log_tool.py

Stdlib-only Python, no install step. Handles adding, searching, and removing entries. Usage:

```bash
python3 scripts/log_tool.py --file log.jsonl add --field client-preference --content "..." --tags "a,b"
python3 scripts/log_tool.py --file log.jsonl search --query "..."
python3 scripts/log_tool.py --file log.jsonl forget --id <id>
```

- `add` fuzzy-dedupes: a repeated point bumps `mentions` instead of creating a duplicate.
- `search` excludes forgotten entries by default (`--include-forgotten` to see them).
- `forget` soft-deletes by id only — it never guesses which entry to remove from a text query, so resolve the id via `search` first.

Always go through this script rather than hand-editing the file — hand-editing skips deduping and the forgotten-entry bookkeeping. This copy is generic on purpose (no plugin name baked in) — the same file is seeded into every plugin's memory folder, so fixes to it stay portable rather than drifting between copies.

## context.json

`{"instructionsFile": "<path or null>"}` — if the parent of this folder has a `CLAUDE.md`, `AGENTS.md`, or `README.md` describing how the broader system/folder is organized, its path is recorded here so any agent can find it without re-discovering it.

## Ownership convention

Any file or folder here **not** prefixed with a plugin's name (e.g. `business-manager.config.json`, `business-manager/`) is shared, plugin-agnostic data — safe for any agent to read and, for `log.jsonl`/`log-schema.json`, to extend through the script above. Plugin-prefixed files are that plugin's own private bookkeeping — leave them alone unless you are that plugin.
