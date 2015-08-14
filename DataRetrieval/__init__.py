__author__ = 'Kishan'

import config as configpackage
import config.config as config
import os

os.chdir(configpackage.config_file_path)

config.set_up()

riot_api_key = config.riot_api_key
pushbullet_api_key = config.pushbullet_api_key
data_directory = config.data_directory
match_ids_subdirectory = config.match_ids_subdirectory
match_data_directory = config.match_data_directory


api_challenge_goal = input('\nData retrieval for which api challenge goal? '
                           'Enter "1" for Bilgewater. '
                           'Etner "2" for APItem: ')

if api_challenge_goal == '1':
    api_challenge_goal = 'Bilgewater'
elif api_challenge_goal == '2':
    api_challenge_goal = 'APItem'
else:
    print('Invalid entry. Bilgewater selected by default')
    api_challenge_goal = 'Bilgewater'


match_data_directory = os.path.join(match_data_directory, api_challenge_goal + 'MatchData')
match_id_directory = os.path.join(match_ids_subdirectory, api_challenge_goal + 'MatchIds')
