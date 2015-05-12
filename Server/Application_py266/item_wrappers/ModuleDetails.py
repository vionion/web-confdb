# File ModuleDetails.py Description:
# This contains the wrapper class of the ModuleDetails entity. 
# The ModuleDetails class represents the main details to desplay on each module
#
# Class: ModuleDetails

class ModuleDetails(object):

    def __init__(self, id=0, name="", mti=0, author="", mclass = ""):
        self.id = id
        self.gid = -1
        self.name = name
        self.mti = mti
        self.author = author
        self.mclass = mclass