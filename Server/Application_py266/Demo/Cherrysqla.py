# -*- coding: utf-8 -*-
import cherrypy
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.sql import select
from sqlalchemy.sql import text
from sqlalchemy import Sequence
from operator import attrgetter
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from saplugin import Version, Pathidconf, Pathids, Paths, Response, Parameter, ResponseTree, Pathitems, Pathitem, Pathelement, ResponseTreeItem, Modelement, Parameter, Moduleitem, ModTelement, ModToTemp, ModTemplate, Directory, Configuration, FolderItem, Moduletypes, ModuleDetails #AddressUser #Module,
import json
from schema import * #PathsSchema, ModuleSchema, ResponseSchema, ParameterSchema, ResponseParamsSchema, ResponsePathsSchema, ResponsePathTreeSchema, PathsTreeSchema, PathsItemSchema, ResponsePathItemsSchema, ResponsePathItemSchema, ResponseParamSchema, ParameterSchema
from collections import OrderedDict
from utils import * #Counter, ModulesDict, SequencesDict, PathsDict

import os.path
current_dir = os.path.dirname(os.path.abspath(__file__))

metadata = MetaData()    
    
class Root(object):
    
    idgen = Counter()
    idfolgen = FolderItemCounter()
    
    cnfMap = ConfigsDict()
    folMap = FoldersDict()
    
    patsMap = PathsDict()
    seqsMap = SequencesDict()
    modsMap = ModulesDict()
    
    #def __init__(self):
    #    self.types = dict()
    #    db = cherrypy.request.db
    #    for row in db.query(Paetypes).all():
    #        self.types[row.id] = row.name    
    _cp_config = {'tools.staticdir.on' : True,
                  'tools.staticdir.root': current_dir,
                  'tools.staticdir.dir' : 'Demo110315', #ModParams #/Users/vdaponte/Sites/
                  'tools.staticdir.index' : 'index.html',
    }

    @cherrypy.expose
    def index(self):
        # Get the SQLAlchemy session associated
        # with this request.
        # It'll be released once the request
        # processing terminates
        db = cherrypy.request.db
        #self.table = Table("u_confversions", metadata, Column('id', Integer, primary_key=True), autoload=True)
        ver = db.query(Version).first()
        print ver.id
        print ver.name
        print ver.id_release
        return "Hello World"
    
    #Get a the list of items in a path 
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allpathitems(self, _dc=101, ver=-2, cnf=-2,node=1, itype=""):
        db = cherrypy.request.db

        if(itype == 'pat'):
            print "IN PAT, VER: ",ver
            node = int(node) 
            
            id_p = 0
            id_p = self.patsMap.get(node)
            
            ver = int(ver)
            
            resp = Response()
            schema = ResponsePathItemSchema()
            #Retreive all the sequences and their items of the path
            elements = db.query(Pathelement).from_statement(text("SELECT "
                            + "u_paelements.id, "
                            + "u_paelements.name, "
                            + "u_paelements.paetype "                                 
        #						+ "u_pathid2pae.id_parent,"
        #						+ "u_pathid2pae.ord, "                       
        #						+ "DECODE(u_paelements.paetype,1, 'Module', 2, 'Sequence', 3, 'OutputModule', 'Undefined') AS entry_type, "                    
        #						+ "u_pathid2pae.operator "                       
                            + "FROM u_pathid2pae, u_paelements, u_pathid2conf "
                            + "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid " 
                            + "and u_pathid2pae.id_pathid=:node "
                            + "and u_pathid2pae.id_pae=u_paelements.id "
                            + "and ((u_pathid2pae.lvl=0 and u_paelements.paetype=2) or u_pathid2pae.lvl>0) "
                            + "and u_pathid2conf.id_confver=:leng "
                            + "order by u_pathid2pae.id ")).params(node=id_p, leng=ver).all()
            
            items = db.query(Pathitems).from_statement(text("SELECT "
                            + "u_pathid2pae.id, "
        #						+ "u_paelements.name, "
        #                        + "u_paelements.paetype, "
                            + "u_pathid2pae.id_pathid, "                                                             
                            + "u_pathid2pae.id_pae, "                                                        
                            + "u_pathid2pae.id_parent,"
                            + "u_pathid2pae.lvl, " 
                            + "u_pathid2pae.ord "                                             
        #						+ "DECODE(u_paelements.paetype,1, 'Module', 2, 'Sequence', 3, 'OutputModule', 'Undefined') AS entry_type, "                    
        #						+ "u_pathid2pae.operator "                       
                            + "FROM u_pathid2pae,u_paelements, u_pathid2conf  "
                            + "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid " 
                            + "and u_pathid2pae.id_pathid=:node "
                            + "and u_pathid2pae.id_pae=u_paelements.id "
                            + "and ((u_pathid2pae.lvl=0 and u_paelements.paetype=2) or u_pathid2pae.lvl>0) "
                            + "and u_pathid2conf.id_confver=:leng "
                            + "order by u_pathid2pae.id ")).params(node=id_p, leng=ver).all()

            print "RESULTSSSS: ", len(items), len(elements)

            items_dict = dict((x.id, x) for x in items)
            
