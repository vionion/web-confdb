from collections import namedtuple

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.sql import select
from sqlalchemy.sql import text
from sqlalchemy import Sequence
from operator import attrgetter
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
import json

# from confdb_tables.cachedb_tables import *
#from sqlalchemy_plugin.saplugin import Version, Pathidconf, Pathids, Paths, Pathitems, Pathelement, Modelement, Moduleitem, ModTelement, ModToTemp, ModTemplate, Directory, Configuration, Moduletypes,
from utils import byteify

from item_wrappers.Parameter import Parameter

from exposed.params_builder import ParamsBuilder

from confdb_v2.tables import ModuleitemFull
from tables import ModuleCached, IdMapping


class CacheDbQueries(object):


    def patMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):

        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: patMappingDictPut - input parameters error')

        return_value = -2

        try:
            internal_id = self.get_internal_id(db, dbid, itemtype, log)
            if internal_id is not None:
                statement = select([func.uniqueMapping_put(str(internal_id), src, "patsMapping", unique, itemtype)])
                return_value = db.execute(statement)
                return_value = return_value.first()
            else:
                print('Dou!')
                return -2

        except Exception as e:
            msg = 'ERROR: Query patMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value

        return return_value[0]

    # this method returns internal id for item, which is for Postgres cache, in our case, and it is unique
    # also, it is mapped 1:1 to Oracle id and 1:M to client ids in Postgres
    def patMappingDictGetInternal(self, gid, src, itemtype, db, log):

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

        internal_id = return_value[0]
        return internal_id

    # this method returns external id for item, which is for Oracle, in our case, and it is unique
    def patMappingDictGetExternal(self, gid, src, itemtype, db, log):
        internal_id = self.patMappingDictGetInternal(gid, src, itemtype, db, log)
        external_id = self.get_external_id(db, internal_id, itemtype, log)
        return external_id

    def endpatMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):

        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: patMappingDictPut - input parameters error')

        return_value = -2

        try:
            internal_id = self.get_internal_id(db, dbid, itemtype, log)
            statement = select([func.uniqueMapping_put(str(internal_id), src, "endpatsMapping",unique, itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()

        except Exception as e:
            msg = 'ERROR: Query patMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value

        return return_value[0]

    # this method returns internal id for item, which is for Postgres cache, in our case, and it is unique
    # also, it is mapped 1:1 to Oracle id and 1:M to client ids in Postgres
    def endpatMappingDictGetInternal(self, gid, src, itemtype, db, log):

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

        internal_id = return_value[0]
        return internal_id

    # this method returns external id for item, which is for Oracle, in our case, and it is unique
    def endpatMappingDictGetExternal(self, gid, src, itemtype, db, log):
        internal_id = self.endpatMappingDictGetInternal(gid, src, itemtype, db, log)
        external_id = self.get_external_id(db, internal_id, itemtype, log)
        return external_id

    def allmodMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):

        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: allmodMappingDictPut - input parameters error')

        return_value = -2

        try:
            internal_id = self.get_internal_id(db, dbid, itemtype, log)
            if internal_id is not None:
                statement = select([func.uniqueMapping_put(str(internal_id), src, "allmodsMapping", unique, itemtype)])
                return_value = db.execute(statement)
                return_value = return_value.first()
            else:
                print('Dou!')
                return -2

        except Exception as e:
            msg = 'ERROR: Query allmodMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value

        return return_value[0]

    # this method returns internal id for item, which is for Postgres cache, in our case, and it is unique
    # also, it is mapped 1:1 to Oracle id and 1:M to client ids in Postgres
    def allmodMappingDictGetInternal(self, gid, src, itemtype, db, log):

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

        internal_id = return_value[0]
        return internal_id

    # this method returns external id for item, which is for Oracle, in our case, and it is unique
    def allmodMappingDictGetExternal(self, gid, src, itemtype, db, log):
        internal_id = self.allmodMappingDictGetInternal(gid, src, itemtype, db, log)
        external_id = self.get_external_id(db, internal_id, itemtype, log)
        return external_id

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

    def srvMappingDictGetInternal(self, gid, src, itemtype, db, log):

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

        internal_id = return_value[0]
        return internal_id

    # for now they are the same, we don't map external to internal and to client ids, client id is unique
    def srvMappingDictGetExternal(self, gid, src, itemtype, db, log):
        internal_id = self.srvMappingDictGetInternal(gid, src, itemtype, db, log)
        external_id = self.get_external_id(db, internal_id, itemtype, log)
        return internal_id

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

    def gpsMappingDictGetInternal(self, gid, src, itemtype, db, log):

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

        internal_id = return_value[0]
        return internal_id

    # for now they are the same, we don't map external to internal and to client ids, client id is unique
    def gpsMappingDictGetExternal(self, gid, src, itemtype, db, log):
        internal_id = self.gpsMappingDictGetInternal(gid, src, itemtype, db, log)
        # external_id = self.get_external_id(db, internal_id, itemtype, log)
        return internal_id

    #this causes bugs for some reason (before my changes):
    # ERROR: Query get_internal_id() Error: (psycopg2.InternalError) current transaction is aborted, commands ignored until end of transaction block
    def sumMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):

        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: sumMappingDictPut - input parameters error')

        return_value = -2

        try:
            internal_id = self.get_internal_id(db, dbid, itemtype, log)
            # internal_id = dbid
            statement = select([func.uniqueMapping_put(str(internal_id), src, "sumMapping", unique, itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()

        except Exception as e:
            msg = 'ERROR: Query sumMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value

        return return_value[0]

    def sumMappingDictGetInternal(self, gid, src, itemtype, db, log):

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

        internal_id = return_value[0]
        return internal_id

    def sumMappingDictGetExternal(self, gid, src, itemtype, db, log):
        internal_id = self.sumMappingDictGetInternal(gid, src, itemtype, db, log)
        external_id = self.get_external_id(db, internal_id, itemtype, log)
        return external_id

    def seqMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):

        if (src == -1 or db == None):
            log.error('ERROR: seqMappingDictPut - input parameters error')

        return_value = -2

        try:
            internal_id = self.get_internal_id(db, dbid, itemtype, log)
            statement = select([func.uniqueMapping_put(str(internal_id), src, "seqsMapping", unique, itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()

        except Exception as e:
            msg = 'ERROR: Query seqMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value

        return return_value[0]

    # this method returns internal id for item, which is for Postgres cache, in our case, and it is unique
    # also, it is mapped 1:1 to Oracle id and 1:M to client ids in Postgres
    def seqMappingDictGetInternal(self, gid, src, itemtype, db, log):

        if (id == -1 or db == None):
            log.error('ERROR: seqMappingDictGet - input parameters error')

        return_value = -2

        try:
            statement = select([func.uniqueMapping_get(gid, src, "seqsMapping", itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()
        
        except Exception as e:
            msg = 'ERROR: Query seqMappingDictGet() Error: ' + e.args[0]
            log.error(msg)
            return return_value

        internal_id = return_value[0]
        return internal_id

    # this method returns external id for item, which is for Oracle, in our case, and it is unique
    def seqMappingDictGetExternal(self, gid, src, itemtype, db, log):
        internal_id = self.seqMappingDictGetInternal(gid, src, itemtype, db, log)
        external_id = self.get_external_id(db, internal_id, itemtype, log)
        return external_id

    def strMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):

        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: strMappingDictPut - input parameters error')

        return_value = -2

        try:
            internal_id = self.get_internal_id(db, dbid, itemtype, log)
            statement = select([func.uniqueMapping_put(str(internal_id), src, "strsMapping", unique, itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()

        except Exception as e:
            msg = 'ERROR: Query strMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value

        return return_value[0]

    def strMappingDictGetInternal(self, gid, src, itemtype, db, log):

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

        internal_id = return_value[0]
        return internal_id

    # for now they are the same, we don't map external to internal and to client ids, client id is unique
    def strMappingDictGetExternal(self, gid, src, itemtype, db, log):
        internal_id = self.strMappingDictGetInternal(gid, src, itemtype, db, log)
        external_id = self.get_external_id(db, internal_id, itemtype, log)
        return external_id

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

    # this method returns internal id for item, which is for Postgres cache, in our case, and it is unique
    # also, it is mapped 1:1 to Oracle id and 1:M to client ids in Postgres
    def folMappingDictGetInternal(self, gid, src, itemtype, db, log):

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

        internal_id = return_value[0]
        return internal_id

    # this method returns external id for item, which is for Oracle, in our case, and it is unique
    def folMappingDictGetExternal(self, gid, src, itemtype, db, log):
        internal_id = self.folMappingDictGetInternal(gid, src, itemtype, db, log)
        external_id = self.get_external_id(db, internal_id, itemtype, log)
        return internal_id


    @staticmethod
    def get_module(internal_module_id, cache, log):
        # this module id must be internal id, which is from one of the 'id' columns in tables in cache. Not from Oracle!

        if internal_module_id < 0 or cache is None:
            log.error('ERROR: get_module - input parameters error')
            return -2

        try:
            cached_module = cache.query(ModuleCached).filter(
                ModuleCached.module_id == internal_module_id).first()
            if cached_module is None:
                return None
            else:
                dict_params = byteify(json.loads(cached_module.data))
                # since after json.load we have list of dicts as params, and existing method ParamsBuilder.buildParameterStructure
                # accepts instances of ModuleitemFull object, there is no reason to create another params builder for dicts,
                # it is easier to create objects out of dicts
                obj_params = convert_module_dict2obj(dict_params, log)
                wrapped_params = ParamsBuilder.buildParameterStructure(log, obj_params, cached_module.module_id, set_default=False)
                print('from cache')
                return wrapped_params

        except Exception as e:
            msg = 'ERROR: Query get_module() Error: ' + e.args[0]
            log.error(msg)
            return None

    @staticmethod
    def put_module(module_id, module_params, cache, log):
        # it is possible to reduce amount of data stored in cache, since we don't really use all of the parameter values
        # (check param_builder.buildParameterStructure)
        json_params = json.dumps(module_params, default=lambda o: o.__dict__)
        try:
            module = ModuleCached(data=json_params, module_id=module_id)
            cache.add(module)
            cache.commit()
        except Exception as e:
            msg = 'ERROR: Query put_module() Error: ' + e.args[0]
            log.error(msg)
            return -2

    @staticmethod
    def update_module(module_id, param_name, param_value, cache, log):
        try:
            module = cache.query(ModuleCached).filter(
                ModuleCached.module_id == module_id).first()
            module_data = json.loads(module.data)
            for param in module_data:
                if param['name'] == param_name:
                    param['value'] = param_value
            module.data = json.dumps(module_data)
            print("updated: " + param_name + " - " + param_value)
            flag_modified(module, 'data')
            cache.commit()
        except Exception as e:
            msg = 'ERROR: Query update_module() Error: ' + e.args[0]
            log.error(msg)
            return -2

    def get_all_mod_mappings(self, external_id, src, cache, log):

        if external_id < 0 or cache is None:
            log.error('ERROR: get_all_mod_mappings - input parameters error')

        mappings = []
        try:
            for table_name in ['allmodsMapping', 'patsMapping', 'seqsMapping']:
                statement = select([func.getClientMappings(external_id, src, table_name, 'mod')])
                func_res = cache.execute(statement).fetchone()
                if func_res[0] is not None:
                    mappings.extend(func_res[0])
            int_mappings = [int(x) for x in mappings]

        except Exception as e:
            msg = 'ERROR: Query get_all_mod_mappings() Error: ' + e.args[0]
            log.error(msg)
            return None

        return int_mappings

    def get_internal_id(self, cache, ext_id, itemtype, log):
        try:
            # using postgres function because of multithreading of this requests
            # in this case postgres handles it by itself
            # internal_id = cache.execute(select([func.get_internal_id(ext_id, itemtype)])).first()[0]

            mapping = cache.query(IdMapping).filter(
                IdMapping.external_id == ext_id).filter(
                IdMapping.itemtype == itemtype).first()
            if mapping is None:
                internal_id = self.put_external_id(cache, ext_id, itemtype, log)
            else:
                internal_id = mapping.internal_id

        except Exception as e:
            msg = 'ERROR: Query get_internal_id() Error: ' + e.args[0]
            log.error(msg)
            return None
        return internal_id

    def get_external_id(self, cache, int_id, itemtype, log):
        try:
            mapping = cache.query(IdMapping).filter(
                IdMapping.internal_id == int_id).filter(
                IdMapping.itemtype == itemtype).first()
            if mapping is None:
                return -1
            else:
                external_id = mapping.external_id

        except Exception as e:
            msg = 'ERROR: Query get_internal_id() Error: ' + e.args[0]
            log.error(msg)
            return None
        return external_id

    def put_external_id(self, cache, ext_id, itemtype, log):
        try:
            # locking = cache.query(IdMapping).from_statement(text("LOCK TABLE % s IN ACCESS EXCLUSIVE MODE"))
            # locking.execute()
            # internal_id = cache.execute(select([func.put_external_id(ext_id, itemtype)])).first()[0]
            mapping = IdMapping(external_id=ext_id, itemtype=itemtype)
            cache.add(mapping)
            cache.commit()

        except Exception as e:
            msg = 'ERROR: Query put_external_id() Error: ' + e.args[0]
            log.error(msg)
            return None
        return mapping.internal_id


def convert_module_dict2obj(dict_params, log):
    obj_params = []
    for param in dict_params:
        # just because it is used further in the flow and I have to add it too.
        # Get rid of this generification asap, bad practice!
        param['valuelob'] = None
        obj_params.append(namedtuple("ModuleitemFull", param.keys())(*param.values()))
        if len(param['children']) > 0:
            obj_params.extend(convert_module_dict2obj(param['children'], log))
    return obj_params

