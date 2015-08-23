__author__ = 'Kishan'

import os
from config import config
print('\nCONFIGURATION\n')

os.chdir(os.path.dirname(__file__))
config.set_up()

