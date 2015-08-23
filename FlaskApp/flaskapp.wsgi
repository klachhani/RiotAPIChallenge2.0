#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)

sys.path.append('var/www/RiotAPIChallenge2.0/')

from FlaskApp.FlaskApp import app as application
application.secret_key = 'Kishan144'

