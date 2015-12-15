#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
if len(sys.argv) < 2:
    sys.exit(0)

arg = sys.argv[1]
if ':' in arg:
    db, name = arg.split(':')
    if db in ('orcoff', 'adg'):
        online = True
    else:
        online = False
else:
    name = arg
    online = False

# Load configuration
from Config import *
from Config.ConfDBAuth.ConfDBAuth import ConnectionString
connectionString = ConnectionString()

# Register the SQLAlchemy plugin
from sqlalchemy_plugin.saengine import SAEngine
engine = SAEngine(connectionString)
engine.start()
session = None

from utils import *
#cnfMap = UniqueMapping()

import logging
# create console handler and set level to debug
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter("[%(asctime)s] %(name)s: %(message)s")
# add formatter to console
console.setFormatter(formatter)
# create logger
logger = logging.getLogger("converter.py")
logger.setLevel(logging.DEBUG)
# add console to logger
logger.addHandler(console)

if online:
    session = engine.bind_online()
else:
    session = engine.bind_offline()

from converter.converter import Converter
converter = Converter()

from confdb_queries.confdb_queries import ConfDbQueries
queries = ConfDbQueries()
ver = queries.getConfigurationByName(name, session, logger)
cnf = -1

import os
workdir = os.getcwd()
config_file_name = converter.createConfig(ver, cnf, session, online, workdir, use_cherrypy = False)

