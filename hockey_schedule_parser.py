#!/usr/bin/python3

from html.parser import HTMLParser
import datetime
import urllib.request
import sys

if not __name__ == "__main__":
    sys.exit(1)

SCHEDULE_URL = "https://truenorthhockey.com/asp_pages/Team.aspx?team_id=21902"


class Game:
    def __init__(self, date=None, time=None, location=None, home_team=None, away_team=None):
        self.date = date
        self.time = time
        self.location = location
        self.home_team = home_team
        self.away_team = away_team


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
            self.current_game = Game()

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
csv = "Subject,Start Date,Start Time,End Date,End Time,Location"

for game in parser.games:
    if game.location == "Bye Week":
        continue

    csv += "\n"

    date_time_str = f'{game.date} {game.time}'
    date_time_obj = datetime.datetime.strptime(date_time_str, '%b %d %I:%M %p')

    end_date = date_time_obj + datetime.timedelta(hours=1)
    end_date_day_str = end_date.strftime("%b %d")
    end_date_time_str = end_date.strftime("%I:%M %p")

    csv += f"{game.home_team} vs. {game.away_team},{game.date},{game.time},{end_date_day_str},{end_date_time_str},{game.location}"

print("NOTE: Google Calendar cannot detect duplicates from CSVs so delete any rows that you've already added!\n\nHere is your CSV:\n\n")
print(csv)
