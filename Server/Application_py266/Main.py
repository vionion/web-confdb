# File Main.py Description:
# This file is the entry point of the Server side application.
# It contains the method to instantiate the and starts the server
# as well the Database session
# Class: Root


# -*- coding: utf-8 -*-
import cherrypy
from sqlalchemy import *
from sqlalchemy.orm import *
from cherrypy import _cplogging, _cpconfig, _cplogging, _cprequest, _cpwsgi, tools
from operator import attrgetter
import json
#from collections import OrderedDict
from marshmallow.ordereddict import OrderedDict
from utils import * 

#NEW IMPORT
from exposed.exposed import *
from sqlalchemy_plugin.saplugin import *

import sys
import logging 
import logging.handlers

#Set logging handlers for the first time
#from conflogger import logconfig

import os.path
current_dir = os.path.dirname(os.path.abspath(__file__))

#metadata = MetaData()    
    
class Root(object):
    
    idgen = Counter()
    idfolgen = FolderItemCounter()
    idstrgen = StreamItemCounter()
    
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
    
    funcs = Exposed()
    
    log = cherrypy.log
    
    #def __init__(self):
    #    self.types = dict()
    #    db = cherrypy.request.db
    #    for row in db.query(Paetypes).all():
    #        self.types[row.id] = row.name    
    _cp_config = {'tools.staticdir.on' : True,
                  'tools.staticdir.root': current_dir,
                  'tools.staticdir.dir' : 'Demo110315', 
                  'tools.staticdir.index' : 'index.html',
    }

    @cherrypy.expose
    def index(self):
        # Get the SQLAlchemy session associated
        # with this request.
        # It'll be released once the request
        # processing terminates
        db = cherrypy.request.db

        return "Hello World"
    
    #Get a the list of items in a path 
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allpathitems(self, _dc=101, ver=-2, cnf=-2,node=1, itype=""):
        
        db = cherrypy.request.db
        data = None
        node = int(node)
        ver = int(ver)
        cnf = int(cnf)     

        #Pathitems request
        if(itype == 'pat'):
            data = self.funcs.getPathItems(self.patsMap, self.seqsMap, self.modsMap, self.idgen, node, ver, db, self.log)
        
        else:
            data = self.funcs.getPaths(self.patsMap, self.cnfMap, self.idgen, cnf, ver, db, self.log)
        
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allpathitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Path and its sequences/modules")
    
        return data
    
    #Get a the list of items in a path 
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def pathdetails(self, _dc=101, ver=-2, cnf=-2,node=1, pid=-2):
        
        db = cherrypy.request.db
        data = None
        node = int(node)
        pid = int(pid)
        ver = int(ver)
        cnf = int(cnf)        
        
        if(cnf != -2):
            cnf=self.cnfMap.get(cnf)
        
        pid = self.patsMap.get(pid)
        
        #Path details request
        data = self.funcs.getPathDetails(pid, cnf, ver, db, self.log)
        
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: pathdetails - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Path details")
    
        return data
    
    #Get a the list of items in a path 
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allmoditems(self, _dc=101, length=1, node=1, mid=-2, pid=-2, epit = "" ):
        db = cherrypy.request.db
        pid = int(pid)
        mid = int(mid)
        
        if(epit == "oum"):
            id_oum = self.oumodsMap.get(mid)
            data = self.funcs.getOUModuleItems(id_oum, db, self.log)
        
        else:
            id_p = self.modsMap.get(mid)        
            data = self.funcs.getModuleItems(id_p, db, self.log)
        
        
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allmoditems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Module Parameters")
            
        return data 
    
    #Get the directories of the DB                                                   
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def directories(self,_dc=101, node = ""):
        db = cherrypy.request.db
        
        data = self.funcs.getDirectories(self.folMap, self.idfolgen, self.cnfMap, db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: directories - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the directories")
        
        return data

    #Get the directories of the DB                                                   
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def versions(self, _dc=101, cid = 1):
        db = cherrypy.request.db
        
        cid = int(cid)
        id_c = self.cnfMap.get(cid)
        data = self.funcs.getVersionsByConfig(id_c,db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: versions - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Versions")
        
        return data    
    
    #Get the Module details                                              
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def moddetails(self, _dc=101, mid=0, pid=0):
        db = cherrypy.request.db
        
        mid = int(mid)
        pid = int(pid)
        
        id_m = self.modsMap.get(mid)
        id_p = self.patsMap.get(pid)

        data = self.funcs.getModuleDetails(id_m,id_p,db, self.log)    
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: moddetails - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Module details")
        
        return data
    
    #Get all the Module                                             
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allmodules(self, _dc=101, ver=-2, cnf=-2):
        db = cherrypy.request.db
        
        cnf = int(cnf)
        ver = int(ver)
        cnf = self.cnfMap.get(cnf)
        data = self.funcs.getAllModules(cnf,ver,self.allmodsMap,self.idgen,db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allmodules - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Modules")
        
        return data
    
    #Get the Module details                                              
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allservices(self, _dc=101, ver=-2, cnf=-2, node=-1):
        db = cherrypy.request.db
        
        cnf = int(cnf)
        ver = int(ver)
        cnf = self.cnfMap.get(cnf)
        data = self.funcs.getAllServices(cnf,ver,self.srvsMap,self.idgen,db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allservices - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Services")
        
        return data
    
    #Get a the list of items in a service 
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allsrvitems(self, _dc=101, node=1, sid=-2):
        db = cherrypy.request.db
        sid = int(sid)
        
        id_s = self.srvsMap.get(sid)
        data = self.funcs.getServiceItems(id_s, db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allsrvitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Service Parameters")
    
        return data
    
    #Get a the list of the stream and the items in it(Dataset and Event content) 
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allstreamitems(self, _dc=101,  ver=-2, cnf=-2, node=-1):
        db = cherrypy.request.db
        cnf = int(cnf)
        ver = int(ver)
        cnf = self.cnfMap.get(cnf)
        
        data = self.funcs.getStreamsItems(self.evcMap, self.idstrgen, self.strMap, self.datMap, ver, cnf, db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allstreamitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Stream elements")
            
        return data
    
    #Get a the list of the stream and the items in it(Dataset and Event content) 
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def evcostatements(self, _dc=101, strid=-1):
        db = cherrypy.request.db
        strid = int(strid)
        
        evc = self.evcMap.get(strid)
        
        data = self.funcs.getEvcStatements(evc, db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: evcostatements - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Event content Statements")
            
        return data
    
    
    #Get the Module details                                              
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def cnfdetails(self, _dc=101, ver=-2, cnf=-2):
        db = cherrypy.request.db

        data = None
        ver = int(ver)
        cnf = int(cnf)        
        
        if(cnf != -2):
            cnf=self.cnfMap.get(cnf)

        data = self.funcs.getVersionDetails(cnf, ver, db, self.log)    
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: cnfdetails - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Configuration Details")
        
        return data
    
    
    #Get all the Module                                             
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allesmodules(self, _dc=101, node=-2, ver=-2, cnf=-2):
        db = cherrypy.request.db
        
        cnf = int(cnf)
        ver = int(ver)
        cnf = self.cnfMap.get(cnf)
        data = self.funcs.getAllESModules(cnf,ver,db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allesmodules - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the ES Modules")
        
        return data
    
    #Get all the Module items                                            
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allesmoditems(self, _dc=101, node=-2, mid=-2):
        db = cherrypy.request.db
        
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
    def allseqitems(self, _dc=101, node=-2, ver=-2, cnf=-2):
        db = cherrypy.request.db
        
        cnf = int(cnf)
        ver = int(ver)
        cnf = self.cnfMap.get(cnf)
        data = self.funcs.getAllSequences(self.seqsMap, self.modsMap, self.idgen, cnf,ver,db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allseqitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Sequence modules")
        
        return data
    
    
    
    #Get a the list of items in an end path 
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allendpathitems(self, _dc=101, ver=-2, cnf=-2,node=1, itype=""):
        
        db = cherrypy.request.db
        data = None
        node = int(node)
        ver = int(ver)
        cnf = int(cnf)        
        
        #Pathitems request
        if(itype == 'pat'):
            data = self.funcs.getEndPathItems(self.patsMap, self.seqsMap, self.modsMap, self.oumodsMap, self.idgen, node, ver, db, self.log)
        
        else:
            data = self.funcs.getEndPaths(self.patsMap, self.cnfMap, self.idgen, cnf, ver, db, self.log)
        
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allendpathitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the EndPath and its modules/sequences")
            
        return data
    
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def outmoddetails(self, _dc=101, mid=0, pid=0):
        db = cherrypy.request.db
        
        mid = int(mid)
        pid = int(pid)
        
        id_m = self.oumodsMap.get(mid)
        id_p = self.patsMap.get(pid)

        data = self.funcs.getOUTModuleDetails(id_m,id_p,db, self.log)    
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: outmoddetails - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Output Module Details")
        
        return data
         
        
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allgpsets(self, _dc=101, ver=-2, cnf=-2, node=-1):
        db = cherrypy.request.db
        
        cnf = int(cnf)
        ver = int(ver)
        cnf = self.cnfMap.get(cnf)
        data = self.funcs.getAllGlobalPsets(cnf,ver,self.gpsMap,self.idgen,db)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allgpsets - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Global PSets")
        
        return data
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allgpsetitems(self, _dc=101, node=1, gid=-2):
        db = cherrypy.request.db
        gid = int(gid)
        
        id_s = self.gpsMap.get(gid)
        data = self.funcs.getGpsetItems(id_s, db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allgpsetitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Global PSet Parameters")
        
        return data
    
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def edsource(self, _dc=101, node=-2, ver=-2, cnf=-2):
        db = cherrypy.request.db
        
        cnf = int(cnf)
        ver = int(ver)
        cnf = self.cnfMap.get(cnf)
        data = self.funcs.getEDSource(cnf,ver,db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: edsource - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the ED Source")
        
        return data
    
    #Get all the Module                                             
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def alledsourceitems(self, _dc=101, node=-2, mid=-2):
        db = cherrypy.request.db
        
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
    def essource(self, _dc=101, node=-2, ver=-2, cnf=-2):
        db = cherrypy.request.db
        
        cnf = int(cnf)
        ver = int(ver)
        cnf = self.cnfMap.get(cnf)
        data = self.funcs.getESSource(cnf,ver,db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: essource - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the ES Source")
        
        return data
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allessourceitems(self, _dc=101, node=-2, mid=-2):
        db = cherrypy.request.db
        
        mid = int(mid)

        data = self.funcs.getESSourceItems(mid,db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allessourceitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the ES Source Parameters")
        
        return data
    
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def alldatasetitems(self, _dc=101, dstid=-2, ver=-2, cnf=-2, node=-1):
        db = cherrypy.request.db
        cnf = int(cnf)
        ver = int(ver)
        dstid = int(dstid)
        dstid = self.datMap.get(dstid)
        cnf = self.cnfMap.get(cnf)
        
        data = self.funcs.getDatasetItems(self.patsMap, self.idgen, ver, cnf, dstid, db, self.log)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: alldatasetitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Paths")
            
        return data
    
    #Get a the list of the stream and the items in it(Dataset and Event content)  
    
if __name__ == '__main__':
    # Register the SQLAlchemy plugin
    from sqlalchemy_plugin.saplugin import SAEnginePlugin
    
    # Load configuration
    from Config import connectUrl, cpconfig, base_url

    SAEnginePlugin(cherrypy.engine, connectUrl).subscribe()
    
    # Register the SQLAlchemy tool
    from sqlalchemy_plugin.satool import SATool
    cherrypy.tools.db = SATool()
    
    
#    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'log.access_file':"logs/accessLog.log", 'log.error_file': "logs/errorLog.log", 'log.screen': True})
#    cherrypy.quickstart(Root(), '', {'/': {'tools.db.on': True}})
    
    cherrypy.config.update(cpconfig)
    cherrypy.quickstart(Root(), base_url, {'/': {'tools.db.on': True}})
    