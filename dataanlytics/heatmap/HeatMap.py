__author__ = 'Kishan'

import dataretrieval
import os
import json
import sys
from pylab import *
from matplotlib.colors import LogNorm
import csv
import numpy as np

riot_api_key = dataretrieval.riot_api_key
pb_api_key = dataretrieval.pushbullet_api_key
data_directory = dataretrieval.data_directory
match_data_directory = dataretrieval.match_data_directory

api_challenge_goal = 'Bilgewater' #APItem
region = 'BR'

match_data_directory = os.path.join(match_data_directory, api_challenge_goal + 'MatchData')
match_data_directory = os.path.join(match_data_directory, region)

matches = os.listdir(match_data_directory)

x = []
y = []
minutes = 0

progress_counter = 0
for i in matches: #loop through file in match data directory
    if i.endswith('json'): #only consider .json files
        progress_counter += 1
        sys.stdout.write('\rProgress: ' + str(progress_counter) + '/' + str(len(matches)-1))
        sys.stdout.flush()
        matchdata = os.path.join(match_data_directory, i)
        with open(matchdata, 'r') as f: #open match file
            try:
                data = json.load(f) #load match file as json
            except:
                print('\n' + i + '\n') #print json file if error and skip this file
                continue
            for j in range(len(data['timeline']['frames'])):#range(0,minutes):# #loop through frames
                frames = data['timeline']['frames']
                if len(frames) > minutes:
                    for k in range(6,11):#frames[j]['participantFrames']: #loop through players
                        pariticpant_k = frames[j]['participantFrames'][str(k)]
                        if 'position' in pariticpant_k: #collect position if the frame has this information
                            x.append(pariticpant_k['position']['x'])
                            y.append(pariticpant_k['position']['y'])


h = hist2d(x, y, bins=2000,norm=LogNorm())
show()