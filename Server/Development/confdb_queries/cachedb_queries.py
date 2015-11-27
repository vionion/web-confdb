# File confdb_queries.py Description:
# This files contains the implementations of the methods providing the query 
# to retrieve records from the ConfDb
# 
# Class: ConfDbQueries

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.sql import select
from sqlalchemy.sql import text
from sqlalchemy import Sequence
from operator import attrgetter
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

from confdb_tables.cachedb_tables import *
#from sqlalchemy_plugin.saplugin import Version, Pathidconf, Pathids, Paths, Pathitems, Pathelement, Modelement, Moduleitem, ModTelement, ModToTemp, ModTemplate, Directory, Configuration, Moduletypes, 

class CacheDbQueries(object):
    
    #Returns the Sequences Paelements records (Sequences and their Modules) in a given path
    #@params: 
    #         id_version: id of Confversion table in the confDB
    #         id_pathid: id of path_id table in the confDB
    #         db: database session object
    #
    def getDictEntry(self, id = -1, db=None, log = None):

        if (id == -1 or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getDictEntry - input parameters error')

        elements = db.query(Dict).filter(Dict.id == id).all()
        
        return elements
    
    def putDictEntry(self, gid = -1, dbid = -1, db=None, log = None):

        if (gid == -1 or dbid == -1 or db == None):
#            print ("PARAMETERS EXCEPTION HERE")
            log.error('ERROR: getDictEntry - input parameters error')
        
        new_pair = Dict(gid=gid, dbid=dbid)
        r_value = db.add(new_pair)
        db.commit()
        
        return r_value