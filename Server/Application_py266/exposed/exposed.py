# File exposed.py Description:
# This files contains the implementations of the methods providing responses
# to the exposed path in the Root class.
#
# Class: Exposed

from confdb_v2.queries import ConfDbQueries
from item_wrappers.FolderItem import *
from item_wrappers.ModuleDetails import *
from item_wrappers.Pathitem import *
from item_wrappers.Parameter import *
from item_wrappers.item_wrappers import *
from schemas.responseSchemas import *
from responses.responses import *
from marshmallow import Schema, fields, pprint
from marshmallow.ordereddict import OrderedDict
from params_builder import ParamsBuilder
from summary_builder import SummaryBuilder
import string
import re
import itertools

class Exposed(object):

    queries = ConfDbQueries()
    params_builder = ParamsBuilder()
    summary_builder = SummaryBuilder()
    simple_counter = 0

    #Returns the path items (Sequences and Modules)
    #@params: patsMap: map of paths database ids
    #         seqsMap: map of sequences database ids
    #         modsMap: map of moduels database ids
    #         gid: path node generated id
    #         ver: version id
    #         db: database session object

    def skipPathSequence(self, counter, items, level):
        while(counter < len(items) and items[counter].lvl >= level):
            counter = counter + 1
        return counter

    def getPathSequenceChildren(self, counter, written_sequences, items, elements_dict, level, built_sequences, seqsMap):
        children = []
        while(counter < len(items) and items[counter].lvl == level):
            elem = elements_dict[items[counter].id_pae]
            item = Pathitem(items[counter].id_pae, elem.name, items[counter].id_pathid, elem.paetype, items[counter].id_parent, items[counter].lvl, items[counter].order, items[counter].operator)

            # item.gid = seqsMap.put(idgen,elem,items[counter].id_pathid,items[counter].order,items[counter].lvl,items[counter].id)
            item.gid = seqsMap.put(elem,items[counter].id_pathid,items[counter].order,items[counter].lvl)
            self.simple_counter = self.simple_counter + 1
            counter = counter + 1
            if item.paetype == 2:
                if item.name in written_sequences:
                    item.expanded = False
                    counter, new_children, written_sequences, built_sequences = self.getPathSequenceChildren(counter, written_sequences, items, elements_dict, item.lvl+1, built_sequences, seqsMap)
                    for child in new_children:
                        item.children.append(child)

                else:
                    item.expanded = False
                    counter, new_children, written_sequences, built_sequences = self.getPathSequenceChildren(counter, written_sequences, items, elements_dict, item.lvl+1, built_sequences, seqsMap)
                    for child in new_children:
                        item.children.append(child)

                    written_sequences.add(item.name)
                    built_sequences.add(item)
                
            children.append(item)
            
        return counter, children, written_sequences, built_sequences

    #
    def getPathItems(self, patsMap, seqsMap, modsMap, gid, ver, db, log):

        if (patsMap == None or seqsMap == None or modsMap == None or gid == -1 or db == None or ver == -1):
            log.error('ERROR: getPathItems - input parameters error' + self.log_arguments(gid=gid, ver=ver))

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

        items_dict = dict((x.id, x) for x in items)
        elements_dict = dict((x.id, x) for x in elements)

        built_sequences = set()
        written_sequences = set()
        lvlZeroSeq_Dict = {}  

        seq = {}
        idpaes = {}

        #                                                                                                                   #                                                    
        # ----------------------------------------------------------------------------------------------------------------- #
        #       New Routine for sequences
        #  

        elements_dict = dict((element.id, element) for element in elements)

        counter = 0
        idgen_new = 1

        while counter < len(items):
            elem = elements_dict[items[counter].id_pae]
            item = Pathitem(items[counter].id_pae, elem.name, items[counter].id_pathid, elem.paetype, items[counter].id_parent, items[counter].lvl, items[counter].order, items[counter].operator)
            # item.gid = seqsMap.put(idgen,elem,items[counter].id_pathid,items[counter].order,items[counter].lvl,items[counter].id)
            item.gid = seqsMap.put(elem,items[counter].id_pathid,items[counter].order,items[counter].lvl)

            self.simple_counter = self.simple_counter + 1
            counter = counter + 1
            
            if item.paetype == 2:
                
                if item.lvl == 0:
                    lvlZeroSeq_Dict[item.gid] = item.id
                
                if item.name in written_sequences:
                    counter = self.skipPathSequence(counter, items, item.lvl+1)
                else:
                    counter, new_children, written_sequences, built_sequences = self.getPathSequenceChildren(counter, written_sequences, items, elements_dict, item.lvl+1, built_sequences, seqsMap)
                    for child in new_children:

                        item.children.append(child)

                    written_sequences.add(item.name)
                    item.expanded = False
                    built_sequences.add(item)




        #                                                                                                                   #                                                    
        # ----------------------------------------------------------------------------------------------------------------- #
        #     

        seq = dict((x.gid, x) for x in built_sequences)

        #Retreive the lvl 0 of the path
        lista = queries.getLevelZeroPathItems(id_p, ver, db, log)
        lvlzelems = queries.getLevelZeroPaelements(id_p, ver, db, log)

        lvlzelems_dict = dict((x.id, x) for x in lvlzelems)
        pats = []

        for l in lista:
            elem = lvlzelems_dict[l.id_pae]
            item = Pathitem(l.id_pae , elem.name, l.id_pathid, elem.paetype, l.id_parent, l.lvl, l.order, l.operator)
            item.gid = modsMap.put(elem, l.id_pathid, l.order, l.lvl)
            pats.insert(item.order, item)

