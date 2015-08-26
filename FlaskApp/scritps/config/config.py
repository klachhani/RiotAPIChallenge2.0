__author__ = 'Kishan'

import ConfigParser


configuration = ConfigParser.ConfigParser()
configfilename = 'config.ini'
configuration.read(configfilename)
overwrite = ''
riot_api_key = ''
pushbullet_api_key = ''
data_directory = ''
match_ids_directory = ''
match_data_directory = ''


def read():
    global riot_api_key, \
        pushbullet_api_key, \
        data_directory, \
        match_ids_directory, \
        match_data_directory

    configuration.read(configfilename)

    riot_api_key = configuration.get('API','riot_api_key', 0)
    pushbullet_api_key = configuration.get('API', 'pushbullet_api_key', 0)
    data_directory = configuration.get('Directories', 'data')
    match_ids_directory = configuration.get('Sub-Directories', 'Match_Ids')
    match_data_directory = configuration.get('Sub-Directories', 'Match_Data')

    print('Riot API Key: ' + riot_api_key)
    print('Pushbullet Access Token: ' + pushbullet_api_key)
    print('Data Directory: ' + data_directory)
    print('Match Ids Sub-Directory: ' + match_ids_directory)
    print('Match Data Sub-Directory: ' + match_data_directory)