__author__ = 'Kishan'


import dataretrieval.matchdata
import requests
import os
import json
import sys
from pushbullet import PushBullet
import time

riot_api_key = dataretrieval.matchdata.riot_api_key
pb_api_key = dataretrieval.matchdata.pushbullet_api_key
matchDataFolder = r'E:\Google Drive\RiotAPIChallenge2.0\MatchData'

error = 1
regions = []
matchIds = []
matchIdDirectory = 'MatchIDs/BilgewaterMatchIDs'
matchDataDirectory = 'BilgewaterMatchData'
apiMaxRetryAttempts = 15
progressThisSession = int
start = time
end = time


def main():

    global progressThisSession
    global start

    start = time.clock()
    progressThisSession = 0
    match_ids = get_match_ids()

    for i in range(len(match_ids)):
        progress_counter = len(match_ids[i])
        for j in range(len(match_ids[i])):
            status = get_match_data(str(match_ids[i][j]), regions[i], progress_counter)
            if status == -1:
                return
            progress_counter -= 1
            sys.stdout.write('\rProgress Countdown: ' + regions[i].upper() +
                             ' ' +  str(progress_counter))
            sys.stdout.flush()


def url_builder(region, match_id, riot_api_key):
    https = 'https://'
    riot_api = '.api.pvp.net/api/lol/'
    match_api = '/v2.2/match/'
    timeline = 'true'

    url = https + region + riot_api + region + match_api + match_id + \
          '?includeTimeline=' + timeline + '&api_key=' + riot_api_key
    return url


def get_match_ids():
    match_regions_json = []
    matchIds.clear()
    regions.clear()
    path = os.path.join(matchDataFolder, matchIdDirectory)

    for f in os.listdir(path):
        if f.endswith('.json'):
            if os.path.isfile(os.path.join(path, f.title())):
                match_regions_json.append(os.path.join(path, f))

    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f.title())):
            regions.append((f[:-5]).lower())

    for r in match_regions_json:
        f = open(r)
        matchIds.append(json.load(f))

    return matchIds


def get_match_data(match_id, region, progress_counter):

    global end
    global progressThisSession
    url = url_builder(region, match_id, riot_api_key)
    path = os.path.join(matchDataFolder, matchDataDirectory, region.upper(), match_id + '.json')
    if os.path.isfile(path):
        return 0

    status_code_not_ok = bool
    retry_counter = 0
    while status_code_not_ok:
        try:
            data = requests.request('GET', url)
        except ConnectionError:
            retry_counter += 1
            print('ConnectionError')
            continue
        retry_counter += 1
        if not data.ok:
            status_code_not_ok = True
            sys.stdout.write('\rProgress Countdown: ' + region.upper() + ' ' +
                             str(progress_counter) + '\t\t' + 'Http status code: ' +
                             str(data.status_code) + '\tRetry attempt...' +
                             str(retry_counter) + '/' + str(apiMaxRetryAttempts))
            sys.stdout.flush()
            if retry_counter == apiMaxRetryAttempts:
                end = time.clock()
                this_session_Message = 'This session: ' + str(progressThisSession) + ' Matches retrieved in %.2f' % (end-start) + ' seconds'
                if pb_api_key != '':
                    pb = PushBullet(pb_api_key)
                    pb.push_note('Riot API Data Retrieval', 'Data Retrieval Aborted, ' +
                                 str(progress_counter) + ' remaining for ' + region.upper()
                                 + '.\n' + this_session_Message)

                print( '...Aborting')
                print(this_session_Message)
                return -1
        else:
            data = data.json()
            status_code_not_ok = False


    #time.sleep(0.8)

    with open(path, 'w') as outfile:
        progressThisSession += 1
        json.dump(data, outfile)


if __name__ == '__main__':
    main()
