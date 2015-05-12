# File Item_wrappers.py Description:
# This contains the wrapper class of the several system entity. 
#
# Class: Service
# The Service class represents the Service modules

class Service(object):

    def __init__(self, id=0, template_id = -1, release_id = -1, name="", s_type=""):
        self.id = id
        self.gid = -1
        self.template_id = template_id
        self.release_id = release_id
        self.name = name
        self.s_type = s_type
        
        
class PathDetails(object):

    def __init__(self, id=0, name="", labels=None, values=[],author="", description=""):
        self.gid = id
        self.name = name
        self.labels = labels
        self.values = values
        self.author = author
        self.desc = description
        
class Streamitem(object):

    def __init__(self, id=0, fractodisk = -1, name="", s_type=""):
        self.id = id
        self.gid = -1
        self.name = name
        self.fractodisk = fractodisk
        self.s_type = s_type
        self.children = []
        
class ESModuleDetails(object):

    def __init__(self, id=0, id_templ = -1, name="", mclass = "", order = -1):
        self.id = id
        self.gid = -1
        self.id_templ = id_templ
        self.name = name
        self.mclass = mclass 
        self.order = order 
            
class OutputModuleDetails(object):

    def __init__(self, id=0, name="", mclass = "", author="", stream="", streamid = -1):
        self.id = id
        self.gid = -1
        self.name = name
        self.mclass = mclass
        self.author = author
        self.stream = stream
        self.streamid = streamid
        
class GlobalPset(object):

    def __init__(self, id=0, name="", tracked = -1):
        self.id = id
        self.gid = -1
        self.name = name
        self.tracked = tracked
        
class EDSource(object):

    def __init__(self, id=0, id_templ = -1, name="", order = -1):
        self.id = id
        self.gid = -1
        self.id_templ = id_templ
        self.name = name
        self.order = order     
          
class ESSource(object):

    def __init__(self, id=0, id_templ = -1, name="", order = -1):
        self.id = id
        self.gid = -1
        self.id_templ = id_templ
        self.name = name
        self.order = order 
        
        