#        #merge the sequences created

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
    #         gid: path node generated id
    #         ver: version id
    #         db: database session object
    #

    def getEndPathItems(self, patsMap, seqsMap, modsMap, oumodsMap, gid, ver, db, log):

        if (patsMap == None or seqsMap == None or modsMap == None or oumodsMap == None or gid == -1 or db == None or ver == -1):
            log.error('ERROR: getEndPathItems - input parameters error' + self.log_arguments(gid=gid, ver=ver))

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
        idpaes = {}

        built_sequences = set()
        written_sequences = set()
        lvlZeroSeq_Dict = {} 

        #                                                                                                                   #                                                    
        # ----------------------------------------------------------------------------------------------------------------- #
        #       New Routine for sequences
        #  

        elements_dict = dict((element.id, element) for element in elements)

        counter = 0
        idgen_new = 1

        while counter < len(items):
            elem = elements_dict[items[counter].id_pae]
            item = Pathitem(items[counter].id_pae, elem.name, items[counter].id_pathid, elem.paetype, items[counter].id_parent, items[counter].lvl, items[counter].order, items[counter].operator)
            # item.gid = seqsMap.put(idgen,elem,items[counter].id_pathid,items[counter].order,items[counter].lvl,items[counter].id)
            item.gid = seqsMap.put(elem,items[counter].id_pathid,items[counter].order,items[counter].lvl)

            self.simple_counter = self.simple_counter + 1
            counter = counter + 1
            
            if item.paetype == 2:
                
                if item.lvl == 0:
                    lvlZeroSeq_Dict[item.gid] = item.id
                
                if item.name in written_sequences:
                    counter = self.skipPathSequence(counter, items, item.lvl+1)
                else:
                    counter, new_children, written_sequences, built_sequences = self.getPathSequenceChildren(counter, written_sequences, items, elements_dict, item.lvl+1, built_sequences, seqsMap)
                    for child in new_children:

                        item.children.append(child)

                    written_sequences.add(item.name)
                    item.expanded = False
                    built_sequences.add(item)


        #                                                                                                                   #                                                    
        # ----------------------------------------------------------------------------------------------------------------- #
        #

        seq = dict((x.gid, x) for x in built_sequences)

        #Retreive the lvl 0 of the path
        lista = queries.getLevelZeroPathItems(id_p, ver, db, log)
        lvlzelems = queries.getLevelZeroPaelements(id_p, ver, db, log)

        lvlzelems_dict = dict((x.id, x) for x in lvlzelems)
        pats = []

        for l in lista:
            elem = lvlzelems_dict[l.id_pae]
            item = Pathitem(l.id_pae , elem.name, l.id_pathid, elem.paetype, l.id_parent, l.lvl, l.order, l.operator)
            item.gid = modsMap.put(elem, l.id_pathid, l.order, l.lvl)
            pats.insert(item.order, item)

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

            oum.gid = oumodsMap.put(oum)

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
    #         cnf: Configuration id (to get the last version)
    #         ver: version id
    #         db: database session object
    #

    def getPaths(self, patsMap, cnfMap, cnf, ver, db, log):

        if (patsMap == None or cnfMap == None or (cnf == -2 and ver == -2) or db == None):
            log.error('ERROR: getPaths - input parameters error' + self.log_arguments(cnf=cnf, ver=ver))

        queries = self.queries
        resp = ResponseTree()
        schema = ResponsePathTreeSchema()

#        print "VER ", ver
#        print "CNF ", cnf

        cnf = cnfMap.get(cnf)

#        print "CNF after get ", cnf

        ver_id = -1

        version = self.getRequestedVersion(ver, cnf, db, log)
        ver_id = version.id

        #DB Queries
        pats = None

        try:
            pats = queries.getPaths(ver_id, db, log)

        except:
            log.error('ERROR: Query getPaths Error')
            return None

#        if (pats == None):
#            return None

        i = 0
        for p in pats:
            p.vid = ver_id
            p.order = i
            p.gid = patsMap.put(p)
            i = i+1

        resp.children = pats

        resp.success = True
        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data


    #Returns the end paths
    #@params: patsMap: map of paths database ids
    #         seqsMap: map of sequences database ids
    #         modsMap: map of moduels database ids
    #         cnf: Configuration id (to get the last version)
    #         ver: version id
    #         db: database session object
    #

    def getEndPaths(self, patsMap, cnfMap, cnf, ver, db, log):

        if (patsMap == None or cnfMap == None or (cnf == -2 and ver == -2) or db == None):
            log.error('ERROR: getEndPaths - input parameters error' + self.log_arguments(cnf=cnf, ver=ver))

        queries = self.queries
        resp = ResponseTree()
        schema = ResponsePathTreeSchema()

#        print "VER ", ver
#        print "CNF ", cnf

        cnf = cnfMap.get(cnf)

#        print "CNF after get ", cnf

        ver_id = -1

        version = self.getRequestedVersion(ver, cnf, db, log)
        ver_id = version.id

        #DB Queries
        pats = None

        try:
            pats = queries.getEndPaths(ver_id, db, log)

        except:
            log.error('ERROR: Query getEndPaths Error')
            return None

#        if (pats == None):
#            return None

        i = 0
        for p in pats:
            p.vid = ver_id
            p.order = i
            p.gid = patsMap.put(p)
            i = i+1

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

    def getOUModuleItems(self, oumid, db, log):

        if (oumid == -2 or db == None):
            log.error('ERROR: getOUModuleItems - input parameters error' + self.log_arguments(oumid=oumid))

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



    def getModuleItems(self, mid, db, log):

        if (mid == -2 or db == None):
            log.error('ERROR: getModuleItems - input parameters error' + self.log_arguments(mid=mid))

        queries = self.queries
        params = []

        id_p = mid

        resp = Response()
        schema = ResponseParamSchema()

        params = self.params_builder.moduleParamsBuilder(id_p, queries, db, log)

        if (params == None):
            return None

        resp.success = True
        resp.children = params

        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data


    #Returns the directories tree
    #@params: folMap: map of directories database ids
    #         cnfMap: map of configurations database ids
    #         db: database session object
    #

#    def getDirectories(self, folMap, cnfMap, db, log):
#
#        if (folMap == None or cnfMap == None or db == None):
#            log.error('ERROR: getDirectories - input parameters error')
#
#        queries = self.queries
#        resp = Response()
#        schema = ResponseFolderitemSchema()
#
#        #DB Queries
#        directories = None
#        fRoot = None
#
#        try:
#            directories =  queries.getAllDirectories(db, log)
#            #finding Root
#            fRoot = queries.getDirectoryByName("/", db, log)
#
#        except:
#            log.error('ERROR: Query getAllDirectories/getDirectoryByName Error')
#            return None
#
#        if (directories == None or fRoot == None):
#            return None
#
#        folder_items_dict ={}
#
#        if (fRoot == None):
#            log.error('ERROR: No Root Node present') #print "NO ROOT!!!!!!"
#
#        for d in directories:
#            f = FolderItem(d.id, d.name, "fol", d.id_parentdir, d.created)
#            f.cmpv = 1
#            f.gid = folMap.put(f)
#
#            configs = queries.getConfigsInDir(d.id, db)
#
#            if (len(configs) > 0):
#                for c in configs:
#                    cnf = FolderItem(c.id, c.name, "cnf", d.id, None)
#                    cnf.gid = cnfMap.put(cnf)
#                    cnf.cmpv = 2
#                    nam = f.name+"/"
#                    cnf.new_name = cnf.name.replace(nam,"")
#                    f.children.append(cnf)
#
#            folder_items_dict[f.id] = f
#
#        #Nesting folders
##        folKeys = folder_items_dict.viewkeys()
#        folKeys = folder_items_dict.keys()
#        for fk in folKeys:
#            if (not(fk == fRoot.id)):
#                fi = folder_items_dict.get(fk)
#                parent_f = folder_items_dict.get(fi.id_parent)
#                if(parent_f.id==fRoot.id):
#                    parent_f.new_name = "/"
#                nam = parent_f.name+"/"
#                fi.new_name = fi.name.replace(nam,"")
#                fi_c = parent_f.children
#                fi_c.append(fi)
#                fi_c.sort(key=lambda par: par.name)
#
#
#        #Append Root
#        resp.success = True
#        rootFol = folder_items_dict.get(fRoot.id)
#        rootFol.expanded = True
#        resp.children = []
#        resp.children.append(rootFol)
#
#        output = schema.dump(resp)
#        #assert isinstance(output.data, OrderedDict)
#
#        return output.data

    def getChildrenDirectories(self, id_parent, folMap, cnfMap, db, log):
        if (id_parent == -2 or folMap == None or cnfMap == None or db == None):
            log.error('ERROR: getDirectories - input parameters error' + self.log_arguments(id_parent=id_parent))

        queries = self.queries
        resp = Response()
        resp.children = []
        schema = ResponseFolderitemSchema()

        #DB Queries
        child_directories = None
        configs = None

        dir_id = folMap.get(id_parent)

        try:
            #get Child directories
            child_directories = queries.getChildDirectories(dir_id, db, log)

            #get Child configurations
            configs = queries.getConfigsInDir(dir_id, db, log)

        except Exception as e:
            msg = 'ERROR: Query getChildDirectories/getConfigsInDir Error: ' + e.args[0]
            log.error(msg)
            return None



        for d in child_directories:
            f = FolderItem(d.id, d.name, "fol", d.id_parentdir, d.created)
            f.cmpv = 1
            c_names = f.name.split('/')
            c_names_len = len(c_names)
            c_names_len = c_names_len-1
            f.new_name = c_names[c_names_len]

            dir_childs = []
            cnf_childs = []
            try:
                #get Child directories
                dir_childs = queries.getChildDirectories(d.id, db, log)

                #get Child configurations
                cnf_childs = queries.getConfigsInDir(d.id, db, log)

            except Exception as e:
                msg = 'ERROR: Query getChildDirectories/getConfigsInDir Error: ' + e.args[0]
                log.error(msg)
                return None

            if (len(dir_childs)==0 and len(cnf_childs)==0):
                f.expandable = False
            else:
                f.expandable = True

            f.gid = folMap.put(f)

            resp.children.append(f)

        resp.children.sort(key=lambda par: par.new_name)

        if (len(configs) > 0):
            for c in configs:
                cnf = FolderItem(c.id, c.name, "cnf", dir_id, None)
                cnf.gid = cnfMap.put(cnf)
                cnf.cmpv = 2
                c_names = cnf.name.split('/')
                c_names_len = len(c_names)
                c_names_len = c_names_len-1
                cnf.new_name = c_names[c_names_len]

                resp.children.append(cnf)

        resp.children.sort(key=lambda par: par.new_name)

        resp.success = True
        output = schema.dump(resp)