#            temps = items_dict.keys()
#            print "KEYSSSSS:"
#            for t in temps:
#                print t
            
            elements_dict = dict((x.id, x) for x in elements)
            seq = {}
            #Build all the sequences 

            for p in items:
                elem = elements_dict[p.id_pae]
                item = Pathitem(p.id_pae, elem.name, p.id_pathid, elem.paetype, p.id_parent, p.lvl, p.order)
                if (item.paetype == 2):
                    item.gid = self.seqsMap.put(self.idgen,elem)                    
                    item.expanded = False
                    seq[item.id]=item
                
                # It is a module
                else:
#                    item.id += 10000
                    item.gid = self.modsMap.put(self.idgen,elem)
                    seq[p.id_parent].children.insert(p.order, item)

            seqs = seq.values #viewvalues()
            for s in seqs:
                if (s.lvl != 0):
                    seq[s.id_parent].children.insert(s.order, s)

        #        for ss in seq.values #viewvalues(): 
        #            print ss.id

            #Retreive the lvl 0 of the path
            lista = db.query(Pathitems).from_statement(text("SELECT "
                            + "u_pathid2pae.id, "
        #						+ "u_paelements.name, "
        #                        + "u_paelements.paetype, "
                            + "u_pathid2pae.id_pathid, " 
                            + "u_pathid2pae.id_pae, "                                                        
                            + "u_pathid2pae.id_parent,"
                            + "u_pathid2pae.lvl, " 
                            + "u_pathid2pae.ord "                                             
        #						+ "DECODE(u_paelements.paetype,1, 'Module', 2, 'Sequence', 3, 'OutputModule', 'Undefined') AS entry_type, "                    
        #						+ "u_pathid2pae.operator "                       
                            + "FROM u_pathid2pae,u_paelements, u_pathid2conf  "
                            + "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid " 
                            + "and u_pathid2pae.id_pathid=:node "
                            + "and u_pathid2pae.id_pae=u_paelements.id "
                            + "and (u_pathid2pae.lvl=0 and u_paelements.paetype!=2) "
                            + "and u_pathid2conf.id_confver=:leng "
                            + "order by u_pathid2pae.id ")).params(node=id_p, leng=ver).all()

            lvlzelems = db.query(Pathelement).from_statement(text("SELECT "
                            + "u_paelements.id, "
                            + "u_paelements.name, "
                            + "u_paelements.paetype "                                 
        #						+ "u_pathid2pae.id_parent,"
        #						+ "u_pathid2pae.ord, "                       
        #						+ "DECODE(u_paelements.paetype,1, 'Module', 2, 'Sequence', 3, 'OutputModule', 'Undefined') AS entry_type, "                    
        #						+ "u_pathid2pae.operator "                       
                            + "FROM u_pathid2pae, u_paelements, u_pathid2conf "
                            + "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid " 
                            + "and u_pathid2pae.id_pathid=:node "
                            + "and u_pathid2pae.id_pae=u_paelements.id "
                            + "and (u_pathid2pae.lvl=0 and u_paelements.paetype!=2) "
                            + "and u_pathid2conf.id_confver=:leng "
                            + "order by u_pathid2pae.id ")).params(node=id_p, leng=ver).all()

            lvlzelems_dict = dict((x.id, x) for x in lvlzelems)
            pats = []

            for l in lista:
                elem = lvlzelems_dict[l.id_pae]
                item = Pathitem(l.id_pae ,elem.name, l.id_pathid, elem.paetype, l.id_parent, l.lvl, l.order)
                item.gid = self.modsMap.put(self.idgen,elem)
