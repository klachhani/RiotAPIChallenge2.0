__author__ = 'Kishan'

from FlaskApp.scripts.config import config
import os

os.chdir(os.path.dirname(__file__))
config.read()