#        assert isinstance(output.data, OrderedDict)

        return output.data


    def getRootDirectory(self, folMap, cnfMap, folMap_online, db, log):

        if (folMap == None or cnfMap == None or folMap_online == None or db == None):
            log.error('ERROR: getDirectories - input parameters error')

        queries = self.queries
        resp = Response()
        schema = ResponseFolderitemSchema()
        resp.children = []

        directories = None
        fRoot = None

        child_directories = None
        configs = None

        #DB Queries
        try:
            #finding Root
            fRoot = queries.getDirectoryByName("/", db, log)

        except Exception as e:
            msg = 'ERROR: Query getDirectoryByName Error: ' + e.args[0]
            log.error(msg)
            return None

        if (fRoot is None):
            log.error('ERROR: No Root Found Error')
            return None

        rootFol = FolderItem(fRoot.id, "Root/", "fol", fRoot.id_parentdir, fRoot.created)
        rootFol.cmpv = 1
        rootFol.new_name = 'Root'
        rootFol.expandable = True

        rootFol.gid = folMap.put(rootFol)

        try:
            #get Child directories
            child_directories = queries.getChildDirectories(fRoot.id, db, log)

            #get Child configurations
            configs = queries.getConfigsInDir(fRoot.id, db, log)

        except Exception as e:
            msg = 'ERROR: Query getChildDirectories/getConfigsInDir Error: ' + e.args[0]
            log.error(msg)
            return None

        for d in child_directories:
            f = FolderItem(d.id, d.name, "fol", d.id_parentdir, d.created)
            f.cmpv = 1
            c_names = f.name.split('/')
            c_names_len = len(c_names)
            c_names_len = c_names_len-1
            f.new_name = c_names[c_names_len]

            dir_childs = []
            cnf_childs = []

            try:
                #get Child directories
                dir_childs = queries.getChildDirectories(d.id, db, log)

                #get Child configurations
                cnf_childs = queries.getConfigsInDir(d.id, db, log)

            except Exception as e:
                msg = 'ERROR: Query getChildDirectories/getConfigsInDir Error: ' + e.args[0]
                log.error(msg)
                return None

            if (len(dir_childs)==0 and len(cnf_childs)==0):
                f.expandable = False
            else:
                f.expandable = True

            if f.new_name == 'cdaq' or f.new_name == 'minidaq':
                f.gid = folMap_online.put(f)

            else:
                f.gid = folMap.put(f)

            resp.children.append(f)

        resp.children.sort(key=lambda par: par.new_name)

        if (len(configs) > 0):
            for c in configs:
                cnf = FolderItem(c.id, c.name, "cnf", dir_id, None)
                cnf.gid = cnfMap.put(cnf)
                cnf.cmpv = 2
                c_names = cnf.name.split('/')
                c_names_len = len(c_names)
                c_names_len = c_names_len-1
                cnf.new_name = c_names[c_names_len]
#                print 'cnf.new_name: ', cnf.new_name

                resp.children.append(cnf)

        resp.success = True

#        resp.children = []
#        resp.children.append(rootFol)

        output = schema.dump(resp)
#        assert isinstance(output.data, OrderedDict)

        return output.data


    #Returns the versions of a given Configurations
    #@params: conf_id: Configuration Table id
    #         db: database session object
    #

    def getVersionsByConfig(self, conf_id, db, log):

        queries = self.queries

        if (conf_id == -2 or db == None):
            log.error('ERROR: getVersionsByConfig - input parameters error' + self.log_arguments(conf_id=conf_id))

        resp = Response()
        schema = ResponseVersionSchema()

        #DB Queries
        versions = None

        try:
            versions = queries.getConfVersions(conf_id, db, log)

        except Exception as e:
            msg = 'ERROR: Query getConfVersions Error: ' + e.args[0]
            log.error(msg)
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

    def getVersionDetails(self, cnf, ver, db, log):

        queries = self.queries

        if (cnf == -2 or ver == -2 or db == None):
            log.error('ERROR: getVersionDetails - input parameters error' + self.log_arguments(cnf=cnf, ver=ver))

        resp = Response()
        schema = ResponseVersionSchema()

        #DB Queries
        version = None

        version = self.getRequestedVersion(ver, cnf, db, log)

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

    def getPathDetails(self, pat_id, cnf, ver, db, log):

        queries = self.queries

        if (pat_id == -2 or db == None):
            log.error('ERROR: getPathDetails - input parameters error' + self.log_arguments(cnf=cnf, ver=ver, pat_id=pat_id))

        resp = Response()
        schema = ResponsePathDetailsSchema()

        #ToDo IdV_er / CNF
        ver_id = -1
        version = None

        id_rel = -1

        version = self.getRequestedVersion(ver, cnf, db, log)
        if (version == None):
            return None

        ver_id = version.id

        id_rel = version.id_release


         #DB Queries
        path = None
        prescaleTemplate = None
        prescale = None
        description = None
        try:
            path = queries.getPathName(pat_id, ver_id, db, log)
            prescaleTemplate = queries.getConfPrescaleTemplate(id_rel, db, log)
            prescale = queries.getConfPrescale(ver_id, prescaleTemplate.id, db, log)
            description = queries.getPathDescription(pat_id, ver_id, db, log)
        except:
            log.error('ERROR: Query getConfPrescaleTemplate/getPathName/getConfPrescale/getPathDescription Error')
            return None

