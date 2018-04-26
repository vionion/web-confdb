# File Item_wrappers.py Description:
# This contains the wrapper class of the several system entity.
#
# Class: Service
# The Service class represents the Service modules

class Service(object):

    def __init__(self, id = 0, template_id = -1, release_id = -1, name = "", s_type = ""):
        self.internal_id = id
        self.template_id = template_id
        self.release_id = release_id
        self.name = name
        self.s_type = s_type


class PathDetails(object):

    def __init__(self, id = 0, name = "", labels = None, values = [], author = "", description = ""):
        self.gid = id
        self.name = name
        self.labels = labels
        self.values = values
        self.author = author
        self.desc = description

class Streamitem(object):

    def __init__(self, id = 0, fractodisk = -1, name = "", s_type = ""):
        self.internal_id = id
        self.name = name
        self.fractodisk = fractodisk
        self.s_type = s_type
        self.children = []

class ESModuleDetails(object):

    def __init__(self, id = 0, id_templ = -1, name = "", mclass = "", order = -1):
        self.internal_id = id
        self.id_templ = id_templ
        self.name = name
        self.mclass = mclass
        self.order = order

class OutputModuleDetails(object):

    def __init__(self, id = 0, name = "", mclass = "", author = "", stream = "", streamid = -1):
        self.id = id
        self.gid = -1
        self.name = name
        self.mclass = mclass
        self.author = author
        self.stream = stream
        self.streamid = streamid

class GlobalPset(object):

    def __init__(self, id = 0, name = "", tracked = -1):
        self.id = id
        self.gid = -1
        self.name = name
        self.tracked = tracked

class EDSource(object):

    def __init__(self, id = 0, id_templ = -1, name = "", tclass = "", order = -1):
        self.internal_id = id
        self.id_templ = id_templ
        self.name = name
        self.tclass = tclass
        self.order = order

class ESSource(object):

    def __init__(self, id = 0, id_templ = -1, name = "", tclass = "", order = -1):
        self.internal_id = id
        self.id_templ = id_templ
        self.name = name
        self.tclass = tclass
        self.order = order

class SummaryColumn(object):

    def __init__(self, gid = -1, name = "", order = -1):
        self.gid = gid
        self.name = name
        self.order = order

class SummaryValue(object):

    def __init__(self, label = "", value = ""):
        self.label = label
        self.value = value

class Summaryitem(object):

    def __init__(self, id = 0, name = "", sit = "", leaf = False, icon = ""):
        self.id = id
        self.gid = -1
        self.name = name
        self.sit = sit
        self.leaf = leaf
        self.icon = icon
        self.children = []
        self.values = []

class ListContainer(object):
    def __init__(self):
        self.children = []

class SmartPrescale(object):
    def __init__(self, stream = -1):
        self.stream = stream
        self.children = {}

class UrlString(object):
    def __init__(self, gid = 0, url = ""):
        self.gid = gid
        self.url = url

#-------------------- Added By Husam ----------------------
class PathObj(object):
    def __init__(self, id = -1, id_path = -1, name = "", pit = ""):
        self.id = id
        self.id_path = id_path
        self.name = name
        self.pit = pit

class FileModuleDetails(object):
    def __init__(self, id = 0, name = "", mt = "", mclass = ""):
        self.id = id
        self.gid = -1
        self.name = name
        self.mt = mt
        self.mclass = mclass

class FilePathitem(object):
    def __init__(self, id = 0, name = "", id_pathid = 0, paetype = -1, order = -1, operator = 0):
        self.id = id
        self.gid = -2
        self.name = name
        self.id_pathid = id_pathid
        self.paetype = paetype
        self.order = order
        self.operator = operator
        self.expanded = False
        self.children = []

class FileParameter(object):
    def __init__(self, id = 0, name = "", value = "", paetype = -1, partype = "", order = -1, track = False):
        self.id = id
        self.name = name
        self.value = value
        self.moetype = paetype
        self.paramtype = partype
        self.order = order
        self.expanded = False
        self.tracked = track
        self.default = False
        self.children = []

class FileEvcoParameter(object):
    def __init__(self, id = 0, statement_type = "", class_name = "", module_element = "", extra_name = "", process_name = ""):
        self.id = id
        self.classn = class_name
        self.modulel = module_element
        self.extran = extra_name
        self.processn = process_name
        self.statementtype = statement_type

class FileVersion(object):
    def __init__(self, id = 0, name = ""):
        self.id = id
        self.name = name

class EndPathPrescale(object):
    def __init__(self, streamid):
        self.streamid = streamid
        self.prescales = {}


class Path(object):

    def __init__(self, internal_id=0, id_path=0, description="", name="", vid=0, order=0, isEndPath=0):
        self.internal_id = internal_id
        self.name = name
        self.id_path = id_path
        self.description = description
        self.vid = vid
        self.order = order
        self.isEndPath = isEndPath
        self.pit = "pat"
