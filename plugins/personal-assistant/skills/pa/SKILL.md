---
name: pa
description: General entry point for personal-assistant — figures out what a request needs, pulls relevant memory context first, runs the right existing capability (or handles the task directly if none fits cleanly), and decides at the end whether anything from the run is worth logging to shared agent-memory. Use for open-ended requests that don't obviously map to one specific pa- capability, or when the user just wants "personal assistant" to handle something end-to-end. Triggers on "personal assistant, ...", "/pa ...", or any request where the right specific capability isn't obvious up front.
---

# PA

The general-purpose front door to personal-assistant. Unlike the other capabilities, this one doesn't do one fixed thing — it decides what to do, does it (delegating to an existing capability where one fits), and closes the loop on memory.

## 1. Gate-check root

Resolve `<agentMemoryPath>`: check the `AGENT_MEMORY_PATH` environment variable first, then `~/.agent-memory/root.json`. If neither resolves, stop and tell the user to run `pa-setup` first.

## 2. Load context before deciding anything

Search `<agentMemoryPath>/log.jsonl` for anything relevant to the request:

```bash
python3 <agentMemoryPath>/scripts/log_tool.py --file <agentMemoryPath>/log.jsonl search --query "<topic>"
```

Do this *before* deciding on an approach — prior ideas and context should shape the plan, not just the output.

## 3. Decide the approach

Read `modules.json` to see what's already registered (`pa-log`, `pa-recall`, `pa-forget`, `pa-add-log-field`, `pa-add-func`, plus whatever's been added since).

- **A registered capability is a clean fit** — run it, using the context already gathered in step 2 so it isn't rediscovered. Don't ask the user to repeat themselves in capability-specific terms; translate the request yourself.
- **Nothing fits, but it's a reasonable one-off** — just do the work directly, grounded in step 2's context.
- **Nothing fits, and it looks like something that'll come up again** — do the task now regardless (don't block on this), but mention afterward that `pa-add-func` could turn it into a real capability if it's going to recur.

If the request is genuinely ambiguous about which of two capabilities it means, ask — don't guess on something consequential. Otherwise, proceed; this skill exists specifically so the user doesn't have to name the right capability themselves.

## 4. Decide whether to log the outcome

After the work is done — regardless of which path in step 3 was taken — apply judgment: is there something here worth any future run knowing (an idea, a decision, a pattern in how the user thinks or works, or something that warrants a new field via `pa-add-log-field`)? If yes:

```bash
python3 <agentMemoryPath>/scripts/log_tool.py --file <agentMemoryPath>/log.jsonl add \
  --field "<field>" --content "<content>" --tags "<comma,separated,tags>"
```

No separate confirmation round-trip needed here — the content is already well-defined by the completed task, unlike `pa-log`'s job of distilling something from open-ended conversation. Just log it and **say so plainly in the final response** so the user can `pa-forget` it if it's wrong. If nothing surfaced is worth persisting, don't log anything — most runs won't produce something log-worthy, and that's fine.

## 5. Return

Show the actual result of the work, which capability (if any) handled it, and the one-line note from step 4 if anything was logged.
