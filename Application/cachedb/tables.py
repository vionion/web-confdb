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

class PathsCached(BaseCache):
    __tablename__ = 'paths_cache'
    version_id = Column('version_id', Integer, primary_key=True)
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

class ModulesNames(BaseCache):
    __tablename__ = 'modules_names_cache'
    version_id = Column('version_id', Integer, primary_key=True)
    names = Column('names', ARRAY(String))

class IdMapping(BaseCache):
    __tablename__ = 'ext2int_id_mapping'
    internal_id = Column('internal_id', Integer, primary_key=True)
    external_id = Column('external_id', Integer)
    itemtype = Column('itemtype', String)
    source = Column('source', Integer)

