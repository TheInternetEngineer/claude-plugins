---
name: setup
description: Onboarding for business-manager — locates or creates the Drive business root, and collects the required fields for every registered capability so they can activate. Triggers on "set up business manager", "run setup", "configure business manager", or first use of any other business-manager capability that reports missing config.
---

# Setup

Establishes the one piece of state every other capability depends on: the Drive business root, and its `config.json`.

## 1. Locate or create the business root

- Search Drive for an existing folder literally named `_business-manager`.
- **Found:** read `_business-manager/config.json` from inside it. This is the existing config — don't recreate it.
- **Not found:** ask the user which Drive folder is their business root (or to confirm the top-level Drive), then create `_business-manager/` inside it, with empty `config.json` (`{"modules": {}}`) and a `memory/` subfolder.

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

Write the full result back to `_business-manager/config.json`:
```json
{
  "modules": {
    "write-email": { "enabled": true, "senderName": "...", "businessName": "..." }
  }
}
```

## 5. Report

Tell the user, per capability: enabled, or disabled + exactly what's missing.