#                item.id += 10000 
                pats.insert(item.order,item)

            #merge the sequences created
            for ss in seq.values: #viewvalues():
#                ss.id += 5000
                pats.insert(ss.order, ss)

            #output = output+"<br>"+pat.name
            resp.success = True
            resp.children = pats
        #Retreive paths
        else:
            resp = ResponseTree()
            schema = ResponsePathTreeSchema()
            
            cnf = int(cnf)
            print "CNF ", cnf
            cnf = self.cnfMap.get(cnf)
            
            #TO COMMENT
#            cnf = 34
            
            ver = int(ver)
            
            ver_id = -1
            
            if((ver == -2) and (cnf == -2)):
                print "VER CNF ERROR"
            
            elif(cnf != -2):
                print "CNF ", cnf
                configs = db.query(Version).from_statement(text("SELECT u_confversions.id, u_confversions.version FROM u_configurations, u_confversions WHERE u_configurations.id = u_confversions.id_config and u_configurations.id=:id_conf")).params(id_conf=cnf).all()
                configs.sort(key=lambda par: par.version, reverse=True)
                ver_id = configs[0].id
            
            elif(ver != -2):
                ver_id = ver
            
            pats = db.query(Pathids).from_statement(text("SELECT u_pathids.id, u_pathids.id_path "
						  + "FROM  u_pathids, u_pathid2conf "
						  + "WHERE u_pathids.id = u_pathid2conf.id_pathid "
						  + "AND u_pathid2conf.id_confver=:idv AND u_pathids.isEndPath = 0 order by u_pathid2conf.ord")).params(idv=ver_id).all()
            #output = output+"<br>"+pat.name
            
            for p in pats:
                p.vid = ver_id
                p.gid = self.patsMap.put(self.idgen,p)
#                print "CHIAVE: ",p.gid, " VALORE: ", self.patsMap.get(p.gid)
                
            resp.children = pats  
        
        resp.success = True
        output = schema.dump(resp)
        assert isinstance(output.data, OrderedDict)
        
        #output = output + """</body> </html>""" 
        return output.data
    
    
    #Get a the list of items in a path 
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allmoditems(self, _dc=101, length=1, node=1, mid=0, pid=0):
        db = cherrypy.request.db
        params = []
        mid = int(mid)
        id_p = self.modsMap.get(mid)
        pid = int(pid)
        id_pathid = self.patsMap.get(pid)
        
        print "ID_P: ", id_p, mid
        
        resp = Response()
        schema = ResponseParamSchema()
        
#        try_template_id = db.query(ModToTemp).filter(ModToTemp.id_pae==252).all()
#        print "TRY: ", try_template_id 
        
#        print " Check paelement 463673  " #9240
#        myCheck = db.query(Moduleitem).filter(Moduleitem.id_pae==463673).order_by(Moduleitem.id).all()
#        myCheckT = db.query(ModToTemp).filter(ModToTemp.id_pae==463673).first()
#        myCheckTempelements = db.query(ModTelement).filter(ModTelement.id_modtemp == myCheckT.id).all() 
#        print "ITEMS: ", len(myCheck), "TemplateITEMS: ", len(myCheckTempelements)
        
        #Retreive the module template
        template_id = db.query(ModToTemp).filter(ModToTemp.id_pae==id_p).first()
        print "TID:" ,template_id.id_templ
        template = db.query(ModTemplate).filter(ModTemplate.id==template_id.id_templ).first()
        
        #Retreive template parameters
        tempelements = db.query(ModTelement).filter(ModTelement.id_modtemp==template.id).all()        
        tempelements_dict = dict((x.id, x) for x in tempelements)
        
        print "TLEME: ", len(tempelements)
        
        #Build template parameters
        temp_pset = {}
        temp_vpset = {}
        temp_parents = {}
        temp_parents[0]=-1
        
        #Build all the vpsets/psets 
        
        temp_params = []
        temp_params_dict = {}
        temp_params_name_dict = {}
        
        for p in tempelements:
