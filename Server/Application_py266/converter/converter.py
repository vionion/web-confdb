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
from data_builder import DataBuilder
import multiprocessing
import logging


class Converter(object):

    queries = ConfDbQueries()

    def __init__(self, threads = 4):
        self. threads = threads

    def createConfig(self, ver=-2, cnf=-2, db = None, online = "False", filename = "", use_cherrypy = False):

        if use_cherrypy:
            import cherrypy
            self.logger = cherrypy.log

            # implement part of the logging interface in cherrypy logger
            def log(self, lvl, msg, *args, **kwargs):
                if args:
                    msg = msg % args
                if kwargs and 'exc_info' in kwargs and kwargs['exc_info']:
                    traceback = True
                else:
                    traceback=False
                self.error(msg, '', lvl, traceback)

            def debug(self, msg, *args, **kwargs):
                self.log(logging.DEBUG, msg, *args, **kwargs)

            def info(self, msg, *args, **kwargs):
                self.log(logging.INFO, msg, *args, **kwargs)

            def warning(self, msg, *args, **kwargs):
                self.log(logging.WARNING, msg, *args, **kwargs)

            def critical(self, msg, *args, **kwargs):
                self.log(logging.CRITICAL, msg, *args, **kwargs)

            import types
            self.logger.log      = types.MethodType(log,      self.logger)
            self.logger.debug    = types.MethodType(debug,    self.logger)
            self.logger.info     = types.MethodType(info,     self.logger)
            self.logger.warning  = types.MethodType(warning,  self.logger)
            self.logger.critical = types.MethodType(critical, self.logger)

        else:
            formatter = logging.Formatter("[%(asctime)s - %(levelname)s/%(processName)s] %(name)s: %(message)s")
            handler   = logging.StreamHandler()
            handler.setFormatter(formatter)
            self.logger = multiprocessing.get_logger()
            self.logger.setLevel(logging.INFO)
            self.logger.addHandler(handler)

        version = None
        release = None
        try:
            version = DataBuilder.getRequestedVersion(ver, cnf, db)
        except Exception as e:
            msg = 'ERROR: Query getRequestedVersion Error: ' + e.args[0]
            self.logger.error(msg)

        if version == None:
            print "\nCould Not Find The Requested Version.\n"
            return

        self.data_builder = DataBuilder(db, version, self.logger)

        try:
            release = self.queries.getRelease(version.id_release, db, self.logger)
        except Exception as e:
            msg = 'ERROR: Query getRelease Error: ' + e.args[0]
            self.logger.error(msg)

        # Adding File's Headers
        self.logger.info('retrieving header...')
        header = self.writeHeader(version.name, release.releasetag, version.processname)#version.config)
        self.logger.info('done')

        tasks = [
            ('paths',          'getPaths'),
            ('modules',        'getModules'),
            ('sequences',      'getSequences'),
            ('datasets',       'getDatasetsPaths'),
            ('psets',          'getGlobalPsets'),
            ('streams',        'getStreams'),
            ('source',         'getEDSources'),
            ('esproducers',    'getESModules'),
            ('essources',      'getESSource'),
            ('services',       'getServices'),
            ('outputmodules',  'getOutputModules'),
            ('endpaths',       'getEndPaths'),
            ('schedule',       'getSchedule'),
        ]

        # build each part of the configuration
        parts = {}
        import task

        if self.threads == 1:
            # single threaded version
            import itertools
            task.initialize(online, version, use_cherrypy)
            for key, val in itertools.imap(task.worker, tasks):
                parts[key] = val
        else:
            # multiprocess version
            pool = multiprocessing.Pool(processes = self.threads, initializer = task.initialize, initargs = (online, version, use_cherrypy))
            for key, val in pool.imap_unordered(task.worker, tasks):
                parts[key] = val
            pool.close()
            pool.join()

        # combinine all parts
        data = \
            header + \
            parts['psets'] + \
            parts['streams'] + \
            parts['datasets'] + \
            parts['source'] + \
            parts['essources'] + \
            parts['esproducers'] + \
            parts['services'] + \
            parts['modules'] + \
            parts['outputmodules'] + \
            parts['sequences'] + \
            parts['paths'] + \
            parts['endpaths'] + \
            parts['schedule']

        try:
            file = open(filename,'w')
            file.write(data)
            file.close()
            return True
        except Exception as e:
            msg = 'ERROR: Writting to file %s: %s' % (filename, e.args[0])
            self.logger.error(msg)
            return False


    def writeHeader(self, version_name, release_tag, process_name):
        result = "# " + version_name + " (" + release_tag + ")" + "\n\n"
        result = result + 'import FWCore.ParameterSet.Config as cms\n\n'
        result = result + 'process = cms.Process( "' + process_name + '" )\n\n'
        result = result + 'process.HLTConfigVersion = cms.PSet(\n'
        result = result + self.data_builder.getTab(2) + "tableName = cms.string('" + version_name + "')\n)\n\n"

        return result

