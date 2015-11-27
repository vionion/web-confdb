from confdb_queries.confdb_queries import ConfDbQueries
from confdb_queries.cachedb_queries import CacheDbQueries
from item_wrappers.FolderItem import *
from item_wrappers.ModuleDetails import *
from item_wrappers.Pathitem import *
from item_wrappers.Parameter import *
from item_wrappers.item_wrappers import *
from marshmallow import Schema, fields, pprint
from collections import OrderedDict

import string
import re

class DataManager(object):
    
    confdb_queries = ConfDbQueries()
    cache_queries = CacheDbQueries()
    
    def getDictEntry(self, gid = -1, online = 'False', request=None, log = None):

        if (gid == -1 or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getDictEntry - input parameters error')
    
        if online == 'True' or online == 'true':
            print 'db = db_online'
            db = request.db_online
            folMap = self.folMap_online
            cnfMap = self.cnfMap_online
            
        else:
            db = db_offline
            folMap = self.folMap
            cnfMap = self.cnfMap
        

        elements = db.query(Dict).filter(Dict.id == id).all()
        
        return elements
    
    def putDictEntry(self, dbid = -1, online = 'False', db=None, log = None):

        if (gid == -1 or dbid == -1 or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getDictEntry - input parameters error')
        
        new_pair = Dict(gid=gid, dbid=dbid)
        r_value = db.add(new_pair)
        db.commit()
        
        return r_value
    
    
    
    