---
name: add-log-field
description: Registers a new log field/category (e.g. "decision", "blocker", "energy-level") in the personal assistant's log schema, so future log entries can use it. Triggers on "add a new log field", "I want to start logging X too", "create a log category for Y".
---

# Add Log Field

Extends what the `log` capability can capture, without touching the log skill's logic.

## 1. Interview

Ask for, in one pass:
- **Field name** — a single lowercase noun, kebab-case if multi-word (matches the existing convention: `idea`). Reject verb-first names — that convention is reserved for capabilities themselves.
- **Description** — one sentence on what belongs under this field. Becomes the schema entry and guides future field inference in `log`.

## 2. Check for collisions

Read `log-schema.json`. If the field name already exists, stop and ask whether they want a different name or to update the existing field's description instead.

## 3. Register

Add an entry to `log-schema.json`:
```json
"<field-name>": {
  "description": "<one-line description>"
}
```

## 4. Report

Confirm the field is registered and that `log` will recognize it on the next entry.
