__author__ = 'Kishan'

import requests
import os

url_1 = 'https://euw.api.pvp.net/api/lol/'
url_2 = '/v2.2/match/'
api_key = '22bc9503-0705-4bfd-afbe-43f3c2fdaadf'
rootpath = os.path.split(os.getcwd())[0]
matchIds = []

def urlBuilder(url_1, region, url_2, matchId, timeline, api_key):
    url = url_1 + region + url_2 + matchId + '?includeTimeline=' + timeline + '&api_key' + api_key

def getMatchIds():
    matchIds.clear()
    path = os.path.join(rootpath,'MatchData\MatchIDs\BilgewaterMatchIDs')
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f.title())):
            matchIds.append(f)
    


def main():
    getMatchIds()


if __name__ == '__main__':
    main()
