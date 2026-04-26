import json
import os
from datetime import datetime, timedelta

DATA_FILE = os.path.join(os.path.dirname(__file__), "timetable.json")
ALL_AUDITORIUMS_LABEL = "All Auditoriums"


def load_timetable():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_venue_list():
    timetable_data = load_timetable()
    all_venues = sorted(
        {entry.get("ROOM", "") for entry in timetable_data if entry.get("ROOM")},
        key=lambda item: (0 if "auditorium" in item.lower() else 1, item)
    )
    return [ALL_AUDITORIUMS_LABEL] + all_venues


def get_week_dates():
    today = datetime.now().date()
    if today.weekday() >= 5:
        monday = today + timedelta(days=(7 - today.weekday()))
    else:
        monday = today - timedelta(days=today.weekday())
    return [monday + timedelta(days=i) for i in range(7)]


def parse_date(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).date()
    except ValueError:
        return None
