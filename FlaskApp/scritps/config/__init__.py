__author__ = 'Kishan'

from FlaskApp.scritps.config import config
import os

print('\nCONFIGURATION\n')

os.chdir(os.path.dirname(__file__))
config.read()

