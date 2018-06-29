import calendar
from collections import namedtuple

import copy

from datetime import datetime
from sqlalchemy import *
from sqlalchemy.exc import IntegrityError
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
# from sqlalchemy_plugin.saplugin import Version, Pathidconf, Pathids, Paths, Pathitems, Pathelement, Modelement, Moduleitem, ModTelement, ModToTemp, ModTemplate, Directory, Configuration, Moduletypes,
from utils import byteify

from item_wrappers.Parameter import Parameter
from item_wrappers.Pathitem import Pathitem
from item_wrappers.item_wrappers import *

from exposed.params_builder import ParamsBuilder

from confdb_v2.tables import Pathelement, EvCoToStream
from tables import *


class CacheDbQueries(object):

    def patMappingDictPut(self, src, dbid, itemtype, db, log, unique=1):

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

    def endpatMappingDictPut(self, src, dbid, itemtype, db, log, unique=1):

        if (src == -1 or dbid == -1 or db == None):
            log.error('ERROR: patMappingDictPut - input parameters error')

        return_value = -2

        try:
            internal_id = self.get_internal_id(db, dbid, itemtype, src, log)
            statement = select([func.uniqueMapping_put(internal_id, "endpatsMapping", unique, itemtype)])
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

    def allmodMappingDictPut(self, src, dbid, itemtype, db, log, unique=1):

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

    def srvMappingDictPut(self, src, dbid, itemtype, db, log, unique=1):

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

    def gpsMappingDictPut(self, src, dbid, itemtype, db, log, unique=1):

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

    # this causes bugs for some reason (before my changes):
    # ERROR: Query get_internal_id() Error: (psycopg2.InternalError) current transaction is aborted, commands ignored until end of transaction block
    def sumMappingDictPut(self, src, dbid, itemtype, db, log, unique=1):

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

    def seqMappingDictPut(self, src, dbid, itemtype, db, log, unique=1):

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

    def strMappingDictPut(self, src, dbid, itemtype, db, log, unique=1):

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

    def folMappingDictPut(self, src, dbid, itemtype, db, log, unique=1):

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
    def get_params(internal_entity_id, ver, cache, log):
        # this param id must be internal id, which is from one of the 'id' columns in tables in cache. Not from Oracle!

        if internal_entity_id < 0 or cache is None:
            log.error('ERROR: get_params - input parameters error')
            return -2

        try:
            cached_params = cache.query(ParamsCached).filter(
                ParamsCached.id == internal_entity_id).filter(
                ParamsCached.version_id == ver).first()
            if cached_params is None:
                return None
            else:
                dict_params = byteify(json.loads(cached_params.data))
                # since after json.load we have list of dicts as params, and existing method ParamsBuilder.buildParameterStructure
                # accepts instances of ModuleitemFull object, there is no reason to create another params builder for dicts,
                # it is easier to create objects out of dicts
                obj_params = convert_module_dict2obj(dict_params, log)
                wrapped_params = ParamsBuilder.buildParameterStructure(log, obj_params, cached_params.id)
                return wrapped_params

        except Exception as e:
            msg = 'ERROR: Query get_params() Error: ' + e.args[0]
            log.error(msg)
            return None

    @staticmethod
    def put_params(internal_entity_id, params, ver, cache, log):
        # it is possible to reduce amount of data stored in cache, since we don't really use all of the parameter values
        # (check param_builder.buildParameterStructure)
        json_params = json.dumps(params, default=lambda o: o.__dict__)
        try:
            params = ParamsCached(data=json_params, id=internal_entity_id, version_id=ver)
            cache.add(params)
            cache.commit()
        except Exception as e:
            msg = 'ERROR: Query put_params() Error: ' + e.args[0]
            log.error(msg)
            return -2

    @staticmethod
    def update_params(internal_entity_id, param_name, param_value, ver, cache, log):
        try:
            params = cache.query(ParamsCached).filter(
                ParamsCached.id == internal_entity_id).filter(
                ParamsCached.version_id == ver).first()
            json_params = json.loads(params.data)
            for param in json_params:
                if param['name'] == param_name:
                    param['value'] = param_value
                    param['default'] = False
                    param['changed'] = True
            params.data = json.dumps(json_params)
            params.changed = True
            print("updated: " + param_name + " - " + param_value)
            flag_modified(params, 'data')
            flag_modified(params, 'changed')
            cache.commit()
        except Exception as e:
            msg = 'ERROR: Query update_params() Error: ' + e.args[0]
            log.error(msg)
            return -2

    def get_path_items(self, parent_id, cache, log, lvl=0):
        items = []
        if parent_id < 0 or cache is None:
            log.error('ERROR: get_path_items - input parameters error')
            return items
        try:
            cached_path_children = cache.query(PathItemsHierarchy).filter(
                PathItemsHierarchy.parent_id == parent_id).all()
            if len(cached_path_children) is 0:
                return items
            else:
                for children in cached_path_children:
                    item = self.get_wrapped_item(cache, children, lvl)
                    item.children = self.get_path_items(item.internal_id, cache, log, lvl + 1)
                    items.append(item)
                items.sort(key=lambda x: x.order, reverse=False)
                return items

        except Exception as e:
            msg = 'ERROR: Query get_path_items() Error: ' + e.args[0]
            log.error(msg)
            return []

    def get_wrapped_item(self, cache, children, lvl):
        path_item = cache.query(PathItemsCached).filter(
            PathItemsCached.path_item_id == children.child_id).first()
        dict_pathitem = byteify(json.loads(path_item.data))
        item = Pathitem(dict_pathitem['internal_id'], dict_pathitem['name'], dict_pathitem['id_pathid'],
                        dict_pathitem['paetype'], dict_pathitem['id_parent'],
                        0, 0, dict_pathitem['operator'])
        item.expanded = dict_pathitem['expanded']
        item.order = children.order
        item.lvl = lvl
        return item

    def put_path_items(self, parrent_id, path_items, cache, log):
        nodes = []
        for pathitem in path_items:
            children = self.get_path_items(pathitem.internal_id, cache, log, pathitem.lvl + 1)
            if len(children) is 0:
                self.put_path_items(pathitem.internal_id, pathitem.children, cache, log)
            else:
                pathitem.children = children
            self.put_path_item(pathitem, parrent_id, cache, log)
            nodes.append(pathitem)
        return nodes

    @staticmethod
    def put_path_item(pathitem, parrent_id, cache, log):
        pathitem_copy = copy.deepcopy(pathitem)
        pathitem_copy.children = []
        json_path_item = json.dumps(pathitem_copy, default=lambda o: o.__dict__)
        try:
            if not cache.query(exists().where(PathItemsCached.path_item_id == pathitem.internal_id)).scalar():
                params = PathItemsCached(data=json_path_item, path_item_id=pathitem_copy.internal_id)
                cache.add(params)
            if not cache.query(exists().where(PathItemsHierarchy.parent_id == parrent_id).where(PathItemsHierarchy.child_id == pathitem.internal_id)).scalar():
                pih = PathItemsHierarchy(parent_id=parrent_id, child_id=pathitem.internal_id, order=pathitem.order)
                cache.add(pih)
            cache.commit()
        except Exception as e:
            msg = 'ERROR: Query put_path_items() Error: ' + e.args[0]
            log.error(msg)
        except IntegrityError as e:
            cache.rollback()
            msg = 'ERROR: Query put_path_items() Error: ' + e.args[0]
            log.error(msg)

    @staticmethod
    def get_paths(version_id, cache, log):
        if version_id < 0 or cache is None:
            log.error('ERROR: get_paths - input parameters error')
            return []

        try:
            cached_paths = cache.query(PathsCache).filter(
                PathsCache.version_id == version_id).all()
            if len(cached_paths) is 0:
                return []
            else:
                wrapped_paths = []
                for path in cached_paths:
                    dict_path = byteify(json.loads(path.data))
                    wrapped_paths.append(Path(dict_path['internal_id'], dict_path['id_path'], dict_path['description'], dict_path['name'], dict_path['vid'], dict_path['order'], dict_path['isEndPath']))
                return wrapped_paths

        except Exception as e:
            msg = 'ERROR: Query get_paths() Error: ' + e.args[0]
            log.error(msg)
            return []

    @staticmethod
    def put_paths(ver_id, paths, cache, log):
        try:
            for path in paths:
                json_path = json.dumps(path, default=lambda o: o.__dict__)
                cached_path = PathsCache(data=json_path, version_id=ver_id, isEndPath=path.isEndPath, name=path.name, path_id=path.internal_id)
                cache.add(cached_path)
            cache.commit()
        except Exception as e:
            msg = 'ERROR: Query put_paths() Error: ' + e.args[0]
            log.error(msg)
            return -2

    # Code in get_paths/get_endpaths and put_path/put_enpaths may be reused
    @staticmethod
    def get_endpaths(version_id, cache, log):
        if version_id < 0 or cache is None:
            log.error('ERROR: get_endpaths - input parameters error')
            return -2

        try:
            cached_paths = cache.query(EndPathsCached).filter(
                EndPathsCached.version_id == version_id).first()
            if cached_paths is None:
                return None
            else:
                dict_paths = byteify(json.loads(cached_paths.data))
                wrapped_paths = []
                for path in dict_paths:
                    wrapped_paths.append(Path(path['internal_id'], path['id_path'], path['description'], path['name'], path['vid'], path['order'], path['isEndPath']))
                return wrapped_paths

        except Exception as e:
            msg = 'ERROR: Query get_endpaths() Error: ' + e.args[0]
            log.error(msg)
            return None

    @staticmethod
    def put_endpaths(ver_id, paths, cache, log):
        try:
            json_paths = json.dumps(paths, default=lambda o: o.__dict__)
            params = EndPathsCached(data=json_paths, version_id=ver_id)
            cache.add(params)
            cache.commit()
        except Exception as e:
            msg = 'ERROR: Query put_endpaths() Error: ' + e.args[0]
            log.error(msg)
            return -2

    @staticmethod
    def get_service_messages(cache, log):
        try:
            d = datetime.utcnow()
            unixtime_now = calendar.timegm(d.utctimetuple())
            service_messages = cache.query(ServiceMessage).filter(
                ServiceMessage.due_date >= unixtime_now).all()
            if len(service_messages) is 0:
                return []
            else:
                return service_messages
        except Exception as e:
            msg = 'ERROR: Query get_service_messages() Error: ' + e.args[0]
            log.error(msg)
            return []

    @staticmethod
    def get_modules_names(version_id, cache, log):
        if version_id < 0 or cache is None:
            log.error('ERROR: get_module_names - input parameters error')
            return []

        try:
            cached_names_list = cache.query(ModulesNames).filter(
                ModulesNames.version_id == version_id).first()
            if cached_names_list is None:
                return []
            else:
                wrapped_names = []
                for name in cached_names_list.names:
                    wrapped_names.append(Pathelement(name=name))
                return wrapped_names

        except Exception as e:
            msg = 'ERROR: Query get_module_names() Error: ' + e.args[0]
            log.error(msg)
            return []

    def get_changed_params(self, version_id, cache, log):
        if version_id < 0 or cache is None:
            log.error('ERROR: get_changed_params - input parameters error')
            return {}, {}
        try:
            changed_params = cache.query(ParamsCached).filter(
                ParamsCached.version_id == version_id).filter(
                ParamsCached.changed == True).all()
            if len(changed_params) is 0:
                return {}, {}
            else:
                params = {}
                from_templates = {}
                for param in changed_params:
                    dict_params = byteify(json.loads(param.data))
                    obj_params = convert_module_dict2obj(dict_params, log)
                    for obj_param in obj_params:
                        if hasattr(obj_param, 'changed') and obj_param.changed is True:
                            if hasattr(obj_param, 'id_field_module'):
                                params[obj_param.id_field_module] = obj_param
                            elif hasattr(obj_param, 'id_field_templ'):
                                from_templates[obj_param.id_field_templ] = obj_param
                return params, from_templates
        except Exception as e:
            msg = 'ERROR: Query get_changed_params() Error: ' + e.args[0]
            log.error(msg)
            return {}, {}

    @staticmethod
    def put_modules_names(ver_id, names_list, cache, log):
        try:
            names = ModulesNames(names=names_list, version_id=ver_id)
            cache.add(names)
            cache.commit()
        except Exception as e:
            msg = 'ERROR: Query put_modules_names() Error: ' + e.args[0]
            log.error(msg)
            return -2

    # TODO: implement when needed
    @staticmethod
    def update_modules_names(version_id, params_list, cache, log):
        print('not implemented yet')

    @staticmethod
    def get_evcon_names(version_id, cache, log):
        if version_id < 0 or cache is None:
            log.error('ERROR: get_evcon_names - input parameters error')
            return []

        try:
            cached_names = cache.query(EvconNames).filter(
                EvconNames.version_id == version_id).all()
            if len(cached_names) is 0:
                return []
            else:
                wrapped_names = []
                for evconName in cached_names:
                    wrapped_names.append(EvcoName(evconName.event_id, evconName.name))
                return wrapped_names

        except Exception as e:
            msg = 'ERROR: Query get_evcon_names() Error: ' + e.args[0]
            log.error(msg)
            return []

    def put_evcon_names(self, ver_id, names_list, cache, src, log):
        try:
            wrapped_names = []
            for name in names_list:
                internal_id = self.get_internal_id(cache, name.id_evco, 'evc', src, log)
                if not cache.query(exists().where(EvconNames.event_id == internal_id).where(EvconNames.version_id == ver_id)).scalar():
                    evco_name = EvconNames(event_id=internal_id, name=name.name, version_id=ver_id)
                    wrapped_names.append(EvcoName(evco_name.event_id, evco_name.name))
                    cache.add(evco_name)
            cache.commit()
            return wrapped_names
        except Exception as e:
            msg = 'ERROR: Query put_evcon_names() Error: ' + e.args[0]
            log.error(msg)
            return []

    @staticmethod
    def get_datasets_paths(version_id, dsid, cache, log):
        if version_id < 0 or cache is None:
            log.error('ERROR: get_datasets_paths - input parameters error')
            return None
        try:
            dataset_relation = cache.query(Path2Datasets).filter(
                Path2Datasets.version_id == version_id).filter(
                Path2Datasets.dataset_id == dsid).first()
            if dataset_relation is None:
                return None
            else:
                paths_wrapped = []
                for path_id in dataset_relation.path_ids:
                    cached_path = cache.query(PathsCache).filter(PathsCache.path_id == path_id).first()
                    paths_wrapped.append(DatasetsPath(cached_path.path_id, cached_path.name, 0, dsid, 'pit', cached_path.isEndPath, version_id))
                return paths_wrapped

        except Exception as e:
            msg = 'ERROR: Query get_datasets_paths() Error: ' + e.args[0]
            log.error(msg)
            return None

    @staticmethod
    def put_datasets_paths(paths, dsid, ver_id, cache, log):
        try:
            for path in paths:
                if not cache.query(exists().where(PathsCache.path_id == path.internal_id)).scalar():
                    json_path = json.dumps(path, default=lambda o: o.__dict__)
                    cached_path = PathsCache(data=json_path, version_id=ver_id, isEndPath=path.isEndPath,
                                             name=path.name, path_id=path.internal_id)
                    cache.add(cached_path)
                dataset_relation = cache.query(Path2Datasets).filter(
                    Path2Datasets.version_id == ver_id).filter(
                    Path2Datasets.dataset_id == dsid).first()
                if dataset_relation is None:
                    path_relation = Path2Datasets(dataset_id=dsid, path_ids=[path.internal_id], version_id=ver_id)
                    cache.add(path_relation)
                else:
                    if path.internal_id not in dataset_relation.path_ids:
                        dataset_relation.path_ids.append(path.internal_id)
                        flag_modified(dataset_relation, 'path_ids')
            cache.commit()
        except Exception as e:
            msg = 'ERROR: Query put_datasets_paths() Error: ' + e.args[0]
            log.error(msg)

    @staticmethod
    def update_datasets_paths(path_ids, dsid, ver_id, cache, log):
        try:
            dataset_relation = cache.query(Path2Datasets).filter(
                Path2Datasets.version_id == ver_id).filter(
                Path2Datasets.dataset_id == dsid).first()
            if dataset_relation is not None:
                dataset_relation.path_ids = path_ids
                flag_modified(dataset_relation, 'path_ids')
                cache.commit()
        except Exception as e:
            msg = 'ERROR: Query update_datasets_paths() Error: ' + e.args[0]
            log.error(msg)

    @staticmethod
    def add_parrent2dataset(path_id, dsid, version, cache, log):
        try:
            dataset_relation = cache.query(Path2Datasets).filter(
                    Path2Datasets.version_id == version).filter(
                    Path2Datasets.dataset_id == dsid).first()
            if dataset_relation is None:
                dataset_relation = Path2Datasets(dataset_id=dsid, path_ids=[path_id], version_id=version)
                cache.add(dataset_relation)
            else:
                if path_id not in dataset_relation.path_ids:
                    dataset_relation.path_ids.append(path_id)
                    flag_modified(dataset_relation, 'path_ids')
            cache.commit()
        except Exception as e:
            msg = 'ERROR: Query add_parrent2dataset() Error: ' + e.args[0]
            log.error(msg)

    @staticmethod
    def remove_parrent2dataset(path_id, dsid, version, cache, log):
        try:
            dataset_relation = cache.query(Path2Datasets).filter(
                    Path2Datasets.version_id == version).filter(
                    Path2Datasets.dataset_id == dsid).first()

            if dataset_relation is not None and path_id in dataset_relation.path_ids:
                dataset_relation.path_ids.remove(path_id)
                flag_modified(dataset_relation, 'path_ids')
            cache.commit()
        except Exception as e:
            msg = 'ERROR: Query remove_parrent2dataset() Error: ' + e.args[0]
            log.error(msg)

    def drag_n_drop_reorder(self, node_id, parent_id, new_order, cache, log):
        try:
            moved_node = cache.query(PathItemsHierarchy).filter(PathItemsHierarchy.parent_id == parent_id).filter(
                PathItemsHierarchy.child_id == node_id).first()
            if moved_node.order > new_order:
                self.update_orders(cache, new_order, moved_node.order - 1, parent_id, 1)
                moved_node.order = new_order
            else:
                self.update_orders(cache, moved_node.order + 1, new_order - 1, parent_id, -1)
                moved_node.order = new_order - 1

        except Exception as e:
            msg = 'ERROR: Query drag_n_drop_reorder() Error: ' + e.args[0]
            log.error(msg)
            return -2

    @staticmethod
    def update_orders(cache, order_from, order_to, parent_id, diff):
        nodes_to_update = cache.query(PathItemsHierarchy) \
            .filter(PathItemsHierarchy.parent_id == parent_id) \
            .filter(PathItemsHierarchy.order.between(order_from, order_to)).all()
        for node in nodes_to_update:
            node.order = node.order + diff

    def drag_n_drop_add_parent(self, node_id, parent_id, new_order, cache, log):
        try:
            max_order = self.get_max_order(cache, parent_id, log)
            if not cache.query(exists().where(PathItemsHierarchy.parent_id == parent_id).where(
                    PathItemsHierarchy.child_id == node_id)).scalar():
                copied_node = PathItemsHierarchy(parent_id=parent_id, child_id=node_id, order=new_order)
                cache.add(copied_node)
            self.update_orders(cache, new_order, max_order, parent_id, 1)

        except Exception as e:
            msg = 'ERROR: Query drag_n_drop_add_parent() Error: ' + e.args[0]
            log.error(msg)
            return -2

    @staticmethod
    def get_max_order(cache, parent_id, log):
        try:
            max_order = cache.query(PathItemsHierarchy.order).filter(
                PathItemsHierarchy.parent_id == parent_id).count()
        except Exception as e:
            msg = 'ERROR: Query get_max_order() Error: ' + e.args[0]
            log.error(msg)
            return None
        return max_order

    def drag_n_drop_move(self, node_id, parent_id, old_parent_id, new_order, cache, log):
        self.drag_n_drop_add_parent(node_id, parent_id, new_order, cache, log)
        self.drag_n_drop_delete_parent(node_id, old_parent_id, cache, log)

    def drag_n_drop_delete_parent(self, node_id, parent_id, cache, log):
        try:
            moved_node = cache.query(PathItemsHierarchy).filter(PathItemsHierarchy.parent_id == parent_id).filter(
                PathItemsHierarchy.child_id == node_id).first()
            max_order = self.get_max_order(cache, parent_id, log)
            self.update_orders(cache, moved_node.order, max_order, parent_id, -1)
            cache.delete(moved_node)

        except Exception as e:
            msg = 'ERROR: Query drag_n_drop_delete_parent() Error: ' + e.args[0]
            log.error(msg)
            return -2

    @staticmethod
    def get_all_mod_mappings(external_id, cache, log):

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
            if mapping is None or mapping.external_id < 0:
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

    def get_event_statements(self, statement_id, cache, log):
        if statement_id < 0 or cache is None:
            log.error('ERROR: get_event_statements - input parameters error')
            return -2

        try:
            cached_statements = cache.query(EventStatementsCached).filter(
                EventStatementsCached.statement_id == statement_id).all()
            if len(cached_statements) is 0:
                return None
            else:
                wrapped_statements = []
                for statement in cached_statements:
                    dict_statement = byteify(json.loads(statement.data))
                    wrapped_statements.append(
                        EvCoStatement(statement.statement_id, dict_statement['modulel'],
                                      dict_statement['classn'], dict_statement['extran'], dict_statement['processn'],
                                      dict_statement['statementtype'], statement.statement_rank))
                return wrapped_statements

        except Exception as e:
            msg = 'ERROR: Query get_event_statements() Error: ' + e.args[0]
            log.error(msg)
            return None

    def put_event_statements(self, statement_id, statements, cache, log):
        for statement in statements:
            json_params = json.dumps(statement, default=lambda o: o.__dict__)
            try:
                cached_statement = EventStatementsCached(data=json_params, statement_id=statement_id, statement_rank=statement.statementrank)
                cache.add(cached_statement)
                cache.commit()
            except Exception as e:
                msg = 'ERROR: Query put_params() Error: ' + e.args[0]
                log.error(msg)
                return -2

    @staticmethod
    def update_event_statements(internal_id, statementrank, param_name, param_value, cache, log):
        try:
            statement = cache.query(EventStatementsCached)\
                .filter(EventStatementsCached.statement_id == internal_id)\
                .filter(EventStatementsCached.statement_rank == statementrank)\
                .first()
            json_statement = json.loads(statement.data)
            json_statement[param_name] = param_value
            print("updated: " + param_name + " - " + str(param_value))
            statement.data = json.dumps(json_statement)
            flag_modified(statement, 'data')
            cache.commit()
        except Exception as e:
            msg = 'ERROR: Query update_event_statements() Error: ' + e.args[0]
            log.error(msg)
            return -2

    @staticmethod
    def get_max_rank(cache, statements_id, log):
        try:
            max_rank = cache.query(EventStatementsCached.statement_rank).filter(
                EventStatementsCached.statement_id == statements_id).count()
        except Exception as e:
            msg = 'ERROR: Query get_max_rank() Error: ' + e.args[0]
            log.error(msg)
            return None
        return max_rank

    def add_event_statement(self, statements_id, drop_line, cache, log):
        try:
            new_rank = self.get_max_rank(cache, statements_id, log)
            data = {
                "classn": "*",
                "internal_id": statements_id,
                "statementtype": 0 if drop_line else 1,
                "processn": "*",
                "extran": "*",
                "modulel": "*",
                "statementrank": new_rank}
            statement = EventStatementsCached(statement_id=statements_id, statement_rank=new_rank, data=json.dumps(data))
            cache.add(statement)
            cache.commit()

            data['stype'] = 'keep' if data.get('statementtype') == 1 else 'drop'
            return data
        except Exception as e:
            msg = 'ERROR: Query add_event_statement() Error: ' + e.args[0]
            log.error(msg)
            return -2

    @staticmethod
    def delete_event_statement(statements_id, rank, cache, log):
        try:
            cache.query(EventStatementsCached) \
                .filter(EventStatementsCached.statement_id == statements_id) \
                .filter(EventStatementsCached.statement_rank == rank) \
                .delete()
            cache.commit()
            statements_to_update = cache.query(EventStatementsCached).filter(
                EventStatementsCached.statement_id == statements_id).filter(
                EventStatementsCached.statement_rank > rank).all()
            if len(statements_to_update) > 0:
                for statement in statements_to_update:
                    dict_statement = byteify(json.loads(statement.data))
                    statement.statement_rank = statement.statement_rank - 1
                    dict_statement['statementrank'] = statement.statement_rank
                    statement.data = json.dumps(dict_statement)
                cache.commit()
        except Exception as e:
            msg = 'ERROR: Query delete_event_statement() Error: ' + e.args[0]
            log.error(msg)

    def update_streams_event(self, stream_id, internal_evcon_id, version_id, value, cache, log):
        try:
            seh = cache.query(StreamEventHierarchy).filter(
                StreamEventHierarchy.stream_id == stream_id).filter(
                StreamEventHierarchy.version_id == version_id).first()
            if internal_evcon_id > 0:
                seh.event_id = internal_evcon_id
                cache.commit()
                return internal_evcon_id
            else:
                # Hardcoded again :(
                src = 0
                internal_id = self.get_internal_id(cache, -1, 'evc', src, log)
                evco_name = EvconNames(event_id=internal_id, name=value, version_id=version_id)
                cache.add(evco_name)
                seh.event_id = internal_id
                cache.commit()
                self.add_event_statement(internal_id, true, cache, log)
                return internal_id
        except Exception as e:
            msg = 'ERROR: Query update_event_statements() Error: ' + e.args[0]
            log.error(msg)
            return -2

    @staticmethod
    def add_stream_event_relation(stream_id, event_id, version_id, cache, log):
        try:
            if not cache.query(exists().where(StreamEventHierarchy.stream_id == stream_id).where(StreamEventHierarchy.version_id == version_id)).scalar():
                seh = StreamEventHierarchy(stream_id=stream_id, event_id=event_id, version_id=version_id)
                cache.add(seh)
                cache.commit()
        except Exception as e:
            msg = 'ERROR: Query add_stream_event_relation() Error: ' + e.args[0]
            log.error(msg)
            return -2

    @staticmethod
    def get_streams_events_relations(version_id, cache, log):
        try:
            cached_relations = cache.query(StreamEventHierarchy).filter(
                StreamEventHierarchy.version_id == version_id).all()
            if len(cached_relations) is 0:
                return []
            else:
                wrapped_relations = []
                for s_e_relation in cached_relations:
                    wrapped_relations.append(
                        {'id_streamid': s_e_relation.stream_id, 'id_evcoid': s_e_relation.event_id})
                return wrapped_relations
        except Exception as e:
            msg = 'ERROR: Query get_streams_events_relations() Error: ' + e.args[0]
            log.error(msg)
            return -2

    def getCompletePathSequencesItems(self, cache, id_pathid, log, lvl=0):
        result = list()
        try:
            cached_path_children = cache.query(PathItemsHierarchy).filter(
                PathItemsHierarchy.parent_id == id_pathid).all()
            if len(cached_path_children) is 0:
                return result
            else:
                for children in cached_path_children:
                    item = self.get_wrapped_item(cache, children, lvl)
                    if (item.paetype == 2 and item.lvl == 0) or item.lvl > 0:
                        result.append(item)
                    children = self.getCompletePathSequencesItems(cache, item.internal_id, log, lvl + 1)
                    if children.__len__() > 0:
                        result.extend(children)

        except Exception as e:
            msg = 'ERROR: Query getCompletePathSequencesItems() Error: ' + e.args[0]
            log.error(msg)
        return result

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
