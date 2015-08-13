__author__ = 'Kishan'

import dataretrieval
import os
import json
import sys

riot_api_key = dataretrieval.riot_api_key
pb_api_key = dataretrieval.pushbullet_api_key
data_directory = dataretrieval.data_directory
match_data_directory = dataretrieval.match_data_directory
print(match_data_directory)

api_challenge_goal = 'Bilgewater' #APItem
region = 'BR'

match_data_directory = os.path.join(match_data_directory, api_challenge_goal + 'MatchData')
match_data_directory = os.path.join(match_data_directory, region)

matches = os.listdir(match_data_directory)

xmax = float('-inf')
xmin= float('inf')
ymax = float('-inf')
ymin = float('inf')

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
            for j in range(len(data['timeline']['frames'])):
                for k in data['timeline']['frames'][j]['participantFrames']:
                    pariticpant_k = data['timeline']['frames'][j]['participantFrames'][k]
                    if 'position' in pariticpant_k: #collect position if the frame has this information
                        xmax = max(xmax, float(pariticpant_k['position']['x']))
                        xmin = min(xmin, float(pariticpant_k['position']['x']))
                        ymax = max(ymax, float(pariticpant_k['position']['y']))
                        ymin = min(ymin, float(pariticpant_k['position']['y']))

print('\n' + str(int(xmin)) + ' ' + str(int(xmax)) + '\n' + str(int(ymin)) + ' ' + str(int(ymax)))



#    with open(matchdata, 'r') as myfile:
#        text = myfile.read()
#    print(text[163900:163950])