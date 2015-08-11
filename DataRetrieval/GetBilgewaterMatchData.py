__author__ = 'Kishan'

import requests
import os
import json
import urllib
import sys

api_key = ''

https = 'https://'
riot_api = '.api.pvp.net/api/lol/'
match_api = '/v2.2/match/'
timeline = 'true'
rootpath = os.path.split(os.getcwd())[0]
noError = 200
regions = []
matchIds = []

def urlBuilder(region, matchId, timeline, api_key):
    url = https + region + riot_api + region + match_api + matchId + '?includeTimeline=' + timeline + '&api_key=' + api_key
    return url


def getMatchIds():
    matchRegionsJson = []
    matchIds.clear()
    regions.clear()
    path = os.path.join(rootpath, 'MatchData\MatchIDs\BilgewaterMatchIDs')

    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f.title())):
            matchRegionsJson.append(os.path.join(path, f))

    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f.title())):
            regions.append((f[:-5]).lower())

    for r in matchRegionsJson:
        f = open(r)
        matchIds.append(json.load(f))

    return matchIds



def getMatchData(matchId, region):
    url = urlBuilder(region, matchId, timeline, api_key)
    path = os.path.join(rootpath, 'MatchData\BilgewaterMatchData', region.upper(), matchId + '.json')
    if (os.path.isfile(path)):
        return 0
    data = requests.get(url).json()

    if (len(data) < noError):
        return -1


    with open(path, 'w') as outfile:
        json.dump(data, outfile)

    return 1


def main():
    global api_key
    api_key = input('Enter you api-key: ')
    matchIds = getMatchIds()

    progressCounter = 0
    for i in range(len(matchIds)):
        for j in range(len(matchIds[i])):
            status = getMatchData(str(matchIds[i][j]), regions[i])
            if (status == -1):
                print('\nAPI Error')
                return
            progressCounter += 1
            progress = str(10000*i+j+1)
            sys.stdout.write('\rProgress: ' + progress)
            sys.stdout.flush()





if __name__ == '__main__':
    main()
