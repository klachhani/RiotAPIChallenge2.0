__author__ = 'Kishan'

import os
import sys
import data_retrieval
import json
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


riot_api_key = data_retrieval.riot_api_key
pb_api_key = data_retrieval.pushbullet_api_key
data_directory = data_retrieval.data_directory
match_data_directory = data_retrieval.match_data_directory

api_challenge_goal = 'Bilgewater' #APItem
region = 'BR'

match_data_directory = os.path.join(match_data_directory, region)

matches = os.listdir(match_data_directory)[1:100]

x = []
y = []


for minutes in range(1,32):
    print(minutes-1)
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
                for j in range(minutes - 1,minutes):#range(len(data['timeline']['frames'])): #loop through frames
                    frames = data['timeline']['frames']
                    if len(frames) > minutes:
                        for k in frames[j]['participantFrames']: #loop through players
                            pariticpant_k = frames[j]['participantFrames'][str(k)]
                            if 'position' in pariticpant_k: #collect position if the frame has this information
                                x.append(pariticpant_k['position']['x'])
                                y.append(pariticpant_k['position']['y'])


    h = plt.hist2d(x, y, bins=1000 , norm=LogNorm())
    print(len(h[0].tolist()[0]))
    fig = plt.gcf()
    fig.set_size_inches(10,10)
    fig.savefig(str(minutes - 1) + '.png', dpi=300)
    print()
