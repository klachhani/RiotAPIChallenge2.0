__author__ = 'Kushil'

import os
import json
import sys
import csv
import config.config as config

region = 'BR'

match_data_directory = config.match_data_directory

print(match_data_directory)
match_data_directory = os.path.join(match_data_directory, region)
print(match_data_directory)
matches = os.listdir(match_data_directory)

#initalising dictionary
bans = {}
bans["first"] = {}
bans["second"] = {}
bans["third"] = {}
bans["fourth"] = {}
bans["fifth"] = {}
bans["sixth"] = {}

#initialising variables
first = []
second = []
third = []
fourth = []
fifth = []
sixth = []

minutes = 0

progress_counter = 0
for i in matches:   #loop through file in match data directory
    if i.endswith('json'):  #only consider .json files
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
            try:
                first.append(int(data["teams"][0]["bans"][0]["championId"]))
                second.append(int(data["teams"][1]["bans"][0]["championId"]))
                third.append(int(data["teams"][0]["bans"][1]["championId"]))
                fourth.append(int(data["teams"][1]["bans"][1]["championId"]))
                fifth.append(int(data["teams"][0]["bans"][2]["championId"]))
                sixth.append(int(data["teams"][1]["bans"][2]["championId"]))
            except:
                pass


def dictcreate(bannumber,name):
    for i in range(0,len(bannumber)):
        bans[name][bannumber[i]]=0

    return bans[str(name)]

def dictfill(bannumber,name):
    for key in bannumber:
        bans[name][key] +=1

def listcreate(bannumber):
    banlist=[]
    for keys in bans[bannumber].keys():
        banlist.append([keys,bans[bannumber][keys]])
    return banlist

dictcreate(first,"first")
dictfill(first,"first")
dictcreate(second,"second")
dictfill(second,"second")
dictcreate(third,"third")
dictfill(third,"third")
dictcreate(fourth,"fourth")
dictfill(fourth,"fourth")
dictcreate(fifth,"fifth")
dictfill(fifth,"fifth")
dictcreate(sixth,"sixth")
dictfill(sixth,"sixth")

with open('test1.json', 'w')as f:
   json.dump(bans,f)
