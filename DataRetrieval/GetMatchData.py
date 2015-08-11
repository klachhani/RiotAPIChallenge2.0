__author__ = 'Kishan'

import requests
import os
import json
import urllib
api_key = ''

url_1 = 'https://euw.api.pvp.net/api/lol/'
url_2 = '/v2.2/match/'
timeline = 'true'
rootpath = os.path.split(os.getcwd())[0]
matchRegions = []
matchIds = []


def urlBuilder(region, matchId, timeline, api_key):
    url = url_1 + region + url_2 + matchId + '?includeTimeline=' + timeline + '&api_key=' + api_key
    print(url)
    return url


def getMatchIds():
    matchRegions.clear()
    path = os.path.join(rootpath, 'MatchData\MatchIDs\BilgewaterMatchIDs')
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f.title())):
            matchRegions.append(os.path.join(path, f))

    for r in matchRegions:
        f = open(r)
        matchIds.append(json.load(f))

    return matchIds


def getMatchData(matchId):
    url = urlBuilder('euw', matchId, timeline, api_key)
    data = requests.get(url).json()
    print(os.path.join(rootpath, 'MatchData', 'BilgewaterMatchData', 'EUW', matchId + '.json'))

    with open(os.path.join(rootpath, 'MatchData', 'BilgewaterMatchData', 'EUW', matchId + '.json'), 'w') as outfile:
        json.dump(data, outfile)


def main():
    global api_key
    api_key = input('Enter you api-key: ')
    getMatchIds()
    getMatchData(str(matchIds[2][0]))


if __name__ == '__main__':
    main()
