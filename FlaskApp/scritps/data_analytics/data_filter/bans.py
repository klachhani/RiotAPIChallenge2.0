__author__ = 'Kushil'

import os
import json
import sys
import csv
from FlaskApp.scritps.config import config
import FlaskApp.scritps.data_retrieval.match_data.get_match_data as matchdata
import FlaskApp.scritps.data_retrieval.static_data.get_champion_id as champ_keys

regions = (matchdata.get_match_regions()) #Limit regions?
match_data_directory = config.match_data_directory
matches = os.listdir(os.path.join(match_data_directory, str(regions[0])))
banorder=["first","second","third","fourth","fifth","sixth"]

def main():
    bans_json = {}
    dictcreate(bans_json)
    dictfill(bans_json)
    writedict(bans_json, "test3")
    print("done")

def idlist(): #Creates list of champion id
    id=[]
    for ids in champ_keys.get_champion_key_by_id("br"):
        id.append(int(ids))
    return id

def dictcreate(bans_json): #creates empty dictionary
    bans_json["region"] = {}
    id=idlist()
    for i in regions: #cycles through reigons
        bans_json["region"][str(i)] = {}
        for b in id: #Cycles through champs
            bans_json["region"][str(i)][b] = {"total":0}
            for a in banorder: # puts banorders
                bans_json["region"][str(i)][b][str(a)] = {"win":0,"loss":0,"total":0}

def dictfill(bans_json):
    progress_counter = 0
    for folders in range(0,len(regions)):
        matches = os.listdir(os.path.join(match_data_directory, str(regions[folders])))
        for i in matches:   #loop through file in match data directory
            if i.endswith('json'):  #only consider .json files
                progress_counter += 1
                sys.stdout.write('\rProgress: ' + str(progress_counter) + '/' + str(len(matches)-1))
                sys.stdout.flush()
                matchdata = os.path.join(os.path.join(match_data_directory, str(regions[folders])), i)
                with open(matchdata, 'r') as f: #open match file
                    try:
                        data = json.load(f) #load match file as json
                    except:
                        pass
            for n in range(0,2): #Takes information from data file
                if "bans" in data["teams"][n]: #see if banned champions
                    k=len(data["teams"][n]["bans"]) #Checks how many banned
                    for m in range(0,k): #cycles through bans
                        t=data["teams"][n]["bans"][m]["pickTurn"] -1
                        champid=data["teams"][n]["bans"][m]["championId"]
                        bans_json["region"][regions[folders]][int(champid)]["total"]+= 1
                        bans_json["region"][regions[folders]][int(champid)][banorder[t]]["total"] += 1
                        if data["teams"][n]["winner"] != True :
                            bans_json["region"][regions[folders]][int(champid)][banorder[t]]["loss"]+=1
                        else:
                            bans_json["region"][regions[folders]][int(champid)][banorder[t]]["win"]+=1
                else:
                    print(matchdata) #optional to see what matches bans were not made


def writedict(bans_json,name): #saves jason
    os.chdir(os.path.dirname(__file__))
    with open(name+'.json', 'w')as f:
        json.dump(bans_json,f)


main()


