# [Business Name] — Agent Instructions & Map

*[Business Name] — for any agent (Claude or otherwise) working in this folder tree.*

Copy this file to the top of your business's folder — the same Drive/Dropbox/iCloud root that contains (or will contain) `_business-memory/`. Fill in every `[bracket]`, delete this line and the one above, and keep the file itself short: it's a map and a set of invariants, not the memory. Facts and decisions belong in `_business-memory/log.jsonl`, not here — this file should stay stable while that log grows.

## What this business is

[One paragraph: what the business does, who it serves, how it makes money.]

## Corporate structure

[Only if relevant — a holding company, multiple brands sharing this Drive, adjacent projects that should NOT be conflated with this business. Delete this section if there's nothing to disambiguate.]

## Hard invariants (rarely change, always apply)

[Things that should never drift regardless of who's working here or when — brand name spelling, a name that's retired and shouldn't resurface from old files, a rule with no exceptions (e.g. "X is never public"). Keep this list short — if something changes occasionally, it belongs in the log, not here.]

## Visual identity

[Colors, fonts, logo usage — whatever a content-producing capability needs to stay on-brand without reading a separate brand guide every time. Optional if you'd rather keep this in a dedicated brand-guide file and just point to it here.]

## Where things live (top-level folder structure)

[A short map of the folders under this root and what's in each — enough for an agent to know where to look, not a full directory listing. Update this when the top-level structure changes; don't bother for every subfolder rename.]

## Accumulated business judgment

`_business-memory/log.jsonl` holds the running record of positioning decisions, campaign plans/learnings, preferences, resource locations, and anything else worth remembering across sessions. Read, search, and append it via `_business-memory/scripts/log_tool.py` — see that folder's `README.md` for exact usage. Check it before making a call that's probably already been made rather than re-deriving something from scratch.

## business-manager plugin

This Drive's `_business-memory` folder also hosts the business-manager plugin's own config (`business-manager.config.json`) — its capabilities (`bm-log`, `bm-setup`, etc.) read and write this same log.

---
*This file is the map, not the memory — for the actual decisions and facts, read `_business-memory/log.jsonl`. Keep this file to structure and invariants only, so it doesn't drift out of sync with the log.*

---

**Auto-loading note:** Claude Code only auto-loads `CLAUDE.md` files into a session's context on its own — it will not automatically read this `AGENTS.md` just by being nearby. Create a one-line sibling file named `CLAUDE.md` in this same folder containing just:

```
@AGENTS.md
```

That imports this file's full content without duplicating it — any Claude Code or Cowork session working anywhere under this folder tree will then pick it up automatically. (`bm-setup` offers to create this for you if it finds an `AGENTS.md` without a `CLAUDE.md` sibling — you don't have to do it by hand if you're running setup anyway.)
