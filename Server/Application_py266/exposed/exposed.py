# File exposed.py Description:
# This files contains the implementations of the methods providing responses 
# to the exposed path in the Root class.
# 
# Class: Exposed

from confdb_queries.confdb_queries import ConfDbQueries
from item_wrappers.FolderItem import *
from item_wrappers.ModuleDetails import *
from item_wrappers.Pathitem import *
from item_wrappers.Parameter import *
from item_wrappers.item_wrappers import *
from schemas.responseSchemas import *
from responses.responses import *
from marshmallow import Schema, fields, pprint
#from collections import OrderedDict
from ordereddict import OrderedDict
from params_builder import ParamsBuilder
import string
import re

class Exposed(object):
    
    queries = ConfDbQueries()
    params_builder = ParamsBuilder()
    
    #Returns the path items (Sequences and Modules)
    #@params: patsMap: map of paths database ids
    #         seqsMap: map of sequences database ids
    #         modsMap: map of moduels database ids
    #         idgen: pathites id (gid) generator
    #         gid: path node generated id
    #         ver: version id
    #         db: database session object
    #    
    def getPathItems(self, patsMap = None, seqsMap = None, modsMap = None, idgen = None, gid=-2, ver=-2, db = None, log = None):
        
        #params check
        if (patsMap == None or seqsMap == None or modsMap == None or idgen == None or gid == -1 or db == None or ver == -1):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getPathItems - input parameters error')
        
        queries = self.queries
        
        id_p = 0
        id_p = patsMap.get(gid)

        resp = Response()
        schema = ResponsePathItemSchema()
        #Retreive all the sequences and their items of the path
        
        #DB Queries
        elements = None
        items = None
        
        try:
            elements = queries.getCompletePathSequences(id_p, ver, db, log)
            items = queries.getCompletePathSequencesItems(id_p, ver, db, log)
        except:
            log.error('ERROR: Query Error')
            return None
            
        if (elements == None or items == None):
            return None
        
        #Elements construction
#        print "RESULTS LEN: ", len(items), len(elements)

        items_dict = dict((x.id, x) for x in items)
        elements_dict = dict((x.id, x) for x in elements)
        
        seq = {}
        lvlZeroSeq_Dict = {} 
        idpaes = {} 
        
        #Build all the sequences 
        for p in items:
            elem = elements_dict[p.id_pae]
            item = Pathitem(p.id_pae, elem.name, p.id_pathid, elem.paetype, p.id_parent, p.lvl, p.order)

            if (item.paetype == 2):
                item.gid = seqsMap.put(idgen,elem,p.id_pathid,p.order,p.lvl)
                item.expanded = False
                seq[item.gid]=item 
                idpaes[item.gid]=p.id_pae  
                if (item.lvl == 0): 
                    iid = item.id   
                    lvlZeroSeq_Dict[item.gid] = iid 

            # It is a module
            else:
                item.gid = modsMap.putItem(idgen,elem,p.id_pathid,p.order,p.lvl)
                id_par = item.id_parent 
#                idPae_values = idpaes.viewvalues()
                idPae_values = idpaes.values()
                lKeys = []
                for key, value in idpaes.iteritems(): 
                    if value == id_par:
                        lKeys.append(key)

#                lKey = [key for key, value in idpaes.iteritems() if value == id_par][0]  

                for lKey in lKeys:
                    childs = seq[lKey].children
                    isIn = False
                    for c in childs:
                        if c.id == item.id:
                            isIn = True
                    if not isIn:
                        seq[lKey].children.insert(p.order, item) 
#                seq[p.id_parent].children.insert(p.order, item)

#        seqs = seq.viewvalues()
        seqs = seq.values()
        for s in seqs:
            if (s.lvl != 0):
                id_par = s.id_parent   
                
                lKey = [key for key, value in idpaes.iteritems() if value == id_par][0]   
                
                childs = seq[lKey].children 
                childs.insert(s.order, s) 
                childs.sort(key=lambda x: x.order, reverse=False) 

        #Retreive the lvl 0 of the path
        lista = queries.getLevelZeroPathItems(id_p, ver, db, log)
        lvlzelems = queries.getLevelZeroPaelements(id_p, ver, db, log)

        lvlzelems_dict = dict((x.id, x) for x in lvlzelems)
        pats = []
            
        for l in lista:
            elem = lvlzelems_dict[l.id_pae]
            item = Pathitem(l.id_pae ,elem.name, l.id_pathid, elem.paetype, l.id_parent, l.lvl, l.order)
            item.gid = modsMap.putItem(idgen,elem,l.id_pathid,l.order,l.lvl)
            pats.insert(item.order,item)
                
#        #merge the sequences created
#        for ss in seq.viewvalues():
#            pats.insert(ss.order, ss)
        
        lvlZeroSeq_Dict_keys = lvlZeroSeq_Dict.keys()
        for lzseq in lvlZeroSeq_Dict_keys: #lvlZeroSeq_Dict.viewkeys(): #viewvalues():   
            lzsequence = seq[lzseq] 
            pats.insert(lzsequence.order, lzsequence)  
            
        pats.sort(key=lambda x: x.order, reverse=False)    
        resp.success = True
        resp.children = pats
        
        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)
        
        return output.data
    
    #Returns the path items (Sequences and Modules)
    #@params: patsMap: map of paths database ids
    #         seqsMap: map of sequences database ids
    #         modsMap: map of moduels database ids
    #         idgen: pathites id (gid) generator
    #         gid: path node generated id
    #         ver: version id
    #         db: database session object
    #    
    
    def getEndPathItems(self, patsMap = None, seqsMap = None, modsMap = None, oumodsMap = None, idgen = None, gid=-2, ver=-2, db = None, log = None):
        
        #params check
        if (patsMap == None or seqsMap == None or modsMap == None or oumodsMap == None or idgen == None or gid == -1 or db == None or ver == -1):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getEndPathItems - input parameters error')
        
        queries = self.queries
        
        id_p = 0
        id_p = patsMap.get(gid)

        resp = Response()
        schema = ResponsePathItemSchema()
        #Retreive all the sequences and their items of the path
        
        #DB Queries
        elements = None
        items = None
        
        try:
            elements = queries.getCompletePathSequences(id_p, ver, db, log)
            items = queries.getCompletePathSequencesItems(id_p, ver, db, log)
        except:
            log.error('ERROR: Query Error')
            return None
            
        if (elements == None or items == None):
            return None

