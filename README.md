# APSPACE Venue Fetcher

A Flask web application that displays venue schedules and free times visually for APSPACE venues.

## Features

- Fetch and display class schedules for various venues
- Visual timeline showing class and free time blocks
- Select specific venues or view all auditoriums
- Choose dates within the current/upcoming week
- Refresh timetable data from the source

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Glatinis/apspace-venue-fetcher.git
   cd apspace-venue-fetcher
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser to `http://localhost:5000`

## Usage

- Select a venue from the dropdown or choose "All Auditoriums"
- Pick a date from the current week
- Click "Refresh" to update the timetable data
- View the visual timeline and detailed schedule list

## Project Structure

- `app.py`: Flask application and routes
- `src/`: Main application package
  - `fetcher.py`: Handles fetching timetable data from the API
  - `parser.py`: Parses and filters class data
  - `utils.py`: Utility functions for data loading and date handling
  - `schedule.py`: Builds timeline blocks for visualization
  - `templates/index.html`: HTML template for the web interface
  - `static/style.css`: CSS styles for the timeline and layout
  - `timetable.json`: Cached timetable data

## Requirements

- Python 3.8+
- Flask
- requests

## License

MIT License
