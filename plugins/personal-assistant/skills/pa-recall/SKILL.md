---
name: pa-recall
description: Reads or searches the shared _agent-memory log and answers in plain language — "what have I said about X?", "show me all my ideas", "what did I log last week about the redesign?". Read-only — never writes, forgets, or modifies entries.
---

# Recall

Answers a question from `log.jsonl` instead of leaving the user to run `log_tool.py` by hand.

## 1. Gate-check root

Resolve `<agentMemoryPath>`: check the `AGENT_MEMORY_PATH` environment variable first, then `~/.agent-memory/root.json`. If neither is set, or the resolved folder is missing `log-schema.json`, stop and tell the user to run `pa-setup` first.

## 2. Work out what's being asked

From the request, figure out:
- **Query text** — the topic/keyword to search for. Can be absent if the user just wants a whole category (e.g. "show me all my ideas").
- **Field filter** — a specific category from `log-schema.json` (`idea` and whatever else has been registered), if the request implies one. Leave unset to search across all fields.

Don't ask a clarifying question for an ambiguous-but-reasonable request — just search broadly and let the results speak. Only ask if the request is genuinely too vague to form any query.

## 3. Search

```bash
python3 <agentMemoryPath>/scripts/log_tool.py --file <agentMemoryPath>/log.jsonl search --query "<query>" --field "<field>"
```

Omit `--query` for a plain category browse, omit `--field` to search everything. Forgotten entries are excluded automatically — don't pass `--include-forgotten` unless the user explicitly asks to see removed entries too.

If the first search comes back empty, try a broader or rephrased query once before concluding there's nothing — don't stop at a single miss for an entry that plausibly exists under different wording.

## 4. Answer, don't just dump

Don't paste raw JSON. Synthesize a direct answer to what was actually asked, citing the relevant entries' content naturally. If several entries are relevant, group or summarize them rather than listing every field verbatim. If nothing relevant exists, say so plainly — don't fabricate an answer or pad it with unrelated results.

Mention an entry's `mentions` count when it's notably high (a recurring point) or when recency/frequency is relevant to the question.

## 5. Stay read-only

Never call `add` or `forget` from this skill, even if the answer surfaces something that looks outdated or worth logging — point the user to `pa-log` or `pa-forget` for that instead.