#        print "RESULTS LEN: ", len(items), len(elements)

        items_dict = dict((x.id, x) for x in items)
        elements_dict = dict((x.id, x) for x in elements)
        
        seq = {}
        lvlZeroSeq_Dict = {} 
        idpaes = {}

        #Build all the sequences 
        for p in items:
            elem = elements_dict[p.id_pae]
            item = Pathitem(p.id_pae, elem.name, p.id_pathid, elem.paetype, p.id_parent, p.lvl, p.order)
            
            if (item.paetype == 2):
                item.gid = seqsMap.put(idgen,elem,p.id_pathid,p.order,p.lvl) 
                item.expanded = False
                seq[item.gid]=item 
                idpaes[item.gid]=p.id_pae  
                if (item.lvl == 0): 
                    iid = item.id   
                    lvlZeroSeq_Dict[item.gid] = iid 
                    
            # It is a module
            else:
                item.gid = modsMap.putItem(idgen,elem,p.id_pathid,p.order,p.lvl)
                id_par = item.id_parent 
#                idPae_values = idpaes.viewvalues()
                idPae_values = idpaes.values()
                lKeys = []
                for key, value in idpaes.iteritems(): 
                    if value == id_par:
                        lKeys.append(key)

#                lKey = [key for key, value in idpaes.iteritems() if value == id_par][0]  

                for lKey in lKeys:
                    childs = seq[lKey].children
                    isIn = False
                    for c in childs:
                        if c.id == item.id:
                            isIn = True
                    if not isIn:
                        seq[lKey].children.insert(p.order, item) 
#                seq[p.id_parent].children.insert(p.order, item)

        seqs = seq.values() #view
        for s in seqs:
            if (s.lvl != 0):
                id_par = s.id_parent   
                
                lKey = [key for key, value in idpaes.iteritems() if value == id_par][0]  
                
                childs = seq[lKey].children 
                childs.insert(s.order, s)
                childs.sort(key=lambda x: x.order, reverse=False) 

        #Retreive the lvl 0 of the path
        lista = queries.getLevelZeroPathItems(id_p, ver, db, log)
        lvlzelems = queries.getLevelZeroPaelements(id_p, ver, db, log)

        lvlzelems_dict = dict((x.id, x) for x in lvlzelems)
        pats = []

        for l in lista:
            elem = lvlzelems_dict[l.id_pae]
            item = Pathitem(l.id_pae ,elem.name, l.id_pathid, elem.paetype, l.id_parent, l.lvl, l.order)
            item.gid = modsMap.putItem(idgen,elem,l.id_pathid,l.order,l.lvl)
            pats.insert(item.order,item)

        #merge the sequences created
#        for ss in seq.viewvalues():
#            pats.insert(ss.order, ss)
        
        lvlZeroSeq_Dict_keys = lvlZeroSeq_Dict.keys()
        for lzseq in lvlZeroSeq_Dict_keys: #lvlZeroSeq_Dict.viewkeys(): #viewvalues():  
            lzsequence = seq[lzseq] 
            pats.insert(lzsequence.order, lzsequence) 

        #DB Queries
        outmodule = None
        
        try:
            outmodule = queries.getOumStreamid(id_p, db, log)

        except:
            log.error('ERROR: Query getOumStreamid Error')
            return None
            
#        if (outmodule == None):
#            return None
        
        if (outmodule != None):
