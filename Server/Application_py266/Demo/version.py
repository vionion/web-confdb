
from sqlalchemy import Sequence
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, select, DateTime, case, and_, func, join 
from sqlalchemy.orm import relationship, backref, column_property, object_session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql import text, literal_column

Base = automap_base()

    
class Pathidconf(Base):
    # nome della tabella
    __tablename__ = 'u_pathid2conf'

    id = Column('id', Integer, primary_key=True)
    id_confver = Column(ForeignKey('u_confversions.id'))
    id_pathid = Column(ForeignKey('u_pathids.id'))
 
class Paths(Base):
    # nome della tabella
    __tablename__ = 'u_paths'

    id = Column('id', Integer, primary_key=True)
    name = Column(String)
    paetype = "pat"

class Pathids(Base):
    # nome della tabella
    __tablename__ = 'u_pathids'

    id = Column('id', Integer, primary_key=True)
    id_path = Column(ForeignKey('u_paths.id'))
    #isendpath = Column(Integer)
    name = column_property(
        select([Paths.name]).where(Paths.id == id_path)
    )
    pit = "pat"

    
class Pathelement(Base):
    # nome della tabella
    __tablename__ = 'u_paelements'

    id = Column('id', Integer, primary_key=True)
    name = Column(String)
    paetype = Column(Integer)
#    id_pathid = column_property(select([Pathitems.id_pathid]).where(Pathitems.id_pae == id))
#    id_parent = column_property(select([Pathitems.id_parent]).where(Pathitems.id_pae == id))
#    order = column_property(select([Pathitems.order]).where(Pathitems.id_pae == id))

#    @property
#    def id_parent(self):
#        return object_session(self).scalar(select([Pathitems.id_parent]).where(Pathitems.id_pae == self.id))

#    @property
#    def id_pathid(self):
#        return object_session(self).scalar(select([Pathitems.id_pathid]).where(Pathitems.id_pae == self.id))
    
#    @property
#    def order(self):
#        return object_session(self).scalar(select([Pathitems.order]).where(Pathitems.id_pae == self.id))    

class Pathitem():

    def __init__(self, id=0,name="", id_pathid= 0, paetype = -1, id_parent = -1, lvl = -1, order = -1):
        self.id = id
#        self.gid = gid
        self.name = name
        self.id_pathid = id_pathid
        self.paetype = paetype
        self.id_parent = id_parent
        self.lvl = lvl
        self.order = order
#        self.loaded = True
        self.expanded = True
        self.children = []
    
class Pathitems(Base):
    __tablename__ = 'u_pathid2pae'

    id = Column('id', Integer, primary_key=True)
    id_pathid = Column(Integer, ForeignKey('u_pathids.id'))
    id_pae = Column('id_pae', Integer, ForeignKey('u_paelements.id'))
    id_parent = Column(Integer)
#    pathelement = relationship("Pathelement", backref=backref("u_pathid2pae"))
    lvl = Column(Integer) #1, 'mod', 2, 'seq', 3, 'oum', 'Undefined'
    order = Column('ord', Integer)
#    name = column_property(select([Pathelement.name]).where(Pathelement.id == id_pae)) 
#    paetype = column_property(select([Pathelement.paetype]).where(Pathelement.id == id_pae))
##    count = column_property(select([func.count(literal_column("u_pathid2pae.id"))]).where(literal_column("u_pathid2pae.id_pae") == id_parent))               

##   
#class Pathitems(Base):
#    __tablename__ = 'u_pathid2pae'
#
#    id = Column('id', Integer, primary_key=True)
#    id_pathid = Column(Integer, ForeignKey('u_pathids.id'))
#    id_pae = Column(Integer, ForeignKey('u_paelements.id'))
#    id_parent = Column(Integer)
##    lvl = Column(Integer) 1, 'mod', 2, 'seq', 3, 'oum', 'Undefined'
#    ord = Column(Integer)
#    name = column_property(select([Pathelement.name]).where(Pathelement.id == id_pae)) 
#    paetype = column_property(select([Pathelement.paetype]).where(Pathelement.id == id_pae))
#    count = column_property(select([func.count(literal_column("u_pathid2pae.id"))]).where(literal_column("u_pathid2pae.id_pae") == id_parent))         

#class Module(Base):
#    # nome della tabella
#    __tablename__ = 'u_paelements'
#
#    id = Column('id', Integer, primary_key=True)
#    name = Column(String)
#    paetype = Column(Integer)
     
