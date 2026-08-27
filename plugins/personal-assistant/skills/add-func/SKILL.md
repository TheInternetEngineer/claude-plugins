---
name: add-func
description: Adds a new capability to the personal-assistant plugin — interviews the user for what it needs, registers it in modules.json, and scaffolds its SKILL.md file. Use when the user wants to add a new function/skill to their personal assistant, e.g. "add a new function for X", "I want a skill that does Y", "add-func".
---

# Add Function

Extends personal-assistant with a new capability without touching any existing file except the registry.

## 1. Interview

Ask for, in one pass:
- **Name** — verb-first, kebab-case (matches the existing convention: `log`, `add-log-field`). Reject noun-role names and explain why (that convention is reserved for sub-agents/agents, tiers above skills).
- **What it does** — one or two sentences; becomes the SKILL.md `description` (also drives auto-triggering, so it should include a couple of example trigger phrases).
- **Required fields** — what info must exist in `config.json` before this capability can run. Empty list is valid if nothing's needed.
- **Depends on** — any other capability whose *output* this one needs to read first (not just config — actual prior work product, e.g. reading the log). Empty list if none.

Current build phase only supports the **skill** tier (atomic, single deliverable, calls nothing else). If the request clearly needs to compose multiple skills or run multi-step (e.g. a planner that reads the log and also schedules), tell the user this belongs in a later tier (super skill / sub-agent) and isn't buildable yet — don't force it into a skill.

## 2. Check for collisions

Read `modules.json`. If the name already exists, stop and ask for a different name.

## 3. Register

Add an entry to `modules.json`:
```json
"<name>": {
  "tier": "skill",
  "description": "<one-line summary>",
  "required_fields": [...],
  "depends_on": [...]
}
```

## 4. Scaffold the skill file

Create `skills/<name>/SKILL.md` following the same shape as `log`:
1. Frontmatter: `name`, `description` (with trigger phrases)
2. Gate-check section — reads `config.json`, checks this capability's `required_fields`, stops with what's missing if incomplete
3. Gather-inputs section — what the invocation itself must supply
4. Load-context section — any `depends_on` capability's output (e.g. `log.jsonl`) + its own `memory/<name>.md` for prior work
5. Do-the-work section — **leave as a clearly marked placeholder** naming the actual task logic still to be written; don't invent it
6. Save-and-log section — output to `outputs/<name>/`, append to `memory/<name>.md`
7. Return section — show the result in chat plus the Drive path

## 5. Report

Tell the user the capability is registered and the file is scaffolded, and flag explicitly that step 5 (do-the-work) needs real instructions before it's usable.
