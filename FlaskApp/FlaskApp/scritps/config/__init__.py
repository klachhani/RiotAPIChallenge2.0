__author__ = 'Kishan'

import os

from FlaskApp.FlaskApp.scritps.config import config

print('\nCONFIGURATION\n')

os.chdir(os.path.dirname(__file__))
config.set_up()

