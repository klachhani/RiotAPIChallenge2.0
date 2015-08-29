__author__ = 'Kishan'

import json
import os
import sys

from FlaskApp.scripts.data_retrieval import static_data
from FlaskApp.scripts.data_retrieval.static_data import static_io
from FlaskApp.scripts.data_analytics import data_filter
from FlaskApp.scripts.config import config

regions = static_data.regions

stat_titles = ['kills',
               'assists',
               'deaths',
               'physicalDamageDealtToChampions',
               'magicDamageDealtToChampions',
               'trueDamageDealtToChampions',
               'minionsKilled',
               'goldEarned',
               'wardsPlaced']

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
    data_filter.write_json(champions_json, 'champions.json')
    sys.stdout.write('done!')
    sys.stdout.flush()


def create_champions_dict(dict):
    champion_keys = static_io.read_json('champions_by_id.json')
    for r in regions:
        dict[r] = {}
        for hast in static_data.highest_achieved_season_tier:
            dict[r][hast] = {}
            for key, value in champion_keys.items():
                dict[r][hast][key] = {'won': {}, 'lost': {}}
                for outcome, stats  in dict[r][hast][key].items():
                    stats = dict[r][hast][key][outcome]
                    stats['picks'] = 0
                    stats['matchDuration'] = 0
                    for t in stat_titles:
                        stats[t] = 0
                        stats[t + '-per5min'] = 0


def populate_dict(dict):
    for r in regions:
        match_data_directory = os.path.join(config.match_data_directory, r.upper())
        matches = os.listdir(match_data_directory)
        progress_counter = len(matches)
        for m in matches:
            if not m.endswith('json'):
                continue
            match_data = os.path.join(match_data_directory, m)
            with open(match_data, 'r') as f:  # open match file
                data = json.load(f)  # load match file as json
                win_team_id = [t['teamId'] for t in data['teams'] if t['winner']][0]
                for p in data['participants']:
                    tier = p['highestAchievedSeasonTier']
                    champion_id = p['championId']
                    team_id = p['teamId']
                    if win_team_id == team_id:
                        stats = dict[r][tier][str(champion_id)]['won']
                        stats['picks'] += 1
                        stats['matchDuration'] += data['matchDuration']
                        for t in stat_titles:
                            stats[t] += p['stats'][t]
                    else:
                        stats = dict[r][tier][str(champion_id)]['lost']
                        stats['matchDuration'] += data['matchDuration']
                        stats['picks'] += 1
                        for t in stat_titles:
                            stats[t] += p['stats'][t]
            progress_counter -= 1
            data_filter.progress_countdown(progress_counter, r)


if __name__ == '__main__':
    main()
