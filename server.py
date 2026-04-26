from flask import Flask, render_template, request, redirect, url_for
from parser import getClasses
from fetcher import refreshTimetables
from utils import ALL_AUDITORIUMS_LABEL, get_week_dates, load_venue_list, parse_date
from schedule import build_timeline_blocks

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    if request.args.get("refresh"):
        selected_venue = request.args.get("venue")
        selected_date = request.args.get("date")
        refreshTimetables()
        if selected_venue and selected_date:
            return redirect(url_for("index", venue=selected_venue, date=selected_date))
        if selected_venue:
            return redirect(url_for("index", venue=selected_venue))
        return redirect(url_for("index"))

    venues = load_venue_list()
    if not venues:
        return "No venues found in timetable.json", 500

    selected_venue = request.args.get("venue", venues[0])
    if request.args.get("all_auditoriums"):
        selected_venue = ALL_AUDITORIUMS_LABEL

    week_dates = get_week_dates()
    default_date = week_dates[0]
    selected_date = parse_date(request.args.get("date")) or default_date
    if selected_date not in week_dates:
        selected_date = default_date

    schedule_rows = []
    if selected_venue != ALL_AUDITORIUMS_LABEL:
        schedule_classes = getClasses(
            venues=[selected_venue],
            minDate=selected_date,
            maxDate=selected_date,
            sortByTime=True,
        )
        schedule_rows.append({
            "venue": selected_venue,
            "blocks": build_timeline_blocks(schedule_classes)
        })
    else:
        auditorium_list = [v for v in venues if v != ALL_AUDITORIUMS_LABEL and "auditorium" in v.lower()]
        for auditorium in auditorium_list:
            row_classes = getClasses(
                venues=[auditorium],
                minDate=selected_date,
                maxDate=selected_date,
                sortByTime=True,
            )
            schedule_rows.append({
                "venue": auditorium,
                "blocks": build_timeline_blocks(row_classes)
            })

    total_blocks = sum(len(row["blocks"]) for row in schedule_rows)

    return render_template(
        "index.html",
        venues=venues,
        selectedVenue=selected_venue,
        weekDates=week_dates,
        selectedDate=selected_date,
        schedule=schedule_rows,
        total_blocks=total_blocks,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
