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
from item_wrappers.Pathitem import Pathitem

from exposed.params_builder import ParamsBuilder

from confdb_v2.tables import ModuleitemFull

from tables import ParamsCached, IdMapping, PathItemsCached


class CacheDbQueries(object):


    def patMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):

        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: patMappingDictPut - input parameters error')

        return_value = -2

        try:
            internal_id = self.get_internal_id(db, dbid, itemtype, src, log)
            if internal_id is not None:
                statement = select([func.uniqueMapping_put(internal_id, "patsMapping", unique, itemtype)])
                return_value = db.execute(statement)
                return_value = return_value.first()

        except Exception as e:
            msg = 'ERROR: Query patMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value

        return return_value[0]

    # this method returns internal id for item, which is for Postgres cache, in our case, and it is unique
    # also, it is mapped 1:1 to Oracle id and 1:M to client ids in Postgres
    def patMappingDictGetInternal(self, gid, itemtype, db, log):

        if (id == -1 or db == None):
            log.error('ERROR: patMappingDictGet - input parameters error')

        return_value = -2

        try:
            statement = select([func.uniqueMapping_get(gid, "patsMapping", itemtype)])
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
        internal_id = self.patMappingDictGetInternal(gid, itemtype, db, log)
        external_id = self.get_external_id(db, internal_id, itemtype, src, log)
        return external_id

    def endpatMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):

        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: patMappingDictPut - input parameters error')

        return_value = -2

        try:
            internal_id = self.get_internal_id(db, dbid, itemtype, src, log)
            statement = select([func.uniqueMapping_put(internal_id, "endpatsMapping",unique, itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()

        except Exception as e:
            msg = 'ERROR: Query patMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value

        return return_value[0]

    # this method returns internal id for item, which is for Postgres cache, in our case, and it is unique
    # also, it is mapped 1:1 to Oracle id and 1:M to client ids in Postgres
    def endpatMappingDictGetInternal(self, gid, itemtype, db, log):

        if (id == -1 or db == None):
            log.error('ERROR: patMappingDictGet - input parameters error')

        return_value = -2

        try:
            statement = select([func.uniqueMapping_get(gid, "endpatsMapping", itemtype)])
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
        internal_id = self.endpatMappingDictGetInternal(gid, itemtype, db, log)
        external_id = self.get_external_id(db, internal_id, itemtype, src, log)
        return external_id

    def allmodMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):

        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: allmodMappingDictPut - input parameters error')

        return_value = -2

        try:
            internal_id = self.get_internal_id(db, dbid, itemtype, src, log)
            if internal_id is not None:
                statement = select([func.uniqueMapping_put(internal_id, "allmodsMapping", unique, itemtype)])
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
    def allmodMappingDictGetInternal(self, gid, itemtype, db, log):

        if (id == -1 or db == None):
            log.error('ERROR: allmodMappingDictGet - input parameters error')

        return_value = -2

        try:
            statement = select([func.uniqueMapping_get(gid, "allmodsMapping", itemtype)])
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
        internal_id = self.allmodMappingDictGetInternal(gid, itemtype, db, log)
        external_id = self.get_external_id(db, internal_id, itemtype, src, log)
        return external_id

    def srvMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):

        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: srvMappingDictPut - input parameters error')

        return_value = -2

        try:
            statement = select([func.uniqueMapping_put(dbid, "srvsMapping", unique, itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()

        except Exception as e:
            msg = 'ERROR: Query srvMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value

        return return_value[0]

    def srvMappingDictGetInternal(self, gid, itemtype, db, log):

        if (id == -1 or db == None):
            log.error('ERROR: srvMappingDictGet - input parameters error')

        return_value = -2

        try:
            statement = select([func.uniqueMapping_get(gid, "srvsMapping", itemtype)])
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
        internal_id = self.srvMappingDictGetInternal(gid, itemtype, db, log)
        external_id = self.get_external_id(db, internal_id, itemtype, src, log)
        return internal_id

    def gpsMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):

        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: gpsMappingDictPut - input parameters error')

        return_value = -2

        try:
            internal_id = self.get_internal_id(db, dbid, itemtype, src, log)
            statement = select([func.uniqueMapping_put(internal_id, "gpsMapping", unique, itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()

        except Exception as e:
            msg = 'ERROR: Query gpsMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value

        return return_value[0]

    def gpsMappingDictGetInternal(self, gid, itemtype, db, log):

        if (id == -1 or db == None):
            log.error('ERROR: gpsMappingDictGet - input parameters error')

        return_value = -2

        try:
            statement = select([func.uniqueMapping_get(gid, "gpsMapping", itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()

        except Exception as e:
            msg = 'ERROR: Query gpsMappingDictGet() Error: ' + e.args[0]
            log.error(msg)
            return return_value

        internal_id = return_value[0]
        return internal_id

    def gpsMappingDictGetExternal(self, gid, src, itemtype, db, log):
        internal_id = self.gpsMappingDictGetInternal(gid, itemtype, db, log)
        external_id = self.get_external_id(db, internal_id, itemtype, src, log)
        return external_id

    #this causes bugs for some reason (before my changes):
    # ERROR: Query get_internal_id() Error: (psycopg2.InternalError) current transaction is aborted, commands ignored until end of transaction block
    def sumMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):

        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: sumMappingDictPut - input parameters error')

        return_value = -2

        try:
            internal_id = self.get_internal_id(db, dbid, itemtype, src, log)
            # internal_id = dbid
            statement = select([func.uniqueMapping_put(internal_id, "sumMapping", unique, itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()

        except Exception as e:
            msg = 'ERROR: Query sumMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value

        return return_value[0]

    def sumMappingDictGetInternal(self, gid, itemtype, db, log):

        if (id == -1 or db == None):
            log.error('ERROR: sumMappingDictGet - input parameters error')

        return_value = -2

        try:
            statement = select([func.uniqueMapping_get(gid, "sumMapping", itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()

        except Exception as e:
            msg = 'ERROR: Query sumMappingDictGet() Error: ' + e.args[0]
            log.error(msg)
            return return_value

        internal_id = return_value[0]
        return internal_id

    def sumMappingDictGetExternal(self, gid, src, itemtype, db, log):
        internal_id = self.sumMappingDictGetInternal(gid, itemtype, db, log)
        external_id = self.get_external_id(db, internal_id, itemtype, src, log)
        return external_id

    def seqMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):

        if (src == -1 or db == None):
            log.error('ERROR: seqMappingDictPut - input parameters error')

        return_value = -2

        try:
            internal_id = self.get_internal_id(db, dbid, itemtype, src, log)
            statement = select([func.uniqueMapping_put(internal_id, "seqsMapping", unique, itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()

        except Exception as e:
            msg = 'ERROR: Query seqMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value

        return return_value[0]

    # this method returns internal id for item, which is for Postgres cache, in our case, and it is unique
    # also, it is mapped 1:1 to Oracle id and 1:M to client ids in Postgres
    def seqMappingDictGetInternal(self, gid, itemtype, db, log):

        if (id == -1 or db == None):
            log.error('ERROR: seqMappingDictGet - input parameters error')

        return_value = -2

        try:
            statement = select([func.uniqueMapping_get(gid, "seqsMapping", itemtype)])
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
        internal_id = self.seqMappingDictGetInternal(gid, itemtype, db, log)
        external_id = self.get_external_id(db, internal_id, itemtype, src, log)
        return external_id

    def strMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):

        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: strMappingDictPut - input parameters error')

        return_value = -2

        try:
            internal_id = self.get_internal_id(db, dbid, itemtype, src, log)
            statement = select([func.uniqueMapping_put(internal_id, "strsMapping", unique, itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()

        except Exception as e:
            msg = 'ERROR: Query strMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value

        return return_value[0]

    def strMappingDictGetInternal(self, gid, itemtype, db, log):

        if (id == -1 or db == None):
            log.error('ERROR: strMappingDictGet - input parameters error')

        return_value = -2

        try:
            statement = select([func.uniqueMapping_get(gid, "strsMapping", itemtype)])
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
        internal_id = self.strMappingDictGetInternal(gid, itemtype, db, log)
        external_id = self.get_external_id(db, internal_id, itemtype, src, log)
        return external_id

    def folMappingDictPut(self, src, dbid, itemtype, db, log, unique = 1):

        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: folMappingDictPut - input parameters error')

        return_value = -2

        try:
            statement = select([func.uniqueMapping_put(dbid, "folsMapping", unique, itemtype)])
            return_value = db.execute(statement)
            return_value = return_value.first()
        
        except Exception as e:
            msg = 'ERROR: Query folMappingDictPut() Error: ' + e.args[0]
            log.error(msg)
            return return_value

        return return_value[0]

    # this method returns internal id for item, which is for Postgres cache, in our case, and it is unique
    # also, it is mapped 1:1 to Oracle id and 1:M to client ids in Postgres
    def folMappingDictGetInternal(self, gid, itemtype, db, log):

        if (id == -1 or db == None):
            log.error('ERROR: folMappingDictGet - input parameters error')

        return_value = -2

        try:
            statement = select([func.uniqueMapping_get(gid, "folsMapping", itemtype)])
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
        internal_id = self.folMappingDictGetInternal(gid, itemtype, db, log)
        external_id = self.get_external_id(db, internal_id, itemtype, src, log)
        return internal_id


    @staticmethod
    def get_params(internal_entity_id, cache, log):
        # this param id must be internal id, which is from one of the 'id' columns in tables in cache. Not from Oracle!

        if internal_entity_id < 0 or cache is None:
            log.error('ERROR: get_module - input parameters error')
            return -2

        try:
            cached_params = cache.query(ParamsCached).filter(
                ParamsCached.id == internal_entity_id).first()
            if cached_params is None:
                return None
            else:
                dict_params = byteify(json.loads(cached_params.data))
                # since after json.load we have list of dicts as params, and existing method ParamsBuilder.buildParameterStructure
                # accepts instances of ModuleitemFull object, there is no reason to create another params builder for dicts,
                # it is easier to create objects out of dicts
                obj_params = convert_module_dict2obj(dict_params, log)
                wrapped_params = ParamsBuilder.buildParameterStructure(log, obj_params, cached_params.id, set_default=False)
                print('from cache')
                return wrapped_params

        except Exception as e:
            msg = 'ERROR: Query get_params() Error: ' + e.args[0]
            log.error(msg)
            return None

    @staticmethod
    def put_params(internal_entity_id, params, cache, log):
        # it is possible to reduce amount of data stored in cache, since we don't really use all of the parameter values
        # (check param_builder.buildParameterStructure)
        json_params = json.dumps(params, default=lambda o: o.__dict__)
        try:
            params = ParamsCached(data=json_params, id=internal_entity_id)
            cache.add(params)
            cache.commit()
        except Exception as e:
            msg = 'ERROR: Query put_params() Error: ' + e.args[0]
            log.error(msg)
            return -2

    @staticmethod
    def update_params(internal_entity_id, param_name, param_value, cache, log):
        try:
            params = cache.query(ParamsCached).filter(
                ParamsCached.id == internal_entity_id).first()
            json_params = json.loads(params.data)
            for param in json_params:
                if param['name'] == param_name:
                    param['value'] = param_value
            params.data = json.dumps(json_params)
            print("updated: " + param_name + " - " + param_value)
            flag_modified(params, 'data')
            cache.commit()
        except Exception as e:
            msg = 'ERROR: Query update_params() Error: ' + e.args[0]
            log.error(msg)
            return -2

    def get_path_items(self, path_id, cache, src, log):
        if path_id < 0 or cache is None:
            log.error('ERROR: get_path_items - input parameters error')
            return -2

        try:
            cached_path = cache.query(PathItemsCached).filter(
                PathItemsCached.path_id == path_id).first()
            if cached_path is None:
                return None
            else:
                dict_path_items = byteify(json.loads(cached_path.data))
                wrapped_paths_items = self.wrap_path_items(dict_path_items, src, cache, log)
                print('from cache')
                return wrapped_paths_items

        except Exception as e:
            msg = 'ERROR: Query get_path_items() Error: ' + e.args[0]
            log.error(msg)
            return None

    def convert_pathitem_dict2obj(self, dict_params):
        obj_items = []
        for param in dict_params:
            obj_items.append(namedtuple("Pathitems", param.keys())(*param.values()))
        return obj_items

    def wrap_path_items(self, dict_path_items, src, cache, log):
        obj_path_items = self.convert_pathitem_dict2obj(dict_path_items)
        wrapped_paths = []
        for pathitem in obj_path_items:
            item = Pathitem(pathitem.id, pathitem.name, pathitem.id_pathid, pathitem.paetype, pathitem.id_parent,
                            pathitem.lvl, pathitem.order, pathitem.operator)
            if item.paetype == 1:
                item.gid = self.patMappingDictPut(src, pathitem.id, "mod", cache, log, 0)
            elif item.paetype == 2:
                item.gid = self.patMappingDictPut(src, pathitem.id, "seq", cache, log, 0)
            item.expanded = pathitem.expanded
            item.children = self.wrap_path_items(pathitem.children, src, cache, log)
            wrapped_paths.append(item)
        return wrapped_paths

    def put_path_items(self, path_id, path_params, cache, log):
        json_params = json.dumps(path_params, default=lambda o: o.__dict__)
        try:
            params = PathItemsCached(data=json_params, path_id=path_id)
            cache.add(params)
            cache.commit()
        except Exception as e:
            msg = 'ERROR: Query put_path_items() Error: ' + e.args[0]
            log.error(msg)
            return -2

    def get_all_mod_mappings(self, external_id, cache, log):

        if external_id < 0 or cache is None:
            log.error('ERROR: get_all_mod_mappings - input parameters error')

        mappings = []
        try:
            for table_name in ['allmodsMapping', 'patsMapping', 'seqsMapping']:
                statement = select([func.getClientMappings(external_id, table_name, 'mod')])
                func_res = cache.execute(statement).fetchone()
                if func_res[0] is not None:
                    mappings.extend(func_res[0])
            int_mappings = [int(x) for x in mappings]

        except Exception as e:
            msg = 'ERROR: Query get_all_mod_mappings() Error: ' + e.args[0]
            log.error(msg)
            return None

        return int_mappings

    def get_internal_id(self, cache, ext_id, itemtype, src, log):
        try:
            # using postgres function because of multithreading of this requests
            # in this case postgres handles it by itself
            # internal_id = cache.execute(select([func.get_internal_id(ext_id, itemtype)])).first()[0]

            mapping = cache.query(IdMapping).filter(
                IdMapping.external_id == ext_id).filter(
                IdMapping.source == src).filter(
                IdMapping.itemtype == itemtype).first()
            if mapping is None:
                internal_id = self.put_external_id(cache, ext_id, itemtype, src, log)
            else:
                internal_id = mapping.internal_id

        except Exception as e:
            msg = 'ERROR: Query get_internal_id() Error: ' + e.args[0]
            log.error(msg)
            return None
        return internal_id

    def get_external_id(self, cache, int_id, itemtype, src, log):
        try:
            mapping = cache.query(IdMapping).filter(
                IdMapping.internal_id == int_id).filter(
                IdMapping.source == src).filter(
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

    def put_external_id(self, cache, ext_id, itemtype, src, log):
        try:
            # locking = cache.query(IdMapping).from_statement(text("LOCK TABLE % s IN ACCESS EXCLUSIVE MODE"))
            # locking.execute()
            # internal_id = cache.execute(select([func.put_external_id(ext_id, itemtype)])).first()[0]
            mapping = IdMapping(external_id=ext_id, itemtype=itemtype, source=src)
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

