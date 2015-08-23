__author__ = 'Kishan'

import configparser
import FlaskApp.FlaskApp.scritps.config
import os

configuration = configparser.ConfigParser()
configfilename = 'config.ini'
configuration.read(configfilename)
overwrite = ''
riot_api_key = ''
pushbullet_api_key = ''
data_directory = ''
match_ids_directory = ''
match_data_directory = ''


def set_up():
    if not os.path.isfile(configfilename):
        overwrite = 'y'
        write_config()
    else:
        read()

    try:
        with open(configfilename, 'x') as configfile:
            read().configuration.write(configfile)
    except FileExistsError as e:
        overwrite = input('Overwrite existing config file (y/n])?\t')
        if overwrite.lower() == 'y':
            write_config()


def read():
    global riot_api_key, \
        pushbullet_api_key, \
        data_directory, \
        match_ids_directory, \
        match_data_directory

    configuration.read(configfilename)

    riot_api_key = configuration['API']['riot_api_key']
    pushbullet_api_key = configuration['API']['pushbullet_api_key']
    data_directory = configuration['Directories']['data']
    match_ids_directory = configuration['Sub-Directories']['Match_Ids']
    match_data_directory = configuration['Sub-Directories']['Match_Data']

    print()
    print('Riot API Key: ' + riot_api_key)
    print('Pushbullet Access Token: ' + pushbullet_api_key)
    print('Data Directory: ' + data_directory)
    print('Match Ids Sub-Directory: ' + match_ids_directory)
    print('Match Data Sub-Directory: ' + match_data_directory)
    print()


def confirm():
    if overwrite.lower() == 'y':
        read()
        proceed = input('Confirmation - Is this correct (y/n)?\t')
        if proceed.lower() == 'n':
            write_config()


def write_config():
    riot_api_key = input('Enter your Riot API key here: ')
    pushbullet_api_key = input('Enter your Pushbullet API key here: ')
    data_directory = input('Enter the directory containing the data here: ')
    match_ids_subdirectory = input('Enter the Bilgewater match ids sub-directory here: ')
    match_data_directory = input('Enter the Bilgewater match data sub-directory here: ')

    configuration['API'] = {'Riot_API_Key': riot_api_key, 'Pushbullet_API_Key': pushbullet_api_key}
    configuration['Directories'] = {'Data': data_directory}
    configuration['Sub-Directories'] = {
        'Match_Ids': match_ids_subdirectory, 'Match_Data': match_data_directory
        }

    with open(configfilename, 'w') as configfile:
        configuration.write(configfile)

    confirm()