#        if (path == None or prescaleTemplate == None or prescale == None):
#            return None

        pathName = path.name
        prescaleParams = []
        labels = None
        found = False
        preRows = None
        values = None
        i = 0
        ppLen = 0
        pd = None

        if prescale:
#            print "PRESCALE: ", prescale, " ", type(prescale)
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

                if(not(len(labels) == len(values))):
                    log.error('ERROR: Prescale rown NOT SAME CARDINALITY')

#                pd = PathDetails(path.id, path.name, labels, values, "", "")
                pd = None
                if (description is not None):
                    #description.value
                    pd = PathDetails(path.id, path.name, labels, values, "", description.description)

                else:
                    pd = PathDetails(path.id, path.name, labels, values, "", "")

            else:
                labels_len = len (labels)
                vals = [1] * labels_len
#                pd = PathDetails(path.id, path.name, labels, vals, "", "")
                pd = None
                if (description is not None):
                    #description.value
                    pd = PathDetails(path.id, path.name, labels, vals, "", description.description)

                else:
                    pd = PathDetails(path.id, path.name, labels, vals, "", "")

        else:
            prescaleParams = self.params_builder.serviceTemplateParamsBuilder(prescaleTemplate.id, self.queries, db, log)

#            print "Getting Labels"
            while (not(found) and i<ppLen):
                print prescaleParams[i].name
                if (prescaleParams[i].name == "lvl1Labels"):
                    found = True
                else:
                    i+=1
#                    print "i++"
            if not found:
                log.error('ERROR: Prescale label not found')

#            print "Building Labels"

            labels = re.findall(r'"([^"]*)"', prescaleParams[i].value)

            if len(labels) == 0:
                log.error('WARNING: No Prescales label found')
#            else:


#            print "Getting Table"

            values = [0]

            if(not(len(labels) == len(values))):
                log.error('ERROR: Prescale labels have not same values cardinality')
#                print "LABELS LEN: ", len(labels)
#                print "ERROR NOT SAME CARDINALITY"

#            pd = PathDetails(path.id, path.name, labels, values, "", "")
            pd = None
            if (description is not None):
                #description.value
                pd = PathDetails(path.id, path.name, labels, values, "", description.description)

            else:
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

    def getModuleDetails(self, mod_id, pat_id, db, log):

        queries = self.queries

        if (mod_id == -2 or pat_id == -2 or db == None):
            log.error('ERROR: getModuleDetails - input parameters error' + self.log_arguments(mod_id=mod_id, pat_id=pat_id))

        resp = Response()
        schema = ResponseModuleDetailsSchema()

        #Retreive the module template
        template_id = None
        template = None
        module = None

        try:
            template_id = queries.getModToTempByPae(mod_id, db, log)
#            print "TID:" , template_id.id_templ
            template = queries.getModTemplate(template_id.id_templ, db, log)

            module = queries.getPaelement(mod_id, db, log)

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

    def getAllModules(self, cnf, ver, modsMap, db, log):

        queries = self.queries

        if ((cnf == -2 and ver == -2) or modsMap == None or db == None):
            log.error('ERROR: getAllModules - input parameters error' + self.log_arguments(cnf=cnf, ver=ver))

        resp = Response()
        schema = ResponseModuleDetailsSchema()

        ver_id = -1
        version = None

        version = None
        version = self.getRequestedVersion(ver, cnf, db, log)
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
            modules = queries.getConfPaelements(ver_id, db, log)
#            print "Getting Templates"
            templates = queries.getRelTemplates(id_rel, db, log)

            m2ts = queries.getMod2TempByVer(ver_id, db, log)

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
                md.gid = modsMap.put(md)

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
    def getAllServices(self, cnf, ver, srvsMap, db, log):

        queries = self.queries

        if ((cnf == -2 and ver == -2) or srvsMap == None or db == None):
            log.error('ERROR: getAllServices - input parameters error' + self.log_arguments(cnf=cnf, ver=ver))

        resp = Response()
        schema = ResponseServiceSchema()

        ver_id = -1

        version = None
        version = self.getRequestedVersion(ver, cnf, db, log)
        if (version == None):
            return None

        ver_id = version.id

        id_rel = version.id_release

        #Retreive the module template
        services = None
        templates = None

        try:
            services = queries.getConfServices(ver_id, db, log)
            templates = queries.getRelSrvTemplates(id_rel, db, log)

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
                srv.gid = srvsMap.put(srv)

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
    def getServiceItems(self, sid, db, log):

        if (sid == -2 or db == None):
            log.error('ERROR: getServiceItems - input parameters error' + self.log_arguments(sid=sid))

        id_p = sid

        resp = Response()
        schema = ResponseParamSchema()

        resp.children = self.params_builder.serviceParamsBuilder(sid, self.queries, db, log)
        if resp.children == None:
            return None

        resp.success = True

        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data


    #Returns all the streams present in a Configuration version
    # If a Config id is given, it will retrieve the last version
    #@params: cnf: Configuration Table id
    #         ver: Version Table id
    #         db: database session object
    #

    def getStreamsItems(self, evcMap, strMap, datMap, ver, cnf, db, log):

        if (ver==-2 or cnf==-2 or db == None):
            log.error('ERROR: getStreamsItems - input parameters error' + self.log_arguments(cnf=cnf, ver=ver))

        version = None
        version = self.getRequestedVersion(ver, cnf, db, log)
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
            streams = self.queries.getConfStreams(ver_id, db, log)
            datasets = self.queries.getConfDatasets(ver_id, db, log)
            relations = self.queries.getConfStrDatRels(ver_id, db, log)

            evcontents = self.queries.getConfEventContents(ver_id, db, log)
    #        evcostatements = self.queries.getConfEventContents(ver_id, db, log)
            evCoToStr = self.queries.getEvCoToStream(ver_id, db, log)

        except:
            log.error('ERROR: Query getConfStreams/getConfDatasets/getConfStrDatRels/getConfEventContents/getEvCoToStream Error')
            return None

#        if (streams == None or datasets == None or relations == None or evcontents == None or evCoToStr == None):
#            return None

        relations_dict = dict((x.id_datasetid, x.id_streamid) for x in relations)
        streams_dict = dict((x.id, x) for x in streams)
        evCoToStr_dict = dict((x.id_streamid, x.id_evcoid) for x in evCoToStr)

