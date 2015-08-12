__author__ = 'Kishan'

import json
import os

apikeys_json = json.load(open(os.path.join
                         (os.path.split(os.path.split
                                        (os.path.dirname(os.path.abspath
                                                         (__file__)))[0])[0], 'apikeys.json')))

riot_api_key = apikeys_json['RiotAPIKey']
pushbullet_api_key = apikeys_json['PushbulletAPIKey']

print('\nRiot API Key: ' + riot_api_key +
      '\nPushbullet API Key: ' + pushbullet_api_key + '\n')
