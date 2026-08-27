#!/usr/bin/env python3
"""CLI for personal-assistant's log.jsonl: add (with fuzzy dedupe) and search,
operating on a local file so the model never has to read the whole log into
context to append or dedupe an entry. Stdlib only, no dependencies."""
import argparse
import difflib
import json
import re
import uuid
from datetime import datetime, timezone


def normalize(text):
    return re.sub(r"[^\w\s]", "", text.lower()).strip()


def load_entries(path):
    entries = []
    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    entries.append(json.loads(line))
    except FileNotFoundError:
        pass
    return entries


def save_entries(path, entries):
    with open(path, "w") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")


def find_similar(entries, field, content, threshold):
    norm_content = normalize(content)
    best, best_ratio = None, 0.0
    for e in entries:
        if e.get("field") != field:
            continue
        ratio = difflib.SequenceMatcher(None, norm_content, normalize(e.get("content", ""))).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best = e
    if best and best_ratio >= threshold:
        return best, best_ratio
    return None, best_ratio


def query_score(query, content):
    """Keyword-oriented score: exact substring, else word overlap, else char-level ratio."""
    norm_query, norm_content = normalize(query), normalize(content)
    if not norm_query:
        return 0.0
    if norm_query in norm_content:
        return 1.0
    query_words = set(norm_query.split())
    content_words = set(norm_content.split())
    overlap = len(query_words & content_words) / len(query_words) if query_words else 0.0
    char_ratio = difflib.SequenceMatcher(None, norm_query, norm_content).ratio()
    return max(overlap, char_ratio)


def cmd_add(args):
    entries = load_entries(args.file)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []

    match, ratio = find_similar(entries, args.field, args.content, args.threshold)
    if match:
        bumped = today not in match["mentions"]
        if bumped:
            match["mentions"].append(today)
        if tags:
            match["tags"] = sorted(set(match.get("tags", [])) | set(tags))
        save_entries(args.file, entries)
        print(json.dumps({
            "action": "bumped" if bumped else "already_current",
            "id": match["id"],
            "content": match["content"],
            "mentions": match["mentions"],
            "similarity": round(ratio, 2),
        }))
        return

    entry = {
        "id": uuid.uuid4().hex[:8],
        "field": args.field,
        "content": args.content,
        "tags": tags,
        "first_seen": today,
        "mentions": [today],
    }
    entries.append(entry)
    save_entries(args.file, entries)
    print(json.dumps({"action": "added", "id": entry["id"]}))


def cmd_search(args):
    entries = load_entries(args.file)
    results = []
    for e in entries:
        if args.id and e["id"] != args.id:
            continue
        if args.field and e.get("field") != args.field:
            continue
        if args.query:
            if query_score(args.query, e.get("content", "")) < args.threshold:
                continue
        results.append(e)
    results.sort(key=lambda e: len(e.get("mentions", [])), reverse=True)
    print(json.dumps(results))


def main():
    parser = argparse.ArgumentParser(description="personal-assistant log tool")
    parser.add_argument("--file", required=True, help="path to a local log.jsonl copy")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add an entry, or bump an existing similar one's mentions")
    p_add.add_argument("--field", required=True)
    p_add.add_argument("--content", required=True)
    p_add.add_argument("--tags", default="")
    p_add.add_argument("--threshold", type=float, default=0.6, help="similarity ratio (0-1) to treat as a dupe")
    p_add.set_defaults(func=cmd_add)

    p_search = sub.add_parser("search", help="look up entries by id, field, and/or fuzzy content match")
    p_search.add_argument("--query", default=None)
    p_search.add_argument("--field", default=None)
    p_search.add_argument("--id", default=None)
    p_search.add_argument("--threshold", type=float, default=0.5)
    p_search.set_defaults(func=cmd_search)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
