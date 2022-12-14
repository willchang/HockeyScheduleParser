#!/usr/local/bin/python3

from html.parser import HTMLParser
import datetime
import urllib.request
import sys

if not __name__ == "__main__":
    sys.exit(1)

if len(sys.argv) != 2:
    print("Usage: ./hockey_schedule_parser.py <output_file>")
    sys.exit(1)

OUTPUT_FILE = sys.argv[1]

# Config
SCHEDULE_URL = "https://truenorthhockey.com/asp_pages/Team.aspx?team_id=21902"
SEASON_YEAR = 2022
IS_SUMMER_SEASON = False
DESC = f"Please update your status so I can coordinate backups.<br><br><b>Beverage Duty:</b> <br><br><a href={SCHEDULE_URL}>View Schedule</a>"

LOCATIONS = {"Rinx": "Rinx Toronto, 65 Orfus Rd, North York, ON M6A 1L7",
             "Ford": "Ford Performance Centre, 400 Kipling Ave, Etobicoke, ON M8V 3L1",
             "Coca": "Coca-Cola Coliseum, 45 Manitoba Dr, Toronto, ON M6K 3C3"}


class Game:
    def __init__(self, date=None, time=None, location=None, home_team=None, away_team=None, desc=None):
        self.date = date
        self.time = time
        self.location = location
        self.home_team = home_team
        self.away_team = away_team
        self.desc = desc


class ScheduleHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.should_start_parsing_table = False
        self.is_parsing_new_row = False
        self.games = []
        self.current_game = None
        self.column_count = 0

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            for attr in attrs:
                if attr[0] == "id" and attr[1] == "ContentPlaceHolder2_GridViewScheduleScore":
                    self.should_start_parsing_table = True
                    break

        if not self.should_start_parsing_table:
            return

        if not self.current_game and tag == "td":
            self.is_parsing_new_row = True
            self.current_game = Game(desc=DESC)

    def handle_endtag(self, tag):
        if tag == "tr" and self.is_parsing_new_row:
            self.is_parsing_new_row = False
            self.games.append(self.current_game)
            self.current_game = None
            self.column_count = 0

    def handle_data(self, data):
        if not self.current_game:
            return

        match self.column_count:
            case 0:
                self.current_game.date = data
            case 1:
                self.current_game.time = data
            case 2:
                self.current_game.location = data
            case 3:
                self.current_game.home_team = data
            case 4:
                self.current_game.away_team = data

        self.column_count += 1


request = urllib.request.urlopen(SCHEDULE_URL)
html_bytes = request.read()
html_string = html_bytes.decode("utf8")
request.close()

parser = ScheduleHTMLParser()
parser.feed(html_string)

# Convert to csv
csv = "Subject,Start Date,Start Time,End Date,End Time,Location,Description"

for game in parser.games:
    if game.location == "Bye Week":
        continue

    csv += "\n"

    date_time_str = f'{game.date} {game.time}'
    start_date = datetime.datetime.strptime(date_time_str, '%b %d %I:%M %p')

    # Adjust year if necessary
    year = SEASON_YEAR
    month = start_date.month
    if not IS_SUMMER_SEASON and 1 <= month and month <= 8:
        year += 1
    start_date = start_date.replace(year=year)

    date_format = "%Y-%m-%d"
    time_format = "%H:%M"

    # Start date strings
    start_date_day_str = start_date.strftime(date_format)
    start_date_time_str = start_date.strftime(time_format)

    # End date strings
    end_date = start_date + datetime.timedelta(hours=1)
    end_date_day_str = end_date.strftime(date_format)
    end_date_time_str = end_date.strftime(time_format)

    location_str = game.location

    for location in LOCATIONS:
        if location_str.startswith(location):
            location_str = LOCATIONS[location]

    csv += f"{game.home_team} vs. {game.away_team} ({game.location}),{start_date_day_str},{start_date_time_str},{end_date_day_str},{end_date_time_str},\"{location_str}\",\"{game.desc}\""

# Write to file
f = open(OUTPUT_FILE, "w")
f.write(csv)
f.close()

print(f'CSV outputted to {OUTPUT_FILE}.')
print()
print("NOTE: Google Calendar cannot detect duplicates from CSVs so delete any rows that you've already added to your calendar!")