#            print p.id
            parent = temp_parents.get(p.lvl)
            clvl = p.lvl+1
#            print "TYPE: ", type(p.moetype), p.moetype
            item = Parameter(p.id, p.name, p.value, p.moetype, p.paramtype, parent, p.lvl, p.order, p.tracked)
            item.default = True
            
#            print item
            temp_params_name_dict[item.name] = item
            
            # It is a vpset
            if (item.moetype == 3):
#                item.gid = self.seqsMap.put(self.idgen,elem)
                temp_parents[clvl] = p.id
                item.expanded = False
                temp_vpset[item.id] = item
        
            # It is a pset
            elif (item.moetype == 2):
#                item.gid = self.seqsMap.put(self.idgen,elem)
                temp_parents[clvl] = p.id
                item.expanded = False
                temp_pset[item.id]=item
                if (temp_vpset.has_key(item.id_parent)):                
                    temp_vpset[item.id_parent].children.insert(item.order, item)

            # It is a param
            else:
#                item.gid = self.modsMap.put(self.idgen,elem)
                if(item.lvl == 0):
                    temp_params.insert(item.order,item)
                    temp_params.sort(key=lambda par: par.order)
                else:
                    tps = temp_pset[item.id_parent].children
                    tps.insert(item.order, item)
                    tps.sort(key=lambda par: par.order)
           
        #complete Pset construction
        temp_psets = temp_pset.values #viewvalues() 
        for s in temp_psets:
            if (s.lvl != 0):
                if (temp_pset.has_key(s.id_parent)):
#                    pset[s.id_parent].children.insert(s.order, s)
                    tps = temp_pset[s.id_parent].children
                    tps.insert(s.order, s)
                    tps.sort(key=lambda par: par.order)

        #merge the psets created
        temp_psKeys = temp_pset.keys() #viewkeys()               
        
        for ss in temp_psKeys:
            s = temp_pset.get(ss)
            if(s.lvl==0):
                temp_params.insert(s.order, s)
#                params.sort(key=lambda par: par.order)
        
        #merge the vpsets created
        temp_vpsKeys = temp_vpset.keys() #viewkeys()               
        
        for ss in temp_vpsKeys:
            s = temp_vpset.get(ss)
            if(s.lvl==0):
                temp_params.insert(s.order, s)
        
        temp_params_dict = dict((x.id, x) for x in temp_params)
        
        #------------------------------------------------------------------------------------------------------------
        #Retreive all the parameters of the module
        items = []
        #items = db.query(Moduleitem).filter(Moduleitem.id_pae==id_p).order_by(Moduleitem.id).all()
        
        items = db.query(Moduleitem).from_statement(text("SELECT DISTINCT u_pae2moe.id, u_pae2moe.id_pae, u_pae2moe.id_moe, u_pae2moe.lvl, u_pae2moe.ord "
        + "FROM u_pae2moe, u_pathid2pae "
        + "WHERE u_pae2moe.id_pae =:id_pae "
        + "AND u_pathid2pae.id_pae = u_pae2moe.id_pae "
        + "AND u_pathid2pae.id_pathid =:id_pid "                                                 
        + "ORDER BY u_pae2moe.id_moe")).params(id_pae=id_p, id_pid=id_pathid).all()
        
        print "ITEMS: ", len(items)
        
        moeIds = []
        for it in items:
            moeIds.append(int(it.id_moe))
#            print "ID_MOE: ",it.id_moe
        
        elements = db.query(Modelement).filter(Modelement.id.in_(moeIds)).order_by(Modelement.id).all()
        
        print "ELEMENTS: ", len(elements) 

#        items_dict = dict((x.id, x) for x in items)
        elements_dict = dict((x.id, x) for x in elements)

        pset = {}
        vpset = {}
        parents = {}
        
        parents[0]=-1
        #Build all the vpsets/psets 
        
        not_in = []
        params = []
        pset_name_dict = {}
        vpset_name_dict = {}
        params_mod_name_dict = {}
        
        for p in items:
#            print p.id_moe
            elem = elements_dict[p.id_moe]
            parent = parents.get(p.lvl)
            clvl = p.lvl+1
