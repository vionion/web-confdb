# File Main.py Description:
# This file is the entry point of the Server side application.
# It contains the method to instantiate the and starts the server
# as well the Database session
# Class: Root


# -*- coding: utf-8 -*-
import cherrypy
import glob

from cherrypy.lib.static import serve_file
from sqlalchemy import *
from sqlalchemy.orm import *
from cherrypy import _cplogging, _cpconfig, _cplogging, _cprequest, _cpwsgi, tools 

#from sqlalchemy.sql import select
#from sqlalchemy.sql import text
#from sqlalchemy import Sequence
from operator import attrgetter
#from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
 #AddressUser #Module,
import json
#from schema import * #PathsSchema, ModuleSchema, ResponseSchema, ParameterSchema, ResponseParamsSchema, ResponsePathsSchema, ResponsePathTreeSchema, PathsTreeSchema, PathsItemSchema, ResponsePathItemsSchema, ResponsePathItemSchema, ResponseParamSchema, ParameterSchema
from collections import OrderedDict
from utils import * #Counter, ModulesDict, SequencesDict, PathsDict

#NEW IMPORT
from exposed.exposed import *
from sqlalchemy_plugin.saplugin import *

#from saplugin import Version, Pathidconf, Pathids, Paths, Response, Parameter, ResponseTree, Pathitems, Pathitem, Pathelement, ResponseTreeItem, Modelement, Parameter, Moduleitem, ModTelement, ModToTemp, ModTemplate, Directory, Configuration, FolderItem, Moduletypes, ModuleDetails

import sys
import logging 
import logging.handlers

#Set logging handlers for the first time
from conflogger import logconfig

from confdb_queries.cachedb_queries import CacheDbQueries

import os.path
current_dir = os.path.dirname(os.path.abspath(__file__))

#logging params
LOG_DIR = 'logs'
ACCESS_LOG_FILENAME = 'accessLog.log'
ERROR_LOG_FILENAME = 'errorLog.log'
#metadata = MetaData()    
    
class Root(object):
    
    #----------- OFFLINE DB ---------
    idgen = Counter()
    idstrgen = StreamItemCounter()
    idsumgen = SummaryItemCounter()
    
    cnfMap = ConfigsDict()
    folMap = FoldersDict()
    
    patsMap = PathsDict()
    seqsMap = SequencesDict()
    modsMap = ModulesDict()
    oumodsMap = OutputModulesDict()
    allmodsMap = AllModulesDict()
    
    srvsMap = ServicesDict()
    
    strMap = StreamsDict()
    datMap = DatasetsDict()
    evcMap = EvcoDict()
    
    gpsMap = GpsetsDict()
    
    sumMap = SummaryitemsDict()
    
    #----------- ONLINE DB ---------
    idgen_online = Counter()
    idstrgen_online = StreamItemCounter()
    idsumgen_online = SummaryItemCounter()
    
    cnfMap_online = ConfigsDict()
    folMap_online = FoldersDict()
    
    patsMap_online = PathsDict()
    seqsMap_online = SequencesDict()
    modsMap_online = ModulesDict()
    oumodsMap_online = OutputModulesDict()
    allmodsMap_online = AllModulesDict()
    
    srvsMap_online = ServicesDict()
    
    strMap_online = StreamsDict()
    datMap_online = DatasetsDict()
    evcMap_online = EvcoDict()
    
    gpsMap_online = GpsetsDict()
    
    sumMap_online = SummaryitemsDict()
    
    #---- General purpose ---------
    idfolgen = FolderItemCounter()
    funcs = Exposed()
    cache_queries = CacheDbQueries()
    
    log = cherrypy.log
    
    #def __init__(self):
    #    self.types = dict()
    #    db = cherrypy.request.db
    #    for row in db.query(Paetypes).all():
    #        self.types[row.id] = row.name    
    _cp_config = {'tools.staticdir.on' : True,
#                  'tools.staticdir.root': current_dir,
                  'tools.staticdir.dir' : '/Users/vdaponte/Dropbox/CmsConfigExplorer',#'/Users/vdaponte/Dropbox/Demo110315',  #'/Users/vdaponte/Dropbox/LockedGrid',# #'Demo110315', #ModParams #
                  'tools.staticdir.index' : 'index.html'
    }

    @cherrypy.expose
    def index(self):
        # Get the SQLAlchemy session associated
        # with this request.
        # It'll be released once the request
        # processing terminates
        
