__author__ = 'Kushil'
import os
import json
import sys
import requests

r = requests.get('https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion?dataById=True&api_key=094064d6-f3b5-40f5-b201-daf52c9225fb')
data1=r.json()

api_challenge_goal = 'Bilgewater' #APItem
region = 'BR'

match_data_directory = r'C:\Users\Kushil\PycharmProjects\RiotAPIChallenge2.0\dataanlytics'

json_data = open(r'C:\Users\Kushil\PycharmProjects\RiotAPIChallenge2.0\dataanlytics\test1.json')
data2 = json.load(json_data)

names=[]
for keys in data1["data"].keys():
        names.append(keys)

reigon={}
reigon["BR"]={}
reigon["BR"]["champions"]={}

print(names)

for i in range(0,len(names)):
    reigon["BR"]["champions"][names[i]]={"name":"name","first":0,"second":0,"third":0,"fourth":0,"fifth":0,"sixth":0,"Total":0,}

with open('test2.json', 'w')as f:
   json.dump(reigon,f)