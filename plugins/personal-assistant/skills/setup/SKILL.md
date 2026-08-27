---
name: setup
description: Onboarding for personal-assistant — locates or creates the shared _agent-memory folder via the AGENT_MEMORY_PATH environment variable, and collects the required fields for every registered capability so they can activate. Triggers on "set up personal assistant", "run setup", "configure personal assistant", or first use of any other personal-assistant capability that reports missing config.
---

# Setup

Establishes the one piece of state every other capability depends on: an **agent memory folder** — a shared, plugin-agnostic directory that any agent (this plugin or any other, Claude-based or not) can find and read through one convention: the `AGENT_MEMORY_PATH` environment variable.

The folder itself can be anything: a folder on the desktop, a project repo, or — recommended, since it makes the same memory available on every machine the user works from — a directory synced by Drive/Dropbox/iCloud desktop apps (in which case it just looks like an ordinary local folder here; no cloud connector needed). The user picks it; nothing about it is Drive-specific or personal-assistant-specific.

## 1. Discover the memory path

Check, in order, stopping at the first hit:

1. **Environment variable** — run `echo "$AGENT_MEMORY_PATH"` (or equivalent). If it's set and non-empty, that's the memory path.
2. **Local pointer file** — read `~/.agent-memory/root.json`. If it exists, it contains `{"agentMemoryPath": "<absolute path>"}`. This exists because a shell env var only becomes visible to *new* shells after step 3 below persists it — this file is the reliable fallback for the current and any other Claude Code session in the meantime.
3. **Neither found — first run.** Ask the user for an absolute path. Two things can happen:
   - They point at an existing `_agent-memory` folder (has `log.jsonl`/`log-schema.json` already) — use it as-is.
   - They give any other folder (existing or new) — create an `_agent-memory` subfolder inside it, and the memory path is that subfolder.

   Mention it can be a Drive/Dropbox/iCloud-synced location, so the same memory is reachable from any machine that has that sync client signed in — that's the recommended default if they're not sure. Expand `~`. Create directories as needed once the user confirms.

   Once resolved, persist the path two ways so it's durable everywhere:
   - Write `~/.agent-memory/root.json` = `{"agentMemoryPath": "<path>"}` (takes effect immediately, this session).
   - Persist the env var for future shells/tools: detect the user's shell (`$SHELL` — `/bin/zsh` → `~/.zshrc`, `/bin/bash` → `~/.bashrc`) and, only if an `AGENT_MEMORY_PATH` export isn't already present in that file, append:
     ```
     # added by personal-assistant: agent memory path
     export AGENT_MEMORY_PATH="<path>"
     ```
     Tell the user this takes effect in new terminals/sessions, not the current one.

## 2. Locate or create the memory folder's contents

At `<agentMemoryPath>/`, if it's empty or missing these files, create:
- `log-schema.json` — copy this plugin's `log-schema.json` (repo root) as the seed. From now on `add-log-field` edits this copy, not the plugin repo's.
- `scripts/log_tool.py` — copy this plugin's `scripts/log_tool.py`, so the folder is self-contained and usable by any agent even without this plugin installed.
- `README.md` — copy this plugin's `templates/AGENT-MEMORY-README.md`.
- `context.json` — `{"instructionsFile": null}` (filled in by step 3).

If these already exist, leave them (and `log.jsonl`) alone — never overwrite user data. Only refresh `scripts/log_tool.py` in place if it's missing, or the user explicitly asks to update it.

## 3. Locate or create this plugin's own config

This plugin's own bookkeeping is namespaced by filename so other agents know to leave it alone: `<agentMemoryPath>/personal-assistant.config.json`. Read it if it exists; otherwise create it as `{"modules": {}}`.

## 4. Pick up existing system instructions, if any

Check the parent of `<agentMemoryPath>` for an existing instructions file — `CLAUDE.md`, `AGENTS.md`, or `README.md`, in that order of preference. If one exists and `context.json`'s `instructionsFile` isn't already set, read it for how the user's broader system/folder is organized, and record its path there — this is shared, so any agent benefits, not just this plugin. If none exists, leave it `null` — don't create one speculatively.

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

Write the full result back to `<agentMemoryPath>/personal-assistant.config.json`:
```json
{
  "modules": {
    "log": { "enabled": true }
  }
}
```

## 8. Report

Tell the user: the memory path, whether it came from the env var, the pointer file, or was just created; that it's shared and any other agent can read `log.jsonl` from it directly by checking `AGENT_MEMORY_PATH`; per-capability enabled/disabled status (+ exactly what's missing if disabled); and whether an instructions file was picked up.
