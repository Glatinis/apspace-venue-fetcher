from datetime import datetime


def parse_datetime(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def format_minutes(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"


def percent_position(start_min):
    return max(0.0, min(100.0, ((start_min - 8 * 60) / (10 * 60)) * 100))


def percent_width(start_min, end_min):
    width = ((end_min - start_min) / (10 * 60)) * 100
    return max(1.0, min(100.0, width))


def build_timeline_blocks(classes):
    if not classes:
        return [
            {
                "type": "free",
                "start_short": "10:00",
                "end_short": "16:00",
                "left": 33.33,
                "width": 40.0,
                "module": "Free window",
                "lecturer": ""
            }
        ]

    parsed = []
    for entry in classes:
        start_dt = parse_datetime(entry.get("TIME_FROM_ISO"))
        end_dt = parse_datetime(entry.get("TIME_TO_ISO"))
        if not start_dt or not end_dt or end_dt <= start_dt:
            continue
        parsed.append({
            "entry": entry,
            "start": start_dt,
            "end": end_dt,
            "start_min": start_dt.hour * 60 + start_dt.minute,
            "end_min": end_dt.hour * 60 + end_dt.minute,
        })

    parsed.sort(key=lambda item: item["start_min"])
    blocks = []
    cursor = 8 * 60

    def add_free_block(start_min, end_min):
        start_min = max(start_min, 10 * 60)
        end_min = min(end_min, 16 * 60)
        if end_min - start_min < 45:
            return
        blocks.append({
            "type": "free",
            "start_short": format_minutes(start_min),
            "end_short": format_minutes(end_min),
            "left": percent_position(start_min),
            "width": percent_width(start_min, end_min),
            "module": "Free window",
            "lecturer": ""
        })

    for item in parsed:
        if item["start_min"] - cursor >= 45:
            add_free_block(cursor, item["start_min"])
        blocks.append({
            "type": "class",
            "start_short": format_minutes(item["start_min"]),
            "end_short": format_minutes(item["end_min"]),
            "left": percent_position(item["start_min"]),
            "width": percent_width(item["start_min"], item["end_min"]),
            "module": item["entry"].get("MODULE_NAME", "Unnamed class"),
            "lecturer": item["entry"].get("NAME", "Unknown")
        })
        cursor = max(cursor, item["end_min"])

    if cursor < 16 * 60:
        add_free_block(cursor, 16 * 60)

    return blocks
