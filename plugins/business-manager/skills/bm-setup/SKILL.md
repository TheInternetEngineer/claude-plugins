---
name: bm-setup
description: Onboarding for business-manager — locates or creates the shared _business-memory folder and business-manager's own config within it, and collects the required fields for every registered capability so they can activate. Triggers on "set up business manager", "run setup", "configure business manager", or first use of any other business-manager capability that reports missing config.
---

# Setup

Establishes one piece of state every other capability depends on: the shared **`_business-memory`** folder — recurring business judgment any agent can read, not owned by this plugin alone — inside which business-manager keeps its own private config and working files, namespaced by filename per the ownership convention in `_business-memory/README.md`.

Not tied to Google Drive specifically. It's just a folder — plain local, or inside whatever cloud-sync client (Drive, Dropbox, iCloud Drive, etc.) the user already uses. If it happens to be Drive-synced, it works because Drive Desktop mirrors it as an ordinary local folder — no Drive API or connector involved either way.

## 1. Discover the business-memory path

Check, in order, stopping at the first hit:

1. **Environment variable** — run `echo "$BUSINESS_MEMORY_PATH"`. If set and non-empty, that's the memory path.
2. **Local pointer file** — read `~/.business-memory/root.json`. If it exists, it contains `{"businessMemoryPath": "<absolute path>"}`. This exists because a shell env var only becomes visible to *new* shells after step 3 persists it — this file is the reliable fallback until then.
3. **Neither found — first run.**
   a. Ask if a business-memory folder already exists somewhere (a previous setup, another machine, a synced folder they know the path to). If yes, use that path as-is (it should already have `log.jsonl`/`log-schema.json`; if it's empty, confirm that's intentional before treating it as fresh).
   b. If not, advise before asking for a path: a plain local folder only lives on this machine — it won't be there from another computer. A folder inside cloud-synced storage is reachable from anywhere that sync account is signed in. Recommend synced unless they're sure this machine is the only place this will ever be used.
   c. Ask for the absolute path. Expand `~`. Create a `_business-memory` subfolder inside it (unless they point straight at an existing `_business-memory` folder — use that as-is). Create directories as needed once confirmed.

   Once resolved, persist the path two ways:
   - Write `~/.business-memory/root.json` = `{"businessMemoryPath": "<path>"}` (effective immediately, this session).
   - Idempotently append to the user's shell rc (`$SHELL` → `/bin/zsh`: `~/.zshrc`, `/bin/bash`: `~/.bashrc`; skip if `BUSINESS_MEMORY_PATH` is already exported there):
     ```
     # added by business-manager: business memory path
     export BUSINESS_MEMORY_PATH="<path>"
     ```
     Tell the user this takes effect in new terminals/sessions, not the current one.

## 2. Locate or create the business-memory folder's contents

At `<businessMemoryPath>/`, if it's empty or missing these files, create:
- `log-schema.json` — copy this plugin's `log-schema.json` (repo root) as the seed. From now on `bm-add-log-field` edits this copy, not the plugin repo's.
- `scripts/log_tool.py` — copy this plugin's `scripts/log_tool.py`, so the folder is self-contained and usable by any agent even without this plugin installed.
- `README.md` — copy this plugin's `templates/BUSINESS-MEMORY-README.md`.
- `context.json` — `{"instructionsFile": null}` (filled in by step 3).

If these already exist, leave them (and `log.jsonl`) alone — never overwrite user data. Only refresh `scripts/log_tool.py` in place if it's missing, or the user explicitly asks to update it.

## 3. Locate or create this plugin's own config

This plugin's own bookkeeping is namespaced by filename so other agents know to leave it alone: `<businessMemoryPath>/business-manager.config.json`. Read it if it exists; otherwise create it as `{"modules": {}}`.

## 4. Pick up existing system instructions, if any

Check the parent of `<businessMemoryPath>` for an existing instructions file — `CLAUDE.md`, `AGENTS.md`, or `README.md`, in that order of preference. If one exists and `context.json`'s `instructionsFile` isn't already set, read it and record its path there — this is shared, so any agent benefits, not just this plugin. If none exists, leave it `null`.

## 5. Read the capability registry

Read `modules.json` from this plugin's repo root — it lists every registered capability with its `required_fields` and `depends_on`.

## 6. Collect only what's missing

For each capability in `modules.json`:
- Compare its `required_fields` against what's already in `<businessMemoryPath>/business-manager.config.json`.
- Skip fields already answered — never re-ask.
- Batch the remaining questions to the user, grouped by capability, in one pass (don't interrogate one field at a time across many turns).

## 7. Compute enabled state

A capability is `enabled: true` only if:
- every field in its `required_fields` is present in `business-manager.config.json`, **and**
- every capability listed in its `depends_on` is itself `enabled: true`

Write the full result back to `<businessMemoryPath>/business-manager.config.json`:
```json
{
  "modules": {
    "write-email": { "enabled": true, "senderName": "...", "businessName": "..." }
  }
}
```

## 8. Report

Tell the user: the business-memory path, whether it came from the env var, the pointer file, or was just created; that it's shared and any other agent can read `log.jsonl` from it directly via `BUSINESS_MEMORY_PATH`; per-capability enabled/disabled status (+ exactly what's missing if disabled); and whether an instructions file was picked up.
