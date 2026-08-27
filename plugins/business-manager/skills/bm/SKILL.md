---
name: bm
description: General entry point for business-manager — figures out what a request needs, pulls relevant business-memory context first, runs the right existing capability (or handles the task directly if none fits cleanly), and decides at the end whether anything from the run is worth logging to shared business-memory. Use for open-ended business requests that don't obviously map to one specific bm- capability, or when the user just wants "business manager" to handle something end-to-end. Triggers on "business manager, ...", "/bm ...", "handle this for the business", or any business task where the right specific capability isn't obvious up front.
---

# BM

The general-purpose front door to business-manager. Unlike the other capabilities, this one doesn't do one fixed thing — it decides what to do, does it (delegating to an existing capability where one fits), and closes the loop on memory.

## 1. Gate-check root

Resolve `<businessMemoryPath>`: check the `BUSINESS_MEMORY_PATH` environment variable first, then `~/.business-memory/root.json`. If neither resolves, stop and tell the user to run `bm-setup` first.

## 2. Load context before deciding anything

Search `<businessMemoryPath>/log.jsonl` for anything relevant to the request:

```bash
python3 <businessMemoryPath>/scripts/log_tool.py --file <businessMemoryPath>/log.jsonl search --query "<topic/client/campaign>"
```

Also read `<businessMemoryPath>/business-manager/brand-guide.md` if the task is content-producing and the file exists. Do this *before* deciding on an approach — prior decisions and preferences should shape the plan, not just the output.

## 3. Decide the approach

Read `modules.json` to see what's already registered (`write-email`, `bm-log`, `bm-recall`, `bm-forget`, `bm-add-log-field`, `bm-add-func`, plus whatever's been added since).

- **A registered capability is a clean fit** — run it, using the context already gathered in step 2 so it isn't rediscovered. Don't ask the user to repeat themselves in capability-specific terms; translate the request yourself.
- **Nothing fits, but it's a reasonable one-off** — just do the work directly, grounded in step 2's context and the brand guide where relevant. Don't force it into an ill-fitting capability.
- **Nothing fits, and it looks like something that'll come up again** — do the task now regardless (don't block on this), but mention afterward that `bm-add-func` could turn it into a real capability if it's going to recur.

If the request is genuinely ambiguous about which of two capabilities it means, or needs information no capability's gate-check would catch, ask — don't guess on something consequential. Otherwise, proceed; this skill exists specifically so the user doesn't have to name the right capability themselves.

## 4. Decide whether to log the outcome

After the work is done — regardless of which path in step 3 was taken — apply the same judgment `write-email` already applies at its own closing step: is there a fact here worth any future run knowing (a client preference, a campaign learning, a positioning decision, a resource location, or something that warrants a new field via `bm-add-log-field`)? If yes:

```bash
python3 <businessMemoryPath>/scripts/log_tool.py --file <businessMemoryPath>/log.jsonl add \
  --field "<field>" --content "<content>" --tags "<comma,separated,tags>"
```

No separate confirmation round-trip needed here — the content is already well-defined by the completed task, unlike `bm-log`'s job of distilling something from open-ended conversation. Just log it and **say so plainly in the final response** (what was logged, under which field) so the user can `bm-forget` it if it's wrong. If nothing surfaced is worth persisting, don't log anything — most runs won't produce something log-worthy, and that's fine.

## 5. Return

Show the actual result of the work, which capability (if any) handled it, and the one-line note from step 4 if anything was logged.
