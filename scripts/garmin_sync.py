import os
import sys
import datetime
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

import garminconnect

REPO_ROOT = os.path.join(os.path.dirname(__file__), "..")
HEALTH_DIR = os.path.join(REPO_ROOT, "health")


def fmt(value, suffix=""):
    """Return the value formatted for YAML frontmatter, or blank if missing."""
    if value is None:
        return ""
    return f"{value}{suffix}"


def sync(target_date):
    email = os.environ.get("GARMIN_EMAIL")
    password = os.environ.get("GARMIN_PASSWORD")
    if not email or not password:
        print("ERROR: GARMIN_EMAIL / GARMIN_PASSWORD not set in .env")
        sys.exit(1)

    client = garminconnect.Garmin(email, password)
    client.login()

    stats = client.get_stats(target_date) or {}
    resting_hr = stats.get("restingHeartRate")
    bb_high = stats.get("bodyBatteryHighestValue")
    bb_low = stats.get("bodyBatteryLowestValue")

    sleep_hours = None
    try:
        sleep = client.get_sleep_data(target_date) or {}
        daily = sleep.get("dailySleepDTO", {})
        seconds = daily.get("sleepTimeSeconds")
        if seconds:
            sleep_hours = round(seconds / 3600, 1)
    except Exception:
        pass

    hrv_value = None
    try:
        hrv = client.get_hrv_data(target_date) or {}
        summary = hrv.get("hrvSummary", {})
        hrv_value = summary.get("lastNightAvg")
    except Exception:
        pass

    os.makedirs(HEALTH_DIR, exist_ok=True)
    fpath = os.path.join(HEALTH_DIR, f"{target_date}-health.md")

    content = f"""---
date: {target_date}
type: health
resting_hr: {fmt(resting_hr)}
sleep_hours: {fmt(sleep_hours)}
hrv: {fmt(hrv_value)}
body_battery_high: {fmt(bb_high)}
body_battery_low: {fmt(bb_low)}
---

# Health — {target_date}

- Resting HR: {fmt(resting_hr, ' bpm') or '_not available_'}
- Sleep: {fmt(sleep_hours, ' h') or '_not available_'}
- HRV: {fmt(hrv_value, ' ms') or '_not available_'}
- Body Battery: {fmt(bb_high) or '?'} / {fmt(bb_low) or '?'}

## Links
[[Health]]
"""
    with open(fpath, "w") as f:
        f.write(content)

    print(f"Wrote {fpath}")
    print(f"  Resting HR: {resting_hr}, Sleep: {sleep_hours}h, HRV: {hrv_value}, Body Battery: {bb_high}/{bb_low}")


if __name__ == "__main__":
    date_arg = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
    sync(date_arg)
