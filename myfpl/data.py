import requests
from bs4 import BeautifulSoup
import json
import re
import codecs
import pandas as pd
import time

TEAM_INDEX = {
    1: 'Arsenal',
    2: 'Aston_Villa',
    3: 'Brentford',
    4: 'Brighton',
    5: 'Burnley',
    6: 'Chelsea',
    7: 'Crystal_Palace',
    8: 'Everton',
    9: 'Leicester',
    10: 'Leeds',
    11: 'Liverpool',
    12: 'Manchester_City',
    13: 'Manchester_United',
    14: 'Newcastle_United',
    15: 'Norwich',
    16: 'Southampton',
    17: 'Tottenham',
    18: 'Watford',
    19: 'West_Ham',
    20: 'Wolverhampton_Wanderers',
}

TEAM_ID_INDEX = dict(zip(TEAM_INDEX.values(), TEAM_INDEX.keys()))


def get_data(url):
    response = requests.get(url)
    html = (response.text)
    parsed_html = BeautifulSoup(html, 'html.parser')
    scripts = parsed_html.findAll('script')
    filtered_scripts = []
    for script in scripts:
        if len(script.contents) > 0:
            filtered_scripts += [script]
    return scripts


def get_epl_data():
    scripts = get_data("https://understat.com/league/EPL/2021")
    teamData = {}
    playerData = {}
    for script in scripts:
        for c in script.contents:
            split_data = c.split('=')
            data = split_data[0].strip()
            if data == 'var teamsData':
                content = re.findall(r'JSON\.parse\(\'(.*)\'\)', split_data[1])
                decoded_content = codecs.escape_decode(content[0], "hex")[0].decode('utf-8')
                teamData = json.loads(decoded_content)
            elif data == 'var playersData':
                content = re.findall(r'JSON\.parse\(\'(.*)\'\)', split_data[1])
                decoded_content = codecs.escape_decode(content[0], "hex")[0].decode('utf-8')
                playerData = json.loads(decoded_content)
    return teamData, playerData


def get_all_team_data():
    teamData, playerData = get_epl_data()

    new_team_data = []
    for t, v in teamData.items():
        new_team_data += [v]
    final_data = {}
    for data in new_team_data:
        team_frame = pd.DataFrame.from_records(data["history"])
        team = data["title"].replace(' ', '_')
        final_data[team] = team_frame
    return final_data


def get_fixtures_data():
    """ Retrieve the fixtures data for the season
    """
    url = "https://fantasy.premierleague.com/api/fixtures/"
    response = ''
    while response == '':
        try:
            response = requests.get(url)
        except:
            time.sleep(5)
    if response.status_code != 200:
        raise Exception("Response was code " + str(response.status_code))
    data = json.loads(response.text)
    fixtures_df = pd.DataFrame.from_records(data)

    return fixtures_df


def get_static_data():
    """ Retrieve the fpl player data from the hard-coded url
    """
    response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
    if response.status_code != 200:
        raise Exception("Response was code " + str(response.status_code))
    data = json.loads(response.content)
    return data