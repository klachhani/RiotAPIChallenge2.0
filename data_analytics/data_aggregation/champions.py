__author__ = 'Kishan'

from data_retrieval.match_data import get_match_data
from data_retrieval import static_data
from data_retrieval.static_data import io
from data_analytics import data_aggregation
from config import config
import json
import os
import sys

regions = [(get_match_data.get_match_regions())[0]] #Only 'br'

print('\nCHAMPIONS\n')

def main():
    champions_json = {}

    sys.stdout.write('Creating empty JSON...')
    sys.stdout.flush()
    create_champions_dict(champions_json)
    sys.stdout.write('done!\n')
    sys.stdout.flush()


    sys.stdout.write('Populating dict...')
    sys.stdout.flush()
    populate_dict(champions_json)
    sys.stdout.write('\rPopulating dict...done!\n')
    sys.stdout.flush()

    sys.stdout.write('Writing champions JSON...')
    sys.stdout.flush()
    data_aggregation.write_json(champions_json, 'champions.json')
    sys.stdout.write('done!')
    sys.stdout.flush()


def create_champions_dict(dict):
    champion_keys = io.read_json('champions_by_id.json')
    for r in regions:
        dict[r] = {}
        for hast in static_data.highest_achieved_season_tier:
            dict[r][hast] = {}
            for key, value in champion_keys.items():
                dict[r][hast][key] = {'key': value, 'won': 0, 'lost': 0}


def populate_dict(dict):
    for r in regions:
        match_data_directory = os.path.join(config.match_data_directory, r.upper())
        matches = os.listdir(match_data_directory)
        progress_counter = len(matches)
        for m in matches:
            if not m.endswith('json'): continue
            match_data = os.path.join(match_data_directory, m)
            with open(match_data, 'r') as f: #open match file
                data = json.load(f) #load match file as json
                win_team_id = [t['teamId'] for t in data['teams'] if t['winner']][0]
                for p in data['participants']:
                    tier = p['highestAchievedSeasonTier']
                    champion_id = p['championId']
                    team_id = p['teamId']
                    if win_team_id == team_id: dict[r][tier][str(champion_id)]['won'] += 1
                    else: dict[r][tier][str(champion_id)]['lost'] += 1
            progress_counter -= 1
            data_aggregation.progress_countdown(progress_counter, r)


if __name__ == '__main__':
    main()