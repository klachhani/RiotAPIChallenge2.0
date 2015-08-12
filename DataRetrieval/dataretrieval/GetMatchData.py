__author__ = 'Kishan'

import requests
import os
import json
import sys
import time

rootpath = os.path.split(os.getcwd())[0]
error = 1
regions = []
matchIds = []
matchIdDirectory = 'MatchIDs/BilgewaterMatchIDs'
matchDataDirectory = 'BilgewaterMatchData'

matchDataFolder = r'E:\Google Drive\RiotAPIChallenge2.0\MatchData'



def urlBuilder(region, matchId, api_key):
    https = 'https://'
    riot_api = '.api.pvp.net/api/lol/'
    match_api = '/v2.2/match/'
    timeline = 'true'

    url = https + region + riot_api + region + match_api + matchId + '?includeTimeline=' + timeline + '&api_key=' + api_key
    return url


def getMatchIds():
    matchRegionsJson = []
    matchIds.clear()
    regions.clear()
    path = os.path.join(matchDataFolder, matchIdDirectory)

    for f in os.listdir(path):
        if f.endswith('.json'):
            if os.path.isfile(os.path.join(path, f.title())):
                matchRegionsJson.append(os.path.join(path, f))

    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f.title())):
            regions.append((f[:-5]).lower())

    for r in matchRegionsJson:
        f = open(r)
        matchIds.append(json.load(f))

    return matchIds



def getMatchData(matchId, region, api_key):
    url = urlBuilder(region, matchId, api_key)
    path = os.path.join(matchDataFolder, matchDataDirectory, region.upper(), matchId + '.json')
    if (os.path.isfile(path)):
        return 0
    data = requests.get(url).json()
    time.sleep(0.8)

    if len(data) == error:
        print()
        print(data)
        return -1

    with open(path, 'w') as outfile:
        json.dump(data, outfile)

    return 1


def main():

    api_key = input('Enter you api-key: ')
    matchIds = getMatchIds()

    progressCounter = 10000
    for i in range(len(matchIds)):
        for j in range(len(matchIds[i])):
            status = getMatchData(str(matchIds[i][j]), regions[i], api_key)
            if (status == -1):
                print('\nAPI Error')
                return
            progressCounter -= 1
            sys.stdout.write('\rProgress Countdown: ' + regions[i].upper() + ' ' +  str(progressCounter))
            sys.stdout.flush()






if __name__ == '__main__':
    main()
