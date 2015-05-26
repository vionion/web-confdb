# File Main.py Description:
# This file is the entry point of the Server side application.
# It contains the method to instantiate the and starts the server
# as well the Database session
# Class: Root

#THIS MAIN CAN RUN THE SERVER AS DEAMON ON THE 80 PORT (As Root)


# -*- coding: utf-8 -*-
import cherrypy
from sqlalchemy import *
from sqlalchemy.orm import *
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
from cherrypy.process.plugins import Daemonizer, DropPrivileges

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
    
    srvsMap = ServicesDict()
    
    strMap = StreamsDict()
    datMap = DatasetsDict()
    evcMap = EvcoDict()
    
    gpsMap = GpsetsDict()
    
    funcs = Exposed()
    
    #def __init__(self):
    #    self.types = dict()
    #    db = cherrypy.request.db
    #    for row in db.query(Paetypes).all():
    #        self.types[row.id] = row.name    
    _cp_config = {'tools.staticdir.on' : True,
                  'tools.staticdir.root': current_dir,
                  'tools.staticdir.dir' : 'Demo110315', #'/Users/vdaponte/Dropbox/Demo110315', #ModParams #
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
            data = self.funcs.getPathItems(self.patsMap, self.seqsMap, self.modsMap, self.idgen, node, ver, db)
        
        else:
            data = self.funcs.getPaths(self.patsMap, self.cnfMap, self.idgen, cnf, ver, db)
        
        if (data == None):
            print ("Exception - Error")
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
        data = self.funcs.getPathDetails(pid, cnf, ver, db)
        
        if (data == None):
            print ("Exception - Error")
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
            data = self.funcs.getOUModuleItems(id_oum, db)
        
        else:
            id_p = self.modsMap.get(mid)        
            data = self.funcs.getModuleItems(id_p, db)
        
        
        if (data == None):
            print ("Exception - Error")
            
        return data 
    
    #Get the directories of the DB                                                   
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def directories(self,_dc=101, node = ""):
        db = cherrypy.request.db
        
        data = self.funcs.getDirectories(self.folMap, self.idfolgen, self.cnfMap, db)
        if (data == None):
            print ("Exception - Error")
        
        return data

    #Get the directories of the DB                                                   
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def versions(self, _dc=101, cid = 1):
        db = cherrypy.request.db
        
        cid = int(cid)
        id_c = self.cnfMap.get(cid)
        data = self.funcs.getVersionsByConfig(id_c,db)
        if (data == None):
            print ("Exception - Error")
        
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

        data = self.funcs.getModuleDetails(id_m,id_p,db)    
        if (data == None):
            print ("Exception - Error")
        
        return data
    
    #Get all the Module                                             
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allmodules(self, _dc=101, ver=-2, cnf=-2):
        db = cherrypy.request.db
        
        cnf = int(cnf)
        ver = int(ver)
        cnf = self.cnfMap.get(cnf)
        data = self.funcs.getAllModules(cnf,ver,self.modsMap,self.idgen,db)
        if (data == None):
            print ("Exception - Error")
        
        return data
    
    #Get the Module details                                              
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allservices(self, _dc=101, ver=-2, cnf=-2, node=-1):
        db = cherrypy.request.db
        
        cnf = int(cnf)
        ver = int(ver)
        cnf = self.cnfMap.get(cnf)
        data = self.funcs.getAllServices(cnf,ver,self.srvsMap,self.idgen,db)
        if (data == None):
            print ("Exception - Error")
        
        return data
    
    #Get a the list of items in a service 
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allsrvitems(self, _dc=101, node=1, sid=-2):
        db = cherrypy.request.db
        sid = int(sid)
        
        id_s = self.srvsMap.get(sid)
        data = self.funcs.getServiceItems(id_s, db)
        if (data == None):
            print ("Exception - Error")
            
        return data
    
    #Get a the list of the stream and the items in it(Dataset and Event content) 
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allstreamitems(self, _dc=101,  ver=-2, cnf=-2, node=-1):
        db = cherrypy.request.db
        cnf = int(cnf)
        ver = int(ver)
        cnf = self.cnfMap.get(cnf)
        
        data = self.funcs.getStreamsItems(self.evcMap, self.idstrgen, self.strMap, self.datMap, ver, cnf, db)
        if (data == None):
            print ("Exception - Error")
            
        return data
    
    #Get a the list of the stream and the items in it(Dataset and Event content) 
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def evcostatements(self, _dc=101, strid=-1):
        db = cherrypy.request.db
        strid = int(strid)
        
        evc = self.evcMap.get(strid)
        
        data = self.funcs.getEvcStatements(evc, db)
        if (data == None):
            print ("Exception - Error")
            
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

        data = self.funcs.getVersionDetails(cnf, ver, db)    
        if (data == None):
            print ("Exception - Error")
        
        return data
    
    
    #Get all the Module                                             
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allesmodules(self, _dc=101, node=-2, ver=-2, cnf=-2):
        db = cherrypy.request.db
        
        cnf = int(cnf)
        ver = int(ver)
        cnf = self.cnfMap.get(cnf)
        data = self.funcs.getAllESModules(cnf,ver,db)
        if (data == None):
            print ("Exception - Error")
        
        return data
    
    #Get all the Module items                                            
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allesmoditems(self, _dc=101, node=-2, mid=-2):
        db = cherrypy.request.db
        
        mid = int(mid)

        data = self.funcs.getESModItems(mid,db)
        if (data == None):
            print ("Exception - Error")
        
        return data
    
    #Get all the Sequence items                                             
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allseqitems(self, _dc=101, node=-2, ver=-2, cnf=-2):
        db = cherrypy.request.db
        
        cnf = int(cnf)
        ver = int(ver)
        cnf = self.cnfMap.get(cnf)
        data = self.funcs.getAllSequences(self.seqsMap, self.modsMap, self.idgen, cnf,ver,db)
        if (data == None):
            print ("Exception - Error")
        
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
            data = self.funcs.getEndPathItems(self.patsMap, self.seqsMap, self.modsMap, self.oumodsMap, self.idgen, node, ver, db)
        
        else:
            data = self.funcs.getEndPaths(self.patsMap, self.cnfMap, self.idgen, cnf, ver, db)
        
        if (data == None):
            print ("Exception - Error")
        return data
    
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def outmoddetails(self, _dc=101, mid=0, pid=0):
        db = cherrypy.request.db
        
        mid = int(mid)
        pid = int(pid)
        
        id_m = self.oumodsMap.get(mid)
        id_p = self.patsMap.get(pid)

        data = self.funcs.getOUTModuleDetails(id_m,id_p,db)    
        if (data == None):
            print ("Exception - Error")
        
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
            print ("Exception - Error")
        
        return data
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allgpsetitems(self, _dc=101, node=1, gid=-2):
        db = cherrypy.request.db
        gid = int(gid)
        
        id_s = self.gpsMap.get(gid)
        data = self.funcs.getGpsetItems(id_s, db)
        if (data == None):
            print ("Exception - Error")
            
        return data
    
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def edsource(self, _dc=101, node=-2, ver=-2, cnf=-2):
        db = cherrypy.request.db
        
        cnf = int(cnf)
        ver = int(ver)
        cnf = self.cnfMap.get(cnf)
        data = self.funcs.getEDSource(cnf,ver,db)
        if (data == None):
            print ("Exception - Error")
        
        return data
    
    #Get all the Module                                             
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def alledsourceitems(self, _dc=101, node=-2, mid=-2):
        db = cherrypy.request.db
        
        mid = int(mid)

        data = self.funcs.getEDSourceItems(mid,db)
        if (data == None):
            print ("Exception - Error")
        
        return data
    
    #Get all the Module                                             
    
    
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def essource(self, _dc=101, node=-2, ver=-2, cnf=-2):
        db = cherrypy.request.db
        
        cnf = int(cnf)
        ver = int(ver)
        cnf = self.cnfMap.get(cnf)
        data = self.funcs.getESSource(cnf,ver,db)
        if (data == None):
            print ("Exception - Error")
        
        return data
    
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allessourceitems(self, _dc=101, node=-2, mid=-2):
        db = cherrypy.request.db
        
        mid = int(mid)

        data = self.funcs.getESSourceItems(mid,db)
        if (data == None):
            print ("Exception - Error")
        
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
        
        data = self.funcs.getDatasetItems(self.patsMap, self.idgen, ver, cnf, dstid, db)
        if (data == None):
            print ("Exception - Error")
            
        return data
    
    #Get a the list of the stream and the items in it(Dataset and Event content) 
    
if __name__ == '__main__':
    # Register the SQLAlchemy plugin
    from sqlalchemy_plugin.saplugin import SAEnginePlugin
    from cherrypy.process.plugins import DropPrivileges
    #SAEnginePlugin(cherrypy.engine, 'oracle://cms_hlt_gdr:convertiMi!@(DESCRIPTION = (LOAD_BALANCE=on) (FAILOVER=ON) (ADDRESS = (PROTOCOL = TCP)(HOST = int2r2-s.cern.ch)(PORT = 10121)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = int2r_nolb.cern.ch)))').subscribe()
    #'sqlite:///my.db' cmsr.cern.ch
    
#    dr = DropPrivileges(cherrypy.engine, uid=1000, gid=1000)
    dr = DropPrivileges(cherrypy.engine)
    dr.subscribe()
    
    from cherrypy.process.plugins import Daemonizer
    d = Daemonizer(cherrypy.engine)
    d.subscribe()
    
#    dr = DropPrivileges(cherrypy.engine, uid=1000, gid=1000)
#    dr.subscribe()
    
    SAEnginePlugin(cherrypy.engine, 'oracle://user:password@(DESCRIPTION = (LOAD_BALANCE=on) (FAILOVER=ON) (ADDRESS = (PROTOCOL = TCP)(HOST = hostname)(PORT = port)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = servicename)))').subscribe()
    
    # Register the SQLAlchemy tool
    from sqlalchemy_plugin.satool import SATool
    cherrypy.tools.db = SATool()
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                           'server.socket_port': 80})
    cherrypy.quickstart(Root(), '', {'/': {'tools.db.on': True}})
    