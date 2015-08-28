__author__ = 'Kishan'

import json
import os
import sys

from FlaskApp.scripts.data_retrieval.match_data import get_match_data
from FlaskApp.scripts.data_retrieval import static_data
from FlaskApp.scripts.data_retrieval.static_data import static_io
from FlaskApp.scripts.data_analytics import data_filter
from FlaskApp.scripts.config import config

regions = get_match_data.get_match_regions()  # Only 'br'

print('\nMinions\n')


def main():
    minions_json = {}

    sys.stdout.write('Creating empty JSON...')
    sys.stdout.flush()
    create_champions_dict(minions_json)
    sys.stdout.write('\rCreating empty JSON...done!\n')
    sys.stdout.flush()

    sys.stdout.write('Populating dict...')
    sys.stdout.flush()
    populate_dict(minions_json)
    sys.stdout.write('\rPopulating dict...done!\n')
    sys.stdout.flush()

    sys.stdout.write('Writing champions JSON...')
    sys.stdout.flush()
    data_filter.write_json(minions_json, 'minions.json')
    sys.stdout.write('done!')
    sys.stdout.flush()


def create_champions_dict(minions_json):
    minions = static_io.read_json('minions_by_id.json')
    upgrades = static_io.read_json('upgrades_by_id.json')
    w = len(regions)
    for r in regions:
        minions_json[r] = {}

        for hast in static_data.highest_achieved_season_tier:
            minions_json[r][hast] = {}
            for minion_id, minion_name in minions.items():
                minions_json[r][hast][minion_id] = \
                    {'name': minion_name, 'won': 0, 'lost': 0}
                for upgrade_id, upgarde_name in upgrades.items():
                    minions_json[r][hast][minion_id][upgrade_id] = \
                        {'name': upgarde_name, 'won': 0, 'lost': 0}


def populate_dict(minions_json):
    minions_and_upgrades = static_io.read_json('minions_by_id.json')
    minions_and_upgrades.update(static_io.read_json('upgrades_by_id.json'))
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
                    minion_bought = ''
                    tier = p['highestAchievedSeasonTier']
                    team_id = p['teamId']
                    for frame in data['timeline']['frames']:
                        if 'events' not in frame:
                            continue
                        for event in frame['events']:
                            if event['eventType'] == 'ITEM_PURCHASED' \
                                    and event['participantId'] == p['participantId'] \
                                    and str(event['itemId']) in minions_and_upgrades:
                                item_id = str(event['itemId'])
                                if minion_bought == '':
                                    if win_team_id == team_id:
                                        minions_json[r][tier][item_id]['won'] += 1
                                    else:
                                        minions_json[r][tier][item_id]['lost'] += 1
                                    minion_bought = item_id
                                else:
                                    if win_team_id == team_id:
                                        minions_json[r][tier][minion_bought][item_id]['won'] += 1
                                    else:
                                        minions_json[r][tier][minion_bought][item_id]['lost'] += 1
            progress_counter -= 1
            data_filter.progress_countdown(progress_counter, r)


if __name__ == '__main__':
    main()