#            print "OUM " + str(outmodule)
#            print "OUM "+ str(outmodule.id_streamid)
            stream = queries.getStreamid(outmodule.id_streamid, db, log)
            
            oumName = "hltOutput"+stream.name
            oum = Pathitem(outmodule.id_streamid, oumName, outmodule.id_pathid, 3, -1, 0, outmodule.order)

            oum.gid = oumodsMap.put(idgen,oum)  

            pats.insert(oum.order, oum)    
            
        pats.sort(key=lambda x: x.order, reverse=False)        
        resp.success = True
        resp.children = pats
        
        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)
        
        return output.data
    
    
    #Returns the paths
    #@params: patsMap: map of paths database ids
    #         seqsMap: map of sequences database ids
    #         modsMap: map of moduels database ids
    #         idgen: pathites id (gid) generator
    #         cnf: Configuration id (to get the last version)
    #         ver: version id
    #         db: database session object
    #     
    
    def getPaths(self, patsMap = None, cnfMap = None, idgen = None, cnf=-2, ver=-2, db = None, log = None):
        
        #params check
        if (patsMap == None or cnfMap == None or idgen == None or (cnf == -2 and ver == -2) or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getPaths - input parameters error')
        
        queries = self.queries
        resp = ResponseTree()
        schema = ResponsePathTreeSchema()

#        print "VER ", ver
#        print "CNF ", cnf
        
        cnf = cnfMap.get(cnf)
        
#        print "CNF after get ", cnf
        
        ver_id = -1

        version = self.getRequestedVersion(ver, cnf, db)
        ver_id = version.id
                
        #DB Queries
        pats = None
        
        try:
            pats = queries.getPaths(ver_id,db, log)

        except:
            log.error('ERROR: Query getPaths Error')
            return None
            
#        if (pats == None):
#            return None

        for p in pats:
            p.vid = ver_id
            p.gid = patsMap.put(idgen,p)

        resp.children = pats  
        
        resp.success = True
        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)
        
        return output.data
        

    #Returns the end paths
    #@params: patsMap: map of paths database ids
    #         seqsMap: map of sequences database ids
    #         modsMap: map of moduels database ids
    #         idgen: paths id (gid) generator
    #         cnf: Configuration id (to get the last version)
    #         ver: version id
    #         db: database session object
    #     
    
    def getEndPaths(self, patsMap = None, cnfMap = None, idgen = None, cnf=-2, ver=-2, db = None, log = None):
        
        #params check
        if (patsMap == None or cnfMap == None or idgen == None or (cnf == -2 and ver == -2) or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getEndPaths - input parameters error')
        
        queries = self.queries
        resp = ResponseTree()
        schema = ResponsePathTreeSchema()

#        print "VER ", ver
#        print "CNF ", cnf
        
        cnf = cnfMap.get(cnf)
        
#        print "CNF after get ", cnf
        
        ver_id = -1

        version = self.getRequestedVersion(ver, cnf, db)
        ver_id = version.id

        #DB Queries
        pats = None
        
        try:
            pats = queries.getEndPaths(ver_id,db, log)

        except:
            log.error('ERROR: Query getEndPaths Error')
            return None
            
#        if (pats == None):
#            return None
        
        for p in pats:
            p.vid = ver_id
            p.gid = patsMap.put(idgen,p)

        resp.children = pats  
        
        resp.success = True
        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)
        
        return output.data        
        
    #Returns the paths
    #@params: patsMap: map of paths database ids
    #         modsMap: map of moduels database ids
    #         mid: module id
    #         pid: path id
    #         db: database session object
    #     
    
    def getOUModuleItems(self, oumid=-2, db = None, log = None):
        
        #params check
        if (oumid == -2 or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getOUModuleItems - input parameters error')
            
#        print "OUMID: ", oumid     
        id_p = oumid #srvsMap.get(sid)    
#        print "ID_P: ", id_p, oumid
        
        resp = Response()
        schema = ResponseParamSchema()
        
        resp.children = self.params_builder.outputModuleParamsBuilder(oumid, self.queries, db, log)
        
        if (resp.children == None):
            return None
        
        resp.success = True
         #params 

        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)
        
        return output.data
    
    
    
    def getModuleItems(self, mid=-2, db = None, log = None):
        
        #params check
        if (mid == -2 or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getModuleItems - input parameters error')
        
        queries = self.queries
        params = []
        
        id_p = mid
        
        resp = Response()
        schema = ResponseParamSchema()
        
        params = self.params_builder.moduleParamsBuilder(id_p,queries,db,log)
        
        if (params == None):
            return None
        
        resp.success = True
        resp.children = params

        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)
        
        return output.data        

    
    #Returns the directories tree
    #@params: folMap: map of directories database ids
    #         idfolgen: folder id (gid) generator
    #         cnfMap: map of configurations database ids
    #         db: database session object
    #     
    
    def getDirectories(self, folMap = None, idfolgen = None, cnfMap = None, db = None, log = None):
        
        #params check
        if (folMap == None or cnfMap == None or idfolgen == None or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getDirectories - input parameters error')
        
        queries = self.queries
        resp = Response()
        schema = ResponseFolderitemSchema()
        
        #DB Queries
        directories = None
        fRoot = None
        
        try:
            directories =  queries.getAllDirectories(db, log)
            #finding Root
            fRoot = queries.getDirectoryByName("/",db, log)

        except:
            log.error('ERROR: Query getAllDirectories/getDirectoryByName Error')
            return None
            
        if (directories == None or fRoot == None):
            return None

        folder_items_dict ={}
                
        if (fRoot == None):
            log.error('ERROR: No Root Node present') #print "NO ROOT!!!!!!"
        
        for d in directories:
            f = FolderItem(d.id, d.name, "fol",d.id_parentdir, d.created)
            f.cmpv = 1
            f.gid = folMap.put(idfolgen,f)
            
            configs = queries.getConfigsInDir(d.id,db)          

            if (len(configs) > 0):
                for c in configs:
                    cnf = FolderItem(c.id, c.name, "cnf",d.id, None)
                    cnf.gid = cnfMap.put(idfolgen, cnf)
                    cnf.cmpv = 2
                    nam = f.name+"/"
                    cnf.new_name = cnf.name.replace(nam,"")
                    f.children.append(cnf)
                
            folder_items_dict[f.id] = f
        
        #Nesting folders
#        folKeys = folder_items_dict.viewkeys()
        folKeys = folder_items_dict.keys()
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
                fi_c.sort(key=lambda par: par.name)
                

        #Append Root
        resp.success = True
        rootFol = folder_items_dict.get(fRoot.id)
        rootFol.expanded = True
        resp.children = []
        resp.children.append(rootFol)
        
        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data
    
    
    
    #Returns the versions of a given Configurations
    #@params: conf_id: Configuration Table id
    #         db: database session object
    #                                                   
    
    def getVersionsByConfig(self, conf_id = -2, db = None, log = None):
        
        queries = self.queries

        #params check
        if (conf_id == -2 or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getVersionsByConfig - input parameters error')
            
        resp = Response()
        schema = ResponseVersionSchema()
        
        #DB Queries
        versions = None
        
        try:
            versions = queries.getConfVersions(conf_id,db, log)

        except:
            log.error('ERROR: Query getConfVersions Error')
            return None
            
#        if (versions == None):
#            return None
        
        versions.sort(key=lambda ver: ver.version, reverse=True) 
    
        resp.success = True
        resp.children = versions

        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data
    
    #Returns the versions of a given Configurations
    #@params: conf_id: Configuration Table id
    #         db: database session object
    #                                                   
    
    def getVersionDetails(self, cnf = -2, ver = -2, db = None, log = None):
        
        queries = self.queries

        #params check
        if (cnf == -2 or ver == -2 or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getVersionDetails - input parameters error')
            
        resp = Response()
        schema = ResponseVersionSchema()

        #DB Queries
        version = None

        version = self.getRequestedVersion(ver, cnf, db)

        if (version == None):
            return None
        
        resp.success = True
        resp.children = []
        resp.children.append(version)
        
        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data
    
    
    #Returns the details of a Path (Prescale, etc.)
    #@params: 
    #         pat_id: Path id (Path_id Table id)  
    #         db: database session object
    #                                                   
    
    def getPathDetails(self, pat_id = -2, cnf =-2, ver=-2, db = None, log = None):
        
        queries = self.queries

        #params check
        if (pat_id == -2 or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getPathDetails - input parameters error')
            
        resp = Response()
        schema = ResponsePathDetailsSchema() 
        
        #ToDo IdV_er / CNF
        ver_id = -1
        version = None
        
        id_rel = -1
        
        version = self.getRequestedVersion(ver, cnf, db)
        if (version == None):
            return None
        
        ver_id = version.id

        id_rel = version.id_release
        
        
         #DB Queries
        path = None
        prescaleTemplate = None
        prescale = None
        
        try:
            path = queries.getPathName(pat_id,ver_id,db, log)
#            print "PATH: ",path

            prescaleTemplate = queries.getConfPrescaleTemplate(id_rel,db, log)
#            print "PRESCALETEMPLATE: ",prescaleTemplate

            prescale = queries.getConfPrescale(ver_id,prescaleTemplate.id,db, log)
#            print "PRESCALE: ",prescale

        except:
            log.error('ERROR: Query getConfPrescaleTemplate/getPathName/getConfPrescale Error')
            return None
            
#        if (path == None or prescaleTemplate == None or prescale == None):
#            return None
        
        pathName = path.name
#        print "PATHNAME: ",pathName
        
        prescaleParams = []
        labels = None
        found = False
        preRows = None
        values = None
        i = 0
        ppLen = 0
        pd = None
        
        if prescale:
#            print "PRESCALE: ",prescale, " ", type(prescale)
            prescaleParams = self.params_builder.serviceParamsBuilder(prescale.id, self.queries, db, log)
            
            ppLen = len(prescaleParams)
#            print "PARAMS BUILT"

#            print "Getting Labels"
            while (not(found) and i<ppLen):
#                print prescaleParams[i].name
                if (prescaleParams[i].name == "lvl1Labels"):
                    found = True
                else:
                    i+=1
#                    print "i++"
#
#            print "Labels Got"
#            print "Building Labels"

            labels = re.findall(r'"([^"]*)"', prescaleParams[i].value)

#            print "Labels Built"
#            print "Getting Table"
            i = 0
            found = False
            while (not(found) and i<ppLen):
                if (prescaleParams[i].name == "prescaleTable"):
                    found = True
                else:
                    i+=1

            preRows = prescaleParams[i].children
            pathName = "\""+pathName+"\""

#            print "Got Table row"
#            print "Getting values"
#            print "PREROWS LEN: "+str(len(preRows))+" PPLEN: "+str(ppLen)
            i = 0
            found = False
            ppLen = len(preRows) 
            while (not(found) and i<ppLen):
                if (preRows[i].children[0].value == pathName):
                    found = True
                else:
                    i+=1
            if(found):        
                values = map(int, re.findall('\d+', preRows[i].children[1].value)) 

#                print "GOt values"

                if(not(len(labels) == len(values))):
                    log.error('ERROR: Prescale rown NOT SAME CARDINALITY')
#                    print "ERROR NOT SAME CARDINALITY"

                pd = PathDetails(path.id, path.name, labels, values, "", "")
            else: 
                labels_len = len (labels) 
                vals = [1] * labels_len 
                pd = PathDetails(path.id, path.name, labels, vals, "", "") 
            
        else:
            prescaleParams = self.params_builder.serviceTemplateParamsBuilder(prescaleTemplate.id, self.queries, db,log)

#            print "Getting Labels"
            while (not(found) and i<ppLen):
                print prescaleParams[i].name
                if (prescaleParams[i].name == "lvl1Labels"):
                    found = True
                else:
                    i+=1
                    print "i++"
            if found:
#                print "Labels Got"
            else:
                log.error('ERROR: Prescale label not found') #print "labels not found"
#            print "Building Labels"

            labels = re.findall(r'"([^"]*)"', prescaleParams[i].value)
            
            if len(labels):
#                print "Labels Built"
            else:
                log.error('WARNING: No Prescales label found') #print "labels empty"
                
#            print "Getting Table"

            values = [0]

            if(not(len(labels) == len(values))):
                log.error('ERROR: Prescale labels have not same values cardinality')
#                print "LABELS LEN: ",len(labels)
#                print "ERROR NOT SAME CARDINALITY"

            pd = PathDetails(path.id, path.name, labels, values, "", "")
        
    
        resp.success = True
        resp.children = []
        
        resp.children.append(pd)
        
        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data
    
    
    
    #Returns the details of a Module (template class, Type, etc.)
    #@params: mod_id: Module id (Modulelement Table id)
    #         pat_id: Path id (Path_id Table id)  
    #         db: database session object
    #                                                   
    
    def getModuleDetails(self, mod_id = -2, pat_id = -2, db = None, log = None):
        
        queries = self.queries

        #params check
        if (mod_id == -2 or pat_id == -2 or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getModuleDetails - input parameters error')
            
        resp = Response()
        schema = ResponseModuleDetailsSchema()
        
        #Retreive the module template
        template_id = None
        template = None
        module = None
        
        try:
            template_id = queries.getModToTempByPae(mod_id,db, log)
#            print "TID:" ,template_id.id_templ 
            template = queries.getModTemplate(template_id.id_templ,db, log)
        
            module = queries.getPaelement(mod_id,db, log)

        except:
            log.error('ERROR: Query getModToTempByPae/getModTemplate/getPaelement Error')
            return None
            
#        if (template_id == None or template == None or module == None):
#            return None

        md = ModuleDetails(mod_id, module.name, template.id_mtype, "", template.name)
    
        resp.success = True
        resp.children = []
        
        resp.children.append(md)
        
        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data
    
    #Returns all the modules present in a Configuration version
    # If a Config id is given, it will retrieve the last version
    #@params: conf_id: Configuration Table id
    #         db: database session object
    #                                                   
    
    def getAllModules(self, cnf = -2, ver = -2, modsMap = None, idgen = None, db = None, log = None):
        
        queries = self.queries

        #params check
        if ((cnf == -2 and ver == -2) or modsMap == None or idgen == None or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getAllModules - input parameters error')
            
        resp = Response()
        schema = ResponseModuleDetailsSchema()
        
        ver_id = -1
        version = None
        
        version = None
        version = self.getRequestedVersion(ver, cnf, db)
        if (version == None):
            return None
        
        ver_id = version.id
                
        id_rel = version.id_release
        
        #Retreive the module template
        modules = None
        templates = None
        m2ts = None
        
        try:
#            print "Getting Modules"
            modules = queries.getConfPaelements(ver_id,db, log)
#            print "Getting Templates"
            templates = queries.getRelTemplates(id_rel,db, log)
            
            m2ts = queries.getMod2TempByVer(ver_id,db, log)

        except:
            log.error('ERROR: Query getConfPaelements/getRelTemplates/getMod2TempByVer Error')
            return None
            
#        if (modules == None or templates == None or m2ts == None):
#            return None
 
        templates_dict = dict((x.id, x) for x in templates)
        modules_dict = dict((x.id, x) for x in modules)

        mod2temps_dict = dict((x.id_pae, x.id_templ) for x in m2ts)
        
        md = None
        resp.children = []
        
#        print "Building Modules"
        for m in modules:
            m2t = mod2temps_dict.get(m.id)
            if (templates_dict.has_key(m2t)):
                temp = templates_dict.get(m2t) 
                md = ModuleDetails(m.id, m.name, temp.id_mtype, "", temp.name)
                md.gid = modsMap.putModule(idgen,md)                
                
            else:
                log.error('ERROR: Module key error') #print "ERROR KEY"
            
            if (md != None):
                resp.children.append(md)
        
#        print "len: ", len(resp.children)
        resp.success = True
        
        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data
    
    
    #Returns all the services present in a Configuration version
    # If a Config id is given, it will retrieve the last version
    #@params: cnf: Configuration Table id
    #         db: database session object
    #                                                   
    def getAllServices(self, cnf = -2, ver = -2, srvsMap = None, idgen = None, db = None, log = None):
        
        queries = self.queries

        #params check
        if ((cnf == -2 and ver == -2) or srvsMap == None or idgen == None or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getAllServices - input parameters error')
            
        resp = Response()
        schema = ResponseServiceSchema()
        
        ver_id = -1
        
        version = None
        version = self.getRequestedVersion(ver, cnf, db)
        if (version == None):
            return None
        
        ver_id = version.id

        id_rel = version.id_release
        
        #Retreive the module template
        services = None
        templates = None
        
        try:
            services = queries.getConfServices(ver_id,db, log)
            templates = queries.getRelSrvTemplates(id_rel,db, log)

        except:
            log.error('ERROR: Query getConfServices/getRelSrvTemplates Error')
            return None
            
#        if (services == None or templates == None):
#            return None

        templates_dict = dict((x.id, x) for x in templates)
        
        srv = None
        resp.children = []
        
        for m in services:
            if (templates_dict.has_key(m.id_template)):
                temp = templates_dict.get(m.id_template)
#                print "SER: ", m.id, m.id_template, id_rel, temp.name 
                srv = Service(m.id, m.id_template, id_rel, temp.name, "")
                srv.gid = srvsMap.put(idgen,srv)  
                      
            else:
                log.error('ERROR: Service key error') #print "ERROR KEY"
            
            if (srv != None):
                resp.children.append(srv)
        
        print "len: ", len(resp.children)
        resp.success = True
        
        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data
    
    
    #Returns the service parameters
    #@params: sid: service id
    #         db: database session object
    #     
    def getServiceItems(self, sid=-2, db = None, log = None):
        
        #params check
        if (sid == -2 or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getServiceItems - input parameters error')
            
#        print "SID: ", sid     
        
        id_p = sid #srvsMap.get(sid)    
        
#        print "ID_P: ", id_p, sid
        
        resp = Response()
        schema = ResponseParamSchema()
        
        resp.children = self.params_builder.serviceParamsBuilder(sid, self.queries, db,log)
        if resp.children == None:
            return None
        
        resp.success = True
         #params 

        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)
        
        return output.data
    
    
    #Returns all the streams present in a Configuration version
    # If a Config id is given, it will retrieve the last version
    #@params: cnf: Configuration Table id
    #         ver: Version Table id    
    #         db: database session object
    # 
    
    def getStreamsItems(self, evcMap, idstrgen, strMap, datMap, ver=-2, cnf=-2, db = None, log = None):
    
        #params check
        if (ver==-2 or cnf==-2 or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getStreamsItems - input parameters error')
        
        version = None
        version = self.getRequestedVersion(ver, cnf, db)
        if (version == None):
            return None
        ver_id = version.id

        #Retreive the module template
        streams = None
        datasets = None
        relations = None
        evcontents = None
        evCoToStr = None
        
        try:
            streams = self.queries.getConfStreams(ver_id,db, log)
            datasets = self.queries.getConfDatasets(ver_id,db, log)
            relations = self.queries.getConfStrDatRels(ver_id,db, log)

            evcontents = self.queries.getConfEventContents(ver_id,db, log)
    #        evcostatements = self.queries.getConfEventContents(ver_id,db, log)
            evCoToStr = self.queries.getEvCoToStream(ver_id,db, log)

        except:
            log.error('ERROR: Query getConfStreams/getConfDatasets/getConfStrDatRels/getConfEventContents/getEvCoToStream Error')
            return None
            
#        if (streams == None or datasets == None or relations == None or evcontents == None or evCoToStr == None):
#            return None

        relations_dict = dict((x.id_datasetid, x.id_streamid) for x in relations)
        streams_dict = dict((x.id, x) for x in streams)
        evCoToStr_dict = dict((x.id_streamid, x.id_evcoid) for x in evCoToStr)
        
#        print "EVCO LEN: ",len(evcontents) , " STREAM LEN: ",len(streams), " EVCOTOSTR LEN: ",len(evCoToStr)
        
        #---- Building evco ---------------
        evco_dict = {}
        for e in evcontents:
            si = Streamitem(e.id,-1,e.name,"evc")
            si.gid = evcMap.put(idstrgen,si)
            si.id_stream = -2
            evco_dict[e.id] = si
            
        #---- Building streams and datasets
        evcoOut = []
        streams_dict = {}
        for s in streams:
            si = Streamitem(s.id,s.fractodisk,s.name,"str")
            streams_dict[s.id] = si
            if(evCoToStr_dict.has_key(s.id)):
                evcoid = evCoToStr_dict.get(s.id)
                evco = evco_dict.get(evcoid)
                if (evco.id_stream == -2):
                    evco.id_stream = s.id
                    evco_dict[evco.id] = evco
                    si.children.append(evco)
                else:
                    new_evco = Streamitem(evco.id,-1,evco.name,"evc")
                    new_evco.gid = evcMap.putDouble(idstrgen,new_evco)
                    si.children.append(new_evco)
            else:
                evcoOut.append(si)
                
            si.gid = strMap.put(idstrgen,si)

        for d in datasets:
            if (d.id == -1):
                log.error('WARNING: Unassigned Paths') 
#                print "Unassigned Paths"
            else:
                si = Streamitem(d.id,-1,d.name,"dat")
                si.gid = datMap.put(idstrgen,si)
                streamid = relations_dict.get(d.id)
                streams_dict.get(streamid).children.append(si)

        resp = Response()
        
        resp.children = streams_dict.values()
        resp.children.sort(key=lambda par: par.name)
        resp.children.extend(evcoOut)
        
        schema = ResponseStreamItemSchema()
        
        resp.success = True
         #params 

        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)
        
        return output.data
    
    
    
    #Returns all the statements of a given event content
    #@params: evc: Eventcontentids Table id 
    #         db: database session object
    # 
    
    def getEvcStatements(self, evc=-2, db = None, log = None):
    
        #params check
        if (evc==-2 or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getEvcStatements - input parameters error')
        
        #Retreive the module template
        evcostatements = None
        evcotostats = None
        
        try:
            evcostatements = self.queries.getEvCoStatements(evc,db, log) 
            evcotostats = self.queries.getEvCoToStat(evc,db, log) 

        except:
            log.error('ERROR: Query getEvCoStatements/getEvCoToStat Error')
            return None
            
#        if (evcostatements == None or evcotostats == None):
#            return None

        evcotostats_dict = dict((x.id_stat, x.statementrank) for x in evcotostats)
        
        for st in evcostatements:
            r = evcotostats_dict.get(st.id)
            st.statementrank = r
        
        evcostatements.sort(key=lambda par: par.statementrank)
        
        resp = Response()
        resp.children = evcostatements
        schema = ResponseEvcStatementSchema()
        
        resp.success = True
         #params 

        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)
        
        return output.data  
    
    
    
    #Returns all the modules present in a Configuration version
    # If a Config id is given, it will retrieve the last version
    #@params: conf_id: Configuration Table id
    #         db: database session object
    #                                                   
    
    def getAllESModules(self, cnf = -2, ver = -2, db = None, log = None):
        
        queries = self.queries

        #params check
        if ((cnf == -2 and ver == -2) or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getAllESModules - input parameters error')
            
        resp = Response()
        schema = ResponseESModuleDetailsSchema()
        
        ver_id = -1
        version = None
        
        version = self.getRequestedVersion(ver, cnf, db)
        ver_id = version.id
                
        id_rel = version.id_release
        
        #Retreive the module template
        modules = None
        templates = None
        conf2esm = None
        
        try:
#            print "Getting ES Modules"
            modules = queries.getConfESModules(ver_id,db, log)
#            print "Getting ESM Templates"
            templates = queries.getESMTemplates(id_rel,db, log)

#            print "Getting ESM Conf Rel"
            conf2esm = queries.getConfToESMRel(ver_id,db, log)    

        except:
            log.error('ERROR: Query getConfESModules/getESMTemplates/getConfToESMRel Error')
            return None
            
#        if (modules == None or templates == None or conf2esm == None):
#            return None
        
        templates_dict = dict((x.id, x) for x in templates)
        modules_dict = dict((x.id, x) for x in modules)
        conf2esm_dict = dict((x.id_esmodule, x.order) for x in conf2esm)
        
        esmodules = []
        resp.children = [] 
        
#        print "Building ES Modules"
        for m in modules:
            if (templates_dict.has_key(m.id_template) and conf2esm_dict.has_key(m.id)):
                temp = templates_dict.get(m.id_template)
                c2e = conf2esm_dict.get(m.id)
#                print "ESM: ", m.id, m.id_template, m.name, temp.name, c2e 
                esm = ESModuleDetails(m.id, m.id_template, m.name, temp.name, c2e)
                esm.gid = m.id  
                      
            else:
                log.error('ERROR: ES Modules Error Key') #print "ERROR KEY"
            
            if (esm != None):
                esmodules.append(esm) 
                
        esmodules.sort(key=lambda par: par.order)
        resp.children.extend(esmodules)
        
#        print "len: ", len(resp.children)
        resp.success = True
        
        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data
    
    
    def getESModItems(self, esmid=-2, db = None, log = None):
        
        #params check
        if (esmid == -2 or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getESModItems - input parameters error')
            
#        print "SID: ", esmid     

        resp = Response()
        schema = ResponseParamSchema()
        
        resp.children = self.params_builder.esModuleParamsBuilder(esmid, self.queries, db,log)
        
        if resp.children == None:
            return None
        
        resp.success = True
        #params 

        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)
        
        return output.data
    
    
    def getAllSequences(self, seqsMap = None, modsMap = None, idgen = None, cnf=-2, ver=-2, db = None, log = None):
        
        #params check
        if (seqsMap == None or modsMap == None or idgen == None or cnf == -1 or db == None or ver == -1):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getAllSequences - input parameters error')
        
        queries = self.queries
        
        ver_id = -1
        version = None
        
        version = self.getRequestedVersion(ver, cnf, db)
        ver_id = version.id
        
        id_p = 0
#        id_p = patsMap.get(gid)

        resp = Response()
        schema = ResponsePathItemSchema()
        #Retreive all the sequences and their items of the path

        #Retreive the module template
        elements = None
        items = None
        
        try:
            elements = queries.getConfSequences(ver_id, db, log)
            items = queries.getConfSequencesItems(ver_id, db, log)
        except:
            log.error('ERROR: Query getConfSequences/getConfSequencesItems Error')
            return None
            
#        if (elements == None or items == None):
#            return None
        
#        print "RESULTS LEN: ", len(items), len(elements)

        items_dict = dict((x.id, x) for x in items)
        elements_dict = dict((x.id, x) for x in elements)
        
        seq = {}
        
#        print "Building the Sequences: " 
        #Build all the sequences 
        for p in items:
            elem = elements_dict[p.id_pae]
            item = Pathitem(p.id_pae, elem.name, p.id_pathid, elem.paetype, p.id_parent, p.lvl, p.order)
            if (item.paetype == 2):
                item.gid = seqsMap.put(idgen,elem)                    
                item.expanded = False
                seq[item.id]=item

            # It is a module
            else:
                item.gid = modsMap.put(idgen,elem)
                seq[p.id_parent].children.insert(p.order, item)
        
#        print "Sequences Built" 
#        seqs = seq.viewvalues()
        seqs = seq.values()

        resp.success = True
        resp.children = seqs
        
        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)
        
        return output.data

        
    def getOUTModuleDetails(self, mod_id = -2, pat_id = -2, db = None, log = None):
        
        queries = self.queries

        #params check
        if (mod_id == -2 or pat_id == -2 or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getOUTModuleDetails - input parameters error')
            
        resp = Response()
        schema = ResponseOutputModuleDetailsSchema()
        
#        outmodule = queries.getOumStreamid(pat_id, db)      
        stream = None
        
        try:
            stream = queries.getStreamid(mod_id, db, log)
        except:
            log.error('ERROR: Query getStreamid Error')
            return None
            
#        if (stream == None):
#            return None
        
        oumName = "hltOutput"+stream.name
        oumd = OutputModuleDetails(mod_id, oumName, "", "", stream.name, mod_id)
#        oumd.gid = oumodsMap.put(idgen,oum)
        
        resp.success = True
        resp.children = []
        
        resp.children.append(oumd)
        
        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data
    
    #Returns the Global Pset parameters
    #@params: sid: service id
    #         db: database session object
    #     
    def getGpsetItems(self, sid=-2, db = None, log = None):
        
        #params check
        if (sid == -2 or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getGpsetItems - input parameters error')
            
#        print "SID: ", sid     
        
        id_p = sid #srvsMap.get(sid)    
        
#        print "ID_P: ", id_p, sid
        
        resp = Response()
        schema = ResponseParamSchema()
        
        resp.children = self.params_builder.gpsetParamsBuilder(sid, self.queries, db,log)
        if resp.children == None:
            return None
        
        resp.success = True
         #params 

        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)
        
        return output.data
    
    
    #Returns all the services present in a Configuration version
    # If a Config id is given, it will retrieve the last version
    #@params: cnf: Configuration Table id
    #         db: database session object
    #                                                   
    def getAllGlobalPsets(self, cnf = -2, ver = -2, gpsMap = None, idgen = None, db = None, log = None):
        
        queries = self.queries

        #params check
        if ((cnf == -2 and ver == -2) or gpsMap == None or idgen == None or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getAllGlobalPsets - input parameters error')
            
        resp = Response()
        schema = ResponseGlobalPsetSchema()
        
        ver_id = -1
        version = None
        
        version = self.getRequestedVersion(ver, cnf, db)
        ver_id = version.id

        #DB Query
        gpsets = None
        
        try:
            gpsets = queries.getConfGPsets(ver_id,db, log)
        except:
            log.error('ERROR: Query getConfGPsets Error')
            return None
            
#        if (gpsets == None):
#            return None
        
        gps = None
        resp.children = []
        
        for m in gpsets:
            gps = GlobalPset(m.id, m.name, m.tracked)
            gps.gid = gpsMap.put(idgen,gps)  
            if (gps != None):
                resp.children.append(gps)
            else:
                log.error('ERROR: GPSets Error Key') #print "ERROR GPSET" 
        
        print "len: ", len(resp.children)
        resp.success = True
        
        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data
    
    
    
    
    
    def getEDSource(self, cnf = -2, ver = -2, db = None, log = None):
        
        queries = self.queries

        #params check
        if ((cnf == -2 and ver == -2) or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getEDSource - input parameters error')
            
        resp = Response()
        schema = ResponseEDSourceSchema()
        
        ver_id = -1
        version = None
        
        version = self.getRequestedVersion(ver, cnf, db)
        ver_id = version.id
                
        id_rel = version.id_release

        #DB Query
        modules = None
        templates = None
        conf2eds = None
        
        try:
#            print "Getting ED Sources"
            modules = queries.getConfEDSource(ver_id,db, log)
#            print "Getting EDS Templates"
            templates = queries.getEDSTemplates(id_rel,db, log)

#            print "Getting EDS Conf Rel"
            conf2eds = queries.getConfToEDSRel(ver_id,db, log)    
        except:
            log.error('ERROR: Query getConfEDSource/getEDSTemplates/getConfToEDSRel Error')
            return None
            
#        if (modules == None or templates == None or conf2eds == None):
#            return None

        templates_dict = dict((x.id, x) for x in templates)
        modules_dict = dict((x.id, x) for x in modules)
        conf2eds_dict = dict((x.id_edsource, x.order) for x in conf2eds)
        
        edsources = []
        resp.children = [] 
        
#        print "Building ED Source"
        for m in modules:
            if (templates_dict.has_key(m.id_template) and conf2eds_dict.has_key(m.id)):
                temp = templates_dict.get(m.id_template)
                c2e = conf2eds_dict.get(m.id)
#                print "EDS: ", m.id, m.id_template, temp.name, c2e 
                eds = EDSource(m.id, m.id_template, "Source", temp.name, c2e)
                eds.gid = m.id  
                      
            else:
                log.error('ERROR: ED Source Error Key') #print "ERROR KEY"
            
            if (eds != None):
                edsources.append(eds) 
                
        
        edsources.sort(key=lambda par: par.order)
        resp.children.extend(edsources)
        
#        print "len: ", len(resp.children)
        resp.success = True
        
        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data
    
    def getEDSourceItems(self, edsid=-2, db = None, log = None):
        
        #params check
        if (edsid == -2 or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getEDSourceItems - input parameters error')
            
#        print "SID: ", edsid     

        resp = Response()
        schema = ResponseParamSchema()
        
        resp.children = self.params_builder.edSourceParamsBuilder(edsid, self.queries, db,log)
        resp.success = True
         #params 

        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)
        
        return output.data

    
    def getESSource(self, cnf = -2, ver = -2, db = None, log = None):
        
        queries = self.queries

        #params check
        if ((cnf == -2 and ver == -2) or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getESSource - input parameters error')
            
        resp = Response()
        schema = ResponseESSourceSchema()
        
        ver_id = -1
        version = None
        
        version = self.getRequestedVersion(ver, cnf, db)
        ver_id = version.id
                
        id_rel = version.id_release 
        
        #DB Query
        modules = None
        templates = None
        conf2eds = None
        
        try:
#            print "Getting ES Sources"
            modules = queries.getConfESSource(ver_id,db, log)
            
#            print "Getting ESS Templates"
            templates = queries.getESSTemplates(id_rel,db, log)

#            print "Getting ESS Conf Rel"
            conf2ess = queries.getConfToESSRel(ver_id,db, log)  
        except:
            log.error('ERROR: Query getConfESSource/getESSTemplates/getConfToESSRel Error')
            return None
            
#        if (modules == None or templates == None or conf2eds == None):
#            return None
         
        templates_dict = dict((x.id, x) for x in templates)
        modules_dict = dict((x.id, x) for x in modules)
        conf2ess_dict = dict((x.id_essource, x.order) for x in conf2ess)
        
        essources = []
        resp.children = [] 
        
#        print "Building ES Source"
        for m in modules:
            if (templates_dict.has_key(m.id_template) and conf2ess_dict.has_key(m.id)):
                temp = templates_dict.get(m.id_template)
                c2e = conf2ess_dict.get(m.id)
#                print "ESS: ", m.id, m.id_template, m.name, temp.name, c2e 
                ess = ESSource(m.id, m.id_template, m.name, temp.name, c2e)
                ess.gid = m.id  
                      
            else:
                log.error('ERROR: ES source Key') #print "ERROR KEY"
            
            if (ess != None):
                essources.append(ess) 
                
        
        essources.sort(key=lambda par: par.order)
        resp.children.extend(essources)
        
#        print "len: ", len(resp.children)
        resp.success = True
        
        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data
    
    def getESSourceItems(self, essid=-2, db = None, log = None):
        
        #params check
        if (essid == -2 or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getESSourceItems - input parameters error')
            
#        print "SID: ", essid     

        resp = Response()
        schema = ResponseParamSchema()
        
        resp.children = self.params_builder.esSourceParamsBuilder(essid, self.queries, db,log)
        if resp.children == None:
            return None
        
        resp.success = True
         #params 

        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)
        
        return output.data
    
    def getDatasetItems(self, patsMap, idgen, ver=-2, cnf=-2, dstid=-2, db = None, log = None):
    #params check
        if (ver==-2 or cnf==-2 or dstid == -2 or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getDatasetItems - input parameters error')
        
        resp = ResponseTree()
        schema = ResponseDstPathsTreeSchema()
        
        version = self.getRequestedVersion(ver, cnf, db)
        ver_id = version.id
        
        #DB Query
        paths = None
        
        try:
            paths = self.queries.getDatasetPathids(ver_id, dstid, db, log)
              
        except:
            log.error('ERROR: Query getDatasetPathids Error')
            return None
            
#        if (modules == None or templates == None or conf2eds == None):
#            return None
        
        for p in paths:
            p.vid = ver_id
            p.gid = patsMap.put(idgen,p)

        resp.children = paths  
        
        resp.success = True
        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)
        
        return output.data
    
    
    def getRequestedVersion(self, ver=-2, cnf=-2, db = None, log = None):    
        
        ver_id = -1
        version = None
        queries = self.queries
        
        if((ver == -2) and (cnf == -2)):
#            print "VER CNF ERROR"
            log.error('ERROR: getRequestedVersion - input parameters error')

        elif(cnf != -2 and cnf != -1):
#            print "CNF ", cnf
            configs = queries.getConfVersions(cnf, db, log)
            configs.sort(key=lambda par: par.version, reverse=True)
            ver_id = configs[0].id
            version = queries.getVersion(ver_id,db, log)
#            print version

        elif(ver != -2):
            ver_id = ver
            version = queries.getVersion(ver,db, log)
#            print version
            
        return version
    
    