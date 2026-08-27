---
name: bm-add-func
description: Adds a new capability to the business-manager plugin — interviews the user for what it needs, registers it in modules.json, and scaffolds its SKILL.md file. Use when the user wants to add a new function/skill to business manager, e.g. "add a new function for X", "I want a skill that does Y", "add-func".
---

# Add Function

Extends business-manager with a new capability without touching any existing file except the registry.

## 1. Interview

Ask for, in one pass:
- **Name** — verb-first, kebab-case (matches the existing convention: `write-email`, `design-thumbnail`). Reject noun-role names and explain why (that convention is reserved for sub-agents/agents, tiers above skills). If the capability is meta/infrastructure in nature — the kind of thing another plugin using this same shared-memory pattern might also build (like `setup`, `log`, `forget`) — prefix it `bm-` to avoid colliding with another plugin's identically-named skill (e.g. `personal-assistant` has its own `pa-log`). Domain-specific capabilities (`write-email`, future ones) don't need the prefix — they won't collide.
- **What it does** — one or two sentences; becomes the SKILL.md `description` (also drives auto-triggering, so it should include a couple of example trigger phrases).
- **Required fields** — what info must exist in `business-manager.config.json` before this capability can run. Empty list is valid if nothing's needed.
- **Depends on** — any other capability whose *output* this one needs to read first (not just config — actual prior work product). Empty list if none.

Current build phase only supports the **skill** tier (atomic, single deliverable, calls nothing else). If the request clearly needs to compose multiple skills or run multi-step, tell the user this belongs in a later tier (super skill / sub-agent) and isn't buildable yet — don't force it into a skill.

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

Create `skills/<name>/SKILL.md` following the same shape as `write-email` — this is the standard template for any capability that produces a deliverable; don't improvise a different storage pattern per capability:

1. Frontmatter: `name`, `description` (with trigger phrases)
2. Gate-check section — resolves `<businessMemoryPath>` (check `BUSINESS_MEMORY_PATH` env var, then `~/.business-memory/root.json`), then reads `<businessMemoryPath>/business-manager.config.json`, checks this capability's `required_fields`, stops with what's missing if incomplete
3. Gather-inputs section — what the invocation itself must supply
4. Check-shared-business-memory section — search `<businessMemoryPath>/log.jsonl` (via `log_tool.py search`) for relevant `client-preference`/`positioning-decision`/`resource-location`/etc. entries before acting. Don't ask the user where something lives without checking `resource-location` entries first.
5. Check-own-history section — search this capability's own private index, `<businessMemoryPath>/business-manager/memory/<name>.jsonl` (via the **same** `log_tool.py`, just pointed at this file instead of the shared one — never a bespoke hand-written log format), for prior work on the same topic. Won't exist on first run; treat that as no history.
6. Load-other-context section — brand guide (if relevant, at `<businessMemoryPath>/business-manager/brand-guide.md`) + any `depends_on` capability's output
7. Do-the-work section — **leave as a clearly marked placeholder** naming the actual task logic still to be written; don't invent it
8. Save-output section — the finished deliverable to `<businessMemoryPath>/business-manager/outputs/<name>/`
9. Update-own-index section — `log_tool.py add --file <businessMemoryPath>/business-manager/memory/<name>.jsonl` with a short field (e.g. `"done"`) summarizing what happened and the output path. This is a private index — it doesn't need `bm-add-log-field`/schema registration.
10. Log-to-shared-memory section (judgment call, not automatic) — only if something surfaced is worth any agent knowing later, via `log_tool.py add --file <businessMemoryPath>/log.jsonl`
11. Return section — show the result in chat, the output path, and a note if anything was logged to shared business-memory

Only `log.jsonl`/`log-schema.json` at the top of `<businessMemoryPath>` are the shared, cross-agent surface — everything under `business-manager/` is private to this plugin.

## 5. Report

Tell the user the capability is registered and the file is scaffolded, and flag explicitly that step 5 (do-the-work) needs real instructions before it's usable. If the new capability has any `required_fields`, also tell the user to run `bm-setup` — it won't show as enabled until then.
