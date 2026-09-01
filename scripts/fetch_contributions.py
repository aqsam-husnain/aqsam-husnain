"""
fetch_contributions.py — Scrape GitHub contribution calendar (no API key needed).
Saves contribution data and streak metrics to data/contributions.json.
"""
import json
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

USERNAME = "aqsam-husnain"


def fetch_contribution_data():
    """Scrape the GitHub contribution calendar for the past year."""
    url = f"https://github.com/users/{USERNAME}/contributions"
    print(f"📊 Fetching contributions from {url}...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    days = []
    # GitHub uses <td> elements with data-date and data-level attributes
    for td in soup.select("td.ContributionCalendar-day"):
        date = td.get("data-date")
        level = td.get("data-level", "0")
        
        # Try to extract count from the tooltip or tool-tip element
        count = 0
        tool_tip = td.find("tool-tip") or td.find("span", class_="sr-only")
        if tool_tip:
            text = tool_tip.get_text(strip=True)
            match = re.search(r"(\d+)\s+contribution", text)
            if match:
                count = int(match.group(1))
        
        if date:
            days.append({
                "date": date,
                "count": count,
                "level": int(level)
            })

    # Sort by date
    days.sort(key=lambda d: d["date"])
    return days


def calc_metrics(days):
    """Calculate total, current streak, longest streak, and best day."""
    total = sum(d["count"] for d in days)
    best_day = max(days, key=lambda d: d["count"]) if days else {"date": "N/A", "count": 0}

    # Streaks
    current_streak = 0
    longest_streak = 0
    streak = 0
    today = datetime.utcnow().strftime("%Y-%m-%d")

    # Build a date→count map
    date_map = {d["date"]: d["count"] for d in days}

    # Walk backwards from today
    d = datetime.utcnow()
    while True:
        ds = d.strftime("%Y-%m-%d")
        if date_map.get(ds, 0) > 0:
            current_streak += 1
            d -= timedelta(days=1)
        else:
            break

    # Longest streak scan
    streak = 0
    for day in days:
        if day["count"] > 0:
            streak += 1
            longest_streak = max(longest_streak, streak)
        else:
            streak = 0

    return {
        "total_contributions": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day["date"],
        "best_day_count": best_day["count"],
        "last_updated": datetime.utcnow().isoformat() + "Z"
    }


def main():
    root = Path(__file__).resolve().parent.parent
    data_dir = root / "data"
    data_dir.mkdir(exist_ok=True)

    days = fetch_contribution_data()
    print(f"📅 Found {len(days)} days of contribution data.")

    metrics = calc_metrics(days)
    print(f"🔥 Total: {metrics['total_contributions']} | "
          f"Current Streak: {metrics['current_streak']} | "
          f"Longest Streak: {metrics['longest_streak']} | "
          f"Best Day: {metrics['best_day']} ({metrics['best_day_count']})")

    output = {
        "username": USERNAME,
        "metrics": metrics,
        "days": days
    }

    out_path = data_dir / "contributions.json"
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"✅ Saved {out_path}")


if __name__ == "__main__":
    main()