#            print "TYPE: ", type(elem.moetype), elem.moetype
            item = Parameter(p.id_moe, elem.name, elem.value, elem.moetype, elem.paramtype, parent, p.lvl, p.order, elem.tracked)
             
            params_mod_name_dict[item.name]=item
            #Set default
            if (temp_params_name_dict.has_key(item.name)):
                if temp_params_name_dict.get(item.name).value == item.value:
                    item.default = True
            
            # It is a vpset
            if (item.moetype == 3):
#                item.gid = self.seqsMap.put(self.idgen,elem)
                parents[clvl] = p.id_moe
                item.expanded = False
                vpset[item.id] = item
                vpset_name_dict[item.name]=item
        
            # It is a pset
            elif (item.moetype == 2):
#                item.gid = self.seqsMap.put(self.idgen,elem)
                parents[clvl] = p.id_moe
                item.expanded = False
                pset[item.id]=item
                pset_name_dict[item.name]=item
                if (vpset.has_key(item.id_parent)):                
                    vpset[item.id_parent].children.insert(item.order, item)

            # It is a param
            else:
#                item.gid = self.modsMap.put(self.idgen,elem)
                if(item.lvl == 0):
                    params.insert(item.order,item)
                    params.sort(key=lambda par: par.order)
                else:
                    tps = pset[item.id_parent].children
                    tps.insert(item.order, item)
                    tps.sort(key=lambda par: par.order)
        
        #Check ok temp params
        names = temp_params_name_dict.keys() #viewkeys()
        for pn in names:
            if (not(params_mod_name_dict.has_key(pn))): #The param is not in the module
#                print pn
                not_in.append(temp_params_name_dict.get(pn))
        
        
        #Fill the remaining params from Template
        print "LEN NOT_IN: ", len(not_in)
        print not_in
        if (len(not_in) > 0):
            for n in not_in:
#                print "N: ", n
                if (n.lvl != 0):
                    if (n.id_parent in temp_vpset.keys()): #viewkeys()):
                        if(vpset_name_dict.has_key(temp_vpset.get(n.id_parent).name)):
                            vpset_name_dict.get(temp_vpset.get(n.id_parent).name).children.insert(n.order,n)

                    if (n.id_parent in temp_pset.keys()): #viewkeys()):
                        if(pset_name_dict.has_key(temp_pset.get(n.id_parent).name)):
                            pset_name_dict.get(temp_pset.get(n.id_parent).name).children.insert(n.order,n)
                    
                    else:
                        print "DOVE?: ", n.name," " ,n.id, " ",n.id_parent
        
        #complete Pset construction
        psets = pset.values #viewvalues() 
        for s in psets:
            if (s.lvl != 0):
                if (pset.has_key(s.id_parent)):
#                    pset[s.id_parent].children.insert(s.order, s)
                    tps = pset[s.id_parent].children
                    tps.insert(s.order, s)
                    tps.sort(key=lambda par: par.order)

        #merge the psets created
        psKeys = pset.keys() #viewkeys() #pset.keys() #viewkeys()               
#        psKeys = psKeys.sort()
#        psKeys = psKeys.reverse()
        
        for ss in psKeys:
            s = pset.get(ss)
            if(s.lvl==0):
                params.insert(s.order, s)
#                params.sort(key=lambda par: par.order)
        
        #merge the vpsets created
        vpsKeys = vpset.keys() #viewkeys()               
#        vpsKeys = psKeys.sort()
#        vpsKeys = psKeys.reverse()
        
        for ss in vpsKeys:
            s = vpset.get(ss)
            if(s.lvl==0):
                params.insert(s.order, s)
        
        #Merge the remaining template params
        for p in not_in:
            if(p.lvl==0):
                tp = temp_params_dict.get(p.id)
                params.insert(tp.order, p)
                
        params.sort(key=lambda par: par.order)        

#        print "PARAMS: ", len(params)
#        print "THE PARAMS: ", params
        #output = output+"<br>"+pat.name
        resp.success = True
        resp.children = params
        #Retreive paths

        output = schema.dump(resp)
        assert isinstance(output.data, OrderedDict)
        
        #output = output + """</body> </html>""" 
        return output.data
    
    #Get the directories of the DB                                                   
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def directories(self,_dc=101, node = ""):
        db = cherrypy.request.db
        
        resp = Response()
        schema = ResponseFolderitemSchema()
        
        directories = db.query(Directory).all()    
        
        folder_items_dict ={}
        
        #finding Root
        fRoot = db.query(Directory).filter(Directory.name == "/").first()
        if (fRoot == None):
            print "NO ROOT!!!!!!"