#        db = cherrypy.request.db
        
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        return "Hello World"
    
    #Get a the list of items in a path 
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allpathitems(self, _dc=101, ver=-2, cnf=-2,node=1, itype="",online="False",filter=""):
        
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        patsMap = None
        seqsMap = None
        modsMap = None
        idgen = None
        cnfMap = None
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            patsMap = self.patsMap_online
            seqsMap = self.seqsMap_online
            modsMap = self.modsMap_online
            idgen = self.idgen_online
            cnfMap = self.cnfMap_online
            
        else:
            db = db_offline
            patsMap = self.patsMap
            seqsMap = self.seqsMap
            modsMap = self.modsMap
            idgen = self.idgen
            cnfMap = self.cnfMap
            
        data = None
        node = int(node)
        ver = int(ver)
        cnf = int(cnf)     

        #Pathitems request
        if(itype == 'pat'):
            data = self.funcs.getPathItems(patsMap, seqsMap, modsMap, idgen, node, ver, db, self.log)
        
        else:
            data = self.funcs.getPaths(patsMap, cnfMap, idgen, cnf, ver, db, self.log)
        
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allpathitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Path and its sequences/modules")
    
        return data
    
    #Get a the list of items in a path 
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def pathdetails(self, _dc=101, ver=-2, cnf=-2,node=1, pid=-2,online="False"):
        
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        patsMap = None
        cnfMap = None
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            patsMap = self.patsMap_online
            cnfMap = self.cnfMap_online
            
        else:
            db = db_offline
            patsMap = self.patsMap
            cnfMap = self.cnfMap
    
        data = None
        node = int(node)
        pid = int(pid)
        ver = int(ver)
        cnf = int(cnf)        
        
        print "CNF BEFORE: ",cnf
        
        if(cnf != -2):
            cnf=cnfMap.get(cnf)
        
        id_pid = patsMap.get(pid)
        
        print "PID: ", str(pid), " ID_PID: ",id_pid, "CNF: ",cnf
        
        #Path details request
        data = self.funcs.getPathDetails(id_pid, cnf, ver, db, self.log)
        
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: pathdetails - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Path details")
    
        return data
    
    #Get a the list of items in a path 
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allmoditems(self, _dc=101, length=1, node=1, mid=-2, pid=-2, epit = "", allmod="false",online="False",verid=-2):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        modsMap = None
        oumodsMap = None
        allmodsMap = None
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            modsMap = self.modsMap_online
            oumodsMap = self.oumodsMap_online
            allmodsMap = self.allmodsMap_online
            
        else:
            db = db_offline
            modsMap = self.modsMap
            oumodsMap = self.oumodsMap
            allmodsMap = self.allmodsMap
        
        pid = int(pid)
        mid = int(mid)
        
        data = None
        
        if(epit == "oum"):
            id_oum = oumodsMap.get(mid)
            data = self.funcs.getOUModuleItems(id_oum, db, self.log)
        
        else:
            if (allmod == 'true'):
                id_p = allmodsMap.get(mid)        
                data = self.funcs.getModuleItems(id_p, db, self.log)
            else:
                id_p = modsMap.get(mid)        
                data = self.funcs.getModuleItems(id_p, db, self.log)

        
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allmoditems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Module Parameters")
            
        return data 
    
    #Get the directories of the DB                                                   
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def directories(self,_dc=101, node = "",gid = -2, online="False"): 
#        db = cherrypy.request.db
        
        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        db_cache = cherrypy.request.db_cache
        
#        print "ReTURN FORM INSERt: " + str(self.cache_queries.putDictEntry(6,7,db_cache,self.log))
#        entry_cache = self.cache_queries.getDictEntry(3,db_cache,self.log)
#        print "FROM CACHE: " + str(entry_cache[0].gid) + " " + str(entry_cache[0].dbid)
        
 
        folMap = None
        idfolgen = self.idfolgen
        cnfMap = None
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            folMap = self.folMap_online
            cnfMap = self.cnfMap_online
            
        else:
            db = db_offline
            folMap = self.folMap
            cnfMap = self.cnfMap
    
        data = None
        gid = int(gid)
        
        print "GID: ",gid
        
        if gid == -1:
            print "IN -1: "
            data = self.funcs.getRootDirectory(folMap, idfolgen, cnfMap, self.folMap_online, db, self.log)
        
        else:
            data = self.funcs.getChildrenDirectories(gid, folMap, idfolgen, cnfMap, db, self.log)
        
        if (data is None):