#        print "EVCO LEN: ", len(evcontents) , " STREAM LEN: ", len(streams), " EVCOTOSTR LEN: ", len(evCoToStr)

        #---- Building evco ---------------
        evco_dict = {}
        for e in evcontents:
            si = Streamitem(e.id,-1, e.name,"evc")
            si.gid = evcMap.put(si)
	    log_msg = "EVCO: " + str(si.gid) + " " + str(e.id) + " " + str(e.name)
	    log.error(log_msg)
            si.id_stream = -2
            evco_dict[e.id] = si

        #---- Building streams and datasets
        evcoOut = []
        streams_dict = {}
        for s in streams:
            si = Streamitem(s.id, s.fractodisk, s.name,"str")
            streams_dict[s.id] = si
            if(evCoToStr_dict.has_key(s.id)):
                evcoid = evCoToStr_dict.get(s.id)
                evco = evco_dict.get(evcoid)
                if (evco.id_stream == -2):
                    evco.id_stream = s.id
                    evco_dict[evco.id] = evco
		    log_msg = "EVCO IN STREAM: " + str(evco.gid) + " " + str(evco.id) + " " + str(evco.name)
            	    log.error(log_msg)
		    evc_get_gid	= evcMap.get(evco.gid)
                    log_msg2 = "EVCO GET ID FROM GID: " + str(evc_get_gid)
                    log.error(log_msg2)
                    si.children.append(evco)
                else:
                    new_evco = Streamitem(evco.id,-1, evco.name,"evc")
                    new_evco.gid = evcMap.put(new_evco, False)
		    log_msg = "EVCO IN STREAM UNIQUE FALSE: " + str(new_evco.gid) + " " + str(new_evco.id) + " " + str(new_evco.name)
		    log.error(log_msg)
		    evc_get_gid = evcMap.get(new_evco.gid)
		    log_msg2 = "EVCO GET ID FROM GID: " + str(evc_get_gid)
		    log.error(log_msg2)
                    si.children.append(new_evco)
            else:
                evcoOut.append(si)

            si.gid = strMap.put(si)

        for d in datasets:
            if (d.id == -1):
                log.error('WARNING: Unassigned Paths')
#                print "Unassigned Paths"
            else:
                si = Streamitem(d.id,-1, d.name,"dat")
                si.gid = datMap.put(si)
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

    def getEvcStatements(self, evc, db, log):

        if (evc==-2 or db == None):
            log.error('ERROR: getEvcStatements - input parameters error' + self.log_arguments(evc=evc))

        #Retreive the module template
        evcostatements = None
        evcotostats = None

        try:
            evcostatements = self.queries.getEvCoStatements(evc, db, log)
            evcotostats = self.queries.getEvCoToStat(evc, db, log)

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

    def getAllESModules(self, cnf, ver, db, log):

        queries = self.queries

        if ((cnf == -2 and ver == -2) or db == None):
            log.error('ERROR: getAllESModules - input parameters error' + self.log_arguments(cnf=cnf, ver=ver))

        resp = Response()
        schema = ResponseESModuleDetailsSchema()

        ver_id = -1
        version = None

        version = self.getRequestedVersion(ver, cnf, db, log)
        ver_id = version.id

        id_rel = version.id_release

        #Retreive the module template
        modules = None
        templates = None
        conf2esm = None

        try:
#            print "Getting ES Modules"
            modules = queries.getConfESModules(ver_id, db, log)
#            print "Getting ESM Templates"
            templates = queries.getESMTemplates(id_rel, db, log)

#            print "Getting ESM Conf Rel"
            conf2esm = queries.getConfToESMRel(ver_id, db, log)

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


    def getESModItems(self, esmid, db, log):

        if (esmid == -2 or db == None):
            log.error('ERROR: getESModItems - input parameters error' + self.log_arguments(esmid=esmid))

        resp = Response()
        schema = ResponseParamSchema()

        resp.children = self.params_builder.esModuleParamsBuilder(esmid, self.queries, db, log)

        if resp.children == None:
            return None

        resp.success = True
        #params

        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data


    def skipSequence(self, counter, items, level):
        while(counter < len(items) and items[counter].lvl >= level):
            counter = counter + 1
        return counter
    
    def getSequenceChildren(self, counter, written_sequences, items, elements_dict, level, built_sequences, idgen_new):
        children = []
        
        while(counter < len(items) and items[counter].lvl == level):
            elem = elements_dict[items[counter].id_pae]
            item = Pathitem(items[counter].id_pae, elem.name, items[counter].id_pathid, elem.paetype, items[counter].id_parent, items[counter].lvl, items[counter].order, items[counter].operator)
            item.gid = self.simple_counter #idgen_new
            self.simple_counter = self.simple_counter + 1
            counter = counter + 1
            if item.paetype == 2:
                if item.name in written_sequences:
                    item.expanded = False     
                    counter, new_children, written_sequences, built_sequences, idgen_new = self.getSequenceChildren(counter, written_sequences, items, elements_dict, item.lvl+1, built_sequences, idgen_new)

                    for child in new_children:
                        item.children.append(child)
                else:
                    item.expanded = False
                    counter, new_children, written_sequences, built_sequences, idgen_new = self.getSequenceChildren(counter, written_sequences, items, elements_dict, item.lvl+1, built_sequences, idgen_new)

                    for child in new_children:
                        item.children.append(child)

                    written_sequences.add(item.name)
                    built_sequences.add(item)
                
            children.append(item)
            
        return counter, children, written_sequences, built_sequences, idgen_new
    
    def getAllSequences(self, cnf, ver, db, log):
        
        #params check
        if (cnf == -1 or db == None or ver == -1):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getAllSequences - input parameters error')
        
        queries = self.queries
        
        ver_id = -1
        version = None
        
        version = self.getRequestedVersion(ver, cnf, db, log)
        ver_id = version.id
        
        id_p = 0
        self.simple_counter = 1

        resp = Response()
        schema = ResponsePathItemSchema()
        #Retreive all the sequences and their items of the path

        try:
            paths    = queries.getPaths(ver_id, db, log)
            endpaths = queries.getEndPaths(ver_id, db, log)
        except Exception as e:
            msg = 'ERROR: getAllSequences: error querying database for Paths and EndPaths:\n' + e.args[0]
            log.error(msg)
        
        built_sequences = set() 
        written_sequences = set()
        elements = None
        items = None

        for path in itertools.chain(paths, endpaths):
            try:
                elements = queries.getCompletePathSequences(path.id, ver_id, db, log)
                items    = queries.getCompletePathSequencesItems(path.id, ver_id, db, log)
            except Exception as e:
                msg = 'ERROR: getSequences: error querying database for getCompletePathSequences and Items:\n' + e.args[0]
                self.logger.error(msg)
#                raise

            elements_dict = dict((element.id, element) for element in elements)

            counter = 0
            idgen_new = 1

            while counter < len(items):
                elem = elements_dict[items[counter].id_pae]
                item = Pathitem(items[counter].id_pae, elem.name, items[counter].id_pathid, elem.paetype, items[counter].id_parent, items[counter].lvl, items[counter].order, items[counter].operator)
                item.gid = self.simple_counter #idgen_new
                self.simple_counter = self.simple_counter + 1
                counter = counter + 1
                if item.paetype == 2:
                    if item.name in written_sequences:
                        counter = self.skipSequence(counter, items, item.lvl+1)
                    else:       
                        counter, new_children, written_sequences, built_sequences, idgen_new = self.getSequenceChildren(counter, written_sequences, items, elements_dict, item.lvl+1, built_sequences, idgen_new)

                        for child in new_children:
                            item.children.append(child)
    
                        written_sequences.add(item.name)
                        item.expanded = False
                        built_sequences.add(item)
        
        resp.success = True
        resp.children = built_sequences
        
        output = schema.dump(resp)
        
        return output.data
        


    def getOUTModuleDetails(self, mod_id, pat_id, db, log):

        queries = self.queries

        if (mod_id == -2 or pat_id == -2 or db == None):
            log.error('ERROR: getOUTModuleDetails - input parameters error' + self.log_arguments(mod_id=mod_id, pat_id=pat_id))

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
#        oumd.gid = oumodsMap.put(oum)

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
    def getGpsetItems(self, sid, db, log):

        if (sid == -2 or db == None):
            log.error('ERROR: getGpsetItems - input parameters error' + self.log_arguments(sid=sid))

