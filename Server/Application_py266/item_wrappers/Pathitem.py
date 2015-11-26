# File Pathitem.py Description:
# This contains the wrapper class of the Pathitem entity (Sequences and Modules)
#
# Class: Pathitem


class Pathitem(object):

    def __init__(self, id=0,name="", id_pathid= 0, paetype = -1, id_parent = -1, lvl = -1, order = -1, operator = 0):
        self.id = id
        self.gid = -2
#        self.gid = gid
        self.name = name
        self.id_pathid = id_pathid
        self.paetype = paetype
        self.id_parent = id_parent
        self.lvl = lvl
        self.order = order
        self.operator = operator
#        self.loaded = True
        self.expanded = True
        self.children = []
