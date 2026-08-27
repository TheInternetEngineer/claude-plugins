---
name: setup
description: Onboarding for personal-assistant — locates or creates the Drive personal-assistant root, and collects the required fields for every registered capability so they can activate. Triggers on "set up personal assistant", "run setup", "configure personal assistant", or first use of any other personal-assistant capability that reports missing config.
---

# Setup

Establishes the one piece of state every other capability depends on: the Drive personal-assistant root, and its `config.json`.

## 1. Locate or create the personal-assistant root

- Search Drive for an existing folder literally named `_personal-assistant`.
- **Found:** read `_personal-assistant/config.json` from inside it. This is the existing config — don't recreate it.
- **Not found:** ask the user which Drive folder is their root (or to confirm the top-level Drive), then create `_personal-assistant/` inside it, with empty `config.json` (`{"modules": {}}`) and a `memory/` subfolder.

## 2. Read the capability registry

Read `modules.json` from this plugin's repo root — it lists every registered capability with its `required_fields` and `depends_on`.

## 3. Collect only what's missing

For each capability in `modules.json`:
- Compare its `required_fields` against what's already in `config.json`.
- Skip fields already answered — never re-ask.
- Batch the remaining questions to the user, grouped by capability, in one pass (don't interrogate one field at a time across many turns).

## 4. Compute enabled state

A capability is `enabled: true` only if:
- every field in its `required_fields` is present in `config.json`, **and**
- every capability listed in its `depends_on` is itself `enabled: true`

Write the full result back to `_personal-assistant/config.json`:
```json
{
  "modules": {
    "log": { "enabled": true }
  }
}
```

## 5. Report

Tell the user, per capability: enabled, or disabled + exactly what's missing.
