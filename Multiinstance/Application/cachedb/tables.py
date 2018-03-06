# File tables.py Description:
# This files contains tables descriptions for sqlalchemy
#
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base

BaseCache = declarative_base()

class ModuleCached(BaseCache):
    __tablename__ = 'modules_cache'
    id = Column('id', Integer, primary_key=True)
    module_id = Column('module_id', Integer)
    data = Column('data', JSON)

class IdMapping(BaseCache):
    __tablename__ = 'ext2int_id_mapping'
    internal_id = Column('internal_id', Integer, primary_key=True)
    external_id = Column('external_id', Integer)
    source = Column('source', Integer)
    itemtype = Column('itemtype', String)

