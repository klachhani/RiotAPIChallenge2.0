__author__ = 'Kishan'

class Config():
    import configparser
    import config
    import os

    configuration = configparser.ConfigParser()
    configfilename = 'config.ini'
    configuration.read(configfilename)
    overwrite = ''
    riot_api_key = ''
    pushbullet_api_key = ''
    data_directory = ''
    match_ids_subdirectory = ''
    match_data_directory = ''

    def read(self):
        self.configuration.read(self.configfilename)

        self.riot_api_key = self.configuration['API']['riot_api_key']
        self.pushbullet_api_key = self.configuration['API']['pushbullet_api_key']
        self.data_directory = self.configuration['Directories']['data']
        self.match_ids_subdirectory = self.configuration['Sub-Directories']['Match_Ids']
        self.match_data_directory = self.configuration['Sub-Directories']['Match_Data']

        print()
        print('Riot API Key: ' + self.riot_api_key)
        print('Pushbullet Access Token: ' + self.pushbullet_api_key)
        print('Data Directory: ' + self.data_directory)
        print('Match Ids Sub-Directory: ' + self.match_ids_subdirectory)
        print('Match Data Sub-Directory: ' + self.match_data_directory)
        print()

    def confirm(self):
        if self.overwrite.lower() == 'y':
            self.read()
            proceed = input('Confirmation - Is this correct (y/n)?\t')
            if proceed.lower() == 'n':
                self.overwrite_config()


    def set_up(self):
        self.read()
        try:
            with open(self.configfilename, 'x') as configfile:
                self.read().configuration.write(configfile)
        except FileExistsError as e:
            self.overwrite = input('Overwrite existing config file (y/n])?\t')
            if self.overwrite.lower() == 'y':
                self.overwrite_config()

    def overwrite_config(self):
        riot_api_key = input('Enter your Riot API key here: ')
        pushbullet_api_key = input('Enter your Pushbullet API key here: ')
        data_directory = input('Enter the directory containing the data here: ')
        match_ids_subdirectory = input('Enter the match ids sub-directory here: ')
        match_data_directory = input('Enter the match data sub-directory here: ')

        self.configuration['API'] = {'Riot_API_Key': riot_api_key, 'Pushbullet_API_Key' : pushbullet_api_key}
        self.configuration['Directories'] = {'Data' : data_directory}
        self.configuration['Sub-Directories'] = {'Match_Ids' : match_ids_subdirectory, 'Match_Data': match_data_directory}

        with open(self.configfilename, 'w') as configfile:
            self.configuration.write(configfile)

        self.confirm()






