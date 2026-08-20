---
name: wrap-my-day
description: Close out a day in Ricardo's Athlete OS vault — pulls that day's Strava activities into training notes and updates the daily note, keeping Home, the Bases tables, and the graph current. Use when the user says "wrap my day", "wrap up today", "log today's training", or asks to close out a specific date.
---

# Wrap My Day

Closes out one calendar day in this vault: imports any new Strava activities as training notes, and creates/updates that day's note in `daily/`.

## When to use

- User says "wrap my day", "wrap up today", "close out today", "log today's training"
- User asks to backfill a specific past date ("wrap up yesterday", "wrap up 2026-08-15")
- Default target date is **today** unless the user names another date

## Steps

1. **Determine the target date** (default: today, in `YYYY-MM-DD` format).

2. **Fetch that day's activities from Strava** using the `mcp__Strava__list_activities` tool, with `range_start` = `{date}T00:00:00` and `range_end` = `{date}T23:59:59`. Request `first: 20` (a single day never has more).

3. **Build a compact JSON array** — one object per activity with exactly these fields, copied verbatim from the tool result (never invent or estimate a number):
   ```json
   {"id": "...", "sport_type": "...", "start_local": "...", "distance": 0, "moving_time": 0, "elevation_gain": 0}
   ```
   Write this array to a temp file, e.g. `/tmp/wrap-my-day-activities.json`. If there were zero activities that day, write `[]` — the script still updates the daily note with a "no training logged" placeholder.

4. **Run the generator script**:
   ```
   python3 .claude/skills/wrap-my-day/scripts/generate_daily_notes.py /tmp/wrap-my-day-activities.json {date} <repo_root>
   ```
   This script:
   - Skips any activity whose training note file already exists (dedup by filename, which embeds the Strava id)
   - Creates a new training note per new activity, following the exact convention documented in `CLAUDE.md` → Vault conventions (YAML frontmatter, hub wikilink)
   - Creates any missing discipline hub note (mapping: Ride/VirtualRide→Rides, Run→Runs, Swim→Swims, WeightTraining→Lifts, Walk→Walks, other→`<Type>s`), linked to `[[athlete-os]]`
   - Creates or updates `daily/{date}.md` with a `## Training` section linking to that day's training notes, and a `[[Daily]]` hub link

5. **Report the result** to the user: how many new activities were logged, how many were already there (skipped as duplicates), and the date. Since `Home.md` embeds live Bases views (`training/Training.base`) and the graph reads directly from the files, both update automatically — no separate step needed.

6. **Commit and push** the new/changed files (`training/*.md`, `daily/*.md`, any new hub notes) with a commit message like `Wrap up {date}: N new training notes`, if this is a git-backed vault and the user hasn't asked to skip committing.

## Notes

- `avg_hr` is left blank on new notes — the same limitation documented in `CLAUDE.md` (Strava's bulk heart-rate values aren't cheaply available). Never fabricate a value.
- This skill only touches `training/` and `daily/` — it does not touch `health/` (that's fed separately once Garmin is connected) or `reviews/`.
- Idempotent: safe to run multiple times on the same day — already-imported activities and already-linked daily-note entries are never duplicated.
