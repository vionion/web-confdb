#! /usr/bin/env python
# -*- coding: utf-8 -*-

# File Main.py Description:
# This file is the entry point of the Server side application.
# It contains the method to instantiate the and starts the server
# as well the Database session
# Class: Root

import sys
import logging
import logging.handlers
import cherrypy
import os
import tempfile

current_dir = os.path.dirname(os.path.abspath(__file__))

from cherrypy.lib.static import serve_file
from sqlalchemy import *
from sqlalchemy.orm import *
from marshmallow.ordereddict import OrderedDict
from utils import *
from exposed.exposed import *
from converter.converter import *
from inverter.inverter import *
from exposed.parser_functions import *
from sqlalchemy_plugin.saplugin import *

#metadata = MetaData()

class Root(object):

    # shared across databases
    idfolgen = Counter()

    #----------- OFFLINE DB ---------
    idgen = Counter()
    patsMap = UniqueMapping(idgen)
    seqsMap = SequencesMapping(idgen)
    modsMap = ModulesMapping(idgen)
    oumodsMap = UniqueMapping(idgen)
    allmodsMap = UniqueMapping(idgen)
    srvsMap = UniqueMapping(idgen)
    gpsMap = UniqueMapping(idgen)

    idsumgen = Counter()
    sumMap = UniqueMapping(idsumgen)

    cnfMap = UniqueMapping(idfolgen)
    folMap = UniqueMapping(idfolgen)

    idstrgen = Counter()
    strMap = UniqueMapping(idstrgen)
    datMap = UniqueMapping(idstrgen)
    evcMap = UniqueMapping(idstrgen)


    #----------- ONLINE DB ---------
    idgen_online = Counter()
    patsMap_online = UniqueMapping(idgen_online)
    seqsMap_online = SequencesMapping(idgen_online)
    modsMap_online = ModulesMapping(idgen_online)
    oumodsMap_online = UniqueMapping(idgen_online)
    allmodsMap_online = UniqueMapping(idgen_online)
    srvsMap_online = UniqueMapping(idgen_online)
    gpsMap_online = UniqueMapping(idgen_online)

    idsumgen_online = Counter()
    sumMap_online = UniqueMapping(idsumgen_online)

    cnfMap_online = UniqueMapping(idfolgen)
    folMap_online = UniqueMapping(idfolgen)

    idstrgen_online = Counter()
    strMap_online = UniqueMapping(idstrgen_online)
    datMap_online = UniqueMapping(idstrgen_online)
    evcMap_online = UniqueMapping(idstrgen_online)

    config_dict = OrderedDict()

    #---- General purpose ---------
    funcs = Exposed()
    conv = Converter()
    inv = Inverter()
    par_funcs = Parser_Functions()
    config_idgen = Counter()

    log = cherrypy.log

    #def __init__(self):
    #    self.types = dict()
    #    db = cherrypy.request.db
    #    for row in db.query(Paetypes).all():
    #        self.types[row.id] = row.name
    _cp_config = {'tools.staticdir.on' : True,
                  'tools.staticdir.root': current_dir,
                  # prod
                  # 'tools.staticdir.dir' : 'CmsConfigExplorer',
                  # dev
                  'tools.staticdir.dir' : '../Client/CmsConfigExplorer',
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


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allpathitems(self, _dc = 101, ver = -2, cnf = -2,node = 1, itype = "",online = "False", filter = ""):

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline

        request = cherrypy.request

        patsMap = None
        seqsMap = None
        modsMap = None
        cnfMap = None
        src = 0

        if online == 'file':
            if(itype == 'pat'):
                data = self.par_funcs.getPathItemsFromFile(ver, int(node), self.config_dict)
            else:
                data = self.par_funcs.getPathsFromFile(ver, self.config_dict)
            if (data == None):
                self.log.error('ERROR: allpathitems - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the Path and its sequences/modules")
            return data

        else:
            if online == 'True' or online == 'true':
                db = db_online
                patsMap = self.patsMap_online
                seqsMap = self.seqsMap_online
                modsMap = self.modsMap_online
                cnfMap = self.cnfMap_online
                src = 1

            else:
                db = db_offline
                patsMap = self.patsMap
                seqsMap = self.seqsMap
                modsMap = self.modsMap
                cnfMap = self.cnfMap
                src = 0

            data = None
            node = int(node)
            ver = int(ver)
            cnf = int(cnf)

            #Pathitems request
            if(itype == 'pat'):
                data = self.funcs.getPathItems(node, ver, db, self.log, src, request)

            else:
                data = self.funcs.getPaths(cnf, ver, db, self.log, request, src)

            if (data == None):
    #            print ("Exception - Error")
                self.log.error('ERROR: allpathitems - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the Path and its sequences/modules")

            return data

    #Get a the list of items in a path

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def pathdetails(self, _dc = 101, ver = -2, cnf = -2,node = 1, pid = -2,online = "False"):

#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        patsMap = None
        cnfMap = None
        src = 0

        if online == 'file':
            data = self.par_funcs.getPathDetailsFromFile(ver,int(pid), self.config_dict)
            if (data == None):
                self.log.error('ERROR: pathdetails - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the Path details")
            return data

        else:
            if online == 'True' or online == 'true':
                db = db_online
                patsMap = self.patsMap_online
                cnfMap = self.cnfMap_online
                src = 1

            else:
                db = db_offline
                patsMap = self.patsMap
                cnfMap = self.cnfMap
                src = 0

            data = None
            node = int(node)
            pid = int(pid)
            ver = int(ver)
            cnf = int(cnf)

            # if(cnf != -2):
            #     cnf=cnfMap.get(cnf)

            # pid = patsMap.get(pid)

            #Path details request
            data = self.funcs.getPathDetails(pid, cnf, ver, db, self.log, src, cherrypy.request)

            if (data == None):
    #            print ("Exception - Error")
                self.log.error('ERROR: pathdetails - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the Path details")

            return data

    #Get a the list of items in a path

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allmoditems(self, _dc = 101, length = 1, node = 1, mid = -2, pid = -2, epit = "", allmod = "false", online = "False", verid = -1):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline

        modsMap = None
        oumodsMap = None
        allmodsMap = None
        src = 0

        if online == 'file':
            data = self.par_funcs.getModuleItemsFromFile(verid, int(mid), self.config_dict)
            if (data == None):
                self.log.error('ERROR: allmoditems - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the Module Parameters")
            return data

        else:
            if online == 'True' or online == 'true':
                db = db_online
                modsMap = self.modsMap_online
                oumodsMap = self.oumodsMap_online
                allmodsMap = self.allmodsMap_online
                src = 1

            else:
                db = db_offline
                modsMap = self.modsMap
                oumodsMap = self.oumodsMap
                allmodsMap = self.allmodsMap
                src = 0

        pid = int(pid)
        mid = int(mid)

        data = None

        if(epit == "oum"):
            # id_oum = oumodsMap.get(mid)
            # data = self.funcs.getOUModuleItems(id_oum, db, self.log)
            id_oum = mid
            data = self.funcs.getOUModuleItems(id_oum, db, src, cherrypy.request, self.log)

        else:

            data = self.funcs.getModuleItems(mid, db, src, cherrypy.request, allmod, False, self.log)
            # if (allmod == 'true'):
            #     id_p = allmodsMap.get(mid)
            #     data = self.funcs.getModuleItems(id_p, db, self.log)
            # else:
            #     id_p = modsMap.get(mid)
            #     data = self.funcs.getModuleItems(id_p, db, self.log)

        if (data == None):
            # print ("Exception - Error")
            self.log.error('ERROR: allmoditems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Module Parameters")

        return data

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def update_param_val(self):
        input_json = byteify(cherrypy.request.json)
        value = input_json['value']
        mod_id = input_json['modId']
        param_name = input_json['parName']

        # what is this, why it is always 0 in db and what is online db?
        # UPD: TODO: it still might be different from 0, so remove hardcode
        src = 0

        self.funcs.update_module_cache(mod_id, src, param_name, value, cherrypy.request, self.log)
        # TODO: remove it, it is stupid. Return something more enhanced
        return input_json


    # TODO: replace it with tiny object which has only name
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_module_names(self, query="", ver = -2, cnf = -2,online = "False"):
        return self.allmodules(ver=ver, cnf=cnf, online=online)

    #Get the directories of the DB

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def directories(self,_dc = 101, node = "", gid = -2, online = "False"):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        src = 0
        request = cherrypy.request

        folMap = None
        cnfMap = None

        if online == 'True' or online == 'true':
            db = db_online
            folMap = self.folMap_online
            cnfMap = self.cnfMap_online
            src = 1

        else:
            db = db_offline
            folMap = self.folMap
            cnfMap = self.cnfMap
            src = 0

        data = None
        gid = int(gid)

        if gid == -1:
            data = self.funcs.getRootDirectory(db, self.log, request, src)

        else:
            data = self.funcs.getChildrenDirectories(gid, db, self.log,  request, src)

        if (data is None):
            self.log.error('ERROR: directories - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the directories")

        return data
    #Get the directories of the DB

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def versions(self, _dc = 101, cid = 1, online = "False"):

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline

        # cnfMap = 
        src = 0

        if online == 'True' or online == 'true':
            db = db_online
            cnfMap = self.cnfMap_online
            src = 1

        else:
            db = db_offline
            cnfMap = self.cnfMap
            src = 0

        cid = int(cid)
        # id_c = cnfMap.get(cid)
        data = self.funcs.getVersionsByConfig(cid,db, self.log, cherrypy.request, src)
        if (data == None):
            self.log.error('ERROR: versions - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Versions")

        return data

    #Get the Module details

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def moddetails(self, _dc = 101, mid = 0, pid = 0,online = "False", verid = -1):
        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline

        modsMap = None
        patsMap = None
        src = 0

        if online == 'file':
            data = self.par_funcs.getModDetailsFromFile(verid,int(mid), self.config_dict)
            if (data == None):
                self.log.error('ERROR: moddetails - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the Module details")

            return data

        else:
            if online == 'True' or online == 'true':
                db = db_online
                modsMap = self.modsMap_online
                patsMap = self.patsMap_online
                src = 1

            else:
                db = db_offline
                modsMap = self.modsMap
                patsMap = self.patsMap
                src = 0

            mid = int(mid)
            pid = int(pid)

            # id_m = modsMap.get(mid)
            # id_p = patsMap.get(pid)

            data = self.funcs.getModuleDetails(mid,pid,False,db, self.log, src, cherrypy.request)
            if (data == None):
    #            print ("Exception - Error")
                self.log.error('ERROR: moddetails - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the Module details")

            return data

    #Get all the Module

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allmodules(self, _dc = 101, ver = -2, cnf = -2,online = "False"):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline

        cnfMap = None
        allmodsMap = None
        src = 0

        if online == 'file':
            data = self.par_funcs.getModulesFromFile(ver, self.config_dict)
            if (data == None):
                self.log.error('ERROR: allmodules - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the Modules")

            return data

        else:

            if online == 'True' or online == 'true':
                db = db_online
                cnfMap = self.cnfMap_online
                allmodsMap = self.allmodsMap_online
                src = 1

            else:
                db = db_offline
                cnfMap = self.cnfMap
                allmodsMap = self.allmodsMap
                src = 0

        cnf = int(cnf)
        ver = int(ver)
        # cnf = cnfMap.get(cnf)
        data = self.funcs.getAllModules(cnf,ver,db, self.log, cherrypy.request, src)
        if (data == None):
            #print ("Exception - Error")
            self.log.error('ERROR: allmodules - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Modules")

        return data

    #Get the Module details

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allservices(self, _dc = 101, ver = -2, cnf = -2, node = -1, online = "False"):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline

        cnfMap = None
        srvsMap = None
        src = 0

        if online == 'file':
            data = self.par_funcs.getServiceFromFile(ver, self.config_dict)
            if (data == None):
                self.log.error('ERROR: allservices - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the Services")

            return data

        else:
            if online == 'True' or online == 'true':
                db = db_online
                cnfMap = self.cnfMap_online
                srvsMap = self.srvsMap_online
                src = 1

            else:
                db = db_offline
                cnfMap = self.cnfMap
                srvsMap = self.srvsMap
                src = 0

            cnf = int(cnf)
            ver = int(ver)
            # cnf = cnfMap.get(cnf)
            data = self.funcs.getAllServices(cnf,ver,db, self.log, cherrypy.request, src)
            if (data == None):
    #            print ("Exception - Error")
                self.log.error('ERROR: allservices - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the Services")

            return data

    #Get a the list of items in a service

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allsrvitems(self, _dc = 101, node = 1, sid = -2,online = "False", verid = -1):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        srvsMap = None
        src = 0

        if online == 'file':
            data = self.par_funcs.getServiceItemsFromFile(verid, int(sid), self.config_dict)
            if (data == None):
                self.log.error('ERROR: allsrvitems - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the Service Parameters")
            return data

        else:
            if online == 'True' or online == 'true':
                db = db_online
                # srvsMap = self.srvsMap_online
                src = 1

            else:
                db = db_offline
                # srvsMap = self.srvsMap
                src = 0

            sid = int(sid)

            # id_s = srvsMap.get(sid)
            # data = self.funcs.getServiceItems(id_s, db, self.log)
            data = self.funcs.getServiceItems(sid, db, self.log, src, cherrypy.request)
            if (data == None):
    #            print ("Exception - Error")
                self.log.error('ERROR: allsrvitems - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the Service Parameters")

            return data

    #Get a the list of the stream and the items in it(Dataset and Event content)


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allstreamitems(self, _dc = 101,  ver = -2, cnf = -2, node = -1,online = "False"):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        src = 0

        evcMap = None
        strMap = None
        datMap = None
        cnfMap = None

        if online == 'file':
            data = self.par_funcs.getStreamsFromFile(ver, self.config_dict)
            if (data == None):
                self.log.error('ERROR: allstreamitems - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the Stream elements")

            return data

        else:
            if online == 'True' or online == 'true':
                db = db_online
                evcMap = self.evcMap_online
                strMap = self.strMap_online
                datMap = self.datMap_online
                cnfMap = self.cnfMap_online
                src = 1

            else:
                db = db_offline
                evcMap = self.evcMap
                strMap = self.strMap
                datMap = self.datMap
                cnfMap = self.cnfMap
                src = 0

        cnf = int(cnf)
        ver = int(ver)
        # cnf = cnfMap.get(cnf)

        # data = self.funcs.getStreamsItems(evcMap, strMap, datMap, ver, cnf, db, self.log)
        data = self.funcs.getStreamsItems(ver, cnf, db, self.log, cherrypy.request, src)

        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allstreamitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Stream elements")

        return data

    #Get a the list of the stream and the items in it(Dataset and Event content)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def evcostatements(self, _dc = 101, strid = -1,online = "False", verid = -1):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        src = 0

        evcMap = None

        if online == 'file':
            data = self.par_funcs.getEvcoStatementsFromFile(verid, int(strid), self.config_dict)
            if (data == None):
                self.log.error('ERROR: evcostatements - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the Event content Statements")
            return data

        else:
            if online == 'True' or online == 'true':
                db = db_online
                # evcMap = self.evcMap_online
                src = 1

            else:
                db = db_offline
                # evcMap = self.evcMap
                src = 0

        # strid = int(strid)
        evc = int(strid)

        # evc = evcMap.get(strid)
	self.log.error('EVC: ')
	self.log.error(str(evc))		

        data = self.funcs.getEvcStatements(evc, db, self.log, cherrypy.request, src)
        if (data == None):
            # print ("Exception - Error")
            self.log.error('ERROR: evcostatements - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Event content Statements")

        return data


    #Get the Module details

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def cnfdetails(self, _dc = 101, ver = -2, cnf = -2,online = "False"):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        cnfMap = None
        src = 0

        if online == 'file':
            data = self.par_funcs.getCnfDetailsFromFile(ver, self.config_dict)
            if (data == None):
                self.log.error('ERROR: cnfdetails - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the Configuration Details")
            return data

        else:
            if online == 'True' or online == 'true':
                db = db_online
                # cnfMap = self.cnfMap_online
                src = 1

            else:
                db = db_offline
                # cnfMap = self.cnfMap
                src = 0

        data = None
        ver = int(ver)
        cnf = int(cnf)

        # if(cnf != -2):
        #     cnf=cnfMap.get(cnf)

        data = self.funcs.getVersionDetails(cnf, ver, db, self.log, cherrypy.request, src)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: cnfdetails - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Configuration Details")

        return data


    #Get all the Module

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allesmodules(self, _dc = 101, node = -2, ver = -2, cnf = -2,online = "False"):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        cnfMap = None
        src = 0

        if online == 'file':
            data = self.par_funcs.getEsModulesFromFile(ver, self.config_dict)
            if (data == None):
                self.log.error('ERROR: allesmodules - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the ES Modules")

            return data

        else:
            if online == 'True' or online == 'true':
                db = db_online
                # cnfMap = self.cnfMap_online
                src = 1

            else:
                db = db_offline
                # cnfMap = self.cnfMap
                src = 0

        cnf = int(cnf)
        ver = int(ver)
        # cnf = cnfMap.get(cnf)
        data = self.funcs.getAllESModules(cnf, ver, db, self.log, cherrypy.request, src)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allesmodules - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the ES Modules")

        return data

    #Get all the Module items


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allesmoditems(self, _dc = 101, node = -2, mid = -2,online = "False", verid = -1):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        src = 0

        if online == 'file':
            data = self.par_funcs.getEsModulesItemsFromFile(verid, int(mid), self.config_dict)
            if (data == None):
                self.log.error('ERROR: allesmoditems - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the ES Module Parameters")
            return data

        else:
            if online == 'True' or online == 'true':
                db = db_online
                src = 1

            else:
                db = db_offline
                src = 0

        mid = int(mid)

        data = self.funcs.getESModItems(mid,db, src, self.log, cherrypy.request)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allesmoditems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the ES Module Parameters")

        return data

    #Get all the Sequence items

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allseqitems(self, _dc=101, node=-2, ver=-2, cnf=-2,online="False"):

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        src = 0

        cnfMap = None
            
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            # cnfMap = self.cnfMap_online
            src = 1
            
        else:
            db = db_offline
            # cnfMap = self.cnfMap
            src = 0
            
        cnf = int(cnf)
        ver = int(ver)
        # cnf = cnfMap.get(cnf)
        data = self.funcs.getAllSequences(cnf,ver,db, self.log, cherrypy.request, src)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allseqitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Sequence modules")
        
        return data
    

    #Get a the list of items in an end path 
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allseqmoditems(self, _dc=101, node=1, mid=-2, pid=-2, online="False", verid=-2, cnf=-2):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline

        fromSequence = True
        src = 0

        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            src = 1

        else:
            db = db_offline
            src = 0

        pid = int(pid)
        mid = int(mid)

        data = None
      
        # data = self.funcs.getModuleItems(mid, db, self.log)
        data = self.funcs.getModuleItems(mid, db, src, cherrypy.request, "false", fromSequence, self.log)

        
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allmoditems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Module Parameters")
            
        return data
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def seqmoddetails(self, _dc=101, mid=0, pid=0,online="False",verid=-1):
#        db = cherrypy.request.db
        
        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline

        fromSequence = True
        src = 0
        
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = db_online
            src = 1
            
        else:
            db = db_offline
            src = 0
        
        mid = int(mid)
        pid = int(pid)

        # data = self.funcs.getModuleDetails(mid,pid,db, self.log)
        data = self.funcs.getModuleDetails(mid,pid, True, db, self.log, src, cherrypy.request)       
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: moddetails - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Module details")
        
        return data



    #Get a the list of items in an end path
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allendpathitems(self, _dc = 101, ver = -2, cnf = -2,node = 1, itype = "",online = "False"):

#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        src = 0

        request = cherrypy.request

        patsMap = None
        seqsMap = None
        modsMap = None
        oumodsMap = None
        cnfMap = None

        if online == 'file':
            if(itype == 'pat'):
                data = self.par_funcs.getEndPathItemsFromFile(ver,int(node), self.config_dict)
            else:
                data = self.par_funcs.getEndPathsFromFile(ver, self.config_dict)

            if (data == None):
                self.log.error('ERROR: allendpathitems - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the EndPath and its modules/sequences")
            return data

        else:
            if online == 'True' or online == 'true':
                db = db_online

                patsMap = self.patsMap_online
                seqsMap = self.seqsMap_online
                modsMap = self.modsMap_online
                oumodsMap = self.oumodsMap_online
                cnfMap = self.cnfMap_online
                src = 1

            else:
                db = db_offline

                patsMap = self.patsMap
                seqsMap = self.seqsMap
                modsMap = self.modsMap
                oumodsMap = self.oumodsMap
                cnfMap = self.cnfMap
                src = 0

        data = None
        node = int(node)
        ver = int(ver)
        cnf = int(cnf)

        #Pathitems request
        if(itype == 'pat'):
            data = self.funcs.getEndPathItems(node, ver, db, self.log, request, src)

        else:
            data = self.funcs.getEndPaths(cnf, ver, db, self.log, request, src)

        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allendpathitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the EndPath and its modules/sequences")

        return data

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def outmoddetails(self, _dc = 101, mid = 0, pid = 0,online = "False", verid = -1):

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        src = 0

        oumodsMap = None
        patsMap = None

        if online == 'file':
            data = self.par_funcs.getOutmodDetails(verid, int(mid), self.config_dict)
            if (data == None):
                self.log.error('ERROR: outmoddetails - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the Output Module Details")
            return data

        else:
            if online == 'True' or online == 'true':
                db = db_online
                oumodsMap = self.oumodsMap_online
                patsMap = self.patsMap_online
                src = 1

            else:
                db = db_offline
                oumodsMap = self.oumodsMap
                patsMap = self.patsMap
                src = 0


        mid = int(mid)
        pid = int(pid)

        # id_m = oumodsMap.get(mid)
        # id_p = patsMap.get(pid)

        # data = self.funcs.getOUTModuleDetails(id_m,id_p,db, self.log)
        data = self.funcs.getOUTModuleDetails(mid,pid,db, self.log, cherrypy.request, src)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: outmoddetails - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Output Module Details")

        return data

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allgpsets(self, _dc = 101, ver = -2, cnf = -2, node = -1,online = "False"):
       # db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        src = 0

        cnfMap = None
        gpsMap = None

        if online == 'file':
            data = self.par_funcs.getGPsetsFromFile(ver, self.config_dict)
            if (data == None):
                self.log.error('ERROR: allgpsets - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the Global PSets")
            return data

        else:
            if online == 'True' or online == 'true':
                db = db_online
                cnfMap = self.cnfMap_online
                gpsMap = self.gpsMap_online
                src = 1

            else:
                db = db_offline
                cnfMap = self.cnfMap
                gpsMap = self.gpsMap
                src = 0


        cnf = int(cnf)
        ver = int(ver)
        # cnf = cnfMap.get(cnf)
        # data = self.funcs.getAllGlobalPsets(cnf, ver, gpsMap, db, self.log)
        data = self.funcs.getAllGlobalPsets(cnf, ver, db, self.log, cherrypy.request, src)
        if (data == None):
            # print ("Exception - Error")
            self.log.error('ERROR: allgpsets - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Global PSets")

        return data

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allgpsetitems(self, _dc = 101, node = 1, gid = -2, verid = -1, online = "False"):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        src = 0

        gpsMap = None

        if online == 'file':
            data = self.par_funcs.getGPsetsItemsFromFile(verid, int(gid), self.config_dict)
            if (data == None):
                self.log.error('ERROR: allgpsetitems - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the Global PSet Parameters")

            return data

        else:
            if online == 'True' or online == 'true':
                db = db_online
                gpsMap = self.gpsMap_online
                src = 1

            else:
                db = db_offline
                gpsMap = self.gpsMap
                src = 0

        gid = int(gid)

        # id_s = gpsMap.get(gid)
        # data = self.funcs.getGpsetItems(id_s, db, self.log)
        data = self.funcs.getGpsetItems(gid, db, self.log, cherrypy.request, src)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allgpsetitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Global PSet Parameters")

        return data

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def edsource(self, _dc = 101, node = -2, ver = -2, cnf = -2,online = "False"):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        src = 0

        cnfMap = None

        if online == 'file':
            data = self.par_funcs.getEdSourceFromFile(ver, self.config_dict)
            if (data == None):
               # print ("Exception - Error")
                self.log.error('ERROR: edsource - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the ED Source")

            return data

        else:
            if online == 'True' or online == 'true':
                db = db_online
                cnfMap = self.cnfMap_online
                src = 1

            else:
                db = db_offline
                cnfMap = self.cnfMap
                src = 0

        cnf = int(cnf)
        ver = int(ver)
        # cnf = cnfMap.get(cnf)
        # data = self.funcs.getEDSource(cnf,ver,db, self.log)
        data = self.funcs.getEDSource(cnf,ver,db, self.log, cherrypy.request, src)
        if (data == None):
           # print ("Exception - Error")
            self.log.error('ERROR: edsource - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the ED Source")

        return data

    #Get all the Module


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def alledsourceitems(self, _dc = 101, node = -2, mid = -2,online = "False", verid = -1):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        src = 0

        if online == 'file':
            data = self.par_funcs.getEdSourceItemsFromFile(verid, int(mid), self.config_dict)
            if (data == None):
                self.log.error('ERROR: data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the ED Source Parameters")
            return data

        if online == 'True' or online == 'true':
            db = db_online
            src = 1

        else:
            db = db_offline

        mid = int(mid)

        data = self.funcs.getEDSourceItems(mid, db, src, self.log, cherrypy.request)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the ED Source Parameters")

        return data

    #Get all the Module

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def essource(self, _dc = 101, node = -2, ver = -2, cnf = -2,online = "False"):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        src = 0

        cnfMap = None

        if online == 'file':
            data = self.par_funcs.getEsSourcesFromFile(ver, self.config_dict)
            if (data == None):
                self.log.error('ERROR: essource - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the ES Source")

            return data

        else:
            if online == 'True' or online == 'true':
                db = db_online
                cnfMap = self.cnfMap_online
                src = 1

            else:
                db = db_offline
                cnfMap = self.cnfMap
                src = 0

        cnf = int(cnf)
        ver = int(ver)
        # cnf = cnfMap.get(cnf)
        data = self.funcs.getESSource(cnf,ver,db, self.log, cherrypy.request, src)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: essource - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the ES Source")

        return data


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allessourceitems(self, _dc = 101, node = -2, mid = -2,online = "False", verid = -1):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        src = 0

        if online == 'file':
            data = self.par_funcs.getEsSourceItemsFromFile(verid, int(mid), self.config_dict)
            if (data == None):
                self.log.error('ERROR: allessourceitems - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the ES Source Parameters")
            return data

        else:
            if online == 'True' or online == 'true':
                db = db_online
                src = 1
            else:
                db = db_offline
            mid = int(mid)

            data = self.funcs.getESSourceItems(mid, db, src, self.log, cherrypy.request)
            if (data == None):
    #            print ("Exception - Error")
                self.log.error('ERROR: allessourceitems - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the ES Source Parameters")

            return data



    @cherrypy.expose
    @cherrypy.tools.json_out()
    def alldatasetitems(self, _dc = 101, dstid = -2, ver = -2, cnf = -2, node = -1,online = "False"):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        src = 0

        datMap = None
        cnfMap = None
        patsMap = None

        if online == 'file':
            data = self.par_funcs.getDataSetItemsFromFile(ver, int(dstid), self.config_dict)
            if (data == None):
                self.log.error('ERROR: alldatasetitems - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the Paths")
            return data

        else:
            if online == 'True' or online == 'true':
                db = db_online

                datMap = self.datMap_online
                cnfMap = self.cnfMap_online
                patsMap = self.patsMap_online
                src = 1

            else:
                db = db_offline

                datMap = self.datMap
                cnfMap = self.cnfMap
                patsMap = self.patsMap
                src = 0

        cnf = int(cnf)
        ver = int(ver)
        dstid = int(dstid)
        # dstid = datMap.get(dstid)
        # cnf = cnfMap.get(cnf)

        # data = self.funcs.getDatasetItems(patsMap, ver, cnf, dstid, db, self.log)
        data = self.funcs.getDatasetItems(ver, cnf, dstid, db, self.log, cherrypy.request, src)
        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: alldatasetitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Paths")

        return data

    #Get a the list of the stream and the items in it(Dataset and Event content)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allsummarycolumns(self, _dc = 101, ver = -2, cnf = -2, node = -1,online = "False"):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        src = 0

        cnfMap = None

        if online == 'file':
            data = self.par_funcs.getSummaryColumnsFromFile(ver, self.config_dict)
            if (data == None):
                self.log.error('ERROR: alldatasetitems - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the Paths")
            return data

        else:
            if online == 'True' or online == 'true':
                db = db_online
                cnfMap = self.cnfMap_online
                src = 1

            else:
                db = db_offline
                cnfMap = self.cnfMap
                src = 0

        cnf = int(cnf)
        ver = int(ver)
        # cnf = cnfMap.get(cnf)

        data = self.funcs.getSummaryColumns(ver, cnf, db, self.log, cherrypy.request, src)
        if (data == None):
            self.log.error('ERROR: alldatasetitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Paths")

        return data

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allsummaryitems(self, _dc = 101,  ver = -2, cnf = -2, sit = '',node = -1,online = "False"):
#        db = cherrypy.request.db

        db = None
        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline
        src = 0

        cnfMap = None
        sumMap = None

        if online == 'file':
            data = self.par_funcs.getSummaryItemsFromFile(ver, self.config_dict)
            if (data == None):
                self.log.error('ERROR: allsummaryitems - data returned null object')
                cherrypy.HTTPError(500, "Error in retreiving the Stream elements")
            return data

        else:
            if online == 'True' or online == 'true':
                db = db_online

                cnfMap = self.cnfMap_online
                sumMap = self.sumMap_online
                src = 1

            else:
                db = db_offline
                src = 0

                cnfMap = self.cnfMap
                sumMap = self.sumMap

        cnf = int(cnf)
        ver = int(ver)
        # cnf = cnfMap.get(cnf)

        # data = self.funcs.getSummaryItems(sumMap, ver, cnf, db, self.log)
        data = self.funcs.getSummaryItems(sumMap, ver, cnf, db, self.log, cherrypy.request, src)

        if (data == None):
#            print ("Exception - Error")
            self.log.error('ERROR: allstreamitems - data returned null object')
            cherrypy.HTTPError(500, "Error in retreiving the Stream elements")

        return data

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def export(self, _dc = 101,  ver = -2, cnf = -2,online = "False"):
        from LocalConfig import state_dir
        timer = Timer()

        src = 0

        db = None
        cnfMap = None
        if online == 'True' or online == 'true':
            db = cherrypy.request.db_online
            cnfMap = self.cnfMap_online
            src = 1
        else:
            db = cherrypy.request.db_offline
            cnfMap = self.cnfMap
            src = 0

        cnf = int(cnf)
        ver = int(ver)
        # cnf = cnfMap.get(cnf)

        resp = Response()
        schema = ResponseUrlStringSchema()
        resp.success = True
        resp.children = []

        folder = tempfile.mkdtemp(dir = state_dir)
        absolute_filename = self.conv.createConfig(ver, cnf, db, online, folder, cherrypy.request, use_cherrypy = True)
        if absolute_filename is None:
            # handle the case where the dump failed
            resp.success = False
            self.log.info('export failed')
            return schema.dump(resp).data

        relative_filename = absolute_filename[len(state_dir):].lstrip('/')
        config_path = base_url + '/download/?filepath=' + relative_filename
        url = UrlString(1, config_path)
        resp.children.append(url)
        timer.stop()
        self.log.info('export done to file %s in %0.1fs' % (absolute_filename, timer.elapsed))

        return schema.dump(resp).data

    @cherrypy.tools.json_out()
    @cherrypy.expose
    def upload(self, pythonfile = None):
        data = pythonfile.file.read(9999999)

        temp_file = open('temp.py', 'wb')
        temp_file.write(data)
        temp_file.close

        pythonfile = open('temp.py','r')

        # print "My File: ", pythonfile

        config_id = self.config_idgen.getNext()

        config_object = self.inv.readConfig(pythonfile, config_id, self.log)

        self.config_dict[config_id] = config_object

        config_obj = self.config_dict.get(config_id)

        print "CONFIG ID & NAME: ", config_id, config_obj.config_name


        os.unlink('temp.py')

        url = UrlString(config_id,"fake")

        resp = Response()
        schema = ResponseUrlStringSchema()
        resp.success = True
        resp.children = []

        resp.children.append(url)

        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def confname(self, _dc = 101, name = ""):

        db_online = cherrypy.request.db_online
        db_offline = cherrypy.request.db_offline

        cnfMap = None
        db = None
        online = False
        src = 0

        tokens = name.split('=')
        path_tokens = tokens[1].split('/')
        firstFolder = path_tokens[1]

        if firstFolder == 'cdaq' or firstFolder == 'minidaq':

            db = db_online
            cnfMap = self.cnfMap_online
            online = 'true'
            src = 1

        else:
            db = db_offline
            cnfMap = self.cnfMap
            online = 'false'
            src = 0

        config_id = self.funcs.getRoutedConfig(cnfMap, tokens[1], db, self.log, src, cherrypy.request)

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
        from LocalConfig import state_dir
        absolute_filename = state_dir + "/" + filepath
        return serve_file(absolute_filename, "application/x-download", "attachment")

    index.exposed = True


if __name__ == '__main__':

#    from cherrypy.process.plugins import DropPrivileges
#    dr = DropPrivileges(cherrypy.engine, uid=1000, gid=1000)
#    dr = DropPrivileges(cherrypy.engine) #-- UNCOMMENT
#    dr.subscribe() #-- UNCOMMENT

#    from cherrypy.process.plugins import Daemonizer  # -- UNCOMMENT
#    d = Daemonizer(cherrypy.engine)  # -- UNCOMMENT
#    d.subscribe()  # -- UNCOMMENT

    # Load configuration
    from Config import *
    connectionString = ConnectionString()

    # Register the SQLAlchemy plugin
    from sqlalchemy_plugin.saplugin import SAEnginePlugin
    SAEnginePlugin(cherrypy.engine, connectionString).subscribe()

    # Register the SQLAlchemy tool
    from sqlalchemy_plugin.satool import SATool
    cherrypy.tools.db = SATool(current_dir,cherrypy.log)

    root = Root()
    root.download = Download()
    
    # make sure the log files directory exists
    deploy_env = os.environ.get('DEPLOY_ENV')
    if deploy_env != "CMSWEB":
        if 'log.access_file' in cpconfig:
            d = os.path.dirname(cpconfig['log.access_file'])
            if not os.path.exists(d):
                os.makedirs(d)
        if 'log.error_file' in cpconfig:
            d = os.path.dirname(cpconfig['log.error_file'])
            if not os.path.exists(d):
                os.makedirs(d)

    cherrypy.config.update(cpconfig)
    cherrypy.quickstart(root, base_url, {'/': {'tools.db.on': True}}) #Root()
