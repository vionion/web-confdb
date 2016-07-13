from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.sql import select
from sqlalchemy.sql import text
from sqlalchemy import Sequence
from operator import attrgetter
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
import json

# from confdb_tables.cachedb_tables import *
#from sqlalchemy_plugin.saplugin import Version, Pathidconf, Pathids, Paths, Pathitems, Pathelement, Modelement, Moduleitem, ModTelement, ModToTemp, ModTemplate, Directory, Configuration, Moduletypes, 

class CacheDbQueries(object):
    

    def patMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):
        
        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: patMappingDictPut - input parameters error')
        
        return_value = -2

        try:
            dbid = str(dbid)
            statement = select([func.uniqueMapping_put(dbid, src, "patsMapping",unique, itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()
        
        except Exception as e:
            msg = 'ERROR: Query patMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value 
        
        return return_value[0]
    
    def patMappingDictGet(self, gid, src, itemtype, db, log):

        if (id == -1 or db == None):
            log.error('ERROR: patMappingDictGet - input parameters error')
        
        return_value = -2
        
        try:
            statement = select([func.uniqueMapping_get(gid, src, "patsMapping", itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()
        
        except Exception as e:
            msg = 'ERROR: Query patMappingDictGet() Error: ' + e.args[0]
            log.error(msg)
            return return_value     
        
        return return_value[0]


    def endpatMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):
        
        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: patMappingDictPut - input parameters error')
        
        return_value = -2

        try:
            dbid = str(dbid)
            statement = select([func.uniqueMapping_put(dbid, src, "endpatsMapping",unique, itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()
        
        except Exception as e:
            msg = 'ERROR: Query patMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value 
        
        return return_value[0]
    
    def endpatMappingDictGet(self, gid, src, itemtype, db, log):

        if (id == -1 or db == None):
            log.error('ERROR: patMappingDictGet - input parameters error')
        
        return_value = -2
        
        try:
            statement = select([func.uniqueMapping_get(gid, src, "endpatsMapping", itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()
        
        except Exception as e:
            msg = 'ERROR: Query patMappingDictGet() Error: ' + e.args[0]
            log.error(msg)
            return return_value     
        
        return return_value[0]    
    
    
    def allmodMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):
        
        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: allmodMappingDictPut - input parameters error')
        
        return_value = -2

        try:
            dbid = str(dbid)
            statement = select([func.uniqueMapping_put(dbid, src, "allmodsMapping", unique, itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()
#            print return_value[0]
        
        except Exception as e:
            msg = 'ERROR: Query allmodMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value 
        
        return return_value[0]
    
    def allmodMappingDictGet(self, gid, src, itemtype, db, log):

        if (id == -1 or db == None):
            log.error('ERROR: allmodMappingDictGet - input parameters error')
        
        return_value = -2
        
        try:
            statement = select([func.uniqueMapping_get(gid, src, "allmodsMapping", itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()
        
        except Exception as e:
            msg = 'ERROR: Query allmodMappingDictGet() Error: ' + e.args[0]
            log.error(msg)
            return return_value     
        
        return return_value[0]
   
    def srvMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):
        
        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: srvMappingDictPut - input parameters error')
        
        return_value = -2

        try:
            dbid = str(dbid)
            statement = select([func.uniqueMapping_put(dbid, src, "srvsMapping", unique, itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()
        
        except Exception as e:
            msg = 'ERROR: Query srvMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value 
        
        return return_value[0]
    
    def srvMappingDictGet(self, gid, src, itemtype, db, log):

        if (id == -1 or db == None):
            log.error('ERROR: srvMappingDictGet - input parameters error')
        
        return_value = -2
        
        try:
            statement = select([func.uniqueMapping_get(gid, src, "srvsMapping", itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()
        
        except Exception as e:
            msg = 'ERROR: Query srvMappingDictGet() Error: ' + e.args[0]
            log.error(msg)
            return return_value     
        
        return return_value[0]
    
    def gpsMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):
        
        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: gpsMappingDictPut - input parameters error')
        
        return_value = -2

        try:
            dbid = str(dbid)
            statement = select([func.uniqueMapping_put(dbid, src, "gpsMapping", unique, itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()
        
        except Exception as e:
            msg = 'ERROR: Query gpsMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value 
        
        return return_value[0]
    
    def gpsMappingDictGet(self, gid, src, itemtype, db, log):

        if (id == -1 or db == None):
            log.error('ERROR: gpsMappingDictGet - input parameters error')
        
        return_value = -2
        
        try:
            statement = select([func.uniqueMapping_get(gid, src, "gpsMapping", itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()
        
        except Exception as e:
            msg = 'ERROR: Query gpsMappingDictGet() Error: ' + e.args[0]
            log.error(msg)
            return return_value     
        
        return return_value[0]
    
    def sumMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):
        
        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: sumMappingDictPut - input parameters error')
        
        return_value = -2

        try:
            dbid = str(dbid)
            statement = select([func.uniqueMapping_put(dbid, src, "sumMapping", unique, itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()
        
        except Exception as e:
            msg = 'ERROR: Query sumMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value 
        
        return return_value[0]
    
    def sumMappingDictGet(self, gid, src, itemtype, db, log):

        if (id == -1 or db == None):
            log.error('ERROR: sumMappingDictGet - input parameters error')
        
        return_value = -2
        
        try:
            statement = select([func.uniqueMapping_get(gid, src, "sumMapping", itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()
        
        except Exception as e:
            msg = 'ERROR: Query sumMappingDictGet() Error: ' + e.args[0]
            log.error(msg)
            return return_value     
        
        return return_value[0]

    def seqMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):
        
        if (src == -1 or db == None):
            log.error('ERROR: seqMappingDictPut - input parameters error')
        
        return_value = -2

        try:
            value = str(dbid)
            statement = select([func.uniqueMapping_put(value, src, "seqsMapping", unique, itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()
#            print return_value[0]
        
        except Exception as e:
            msg = 'ERROR: Query seqMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value 
        
        return return_value[0]
    
    def seqMappingDictGet(self, gid, src, itemtype, db, log):

        if (id == -1 or db == None):
            log.error('ERROR: seqMappingDictGet - input parameters error')
        
        return_value = -2
        
        try:
            statement = select([func.uniqueMapping_get(gid, src, "seqsMapping", itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()
            tokens = return_value[0].split('#')
            first_token = tokens[0]
            return_value = int(first_token)
        
        except Exception as e:
            msg = 'ERROR: Query seqMappingDictGet() Error: ' + e.args[0]
            log.error(msg)
            return return_value     
        
        return return_value

    def strMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):
        
        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: strMappingDictPut - input parameters error')
        
        return_value = -2

        try:
            dbid = str(dbid)
            statement = select([func.uniqueMapping_put(dbid, src, "strsMapping", unique, itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()
        
        except Exception as e:
            msg = 'ERROR: Query strMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value 
        
        return return_value[0]
    
    def strMappingDictGet(self, gid, src, itemtype, db, log):

        if (id == -1 or db == None):
            log.error('ERROR: strMappingDictGet - input parameters error')
        
        return_value = -2
        
        try:
            statement = select([func.uniqueMapping_get(gid, src, "strsMapping", itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()
        
        except Exception as e:
            msg = 'ERROR: Query strMappingDictGet() Error: ' + e.args[0]
            log.error(msg)
            return return_value     
        
        return return_value[0]

    def folMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):
        
        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: folMappingDictPut - input parameters error')
        
        return_value = -2

        try:
            dbid = str(dbid)
            statement = select([func.uniqueMapping_put(dbid, src, "folsMapping", unique, itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()
        
        except Exception as e:
            msg = 'ERROR: Query folMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value 
        
        return return_value[0]
    
    def folMappingDictGet(self, gid, src, itemtype, db, log):

        if (id == -1 or db == None):
            log.error('ERROR: folMappingDictGet - input parameters error')
        
        return_value = -2
        
        try:
            statement = select([func.uniqueMapping_get(gid, src, "folsMapping", itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()
        
        except Exception as e:
            msg = 'ERROR: Query folMappingDictGet() Error: ' + e.args[0]
            log.error(msg)
            return return_value     
        
        return return_value[0]