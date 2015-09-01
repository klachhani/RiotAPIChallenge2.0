__author__ = 'Kishan'

from FlaskApp.scripts.config import config
import os

# change directory to current file where config.ini should be found and read config
os.chdir(os.path.dirname(__file__))
config.read()
