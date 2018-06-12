# File tables.py Description:
# This files contains tables descriptions for sqlalchemy
#
from sqlalchemy import Column, Integer, String, BigInteger, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base

BaseCache = declarative_base()

class ParamsCached(BaseCache):
    __tablename__ = 'params_cache'
    id = Column('id', Integer, primary_key=True)
    data = Column('data', JSON)

class EndPathsCached(BaseCache):
    __tablename__ = 'endpaths_cache'
    version_id = Column('version_id', Integer, primary_key=True)
    data = Column('data', JSON)

class PathItemsCached(BaseCache):
    __tablename__ = 'path_items_cache'
    path_item_id = Column('path_item_id', Integer, primary_key=True)
    data = Column('data', JSON)

class PathItemsHierarchy(BaseCache):
    __tablename__ = 'path_items_hierarchy'
    parent_id = Column('parent_id', BigInteger, primary_key=True)
    child_id = Column('child_id', BigInteger, primary_key=True)
    order = Column('child_order', Integer)

class StreamEventHierarchy(BaseCache):
    __tablename__ = 'stream_event_hierarchy'
    stream_id = Column('stream_id', BigInteger, primary_key=True)
    event_id = Column('event_id', BigInteger, primary_key=True)
    version_id = Column('ver_id', BigInteger, primary_key=True)

class ModulesNames(BaseCache):
    __tablename__ = 'modules_names_cache'
    version_id = Column('version_id', Integer, primary_key=True)
    names = Column('names', ARRAY(String))

class EvconNames(BaseCache):
    __tablename__ = 'event_configs_names_cache'
    event_id = Column('event_id', BigInteger, primary_key=True)
    name = Column('name', String)
    version_id = Column('ver_id', Integer, primary_key=True)

class PathsCache(BaseCache):
    __tablename__ = 'paths_cache'
    path_id = Column('path_id', BigInteger, primary_key=True)
    name = Column('name', String)
    data = Column('data', JSON)
    isEndPath = Column('is_endpath', Integer)
    version_id = Column('version_id', Integer, primary_key=True)

class Path2Datasets(BaseCache):
    __tablename__ = 'paths2datasets_relation'
    dataset_id = Column('dataset_id', BigInteger, primary_key=True)
    path_ids = Column('path_ids', ARRAY(BigInteger))
    version_id = Column('ver_id', Integer, primary_key=True)

class IdMapping(BaseCache):
    __tablename__ = 'ext2int_id_mapping'
    internal_id = Column('internal_id', Integer, primary_key=True)
    external_id = Column('external_id', Integer)
    itemtype = Column('itemtype', String)
    source = Column('source', Integer)

class EventStatementsCached(BaseCache):
    __tablename__ = 'event_statements_cache'
    statement_id = Column('statement_id', Integer, primary_key=True)
    statement_rank = Column('statement_rank', Integer, primary_key=True)
    data = Column('data', JSON)
