# HockeyScheduleParser

Script to parse hockey schedule into a CSV, specifically for
https://truenorthhockey.com team pages.

## Requirements

- Python 3.10+

## Usage

1. Update `SCHEDULE_URL`, `SEASON_YEAR`, and `IS_SUMMER_SEASON` in
   `hockey_schedule_parser.py`.
    - `SCHEDULE_URL` (string): This is the team page on True North Hockey's website. Note
   that this will work only for team pages and not playoff pages.
    - `SEASON_YEAR` (int): The year the season is starting in.
    - `IS_SUMMER_SEASON` (bool): Whether the season is a summer season or not.
1. Run `./hockey_schedule_parser.py` and provide an output file.
1. Import your CSV into your calendar app.
