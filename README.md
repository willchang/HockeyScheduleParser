# HockeyScheduleParser

Script to parse hockey schedule into a CSV, specifically for
https://truenorthhockey.com.

## Usage

1. (Optional) Go to a team page on True North Hockey's website. In
   `hockey_schedule_parser.py`, update `SCHEDULE_URL` with this new URL.
2. (Optional) Update other parameters in the config if necessary (e.g. `SEASON_YEAR`, `IS_SUMMER_SEASON`, etc.).
3. Run `./hockey_schedule_parser.py`.
4. Copy and paste the CSV output to a file and import that file to your calendar app.