class Paetypes(Base):
     # nome della tabella
    __tablename__ = 'u_paetypes'

    id = Column('id', Integer, primary_key=True)
    name = Column(String)

#------------------ Module items: Pset, VPset, Params ---------------    
class Modelement(Base):
     # nome della tabella
    __tablename__ = 'u_moelements'

    id = Column('id', Integer, primary_key=True)
    name = Column(String)
    moetype = Column(Integer)
    paramtype = Column(String)
    value = Column(String)
    tracked = Column(Integer)
    
class Moduleitem(Base):
     # nome della tabella
    __tablename__ = 'u_pae2moe'

    id = Column('id', Integer, primary_key=True)
    id_pae = Column('id_pae', Integer, ForeignKey('u_paelements.id'))
    id_moe = Column('id_moe', Integer, ForeignKey('u_moelements.id'))
    lvl = Column(Integer)
    order = Column('ord',Integer)
    
class Parameter(object):

    def __init__(self, id=0,name="", value="",paetype = -1, partype="", id_parent = -1, lvl = -1, order = -1, track=False):
        self.id = id
#        self.gid = gid
        self.name = name
        self.value = value
        self.moetype = paetype
        self.paramtype = partype
        self.id_parent = id_parent
        self.lvl = lvl
        self.order = order
#        self.loaded = True
        self.expanded = True
        self.tracked = track
        self.default = False
        self.children = []
        
#-------------------- ED Template ------------------
class ModTemplate(Base):
     # nome della tabella
    __tablename__ = 'u_moduletemplates'

    id = Column('id', Integer, primary_key=True)
    name = Column(String)
    id_mtype = Column('id_mtype', Integer) #ForeignKey('u_moduletypes.id')
        
class ModToTemp(Base):
     # nome della tabella
    __tablename__ = 'u_mod2templ'

    id = Column('id', Integer, primary_key=True)
    id_pae = Column('id_pae', Integer, ForeignKey('u_paelements.id'))
    id_templ = Column('id_templ', Integer, ForeignKey('u_moduletemplates.id'))
 
class ModTelement(Base):
     # nome della tabella
    __tablename__ = 'u_modtelements'

    id = Column('id', Integer, primary_key=True)
    id_modtemp = Column('id_modtemplate', Integer, ForeignKey('u_moduletemplates.id'))
    moetype = Column(Integer)
    name = Column(String)    
    lvl = Column(Integer)
    order = Column('ord',Integer)
    paramtype = Column(String)
    value = Column(String)
    tracked = Column(Integer)
    
class Moduletypes(Base):
    __tablename__ = 'u_moduletypes'

    id = Column('id', Integer, primary_key=True)
    mtype = Column('type', String)
    
class ModuleDetails(object):

    def __init__(self, id=0,name="", mti=0, author="", mclass = ""):
        self.id = id
        self.gid = -1
        self.name = name
        self.mti = mti
        self.author = author
        self.mclass = mclass

#------------ Directories --------------------

class Directory(Base):
    __tablename__ = 'u_directories'
    
    id = Column('id', Integer, primary_key=True)
    id_parentdir = Column(Integer)
    name = Column(String)    
    created = Column(DateTime)
    
class Configuration(Base):
    __tablename__ = 'u_configurations'
    
    id = Column('id', Integer, primary_key=True)
    name = Column(String)    

class Version(Base):
    # nome della tabella
    __tablename__ = 'u_confversions'
    # definisco che id \'e un numero intero in sequenza e chiave primaria
    id = Column('id', Integer, primary_key=True)
    id_config = Column('id_config', Integer, ForeignKey('u_configurations.id'))
    id_parentdir = Column('id_parentdir', Integer, ForeignKey('u_directories.id'))
    name = Column(String)
    id_release = Column(Integer)
    version = Column(Integer)   
    created = Column(DateTime)
    creator = Column(String)
    
class FolderItem(object):

    def __init__(self, id=0,name="", fitype="", id_parent = -1, created = None):
        self.id = id
        self.gid = 0
        self.name = name
        self.fit = fitype
        self.id_parent = id_parent
        self.created = created
        self.expanded = False
        self.children = []
    
    
#-------- Response

class Response(object):
    
    success = False
    children = None
    
class ResponseTree(object):
    
    success = False
    children = None

class ResponseTreeItem(object):
    
    success = False
    children = None