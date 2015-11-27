# File Parameter.py Description:
# This contains the wrapper class of the Parameter entity. 
# The Parameter class represents the parameter of the modules
#
# Class: Parameter

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