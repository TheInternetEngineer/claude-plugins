---
name: setup
description: Onboarding for personal-assistant — locates or creates the local working folder that holds its data, and collects the required fields for every registered capability so they can activate. Triggers on "set up personal assistant", "run setup", "configure personal assistant", or first use of any other personal-assistant capability that reports missing config.
---

# Setup

Establishes the one piece of state every other capability depends on: a **working folder** — an ordinary local directory (plain filesystem, no special API) — and its `config.json`.

The working folder can be anything: a folder on the desktop, a project repo, or a directory synced by Drive/Dropbox/iCloud desktop apps (in which case it just looks like a local folder here — no cloud connector needed). The user picks it; nothing about it is Drive-specific.

## 1. Find the working folder pointer

Read `~/.personal-assistant/root.json` (a small pointer file in the user's home directory — it just says where the real data lives, since that location is user-chosen and can't be hardcoded).

- **Found:** it contains `{"workingFolder": "<absolute path>"}`. Use that path. Don't ask again.
- **Not found:** this is first run. Ask the user for an absolute path to their working folder — mention it can be an existing folder (e.g. a Drive/Dropbox/iCloud-synced folder, so it's remotely backed for free) or a fresh empty one. Expand `~`. Create the folder if it doesn't exist and the user confirms. Write `~/.personal-assistant/root.json` with `{"workingFolder": "<path>"}`.

## 2. Locate or create the personal-assistant root inside it

- If `<workingFolder>/_personal-assistant/config.json` exists, read it — this is the existing config, don't recreate it.
- Otherwise create `<workingFolder>/_personal-assistant/`, with `config.json` (`{"modules": {}, "instructionsFile": null}`) and a `memory/` subfolder.

## 3. Pick up existing system instructions, if any

Check the top level of `<workingFolder>` (not `_personal-assistant/`, the folder itself) for an existing instructions file — `CLAUDE.md`, `AGENTS.md`, or `README.md`, in that order of preference. If one exists and `instructionsFile` isn't already set in `config.json`, read it for how the user's broader system/folder is organized, and record its relative path as `instructionsFile` in `config.json` so other capabilities can find it without re-discovering it. If none exists, leave `instructionsFile` as `null` — don't create one speculatively.

## 4. Read the capability registry

Read `modules.json` from this plugin's repo root — it lists every registered capability with its `required_fields` and `depends_on`.

## 5. Collect only what's missing

For each capability in `modules.json`:
- Compare its `required_fields` against what's already in `config.json`.
- Skip fields already answered — never re-ask.
- Batch the remaining questions to the user, grouped by capability, in one pass (don't interrogate one field at a time across many turns).

## 6. Compute enabled state

A capability is `enabled: true` only if:
- every field in its `required_fields` is present in `config.json`, **and**
- every capability listed in its `depends_on` is itself `enabled: true`

Write the full result back to `<workingFolder>/_personal-assistant/config.json`, preserving `instructionsFile`:
```json
{
  "instructionsFile": "CLAUDE.md",
  "modules": {
    "log": { "enabled": true }
  }
}
```

## 7. Report

Tell the user the working folder path, per capability whether it's enabled or disabled + exactly what's missing, and whether an instructions file was picked up.
