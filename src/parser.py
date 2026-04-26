import json
from datetime import datetime
from .utils import DATA_FILE

def getClasses(venues=None, minDate=None, maxDate=None, sortByTime=True):
    """
    Filter classes by venues and date range.
    """
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        timetable_data = json.load(f)

    if minDate is None:
        minDate = datetime.now().date()

    filtered_classes = []
    for class_entry in timetable_data:
        class_date_str = class_entry.get("DATESTAMP_ISO")
        if not class_date_str:
            continue

        try:
            class_date = datetime.fromisoformat(class_date_str).date()
            if class_date < minDate:
                continue
            if maxDate is not None and class_date > maxDate:
                continue
            if venues is not None and class_entry.get("ROOM", "") not in venues:
                continue
            filtered_classes.append(class_entry)
        except ValueError:
            continue

    seen_classes = set()
    deduplicated_classes = []
    for class_entry in filtered_classes:
        key = (
            class_entry.get("ROOM", ""),
            class_entry.get("DATESTAMP_ISO", ""),
            class_entry.get("TIME_FROM_ISO", ""),
            class_entry.get("MODULE_NAME", "")
        )
        if key not in seen_classes:
            seen_classes.add(key)
            deduplicated_classes.append(class_entry)

    if sortByTime:
        deduplicated_classes.sort(key=lambda x: x.get("TIME_FROM_ISO", ""))

    return deduplicated_classes

def getCurrentAndFutureClasses():
    return getClasses()

def filterClassesByVenue(venue_list):
    return getClasses(venues=venue_list if venue_list else None)

def getClassesByVenueAndDate(venue_name, target_date=None):
    if target_date is None:
        target_date = datetime.now().date()
    return getClasses(venues=[venue_name], minDate=target_date, maxDate=target_date)

if __name__ == "__main__":
    from datetime import timedelta

    venue_name = "Auditorium 4 @ Level 3"
    target_date = datetime.now().date() + timedelta(days=1)

    venue_classes = getClassesByVenueAndDate(venue_name, target_date)

    print(f"Classes at {venue_name} on {target_date}:")
    print(f"Total: {len(venue_classes)}\n")

    if venue_classes:
        for cls in venue_classes:
            time_from = cls.get("TIME_FROM", "")
            time_to = cls.get("TIME_TO", "")
            module_name = cls.get("MODULE_NAME", "")
            lecturer = cls.get("NAME", "")
            print(f"  {time_from} - {time_to}: {module_name}")
            print(f"    Lecturer: {lecturer}\n")
    else:
        print("  No classes scheduled for this venue on that date")