#        rootItem = FolderItem(fRoot.id, fRoot.name, "fol",fRoot.id_parentdir, fRoot.created) 
#        rootItem.gid = self.folMap.put(self.idfolgen,rootItem)
        
        for d in directories:
            f = FolderItem(d.id, d.name, "fol",d.id_parentdir, d.created)
            f.cmpv = 1
            f.gid = self.folMap.put(self.idfolgen,f)
            
#            configs = db.query(Configuration).from_statement(text("SELECT DISTINCT u_configurations.id, u_configurations.name FROM u_configurations JOIN u_confversions ON u_configurations.id = u_confversions.id_config and u_confversions.id_parentdir=:id_par")).params(id_par=d.id).all()

            configs = db.query(Configuration).from_statement(text("SELECT  u_configurations.id, u_configurations.name FROM u_configurations, u_confversions WHERE u_configurations.id = u_confversions.id_config and u_confversions.id_parentdir=:id_par")).params(id_par=d.id).all()            

            if (len(configs) > 0):
#                print "THERE ARE CONFIGS"
                for c in configs:
                    cnf = FolderItem(c.id, c.name, "cnf",d.id, None)
                    cnf.gid = self.cnfMap.put(self.idfolgen,cnf)
                    cnf.cmpv = 2
                    nam = f.name+"/"
                    cnf.new_name = cnf.name.replace(nam,"")
                    f.children.append(cnf)
                
            folder_items_dict[f.id] = f
        
        #Nesting folders
        folKeys = folder_items_dict.keys() #viewkeys()
        for fk in folKeys:
            if (not(fk == fRoot.id)):
                fi = folder_items_dict.get(fk)
                parent_f = folder_items_dict.get(fi.id_parent)
                if(parent_f.id==fRoot.id):
                    parent_f.new_name = "/"
                nam = parent_f.name+"/"
                fi.new_name = fi.name.replace(nam,"") 
                fi_c = parent_f.children
                fi_c.append(fi)
#                fi_c = sorted(fi_c, key=attrgetter('cmpv', 'new_name'))
                fi_c.sort(key=lambda par: par.name)
                

        #Append Root
        resp.success = True
        rootFol = folder_items_dict.get(fRoot.id)
        rootFol.expanded = True
        resp.children = []
        resp.children.append(rootFol)
        
        output = schema.dump(resp)
        assert isinstance(output.data, OrderedDict)

        return output.data

    #Get the directories of the DB                                                   
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def versions(self, _dc=101, cid = 1):
        db = cherrypy.request.db
        
        resp = Response()
        schema = ResponseVersionSchema()
        
        cid = int(cid)
        id_c = self.cnfMap.get(cid)
        
        versions = db.query(Version).filter(Version.id_config == id_c).all()
        
        versions.sort(key=lambda ver: ver.version, reverse=True) 
    
        resp.success = True
        resp.children = versions

        output = schema.dump(resp)
        assert isinstance(output.data, OrderedDict)

        return output.data    
    
    #Get the Module details                                              
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def moddetails(self, _dc=101, mid=0, pid=0):
        db = cherrypy.request.db
        
        resp = Response()
        schema = ResponseModuleDetailsSchema()
                
        mid = int(mid)
        pid = int(pid)
        
        id_m = self.modsMap.get(mid)
        id_p = self.patsMap.get(pid)
#        id_p = mid
        
        print "ID_M: ", id_m, mid
        print "ID_M: ", id_p, pid
        
        #Retreive the module template
        template_id = db.query(ModToTemp).filter(ModToTemp.id_pae==id_m).first()
        print "TID:" ,template_id.id_templ
        template = db.query(ModTemplate).filter(ModTemplate.id==template_id.id_templ).first()
        
        #Template Type
