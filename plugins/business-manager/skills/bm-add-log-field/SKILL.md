---
name: bm-add-log-field
description: Registers a new log field/category (e.g. "vendor-note", "pricing-decision", "hiring-criteria") in the shared _business-memory log schema, so future log entries — from this plugin or any other agent — can use it. Triggers on "add a new log field", "I want to start tracking X too", "create a business-memory category for Y".
---

# Add Log Field

Extends what `bm-log` (and any other agent reading the same shared folder) can capture, without touching any skill's logic.

## 1. Gate-check root

Resolve `<businessMemoryPath>`: check the `BUSINESS_MEMORY_PATH` environment variable first, then `~/.business-memory/root.json`. If neither is set, or the resolved folder is missing `log-schema.json`, stop and tell the user to run `bm-setup` first.

## 2. Interview

Ask for, in one pass:
- **Field name** — a single lowercase noun, kebab-case if multi-word (matches the existing convention: `client-preference`, `campaign-learning`, `positioning-decision`). Reject verb-first names — that convention is reserved for capabilities themselves.
- **Description** — one sentence on what belongs under this field. Becomes the schema entry and guides future field inference in `bm-log`.

## 3. Check for collisions

Read `<businessMemoryPath>/log-schema.json` — the shared, live schema, not the plugin repo's copy (that one is only the first-run seed). If the field name already exists, stop and ask whether they want a different name or to update the existing field's description instead.

## 4. Register

Add an entry to `<businessMemoryPath>/log-schema.json`:
```json
"<field-name>": {
  "description": "<one-line description>"
}
```

## 5. Report

Confirm the field is registered in the shared schema and that `bm-log` — from any agent reading this folder — will recognize it on the next entry.
