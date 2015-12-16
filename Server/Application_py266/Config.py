# -*- coding: utf-8 -*-

import os
import tempfile

from ConfDBAuth import *

# local confguration for CherryPy
cpconfig = {
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8080,
  'log.access_file':    'logs/access.log',
  'log.error_file':     'logs/error.log',
  'log.screen':         True
}

# base URL of the application on the server (e.g. use "/confdb" for "http://cmsweb.cern.ch/confdb"
base_url = ""

# local directory with read-write access for temporary files
state_dir = tempfile.gettempdir()
if 'STATEDIR' in os.environ:
    state_dir = os.environ.get('STATEDIR')