#        print "SID: ", sid

        id_p = sid #srvsMap.get(sid)

#        print "ID_P: ", id_p, sid

        resp = Response()
        schema = ResponseParamSchema()

        resp.children = self.params_builder.gpsetParamsBuilder(sid, self.queries, db, log)
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
    def getAllGlobalPsets(self, cnf, ver, gpsMap, db, log):

        queries = self.queries

        if ((cnf == -2 and ver == -2) or gpsMap == None or db == None):
            log.error('ERROR: getAllGlobalPsets - input parameters error' + self.log_arguments(cnf=cnf, ver=ver))

        resp = Response()
        schema = ResponseGlobalPsetSchema()

        ver_id = -1
        version = None

        version = self.getRequestedVersion(ver, cnf, db, log)
        ver_id = version.id

        #DB Query
        gpsets = None

        try:
            gpsets = queries.getConfGPsets(ver_id, db, log)
        except:
            log.error('ERROR: Query getConfGPsets Error')
            return None

#        if (gpsets == None):
#            return None

        gps = None
        resp.children = []

        for m in gpsets:
            gps = GlobalPset(m.id, m.name, m.tracked)
            gps.gid = gpsMap.put(gps)
            if (gps != None):
                resp.children.append(gps)
            else:
                log.error('ERROR: GPSets Error Key') #print "ERROR GPSET"

        print "len: ", len(resp.children)
        resp.success = True

        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data





    def getEDSource(self, cnf, ver, db, log):

        queries = self.queries

        if ((cnf == -2 and ver == -2) or db == None):
            log.error('ERROR: getEDSource - input parameters error' + self.log_arguments(cnf=cnf, ver=ver))

        resp = Response()
        schema = ResponseEDSourceSchema()

        ver_id = -1
        version = None

        version = self.getRequestedVersion(ver, cnf, db, log)
        ver_id = version.id

        id_rel = version.id_release

        #DB Query
        modules = None
        templates = None
        conf2eds = None

        try:
#            print "Getting ED Sources"
            modules = queries.getConfEDSource(ver_id, db, log)
#            print "Getting EDS Templates"
            templates = queries.getEDSTemplates(id_rel, db, log)

#            print "Getting EDS Conf Rel"
            conf2eds = queries.getConfToEDSRel(ver_id, db, log)
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

#        print "Building EDSource"
        for m in modules:
            if (m.id_template in templates_dict and m.id in conf2eds_dict):
                temp = templates_dict[m.id_template]
                c2e = conf2eds_dict[m.id]
                eds = EDSource(m.id, m.id_template, "Source", temp.name, c2e)
                eds.gid = m.id
                edsources.append(eds)
            else:
                log.error('ERROR: EDSource key error')

        edsources.sort(key=lambda par: par.order)
        resp.children.extend(edsources)

#        print "len: ", len(resp.children)
        resp.success = True

        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data

    def getEDSourceItems(self, edsid, db, log):

        if (edsid == -2 or db == None):
            log.error('ERROR: getEDSourceItems - input parameters error' + self.log_arguments(edsid=edsid))

#        print "SID: ", edsid

        resp = Response()
        schema = ResponseParamSchema()

        resp.children = self.params_builder.edSourceParamsBuilder(edsid, self.queries, db, log)
        resp.success = True
         #params

        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data


    def getESSource(self, cnf, ver, db, log):

        queries = self.queries

        if ((cnf == -2 and ver == -2) or db == None):
            log.error('ERROR: getESSource - input parameters error' + self.log_arguments(cnf=cnf, ver=ver))

        resp = Response()
        schema = ResponseESSourceSchema()

        ver_id = -1
        version = None

        version = self.getRequestedVersion(ver, cnf, db, log)
        ver_id = version.id

        id_rel = version.id_release

        #DB Query
        modules = None
        templates = None
        conf2eds = None

        try:
#            print "Getting ES Sources"
            modules = queries.getConfESSource(ver_id, db, log)

#            print "Getting ESS Templates"
            templates = queries.getESSTemplates(id_rel, db, log)

#            print "Getting ESS Conf Rel"
            conf2ess = queries.getConfToESSRel(ver_id, db, log)
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

    def getESSourceItems(self, essid, db, log):

        if (essid == -2 or db == None):
            log.error('ERROR: getESSourceItems - input parameters error' + self.log_arguments(essid=essid))

#        print "SID: ", essid

        resp = Response()
        schema = ResponseParamSchema()

        resp.children = self.params_builder.esSourceParamsBuilder(essid, self.queries, db, log)
        if resp.children == None:
            return None

        resp.success = True
         #params

        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data

    def getDatasetItems(self, patsMap, ver, cnf, dstid, db, log):
        if (ver==-2 or cnf==-2 or dstid == -2 or db == None):
            log.error('ERROR: getDatasetItems - input parameters error' + self.log_arguments(cnf=cnf, ver=ver, dstid=dstid))

        resp = ResponseTree()
        schema = ResponseDstPathsTreeSchema()

        version = self.getRequestedVersion(ver, cnf, db, log)
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
            p.gid = patsMap.put(p)

        resp.children = paths

        resp.success = True
        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data


    def getRequestedVersion(self, ver, cnf, db, log):

        ver_id = -1
        version = None
        queries = self.queries

        if((ver == -2) and (cnf == -2)):
#            print "VER CNF ERROR"
            log.error('ERROR: getRequestedVersion - input parameters error' + self.log_arguments(cnf=cnf, ver=ver))

        elif(cnf != -2 and cnf != -1):
#            print "CNF ", cnf
            configs = queries.getConfVersions(cnf, db, log)
            configs.sort(key=lambda par: par.version, reverse=True)
            ver_id = configs[0].id
            version = queries.getVersion(ver_id, db, log)
#            print version

        elif(ver != -2 and ver != -1):
            ver_id = ver
            version = queries.getVersion(ver, db, log)
#            print version

        return version

    def getSummaryColumns(self, ver, cnf, db, log):

        if (ver==-2 or cnf==-2 or db == None):
            log.error('ERROR: getSummaryColumns - input parameters error' + self.log_arguments(cnf=cnf, ver=ver))

        resp = ResponseTree()
        schema = ResponseSummaryColumnSchema()

        version = self.getRequestedVersion(ver, cnf, db, log)
        columns = self.summary_builder.getPrescaleColumns(version, self.queries, db, log)

        resp.children = columns

        resp.success = True
        output = schema.dump(resp)

        return output.data

    def getSummaryItems(self, sumMap, ver, cnf, db, log):

        if (ver==-2 or cnf==-2 or db == None):
            log.error('ERROR: getStreamsItems - input parameters error' + self.log_arguments(cnf=cnf, ver=ver))

        resp = Response()
        schema = ResponseSummaryItemSchema()

        resp.success = False

        version = None
        version = self.getRequestedVersion(ver, cnf, db, log)
        if (version == None):
            output = schema.dump(resp)
            return output.data

        ver_id = version.id
        id_rel = version.id_release
        columns = self.summary_builder.getPrescaleColumns(version, self.queries, db, log)

        #Retreive the Prescale
        prescaleTemplate = None
        prescale = None

        try:
            prescaleTemplate = self.queries.getConfPrescaleTemplate(id_rel, db, log)

            prescale = self.queries.getConfPrescale(ver_id, prescaleTemplate.id, db, log)

        except:
            log.error('ERROR: Query getConfPrescaleTemplate/getConfPrescale Error')
            output = schema.dump(resp)
            return output.data

        prescaleParams = []
        labels = None
        found = False
        preRows = None
        values = None
        i = 0
        ppLen = 0
        pd = None

        if prescale:
