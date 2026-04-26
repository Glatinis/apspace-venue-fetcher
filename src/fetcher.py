import json
import requests
from .utils import DATA_FILE

URL = "https://s3-ap-southeast-1.amazonaws.com/open-ws/weektimetable"

def fetchTimetables():
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    print(f"Error: Unable to fetch data. Status code: {response.status_code}")
    return None

def refreshTimetables():
    data = fetchTimetables()
    if data is not None:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print("Data saved to timetable.json")
    else:
        print("Failed to fetch data")