#            print ("Exception - Error")
            self.log.error('ERROR: directories - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the directories")
        
        return data

    #Get the directories of the DB                                                   
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def versions(self, _dc=101, cid = 1,online="False"):
#        db = cherrypy.request.db
        
        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        cnfMap = None
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            cnfMap = self.cnfMap_online
            
        else:
            db = db_offline
            cnfMap = self.cnfMap
    
        cid = int(cid)
        id_c = cnfMap.get(cid)
        data = self.funcs.getVersionsByConfig(id_c,db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: versions - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Versions")
        
        return data    
    
    #Get the Module details                                              
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def moddetails(self, _dc=101, mid=0, pid=0,online="False",verid=-1):
#        db = cherrypy.request.db
        
        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        modsMap = None
        patsMap = None 
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            modsMap = self.modsMap_online
            patsMap = self.patsMap_online
            
        else:
            db = db_offline
            modsMap = self.modsMap
            patsMap = self.patsMap
        
        mid = int(mid)
        pid = int(pid)
        
        id_m = modsMap.get(mid)
        id_p = patsMap.get(pid)

        data = self.funcs.getModuleDetails(id_m,id_p,db, self.log)    
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: moddetails - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Module details")
        
        return data
    
    #Get all the Module                                             
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allmodules(self, _dc=101, ver=-2, cnf=-2,online="False"):
#        db = cherrypy.request.db
        
        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        cnfMap = None
        allmodsMap = None
        idgen = None
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            cnfMap = self.cnfMap_online
            allmodsMap = self.allmodsMap_online
            idgen = self.idgen_online
            
        else:
            db = db_offline
            cnfMap = self.cnfMap
            allmodsMap = self.allmodsMap
            idgen = self.idgen
    
        cnf = int(cnf)
        ver = int(ver)
        cnf = cnfMap.get(cnf)
        data = self.funcs.getAllModules(cnf,ver,allmodsMap,idgen,db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allmodules - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Modules")
        
        return data
    
    #Get the Module details                                              
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allservices(self, _dc=101, ver=-2, cnf=-2, node=-1,online="False"):
#        db = cherrypy.request.db
        
        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        cnfMap = None
        srvsMap = None
        idgen = None
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            cnfMap = self.cnfMap_online
            srvsMap = self.srvsMap_online
            idgen = self.idgen_online
            
        else:
            db = db_offline
            cnfMap = self.cnfMap
            srvsMap = self.srvsMap
            idgen = self.idgen
            
        cnf = int(cnf)
        ver = int(ver)
        cnf = cnfMap.get(cnf)
        data = self.funcs.getAllServices(cnf, ver, srvsMap, idgen, db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allservices - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Services")
        
        return data
    
    #Get a the list of items in a service 
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allsrvitems(self, _dc=101, node=1, sid=-2,online="False",verid=-1):
#        db = cherrypy.request.db
        
        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        srvsMap = None
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            srvsMap = self.srvsMap_online
            
        else:
            db = db_offline
            srvsMap = self.srvsMap
    
        sid = int(sid)
        
        id_s = srvsMap.get(sid)
        data = self.funcs.getServiceItems(id_s, db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allsrvitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Service Parameters")
    
        return data
    
    #Get a the list of the stream and the items in it(Dataset and Event content) 
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allstreamitems(self, _dc=101,  ver=-2, cnf=-2, node=-1,online="False"):
#        db = cherrypy.request.db
        
        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        evcMap = None
        idstrgen = None 
        strMap = None 
        datMap = None
        cnfMap = None
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            evcMap = self.evcMap_online
            idstrgen = self.idstrgen_online
            strMap = self.strMap_online 
            datMap = self.datMap_online
            cnfMap = self.cnfMap_online

        else:
            db = db_offline
            evcMap = self.evcMap
            idstrgen = self.idstrgen 
            strMap = self.strMap 
            datMap = self.datMap
            cnfMap = self.cnfMap
    
        cnf = int(cnf)
        ver = int(ver)
        cnf = cnfMap.get(cnf)
        
        data = self.funcs.getStreamsItems(evcMap, idstrgen, strMap, datMap, ver, cnf, db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allstreamitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Stream elements")
            
        return data
    
    #Get a the list of the stream and the items in it(Dataset and Event content) 
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def evcostatements(self, _dc=101, strid=-1,online="False", verid=-1):
#        db = cherrypy.request.db
        
        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        evcMap = None
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            evcMap = self.evcMap_online
            
        else:
            db = db_offline
            evcMap = self.evcMap
    
        strid = int(strid)
        
        evc = evcMap.get(strid)
        
        data = self.funcs.getEvcStatements(evc, db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: evcostatements - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Event content Statements")
            
        return data
    
    
    #Get the Module details                                              
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def cnfdetails(self, _dc=101, ver=-2, cnf=-2,online="False"):
#        db = cherrypy.request.db
        
        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        cnfMap = None
        
        if online == 'True' or online == 'true': #TO ADD TO ONLINE
            print ' I AM USING THE ONLINE db = db_online'
            db = db_online 
            cnfMap = self.cnfMap_online
            
        else:
            print ' I AM USING THE OFFLINE'
            db = db_offline
            cnfMap = self.cnfMap
            
        data = None
        ver = int(ver)
        cnf = int(cnf)        
        
        if(cnf != -2):
            cnf=cnfMap.get(cnf)
        
        print "VER " + str(ver) + " CNF " +  str(cnf) + " ONLINE " +  str(online)
        
        data = self.funcs.getVersionDetails(cnf, ver, db, self.log)    
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: cnfdetails - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Configuration Details")
        
        return data
    
    
    #Get all the Module                                             
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allesmodules(self, _dc=101, node=-2, ver=-2, cnf=-2,online="False"):
#        db = cherrypy.request.db
        
        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        cnfMap = None
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            cnfMap = self.cnfMap_online
            
        else:
            db = db_offline
            cnfMap = self.cnfMap
            
        cnf = int(cnf)
        ver = int(ver)
        cnf = cnfMap.get(cnf)
        data = self.funcs.getAllESModules(cnf,ver,db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allesmodules - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the ES Modules")
        
        return data
    
    #Get all the Module items                                            
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allesmoditems(self, _dc=101, node=-2, mid=-2,online="False", verid=-1):
#        db = cherrypy.request.db
        
        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online 
            
        else:
            db = db_offline
    
        mid = int(mid)

        data = self.funcs.getESModItems(mid,db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allesmoditems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the ES Module Parameters")
        
        return data
    
    #Get all the Sequence items                                             
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allseqitems(self, _dc=101, node=-2, ver=-2, cnf=-2,online="False"):
#        db = cherrypy.request.db
        
        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        seqsMap = None 
        modsMap = None 
        idgen = None
        cnfMap = None
            
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            
            seqsMap = self.seqsMap_online  
            modsMap = self.modsMap_online 
            idgen = self.idgen_online
            cnfMap = self.cnfMap_online
            
        else:
            db = db_offline
            seqsMap = self.seqsMap  
            modsMap = self.modsMap 
            idgen = self.idgen
            cnfMap = self.cnfMap
            
    
        cnf = int(cnf)
        ver = int(ver)
        cnf = cnfMap.get(cnf)
        data = self.funcs.getAllSequences(seqsMap, modsMap, idgen, cnf,ver,db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allseqitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Sequence modules")
        
        return data
    
    
    
    #Get a the list of items in an end path 
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allendpathitems(self, _dc=101, ver=-2, cnf=-2,node=1, itype="",online="False",filter=""):
        
#        db = cherrypy.request.db
        
        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        patsMap = None
        seqsMap = None
        modsMap = None
        oumodsMap = None
        idgen = None
        cnfMap = None
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            
            patsMap = self.patsMap_online
            seqsMap = self.seqsMap_online
            modsMap = self.modsMap_online
            oumodsMap = self.oumodsMap_online
            idgen = self.idgen_online
            cnfMap = self.cnfMap_online
            
            print "LEN PATSMAP MAIN: ",str(len(self.patsMap_online.patDict.values()))
            
        else:
            db = db_offline
            
            patsMap = self.patsMap
            seqsMap = self.seqsMap
            modsMap = self.modsMap
            oumodsMap = self.oumodsMap
            idgen = self.idgen
            cnfMap = self.cnfMap
        
        data = None
        node = int(node)
        ver = int(ver)
        cnf = int(cnf)        
        
        #Pathitems request
        if(itype == 'pat'):            
            data = self.funcs.getEndPathItems(patsMap, seqsMap, modsMap, oumodsMap, idgen, node, ver, db, self.log)
            
        else:
            data = self.funcs.getEndPaths(patsMap, cnfMap, idgen, cnf, ver, db, self.log)
        
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allendpathitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the EndPath and its modules/sequences")
            
        return data
    
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def outmoddetails(self, _dc=101, mid=0, pid=0,online="False", verid=-1):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        oumodsMap = None
        patsMap = None
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            oumodsMap = self.oumodsMap_online
            patsMap = self.patsMap_online
            
        else:
            db = db_offline
            oumodsMap = self.oumodsMap
            patsMap = self.patsMap
        
        mid = int(mid)
        pid = int(pid)
        
        id_m = oumodsMap.get(mid)
        id_p = patsMap.get(pid)

        data = self.funcs.getOUTModuleDetails(id_m,id_p,db, self.log)    
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: outmoddetails - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Output Module Details")
        
        return data
         
        
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allgpsets(self, _dc=101, ver=-2, cnf=-2, node=-1,online="False"):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        cnfMap = None
        gpsMap = None
        idgen = None
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            cnfMap = self.cnfMap_online
            gpsMap = self.gpsMap_online
            idgen = self.idgen_online
            
        else:
            db = db_offline
            cnfMap = self.cnfMap
            gpsMap = self.gpsMap
            idgen = self.idgen
        
        cnf = int(cnf)
        ver = int(ver)
        cnf = cnfMap.get(cnf)
        data = self.funcs.getAllGlobalPsets(cnf, ver, gpsMap, idgen, db)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allgpsets - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Global PSets")
        
        return data
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allgpsetitems(self, _dc=101, node=1, gid=-2,online="False", verid=-1):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        gpsMap = None
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            gpsMap = self.gpsMap_online
            
        else:
            db = db_offline
            gpsMap = self.gpsMap
            
        gid = int(gid)
        
        id_s = gpsMap.get(gid)
        data = self.funcs.getGpsetItems(id_s, db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allgpsetitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Global PSet Parameters")
        
        return data
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def edsource(self, _dc=101, node=-2, ver=-2, cnf=-2,online="False"):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        cnfMap = None
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online 
            cnfMap = self.cnfMap_online 
            
        else:
            db = db_offline
            cnfMap = self.cnfMap
        
        cnf = int(cnf)
        ver = int(ver)
        cnf = cnfMap.get(cnf)
        data = self.funcs.getEDSource(cnf,ver,db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: edsource - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the ED Source")
        
        return data
    
    #Get all the Module                                             
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def alledsourceitems(self, _dc=101, node=-2, mid=-2,online="False", verid=-1):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online 
            
        else:
            db = db_offline
        
        mid = int(mid)

        data = self.funcs.getEDSourceItems(mid,db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the ED Source Parameters")
        
        return data
    
    #Get all the Module                                             
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def essource(self, _dc=101, node=-2, ver=-2, cnf=-2,online="False"):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        cnfMap = None
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online 
            cnfMap = self.cnfMap_online
            
        else:
            db = db_offline
            cnfMap = self.cnfMap
            
        cnf = int(cnf)
        ver = int(ver)
        cnf = cnfMap.get(cnf)
        data = self.funcs.getESSource(cnf,ver,db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: essource - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the ES Source")
        
        return data
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allessourceitems(self, _dc=101, node=-2, mid=-2,online="False", verid=-1):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online 
            
        else:
            db = db_offline
        
        mid = int(mid)

        data = self.funcs.getESSourceItems(mid,db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allessourceitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the ES Source Parameters")
        
        return data
    
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def alldatasetitems(self, _dc=101, dstid=-2, ver=-2, cnf=-2, node=-1,online="False"):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        datMap = None
        cnfMap = None
        patsMap = None
        idgen = None
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            
            datMap = self.datMap_online
            cnfMap = self.cnfMap_online
            patsMap = self.patsMap_online
            idgen = self.idgen_online
            
        else:
            db = db_offline
            
            datMap = self.datMap
            cnfMap = self.cnfMap
            patsMap = self.patsMap
            idgen = self.idgen
    
        cnf = int(cnf)
        ver = int(ver)
        dstid = int(dstid)
        dstid = datMap.get(dstid)
        cnf = cnfMap.get(cnf)
        
        data = self.funcs.getDatasetItems(patsMap, idgen, ver, cnf, dstid, db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: alldatasetitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Paths")
            
        return data
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allsummarycolumns(self, _dc=101, ver=-2, cnf=-2, node=-1,online="False"):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        cnfMap = None
        
        if online == 'True' or online == 'true': #TO ADD TO ONLINE
            print 'db = db_online'
            db = db_online
            cnfMap = self.cnfMap_online
            
        else:
            db = db_offline
            cnfMap = self.cnfMap
        
        cnf = int(cnf)
        ver = int(ver)
        cnf = cnfMap.get(cnf)
        
        data = self.funcs.getSummaryColumns(ver, cnf, db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: alldatasetitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Paths")
            
        return data
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allsummaryitems(self, _dc=101,  ver=-2, cnf=-2, sit='',node=-1,online="False"):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        cnfMap = None
        idsumgen = None
        sumMap = None
        
        if online == 'True' or online == 'true': #TO ADD TO ONLINE
            print 'db = db_online'
            db = db_online
            
            cnfMap = self.cnfMap_online
            idsumgen = self.idsumgen_online
            sumMap = self.sumMap_online
            
        else:
            db = db_offline
            
            cnfMap = self.cnfMap
            idsumgen = self.idsumgen
            sumMap = self.sumMap
        
        cnf = int(cnf)
        ver = int(ver)
        cnf = cnfMap.get(cnf)
        
        data = self.funcs.getSummaryItems(idsumgen, sumMap, ver, cnf, db, self.log)
        
        
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allstreamitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Stream elements")
            
        return data
    
    
        
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def export(self, _dc=101,  ver=-2, cnf=-2,online="False"):    
        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        cnfMap = None
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            cnfMap = self.cnfMap_online
            
        else:
            db = db_offline
            cnfMap = self.cnfMap
        
        cnf = int(cnf)
        ver = int(ver)
        cnf = cnfMap.get(cnf)
        
        #
        #MAKE PYTHON FILE HERE (cnf,ver,online,db,self.log)
        #
        
        url = UrlString(1,'/download/?filepath=ciccio')
        
        resp = Response()
        schema = ResponseUrlStringSchema()
        resp.success = True
        resp.children = []
        resp.children.append(url)
        
        output = schema.dump(resp)
        assert isinstance(output.data, OrderedDict)

        return output.data

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def upload(self, pythonfile=None):
#        size = 0
#        while True:

        data = pythonfile.file.read(8192)
        print "FILE!!!: ",str(data)
#            if not data:
#                break
#            size += len(data)

#        return out % (size, myFile.filename, myFile.content_type)

        url = UrlString(1,"ciccio")

        resp = Response()
        schema = ResponseUrlStringSchema()
        resp.success = True
        resp.children = []
        
        resp.children.append(url)
        
        output = schema.dump(resp)
        assert isinstance(output.data, OrderedDict)

        return output.data
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def confname(self, _dc=101, name=""):
        
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        
        print "NAAAAAAAMEEEE: "+str(name)
        
        cnfMap = None
        db = None
        online = False
        
        tokens = name.split('=')
        path_tokens = tokens[1].split('/')
        firstFolder = path_tokens[1]
        
        if firstFolder == 'cdaq' or firstFolder == 'minidaq':

            db = db_online
            cnfMap = self.cnfMap_online
            online = 'true'
            
        else:
            db = db_offline
            cnfMap = self.cnfMap
            online = 'false'
        
        config_id = self.funcs.getRoutedConfig(cnfMap, tokens[1], db, self.log)    

        resp = Response()
        schema = ResponseUrlStringSchema()
        
        if config_id == -1 or config_id == None:
            resp.success = False
            
        else:
            resp.success = True
        
        resp.children = []
        
        urlString = str(config_id) + "_" + online
        url = UrlString(0,urlString)
        resp.children.append(url)
        
        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data
    
    
class Download:

    def index(self, filepath):
        x = "/Users/vdaponte/Dropbox/Hlt_ReadonlyGui/Application_py27/Config-3.py" #'/Users/vdaponte/Dropbox/dossier sans titre/Config-3.py' 
        print "I CAN PRINT FILE PATH NOW: ",filepath
#        serve_file(x, "application/x-download", "attachment") #filepath
        
#        cherrypy.lib.static.serve_download(x)
        print "I CAN REMOVE THE FILE NOW"
        return  serve_file(x, "application/x-download", "attachment")
    index.exposed = True

    
if __name__ == '__main__':
    
    # Load configuration
    from Config.Config import * # connectUrlonline, connectUrloffline, cpconfig, base_url #connectUrl,
    
    # Register the SQLAlchemy plugin
    from sqlalchemy_plugin.saplugin import SAEnginePlugin
    
    print connectUrlonline
    print connectUrloffline
    
    connectionString = ConnectionString()
    
    #SAEnginePlugin(cherrypy.engine, 'oracle://cms_hlt_gdr:convertiMi!@(DESCRIPTION = (LOAD_BALANCE=on) (FAILOVER=ON) (ADDRESS = (PROTOCOL = TCP)(HOST = int2r2-s.cern.ch)(PORT = 10121)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = int2r_nolb.cern.ch)))').subscribe()
    #'sqlite:///my.db' cmsr.cern.ch

#    SAEnginePlugin(cherrypy.engine, 'oracle://cms_hlt_gdr_r:convertMe!@(DESCRIPTION = (LOAD_BALANCE=on) (FAILOVER=ON) (ADDRESS = (PROTOCOL = TCP)(HOST = cmsr1-s.cern.ch)(PORT = 10121)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = cms_cond.cern.ch)))').subscribe()
    
#    SAEnginePlugin(cherrypy.engine, connectUrl).subscribe()

#    SAEnginePlugin(cherrypy.engine, connectUrlonline, connectUrloffline).subscribe()

    SAEnginePlugin(cherrypy.engine, connectionString).subscribe()
    
    # Register the SQLAlchemy tool
    from sqlalchemy_plugin.satool import SATool
    
    cherrypy.tools.db = SATool()
    
    
#    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'log.access_file':"logs/accessLog.log", 'log.error_file': "logs/errorLog.log", 'log.screen': True})
    
    #Logging 
    
#    logscope = cherrypy.log

    # Make a new RotatingFileHandler for the error log.
#    fname = getattr(logscope, "rot_error_file", "logs/errorLog.log")
#    h = logging.handlers.TimedRotatingFileHandler(fname, when='midnight')

#    h = logging.handlers.RotatingFileHandler(os.path.join(LOG_DIR, ERROR_LOG_FILENAME), maxBytes=20971520, backupCount=50)
#    h.setLevel(logging.ERROR)
#    h.setFormatter(_cplogging.logfmt)
#    logscope.error_file = ""
#    logscope.error_log.addHandler(h)

    # Make a new RotatingFileHandler for the access log.
#    fname = getattr(logscope, "rot_access_file", "logs/accessLog.log")
#    h = logging.handlers.TimedRotatingFileHandler(fname, when='midnight')
    
#    h = logging.handlers.RotatingFileHandler(os.path.join(LOG_DIR, ACCESS_LOG_FILENAME), maxBytes=20971520, backupCount=50)
#    h.setLevel(logging.INFO)
#    h.setFormatter(_cplogging.logfmt)
#    logscope.access_file = ""
#    logscope.access_log.addHandler(h)
    
#    cherrypy.quickstart(Root(), '', {'/': {'tools.db.on': True}})
    
    cherrypy.config.update(cpconfig)
    
    root = Root()
    root.download = Download()
    
    cherrypy.quickstart(root, base_url, {'/': {'tools.db.on': True}}) #Root()
    
    
    
    