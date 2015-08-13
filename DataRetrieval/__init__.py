__author__ = 'Kishan'

import config as configpackage
import config.config as config
import os

os.chdir(configpackage.config_file_path)

c = config.Config()
c.set_up()

riot_api_key = c.riot_api_key
pushbullet_api_key = c.pushbullet_api_key
data_directory = c.data_directory
match_ids_subdirectory = c.match_ids_subdirectory
match_data_directory = c.match_data_directory