#            print "PRESCALE: ", prescale, " ", type(prescale)
            prescaleParams = self.params_builder.serviceParamsBuilder(prescale.id, self.queries, db, log)

            ppLen = len(prescaleParams)
#            print "PARAMS BUILT"

#            print "Getting Labels"
            while (not(found) and i<ppLen):
                if (prescaleParams[i].name == "lvl1Labels"):
                    found = True
                else:
                    i+=1
#                    print "i++"

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

#            print "Got Table row"

        preRows_dict = {}
        row_i = 0

        if preRows is not None:
            for row in preRows:
                pn = row.children[0].value.translate(None,'"')
                preRows_dict[pn] = row_i
                row_i = row_i+1

        #Retreive the strams and datasets
        streams = None
        datasets = None
        relations = None
        pats = None
        dprels = None
        one_values = []

        try:
            streams = self.queries.getConfStreams(ver_id, db, log)
            datasets = self.queries.getConfDatasets(ver_id, db, log)
            relations = self.queries.getConfStrDatRels(ver_id, db, log)

        except:
            log.error('ERROR: Query getConfStreams/getConfDatasets/getConfStrDatRels/getConfEventContents/getEvCoToStream Error')
            output = schema.dump(resp)
            return output.data
	streams_dict = dict((x.id, x) for x in streams)
        dats_dict = dict((x.id, x) for x in datasets)

        idis = dats_dict.keys()
	str_idis = streams_dict.keys()

#        print "Got stream dat rel"

        pats = None
        dprels = None

        try:

            pats = self.queries.getPaths(ver_id, db, log)
#            print "Got paths"

            dprels = self.queries.getAllDatsPatsRels(ver_id, idis, db, log)
#            print "Got paths dat rels"
	    
	    #get realations output modules - streams
            oumrels = self.queries.getOumStreamRels(ver_id, str_idis, db, log)

            # #get associated end path
            endpaths = self.queries.getEndPathsFromStreams(ver_id, str_idis, db, log)

        except:
            log.error('ERROR: getPaths/getAllDatsPatsRels/getOumStreamRels/getEndPathsFromStreams Error')
            output = schema.dump(resp)
            return output.data

        relations_dict = dict((x.id_datasetid, x.id_streamid) for x in relations)
        #streams_dict = dict((x.id, x) for x in streams)
        pats_dict = dict((x.id, x) for x in pats)
        dprels_dict = {}
	oum_relations_dict = dict((x.id_streamid, x.id_pathid) for x in oumrels)
        endpaths_dict = dict((x.id, x.name) for x in endpaths)

#        print "Got dicts"

        for x in dprels:
#            print 'ID_DSID:', str(x.id_datasetid)
            if x.id_datasetid in dprels_dict.keys():
                dprels_dict[x.id_datasetid].children.append(x.id_pathid)

            else:
                lc = ListContainer()
                lc.children.append(x.id_pathid)
                dprels_dict[x.id_datasetid] = lc

#        print "Got dprels_dict"


        #---- Get l1 Seeds --------------------------------

        l1seeds = self.summary_builder.getL1Seeds(pats_dict.keys(), id_rel, self.queries, db, log)

        if l1seeds is None:
            log.error('ERROR: Seeds None')


        #---- Get Smart Prescales --------------------------------
        smartPre = self.summary_builder.getSmartPrescales(ver_id, id_rel, streams_dict.keys(), self.queries, db, log)

        if smartPre is None:
            log.error('ERROR: Seeds None')

        #------ Building default 1-values row ----------

        if labels is None:
            labels_len = 0
        else:
            labels_len = len(labels)
        one_values = [1] * labels_len
        zero_values = [0] * labels_len

        #---- Building streams and datasets
        evcoOut = []
        streams_dict = {}
	oum_rels_keys = oum_relations_dict.keys()
        end_path_prescale_dict = {}

        for s in streams:
            si = Summaryitem(s.id, s.name,"str", False,'resources/Stream.ico')
            
	    try:

                if s.id in oum_rels_keys:

                    endp_id = oum_relations_dict[s.id]

                    #Check for "HltPrescale" module
                    oumpre = self.queries.getEndPathPrescaleMod(endp_id, db, log)
                
                    if oumpre is not None and len(oumpre) > 0:

                        pre_item = EndPathPrescale(s.id)

                        p_name = endpaths_dict[endp_id]

                        # Insert End Path Prescales

                        # get the prescale from the table dict
                        if(preRows_dict.has_key(p_name)):
                            r_i = preRows_dict.get(p_name)
                            param_values = preRows[r_i].children[1].value
                            values = map(int, re.findall('\d+', param_values)) 

                            if(not(len(labels) == len(values))):
                                log.error("PRESCALE ERROR: NOT SAME CARDINALITY")

                        else:
                            values = one_values

                        # fill the sumitem
                        i2 = 0
                        for c in columns:
                            pre_item.prescales[c.name] = values[i2]
                            sv = c.name + "###" + str(values[i2])
                            si.values.append(sv)
                            i2 = i2 + 1

                        end_path_prescale_dict[s.id] = pre_item

            except:
                log.error('ERROR: End Path Prescales not retreived') 

	    streams_dict[s.id] = si

            si.gid = sumMap.put(si,"str")

#        print "Built stream"
	
	ep_pre_keys = end_path_prescale_dict.keys()

        for d in datasets:
            if (d.id == -1):
#                print "Unassigned Paths"
                log.error("Warning: Unassigned Paths")
            else:
                si = Summaryitem(d.id, d.name,"dat", False, 'resources/Dataset.ico')

                paths = {}
                streamid = relations_dict.get(d.id)

                #-------------------- Getting Smart Prescale ---------------------

                smart_p = None
                smart_paths = None
                hasSmartPrescale = False
                if smartPre is not None:
                    if smartPre.has_key(streamid):
                        smart_p = smartPre[streamid]
                        smart_paths = smart_p.children
                        hasSmartPrescale = True

                #-------------------- Getting datasets paths ---------------------
                if(dprels_dict.has_key(d.id)):

                    dst_paths = dprels_dict[d.id].children

                    for dprel in dst_paths:

                        p = pats_dict[dprel]

                        if hasSmartPrescale:
                            if smart_paths.has_key(p.name):

#                                pat_id = str(p.id)+"pat"+str(d.id) #str(d.id) + "pat" 
                                pat = Summaryitem(p.id,(p.name),"pat", True,'resources/Path_3.ico')
