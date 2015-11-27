# File FolderItem.py Description:
# This contains the wrapper class of the FolderItem entity (Folder and Configurations)
#
# Class: FolderItem


class FolderItem(object):

    def __init__(self, id=0, name="", fitype="", id_parent = -1, created = None):
        self.id = id
        self.gid = 0
        self.name = name
        self.fit = fitype
        self.id_parent = id_parent
        self.created = created
#        self.expanded = False
        self.expandable = False
        self.children = []