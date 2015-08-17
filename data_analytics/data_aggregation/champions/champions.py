__author__ = 'Kishan'

import data_retrieval.match_data.main as matchdata
import data_retrieval
import config.config as config
import requests
import json
import os
import sys

riot_api_key = config.riot_api_key
regions = matchdata.get_match_regions()
highestAchievedSeasonTier = ['CHALLENGER',
                             'MASTER',
                             'DIAMOND',
                             'PLATINUM',
                             'GOLD',
                             'SILVER',
                             'BRONZE',
                             'UNRANKED']


def getchampiondata(region):
    champdata = requests.get('https://global.api.pvp.net/api/lol/static-data/' +
                             region + '/v1.2/champion?&api_key=' + riot_api_key).json()

    champdata = champdata['data']
    return champdata


champions_json = {}
for r in regions:
    champions_json[r] = {}
    champ_data = getchampiondata(r)
    for hast in highestAchievedSeasonTier:
        champions_json[r][hast] = {}
        for key, value in champ_data.items():
            champions_json[r][hast][value['id']] = {'name' : value['name'], 'won' : 0, 'lost' : 0}



match_data_directory = os.path.join(data_retrieval.match_data_directory, 'BR')

matches = os.listdir(match_data_directory)

progress = 0
print()
for m in matches:
    progress += 1
    sys.stdout.write('\r' + str(progress))
    sys.stdout.flush()
    if not m.endswith('json'):
        continue
    else:
        match_data = os.path.join(match_data_directory, m)
        with open(match_data, 'r') as f: #open match file
            data = json.load(f) #load match file as json
            winner = 0
            for t in range(2):
                if data['teams'][t]['winner'] == True:
                    winner = data['teams'][t]['teamId']
            if winner == 0:
                print('winner error')
            for p in range(10):
                tier = data['participants'][p]['highestAchievedSeasonTier']
                champion_id = data['participants'][p]['championId']
                team_id = data['participants'][p]['teamId']
                if winner == team_id:
                    champions_json['br'][tier][champion_id]['won'] += 1
                else:
                    champions_json['br'][tier][champion_id]['lost'] += 1

with open('champions.json', 'w') as outfile:
    json.dump(champions_json, outfile)