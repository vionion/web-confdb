
from sqlalchemy import Sequence
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, select, DateTime, case, and_, func, join, CLOB 
from sqlalchemy.orm import relationship, backref, column_property, object_session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql import text, literal_column

BaseCache = automap_base()

class Dict(BaseCache):
    # nome della tabella
    __tablename__ = 'dict'

    id = Column('id', Integer, primary_key=True)
    gid = Column(Integer)
    dbid = Column(Integer)
    
class DictOnline(BaseCache):
    # nome della tabella
    __tablename__ = 'dictOnline'

    id = Column('id', Integer, primary_key=True)
    gid = Column(Integer)
    dbid = Column(Integer)   
    
class DictOffline(BaseCache):
    # nome della tabella
    __tablename__ = 'dictOffline'

    id = Column('id', Integer, primary_key=True)
    gid = Column(Integer)
    dbid = Column(Integer)        