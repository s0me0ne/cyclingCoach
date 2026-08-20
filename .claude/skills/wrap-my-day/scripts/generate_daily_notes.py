import json, os, sys

HUB_MAP = {
    "Ride": "Rides",
    "VirtualRide": "Rides",
    "Run": "Runs",
    "Swim": "Swims",
    "WeightTraining": "Lifts",
    "Walk": "Walks",
    "Workout": "Workouts",
}


def generate(activities_json_path, target_date, repo_root):
    training_dir = os.path.join(repo_root, "training")
    daily_dir = os.path.join(repo_root, "daily")
    os.makedirs(training_dir, exist_ok=True)
    os.makedirs(daily_dir, exist_ok=True)

    activities = json.load(open(activities_json_path))
    activities.sort(key=lambda a: a["start_local"])

    created = []
    all_stems = []
    skipped = 0

    for a in activities:
        aid = a["id"]
        sport = a["sport_type"]
        hub = HUB_MAP.get(sport, sport + "s")
        date = a["start_local"][:10]
        distance_km = round(a["distance"] / 1000, 2)
        duration_min = round(a["moving_time"] / 60, 1)
        vert_m = round(a["elevation_gain"])

        slug = sport.lower()
        fname = f"{date}-{slug}-{aid}.md"
        fpath = os.path.join(training_dir, fname)
        all_stems.append(os.path.splitext(fname)[0])

        if os.path.exists(fpath):
            skipped += 1
            continue

        content = f"""---
date: {date}
type: {sport}
distance_km: {distance_km}
duration_min: {duration_min}
vert_m: {vert_m}
avg_hr:
strava_id: {aid}
---

# {sport} — {date}

- Distance: {distance_km} km
- Duration: {duration_min} min
- Elevation: {vert_m} m D+

## Links
[[{hub}]]
"""
        with open(fpath, "w") as f:
            f.write(content)

        hub_path = os.path.join(training_dir, f"{hub}.md")
        if not os.path.exists(hub_path):
            with open(hub_path, "w") as f:
                f.write(f"""---
type: hub
---

# {hub}

Hub note for all {hub.lower()} training notes. Individual sessions link back here.

## Links
[[athlete-os]]
""")

        created.append({"file": fname, "sport": sport, "distance_km": distance_km})

    # Update or create the daily note (link every training note for the day, new or pre-existing)
    daily_path = os.path.join(daily_dir, f"{target_date}.md")
    stems = all_stems

    if os.path.exists(daily_path):
        existing = open(daily_path).read()
        new_links = [f"- [[{s}]]" for s in stems if f"[[{s}]]" not in existing]
        if new_links:
            if "## Training" in existing:
                existing = existing.replace(
                    "## Training\n", "## Training\n" + "\n".join(new_links) + "\n", 1
                )
            else:
                existing += "\n## Training\n" + "\n".join(new_links) + "\n"
            with open(daily_path, "w") as f:
                f.write(existing)
    else:
        links_block = "\n".join(f"- [[{s}]]" for s in stems) if stems else "_No training logged today._"
        content = f"""---
date: {target_date}
type: daily
---

# {target_date}

## Training
{links_block}

## Links
[[Daily]]
"""
        with open(daily_path, "w") as f:
            f.write(content)

    return {"created": len(created), "skipped": skipped, "date": target_date, "daily_note": daily_path}


if __name__ == "__main__":
    activities_json_path, target_date, repo_root = sys.argv[1], sys.argv[2], sys.argv[3]
    result = generate(activities_json_path, target_date, repo_root)
    print(json.dumps(result))
