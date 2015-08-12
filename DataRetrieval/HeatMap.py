__author__ = 'Kishan'

import json
import csv


f = open('577776113.json')
data = json.load(f)

pos = []

for i in range(len(data['timeline']['frames'])):
    p = []
    for j in range(1,2):
        x = data['timeline']['frames'][i]['participantFrames'][str(j)]['position']['x']
        y = data['timeline']['frames'][i]['participantFrames'][str(j)]['position']['y']
        p.append(x)
        p.append(y)
    pos.append(p)
print(pos)

with open('some.csv', 'wt', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(pos)