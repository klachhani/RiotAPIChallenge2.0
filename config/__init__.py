__author__ = 'Kishan'

import json
import os

config_json = json.load(open(os.path.join
                         (os.path.split(os.path.split
                                        (os.path.dirname(os.path.abspath
                                                         (__file__)))[0])[0], 'config.json')))

riot_api_key = config_json['RiotAPIKey']
pushbullet_api_key = config_json['PushbulletAPIKey']
data_directory = config_json['DataDirectory']