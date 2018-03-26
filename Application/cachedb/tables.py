# File tables.py Description:
# This files contains tables descriptions for sqlalchemy
#
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSON, ARRAY
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base

BaseCache = declarative_base()

class ParamsCached(BaseCache):
    __tablename__ = 'params_cache'
    id = Column('id', Integer, primary_key=True)
    data = Column('data', JSON)

class IdMapping(BaseCache):
    __tablename__ = 'ext2int_id_mapping'
    internal_id = Column('internal_id', Integer, primary_key=True)
    external_id = Column('external_id', Integer)
    itemtype = Column('itemtype', String)
    source = Column('source', Integer)

