from datetime import datetime
from data import get_static_data
import json


def get_most_recent_gameweek():
    gameweeks = get_static_data()['events']
    now = datetime.utcnow()
    for gameweek in gameweeks:
        next_deadline_date = datetime.strptime(gameweek['deadline_time'], '%Y-%m-%dT%H:%M:%SZ')
        if next_deadline_date > now:
            return gameweek['id'] - 1


def generate_filename():
    gw = get_most_recent_gameweek()
    date = str(datetime.now().date()).replace('-', '_')
    filename = f"files/predictions_after_gw{gw}_on_{date}"
    return filename


def save_to_file(data):
    filename = generate_filename() + ".json"
    f = open(filename, "w")
    f.write(json.dumps(data, indent=4))
    f.close()