#        mtype = db.query(Moduletypes).filter(Moduletypes.id==template.id_mtype).first()
#        print "T type: " , mtype.mtype
        
        module = db.query(Pathelement).get(id_m)
        
        md = ModuleDetails(mid, module.name, template.id_mtype, "", template.name)
    
        resp.success = True
        resp.children = []
        
        resp.children.append(md)
        
        output = schema.dump(resp)
        assert isinstance(output.data, OrderedDict)

        return output.data
    
    #Get the Module details                                              
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def allmodules(self, _dc=101, ver=-2, cnf=-2):
        db = cherrypy.request.db
        
        resp = Response()
        schema = ResponseModuleDetailsSchema()
            
        cnf = int(cnf)
        print "CNF ", cnf
        cnf = self.cnfMap.get(cnf)
        print "CNF ", cnf
        
        ver = int(ver)
        ver_id = -1
        version = None
        
        if((ver == -2) and (cnf == -2)):
            print "VER CNF ERROR"

        elif(cnf != -2):
            print "CNF ", cnf
            configs = db.query(Version).from_statement(text("SELECT u_confversions.id, u_confversions.version FROM u_configurations, u_confversions WHERE u_configurations.id = u_confversions.id_config and u_configurations.id=:id_conf")).params(id_conf=cnf).all()
            configs.sort(key=lambda par: par.version, reverse=True)
            ver_id = configs[0].id
            version = db.query(Version).get(ver_id)
            print version

        elif(ver != -2):
            ver_id = ver
            version = db.query(Version).get(ver)
            print version
        
        id_rel = version.id_release
        
        modules = db.query(Pathelement).from_statement(text("SELECT UNIQUE u_paelements.id, u_paelements.name "
						+ "FROM u_pathid2pae,u_paelements, u_pathid2conf, u_mod2templ "
						+ "WHERE u_pathid2conf.id_pathid=u_pathid2pae.id_pathid "
						+ "and u_pathid2pae.id_pae=u_paelements.id "
						+ "and u_paelements.paetype=1 "
						+ "and u_mod2templ.id_pae=u_paelements.id "
						+ "and u_pathid2conf.id_confver=:ver order by u_paelements.name")).params(ver = ver_id).all()
        
        
        templates = db.query(ModTemplate).from_statement(text("select u_moduletemplates.id, u_moduletemplates.name, "
						+ " u_moduletemplates.id_mtype "
						+ "from u_moduletemplates, u_modt2rele "
						+ "where u_modt2rele.id_release=:id_rel "
						+ "and u_modt2rele.id_modtemplate=u_moduletemplates.id ")).params(id_rel=id_rel).all()
            
        templates_dict = dict((x.id, x) for x in templates)
        
        md = None
        resp.children = []
        
        for m in modules:
            m2t = db.query(ModToTemp).filter(ModToTemp.id_pae == m.id).first()
            if (templates_dict.has_key(m2t.id_templ)):
                temp = templates_dict.get(m2t.id_templ) 
                md = ModuleDetails(m.id, m.name, temp.id_mtype, "", temp.name)
                md.gid = self.modsMap.put(self.idgen,md)                
                
            else:
                print "ERROR KEY"
            
            if (md != None):
#                print "MD: ", md.gid
                resp.children.append(md)
        
        print "len: ", len(resp.children)
        resp.success = True
        
        output = schema.dump(resp)
        assert isinstance(output.data, OrderedDict)

        return output.data
    
    
if __name__ == '__main__':
    # Register the SQLAlchemy plugin
    from saplugin import SAEnginePlugin
    #SAEnginePlugin(cherrypy.engine, 'oracle://cms_hlt_gdr:convertiMi!@(DESCRIPTION = (LOAD_BALANCE=on) (FAILOVER=ON) (ADDRESS = (PROTOCOL = TCP)(HOST = int2r2-s.cern.ch)(PORT = 10121)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = int2r_nolb.cern.ch)))').subscribe()
    #'sqlite:///my.db' cmsr.cern.ch

    SAEnginePlugin(cherrypy.engine, 'oracle://cms_hlt_gdr_r:convertMe!@(DESCRIPTION = (LOAD_BALANCE=on) (FAILOVER=ON) (ADDRESS = (PROTOCOL = TCP)(HOST = cmsr1-s.cern.ch)(PORT = 10121)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = cms_cond.cern.ch)))').subscribe()
    
    # Register the SQLAlchemy tool
    from satool import SATool
    cherrypy.tools.db = SATool()
    
    cherrypy.quickstart(Root(), '', {'/': {'tools.db.on': True}})
    