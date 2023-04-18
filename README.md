# HockeyScheduleParser

Script to parse hockey schedule into a CSV, specifically for
https://truenorthhockey.com team pages.

## Requirements

* Python 3.10+

## Usage

1. Go to a team page on True North Hockey's website. In
   `hockey_schedule_parser.py`, update `SCHEDULE_URL` with this new URL. Note
   that this will work only for team pages and not playoff pages.
2. (Optional) Update other parameters in the config if necessary (e.g.
   `SEASON_YEAR`, `IS_SUMMER_SEASON`, etc.).
3. Run `./hockey_schedule_parser.py` and provide an output file.
4. Import your CSV into your calendar app.
