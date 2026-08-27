---
name: setup
description: Onboarding for personal-assistant — locates or creates the shared _agent-memory working folder, and collects the required fields for every registered capability so they can activate. Triggers on "set up personal assistant", "run setup", "configure personal assistant", or first use of any other personal-assistant capability that reports missing config.
---

# Setup

Establishes the one piece of state every other capability depends on: a **working folder** containing `_agent-memory/` — a shared, plugin-agnostic memory folder that any agent can read and write, not something owned by this plugin alone.

The working folder itself can be anything: a folder on the desktop, a project repo, or a directory synced by Drive/Dropbox/iCloud desktop apps (in which case it just looks like a local folder here — no cloud connector needed). The user picks it; nothing about it is Drive-specific or personal-assistant-specific.

## 1. Find the working folder pointer

Read `~/.agent-memory/root.json` — a small, plugin-agnostic pointer file in the user's home directory. It just says where the real data lives, since that location is user-chosen and can't be hardcoded, and any agent following this same convention can find it the same way.

- **Found:** it contains `{"workingFolder": "<absolute path>"}`. Use that path. Don't ask again.
- **Not found:** this is first run. Ask the user for an absolute path to their working folder — mention it can be an existing folder (e.g. a Drive/Dropbox/iCloud-synced folder, so it's remotely backed for free) or a fresh empty one. Expand `~`. Create the folder if it doesn't exist and the user confirms. Write `~/.agent-memory/root.json` with `{"workingFolder": "<path>"}`.

## 2. Locate or create the shared memory folder

`<workingFolder>/_agent-memory/` is the shared surface — keep it plugin-agnostic. If it doesn't exist yet, create it with:
- `log-schema.json` — copy this plugin's `log-schema.json` (repo root) as the seed. From now on `add-log-field` edits this copy, not the plugin repo's.
- `scripts/log_tool.py` — copy this plugin's `scripts/log_tool.py`, so the folder is self-contained and usable by any agent even without this plugin installed.
- `README.md` — copy this plugin's `templates/AGENT-MEMORY-README.md`.
- `context.json` — `{"instructionsFile": null}` (filled in by step 4).

If `_agent-memory/` already exists, leave `log-schema.json`, `log.jsonl`, `README.md`, and `context.json` alone — never overwrite user data. Only refresh `scripts/log_tool.py` from the plugin repo if it's missing, or the user explicitly asks to update it.

## 3. Locate or create this plugin's own config

This plugin's own bookkeeping is namespaced by filename so other agents know to leave it alone: `<workingFolder>/_agent-memory/personal-assistant.config.json`. Read it if it exists; otherwise create it as `{"modules": {}}`.

## 4. Pick up existing system instructions, if any

Check the top level of `<workingFolder>` (not `_agent-memory/`, the folder itself) for an existing instructions file — `CLAUDE.md`, `AGENTS.md`, or `README.md`, in that order of preference. If one exists and `_agent-memory/context.json`'s `instructionsFile` isn't already set, read it for how the user's broader system/folder is organized, and record its relative path there — this is shared, so any agent benefits, not just this plugin. If none exists, leave it `null` — don't create one speculatively.

## 5. Read the capability registry

Read `modules.json` from this plugin's repo root — it lists every registered capability with its `required_fields` and `depends_on`.

## 6. Collect only what's missing

For each capability in `modules.json`:
- Compare its `required_fields` against what's already in `personal-assistant.config.json`.
- Skip fields already answered — never re-ask.
- Batch the remaining questions to the user, grouped by capability, in one pass (don't interrogate one field at a time across many turns).

## 7. Compute enabled state

A capability is `enabled: true` only if:
- every field in its `required_fields` is present in `personal-assistant.config.json`, **and**
- every capability listed in its `depends_on` is itself `enabled: true`

Write the full result back to `<workingFolder>/_agent-memory/personal-assistant.config.json`:
```json
{
  "modules": {
    "log": { "enabled": true }
  }
}
```

## 8. Report

Tell the user: the working folder path, that `_agent-memory/` there is shared and any other agent can read `log.jsonl` from it directly, per-capability enabled/disabled status (+ exactly what's missing if disabled), and whether an instructions file was picked up.
