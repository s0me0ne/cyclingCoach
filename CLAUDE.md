# Athlete OS — Brain

This vault is Ricardo Marques's Athlete OS: training data, reviews, races, and health, connected in Obsidian as a visual command center.

## Who this is for
See [[athlete-profile]] for full details. Summary: cycling-focused (also runs and lifts), 3-4 years of serious training, ~7.6 h/week average load, targeting two centuries in Sep/Oct 2026.

## Coaching style
Data-driven. Lead with numbers (power, HR, load, trend). Keep commentary short — no fluff, no hype.

## Upcoming races
- 13 Sep 2026 — 100 km, 2600 m D+
- 4 Oct 2026 — 140 km, 1800 m D+

Full details in [[Races]] and individual race notes.

## Zones
Heart-rate and power zones live in [[athlete-profile]] — use them whenever discussing intensity or session targets. HR zones are Strava's MaxHR-based estimate; power zones are Strava-set from FTP 240W.

## Vault conventions
Every future note in this vault follows this structure:

**Folders** — one per domain: `training/` (dated sessions), `reviews/`, `races/`, `health/`.

**Property block** — every note opens with a YAML frontmatter block. Training notes use:
```yaml
date: YYYY-MM-DD
type: Ride | Run | Swim | WeightTraining | Walk | VirtualRide | ...
distance_km: <number>
duration_min: <number>
vert_m: <number>
avg_hr: <number or blank if unavailable>
strava_id: <activity id, for dedup>
```
Race notes use `type: race`, `date`, `distance_km`, `vert_m`, `status`. Hub notes use `type: hub`. Never invent a numeric value — leave the field blank if the source data doesn't have it.

**Hub links** — every dated/leaf note ends with a `## Links` section wikilinking to its discipline hub (e.g. `[[Rides]]`, `[[Runs]]`, `[[Swims]]`, `[[Lifts]]`, `[[Walks]]`, `[[Races]]`). Each hub note itself links to `[[athlete-os]]`, so the graph clusters by discipline with `athlete-os` as the center. See the wikilink rule below for the general version of this.

**Filenames** — dated notes use `YYYY-MM-DD-<type>-<id>.md` (id = Strava activity id where applicable) so re-imports can detect and skip duplicates by checking if the file already exists.

**Wikilink rule** — every new note must link to at least one existing note (a hub, `athlete-os`, or a related note). No orphan notes — this is what keeps the graph connected as the vault grows.
