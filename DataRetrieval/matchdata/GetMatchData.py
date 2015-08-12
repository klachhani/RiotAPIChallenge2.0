__author__ = 'Kishan'

import requests
import os
import json
import sys
from pushbullet import PushBullet
import time

rootpath = os.path.split(os.getcwd())[0]
error = 1
regions = []
matchIds = []
matchIdDirectory = 'MatchIDs/BilgewaterMatchIDs'
matchDataDirectory = 'BilgewaterMatchData'
apiMaxRetryAttempts = 15
riot_api_key = ''
pb_api_key = ''
progressThisSesson = int
start = time
end = time

matchDataFolder = r'E:\Google Drive\RiotAPIChallenge2.0\MatchData'



def urlBuilder(region, matchId, riot_api_key):
    https = 'https://'
    riot_api = '.api.pvp.net/api/lol/'
    match_api = '/v2.2/match/'
    timeline = 'true'

    url = https + region + riot_api + region + match_api + matchId + \
          '?includeTimeline=' + timeline + '&api_key=' + riot_api_key
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



def getMatchData(matchId, region, progressCounter):
    global end
    global progressThisSesson
    url = urlBuilder(region, matchId, riot_api_key)
    path = os.path.join(matchDataFolder, matchDataDirectory, region.upper(), matchId + '.json')
    if (os.path.isfile(path)):
        return 0

    status_code_not_ok = bool
    retry_counter = 0
    while status_code_not_ok:
        data = requests.request('GET', url)
        retry_counter += 1
        if data.ok == False:
            status_code_not_ok = True
            sys.stdout.write('\rProgress Countdown: ' + region.upper() + ' ' +
                             str(progressCounter) + '\t\t' + 'Http status code: ' +
                             str(data.status_code) + '\tRetry attempt...' +
                             str(retry_counter) + '/' + str(apiMaxRetryAttempts))
            sys.stdout.flush()
            if retry_counter == apiMaxRetryAttempts:
                end = time.clock()
                thisSessionMesg = 'This session: ' + str(progressThisSesson) + ' Matches retrieved in %.2f' % (end-start) + ' seconds'
                if pb_api_key != '':
                    pb = PushBullet(pb_api_key)
                    pb.push_note('Riot API Data Retrieval', 'Data Retrieval Aborted, ' +
                                 str(progressCounter) + ' remaining.\n' + thisSessionMesg)

                print( '...Aborting')
                print(thisSessionMesg)
                return -1
        else:
            data = data.json()
            status_code_not_ok = False
            if retry_counter > 1:
                print()


    #time.sleep(0.8)

    with open(path, 'w') as outfile:
        progressThisSesson += 1
        json.dump(data, outfile)


def main():

    global riot_api_key
    global pb_api_key
    global progressThisSesson
    global start
    riot_api_key = input('Enter your Riot api-key: ')
    pb_api_key = input('Enter your Pushbullet api-key (optional): ')

    start = time.clock()
    progressThisSesson = 0
    matchIds = getMatchIds()


    for i in range(len(matchIds)):
        progressCounter = len(matchIds[i])
        for j in range(len(matchIds[i])):
            status = getMatchData(str(matchIds[i][j]), regions[i], progressCounter)
            if (status == -1):
                return
            progressCounter -= 1
            sys.stdout.write('\rProgress Countdown: ' + regions[i].upper() +
                             ' ' +  str(progressCounter))
            sys.stdout.flush()






if __name__ == '__main__':
    main()