#                                pat = Summaryitem(pat_id,(p.name),"pat", True,'resources/Path_3.ico')
                                pat.gid = sumMap.put(pat, False)

                                if not paths.has_key(pat.gid):

                                    if(preRows_dict.has_key(p.name)):
                                        r_i = preRows_dict.get(p.name)
                                        param_values = preRows[r_i].children[1].value
                                        values = map(int, re.findall('\d+', param_values))

                #                        print "GOt values"

                                        if(not(len(labels) == len(values))):
                                            log.error("ERROR NOT SAME CARDINALITY")
                #                                print "ERROR NOT SAME CARDINALITY"

                                    else:
                                        values = one_values

                                    i2 = 0

                                    sp_value = smart_paths[p.name]
                                    smpr = "smart_pre" + "###" + str(sp_value)
                                    pat.values.append(smpr)
					
				    #--STREAM - END PATH PRESCALE ------------------

                                    if streamid in ep_pre_keys:
                                        # APPLY END PATH PRESCALE

                                        ep_item = end_path_prescale_dict[streamid]
                                        for c in columns:

                                            ep_pre_val = ep_item.prescales[c.name]
                                            pre_value = int(values[i2])*int(ep_pre_val)
                                            new_value = sp_value*pre_value
                                            
                                            sv = c.name + "###" + str(new_value)
                                            pat.values.append(sv)
                                            i2 = i2 + 1

                                    else:
                                        #ONLY SMART

                                        for c in columns:

                                            pre_value = int(values[i2])
                                            new_value = sp_value*pre_value
                                            
                                            sv = c.name + "###" + str(new_value)
                                            pat.values.append(sv)
                                            i2 = i2 + 1  

#                                    for c in columns:
#
#                                        sp_value = smart_paths[p.name]
#                                        pre_value = int(values[i2])
#
#                                        new_value = sp_value*pre_value
#
#                                        sv = c.name + "###" + str(new_value) #str(values[i2])
#                                        pat.values.append(sv)
#                                        i2 = i2 + 1

                                    #----- Include l1 seeds ----------------------
                                    if l1seeds is not None:
                                        if l1seeds.has_key(p.id):
                                            seeds_val = l1seeds.get(p.id)
                                            pat.values.append(seeds_val)

                                    paths[pat.gid] = pat

                            # Put The path with prescales 0
                            else:
#                                pat_id = str(p.id)+"pat"+str(d.id) #str(d.id) + "pat" 
                                pat = Summaryitem(p.id,(p.name),"pat", True,'resources/Path_3.ico')
                                pat.gid = sumMap.put(pat, False)

                                values = zero_values

                                smpr = "smart_pre" + "###" + str(0)
                                pat.values.append(smpr)

                                i2 = 0
                                for c in columns:

                                    pre_value = int(values[i2])

                                    new_value = pre_value

                                    sv = c.name + "###" + str(new_value) #str(values[i2])
                                    pat.values.append(sv)
                                    i2 = i2 + 1

                                if l1seeds is not None:
                                    if l1seeds.has_key(p.id):
                                        seeds_val = l1seeds.get(p.id)
                                        pat.values.append(seeds_val)

                                paths[pat.gid] = pat
                        else:
#                            pat_id = str(p.id)+"pat"+str(d.id) #str(d.id) + "pat" 
                            pat = Summaryitem(p.id, p.name,"pat", True,'resources/Path_3.ico')
                            pat.gid = sumMap.put(pat, False)

                            if not paths.has_key(pat.gid):

                                if(preRows_dict.has_key(p.name)):
                                    r_i = preRows_dict.get(p.name)
                                    param_values = preRows[r_i].children[1].value
                                    values = map(int, re.findall('\d+', param_values))

            #                        print "GOt values"

                                    if(not(len(labels) == len(values))):
                                        log.error("ERROR NOT SAME CARDINALITY")
            #                                print "ERROR NOT SAME CARDINALITY"

                                else:
                                    values = one_values
				
				#--- END PATH PRESCALES ----------------------------------
                                if streamid in ep_pre_keys:
                                    # APPLY END PATH PRESCALE

                                    ep_item = end_path_prescale_dict[streamid]
                                    i2 = 0
                                    for c in columns:

                                        ep_pre_val = ep_item.prescales[c.name]
                                        new_value = int(values[i2])*int(ep_pre_val)
                                        
                                        sv = c.name + "###" + str(new_value)
                                        pat.values.append(sv)
                                        i2 = i2 + 1

                                else:
                                    #ONLY PATH PRESCALE

                                    i2 = 0
                                    for c in columns:

                                        sv = c.name + "###" + str(values[i2])
                                        pat.values.append(sv)
                                        i2 = i2 + 1

#                                i2 = 0
#                                for c in columns:
#
#                                    sv = c.name + "###" + str(values[i2])
#                                    pat.values.append(sv)
#                                    i2 = i2 + 1

                                #----- Include l1 seeds ----------------------
    #                            print 'str(len(pat.values)) ', str(len(pat.values))
                                if l1seeds is not None:
                                    if l1seeds.has_key(p.id):
                                        seeds_val = l1seeds.get(p.id)
                                        pat.values.append(seeds_val)

                                paths[pat.gid] = pat


                    if len(paths) > 0:
                        si.children.extend(paths.values())

#                si.children.extend(paths)
                si.gid = sumMap.put(si,"dat")

                streams_dict.get(streamid).children.append(si)

        #---------- Response ---------------------------------

        #resp = Response()

        resp.children = streams_dict.values()
        resp.children.sort(key=lambda par: par.name)

        #schema = ResponseSummaryItemSchema()

        resp.success = True

        output = schema.dump(resp)
#        assert isinstance(output.data, OrderedDict)

        print "got schema dump "

        return output.data


    def getRoutedConfig(self, cnfMap, name, db, log):

        queries = self.queries
	pattern = re.compile("[V][0-9]+$")

        if (cnfMap == None or name == "" or db == None):
            log.error('ERROR: getRoutedConfig - input parameters error' + self.log_arguments(name=name))
            return -1

        confVer_id = -1
	
	path_tokens = name.split('/')
        last_token = path_tokens[-1]

#        try:
#            #get Config by Name
#            confVer_id = queries.getConfigurationByName(name, db, log)
#
#        except Exception as e:
#            msg = 'ERROR: Query getConfigurationByName Error: ' + e.args[0]
#            log.error(msg)
#            return -1
	
	if pattern.match(last_token) is not None:

            #There is the VERSION NUMBER
            try:
                #get Config by Name
                confVer_id = queries.getConfigurationByName(name, db, log)

            except Exception as e:
                msg = 'ERROR: Query getConfigurationByName Error: ' + e.args[0]
                log.error(msg)
                return -1
        
        else:   

            #NO Version number: the last version is chosen
            try:
                #get Config by Name
                conf_id = queries.getMenuByName(name, db, log)

            except Exception as e:
                msg = 'ERROR: Query getMenuByName Error: ' + e.args[0]
                log.error(msg)
                return -1

            version = self.getRequestedVersion(-2, conf_id, db, log)
            confVer_id = version.id

        return confVer_id


    def log_arguments(self, **kwargs):
        width = max(len(arg) for (arg, val) in kwargs.iteritems())
        return ''.join('\n    ' + arg + ':' + ' ' * (width - len(arg)) + ' ' + repr(val) for (arg, val) in kwargs.iteritems())

