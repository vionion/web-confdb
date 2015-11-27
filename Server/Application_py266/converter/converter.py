# File converter.py Description:
#
# Class: Converter

from confdb_queries.confdb_queries import ConfDbQueries
from item_wrappers.FolderItem import *
from item_wrappers.ModuleDetails import *
from item_wrappers.Pathitem import *
from item_wrappers.Parameter import *
from item_wrappers.item_wrappers import *
from schemas.responseSchemas import *
from responses.responses import *
from marshmallow import Schema, fields, pprint
#from ordereddict import OrderedDict
from marshmallow.ordereddict import OrderedDict
from data_builder import DataBuilder
import string
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from multiprocessing import Process, Pipe

import os
import os.path
current_dir_log = os.path.dirname(os.path.abspath(__file__))

class Converter(object):

    data_builder = DataBuilder()
    queries = ConfDbQueries()

    def createConfig(self, ver=-2, cnf=-2, db = None, online="False", log=None, counter=None, current_dir=""):

        version = None
        release = None
        try:
            version = self.data_builder.getRequestedVersion(ver, cnf, db)
        except Exception as e:
            msg = 'ERROR: Query getRequestedVersion Error: ' + e.args[0]
            log.error(msg)

        if version == None:
            print "\nCould Not Find The Requested Version.\n"
            return

        try:
            release = self.queries.getRelease(version.id_release, db, log)
        except Exception as e:
            msg = 'ERROR: Query getRelease Error: ' + e.args[0]
            log.error(msg)

        # Adding Modules of All Paths - Second Process
        parent_conn, child_conn = Pipe()
        proc = Process(target =self.writePathsModules, args=(version.id , version.id_release, child_conn, online))
        proc.start()

        #Adding File's Headers
        header = self.writeHeader(version.name, release.releasetag, version.processname)#version.config)

        #Adding Global Psets
        gpsets = self.data_builder.getGlobalPsets(version.id, db, log)

        # Adding Streams
        streams = 'process.streams = cms.PSet(\n' + self.data_builder.getStreams(version.id, db)

        # Adding Datasets
        datasets = 'process.datasets = cms.PSet(\n' + self.data_builder.getDatasetsPaths(version.id, db)

        # Adding ED-Sources
        edSources = self.data_builder.getEDSources(version.id, version.id_release, db)

        # Adding ES-Sources
        esSources = self.data_builder.getESSource(version.id, version.id_release, db, log)

        # Adding ES-Modules
        esModules = self.data_builder.getESModules(version.id, version.id_release, db, log)

        # Adding Services
        services = self.data_builder.getServices(version.id, version.id_release, db, log)

        # Adding Modules of All End Paths
        endPathModules = self.data_builder.getOutputModules(version.id, version.id_release, db, log)

        # Adding Sequences
        sequences = self.data_builder.getSequences(version.id, version.id_release, db, log)

        # Adding Paths
        paths = self.data_builder.getPaths(version.id, version.id_release, db, log)

        # Adding End Paths
        endPaths = self.data_builder.getEndPaths(version.id, version.id_release, db, log)

        # Adding Scheduler
        schedule = self.data_builder.getSchedule()

        modules = parent_conn.recv()
        proc.join()

        # Combining All Information
        data = header + gpsets + streams + datasets + edSources + esSources + esModules + services + modules + endPathModules + sequences + paths + endPaths + schedule

        try:
            id_file = str(counter.getNext())
           # file_name = 'exported/Config' + id_file + '.py'
           # file_name = '/data/srv/HG1509j-comp4/apps/confdb/Application_py266/exported/Config'        + id_file + '.py'
            folder = ''
            if os.environ.get('STATEDIR') is None:
                log.error('STATEDIR IS NULL')
            else:
                folder = os.environ.get('STATEDIR')
            # folder = os.environ['STATEDIR']
            file_name = folder + '/Config' + id_file + '.py'
            #file_name = current_dir + '/exported/Config' + id_file + '.py'
            log.error('STATE FOLDER DIRECTORY LOGGED----------------------------')
            log.error(folder)
            log.error('CURRENT DIRECTORY LOGGED----------------------------')
            log.error(current_dir_log)
            log.error('FILENAME LOGGED----------------------------')
            log.error(file_name)
            file = open(file_name,'w')
            file.write(data)
            file.close()
            fn_temp = 'Config' + id_file
            return fn_temp
        except Exception as e:
            msg = 'ERROR: Writting to file Error: ' + str(e.args[0])
            log.error(msg)
            return None

    def writeHeader(self, version_name, release_tag, process_name):
        result = "# " + version_name + " (" + release_tag + ")" + "\n\n"
        result = result + 'import FWCore.ParameterSet.Config as cms\n\n'
        result = result + 'process = cms.Process( "' + process_name + '" )\n\n'
        result = result + 'process.HLTConfigVersion = cms.PSet(\n'
        result = result + self.data_builder.getTab(2) + "tableName = cms.string('" + version_name + "')\n)\n\n"

        return result

    def writePathsModules(self, version_id, version_rel, child_conn, online="False"):
        from Config import *
        from sqlalchemy.ext.automap import automap_base
        from confdb_tables.confdb_tables import *

        connectionString = ConnectionString()
        engine = None

        if online == 'True':
            engine = create_engine(connectionString.connectUrlonline)

        else:
            engine = create_engine(connectionString.connectUrloffline)

        Base.prepare(engine, reflect=True)
        session = scoped_session(sessionmaker(engine))

        data = self.data_builder.getModules(version_id, version_rel, session)

        child_conn.send(data)
        child_conn.close()

        session.close()
        engine.dispose()
