---
name: bm-recall
description: Reads or searches the shared _business-memory log and answers in plain language — "what do we know about Acme?", "show me all positioning decisions", "where do our invoices live?", "what's in business memory about the fall campaign?". Read-only — never writes, forgets, or modifies entries.
---

# Recall

Answers a question from `log.jsonl` instead of leaving the user to run `log_tool.py` by hand.

## 1. Gate-check root

Resolve `<businessMemoryPath>`: check the `BUSINESS_MEMORY_PATH` environment variable first, then `~/.business-memory/root.json`. If neither is set, or the resolved folder is missing `log-schema.json`, stop and tell the user to run `bm-setup` first.

## 2. Work out what's being asked

From the request, figure out:
- **Query text** — the topic/name/keyword to search for. Can be absent if the user just wants a whole category (e.g. "show me all positioning decisions").
- **Field filter** — a specific category from `log-schema.json` (`client-preference`, `campaign-learning`, `positioning-decision`, `resource-location`, or any custom one registered later), if the request implies one. Leave unset to search across all fields.

Don't ask a clarifying question for an ambiguous-but-reasonable request — just search broadly and let the results speak. Only ask if the request is genuinely too vague to form any query (e.g. "tell me about the business" with no topic at all).

## 3. Search

```bash
python3 <businessMemoryPath>/scripts/log_tool.py --file <businessMemoryPath>/log.jsonl search --query "<query>" --field "<field>"
```

Omit `--query` for a plain category browse, omit `--field` to search everything. Forgotten entries are excluded automatically — don't pass `--include-forgotten` unless the user explicitly asks to see removed entries too.

If the first search comes back empty, try a broader or rephrased query once before concluding there's nothing — don't stop at a single miss for an entry that plausibly exists under different wording.

## 4. Answer, don't just dump

Don't paste raw JSON. Synthesize a direct answer to what was actually asked, citing the relevant entries' content naturally. If several entries are relevant, group or summarize them rather than listing every field verbatim. If nothing relevant exists, say so plainly — don't fabricate an answer or pad it with unrelated results.

Mention an entry's `mentions` count when it's notably high (a recurring point) or when recency/frequency is relevant to the question.

## 5. Stay read-only

Never call `add` or `forget` from this skill, even if the answer surfaces something that looks outdated or worth logging — point the user to `bm-log` or `bm-forget` for that instead.
