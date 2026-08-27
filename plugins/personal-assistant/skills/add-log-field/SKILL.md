---
name: add-log-field
description: Registers a new log field/category (e.g. "decision", "blocker", "energy-level") in the shared _agent-memory log schema, so future log entries — from this plugin or any other agent — can use it. Triggers on "add a new log field", "I want to start logging X too", "create a log category for Y".
---

# Add Log Field

Extends what `log` (and any other agent reading the same shared folder) can capture, without touching any skill's logic.

## 1. Gate-check root

Read `~/.agent-memory/root.json` for `workingFolder`. If it doesn't exist, or `<workingFolder>/_agent-memory/` doesn't exist, stop and tell the user to run `setup` first.

## 2. Interview

Ask for, in one pass:
- **Field name** — a single lowercase noun, kebab-case if multi-word (matches the existing convention: `idea`). Reject verb-first names — that convention is reserved for capabilities themselves.
- **Description** — one sentence on what belongs under this field. Becomes the schema entry and guides future field inference in `log`.

## 3. Check for collisions

Read `<workingFolder>/_agent-memory/log-schema.json` — the shared, live schema, not the plugin repo's copy (that one is only the first-run seed). If the field name already exists, stop and ask whether they want a different name or to update the existing field's description instead.

## 4. Register

Add an entry to `<workingFolder>/_agent-memory/log-schema.json`:
```json
"<field-name>": {
  "description": "<one-line description>"
}
```

## 5. Report

Confirm the field is registered in the shared schema and that `log` — from any agent reading this folder — will recognize it on the next entry.
