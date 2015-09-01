__author__ = 'Kishan'

import ConfigParser

configuration = ConfigParser.ConfigParser()
configfilename = 'config.ini'
configuration.read(configfilename)
overwrite = ''
riot_api_key = ''
data_directory = ''
match_ids_directory = ''
match_data_directory = ''


# read config info from config.ini file
def read():
    global riot_api_key, \
        data_directory, \
        match_ids_directory, \
        match_data_directory

    configuration.read(configfilename)

    riot_api_key = configuration.get('API', 'riot_api_key', 0)
    data_directory = configuration.get('Directories', 'data')
    match_ids_directory = configuration.get('Sub-Directories', 'Match_Ids')
    match_data_directory = configuration.get('Sub-Directories', 'Match_Data')
