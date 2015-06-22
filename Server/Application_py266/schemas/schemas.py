from marshmallow import Schema, fields, pprint
#from collections import OrderedDict
from ordereddict import OrderedDict


class PathsSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    leaf = False
    loaded = False
    class Meta:
        fields = ("id", "id_path", "name", "pit")
        ordered = True
    
class PathsTreeSchema(Schema):
#    id = fields.Integer()
    gid = fields.Integer()
    id_path = fields.Integer()
    vid = fields.Integer()
    name = fields.String()
    isEndPath = fields.Integer()
    pit = fields.String()
    icon = icon = fields.Method("get_icon")
    
    def get_icon(self,obj):
        if obj.isEndPath == 0:
            return 'resources/Path_3.ico'
        elif obj.isEndPath == 1:
            return 'resources/EndPath.ico'   
        
    class Meta:
        fields = ("gid", "vid", "icon", "id_path", "name", "pit")
        ordered = True

class PathDetailsSchema(Schema):
    gid = fields.Integer()
    name = fields.String()
    labels = fields.List(fields.String())
    values =  fields.List(fields.Integer())  
    author = fields.String()
    desc = fields.String()
 
    class Meta:
        fields = ("gid", "name", "labels", "values", "author", "desc")
        ordered = True        
        
        
class PathItemSchema(Schema):
#    id = fields.Integer()
    gid = fields.Integer()
    name = fields.String()
    id_pathid = fields.String()
    paetype = fields.Integer()
    id_parent = fields.Integer()
    pit = fields.Method("get_item_type")
    leaf = fields.Method("get_leaf")
    icon = fields.Method("get_icon")
    expanded = fields.Boolean()
    children = fields.Nested('self', many=True)
    
    def get_icon(self,obj):
        if obj.paetype == 1:
            return 'resources/Module_3.ico'
        elif obj.paetype == 2:
            return 'resources/Sequence_2.ico'
        elif obj.paetype == 3:
            return 'resources/OutputModule2.ico'
        else:
            return 'resources/Module_3.ico'
    
    def get_item_type(self, obj):
        if obj.paetype == 1:
            return 'mod'
        elif obj.paetype == 2:
            return 'seq'
        elif obj.paetype == 3:
            return 'oum'
        else:
            return 'und'
        
    def get_leaf(self, obj):
        if obj.paetype == 1:
            return True
        else: 
            return False
    
    def get_loaded(self, obj):
        if obj.count == 0:
            return True
        else:
            return False
        
    class Meta:
        fields = ("gid", "name", "id_pathid", "pit", "leaf", "icon","expanded","children")
        ordered = True    
        
class PathsItemSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    paetype = fields.Integer()
    id_parent = fields.Integer()
    pit = fields.Method("get_item_type")
    leaf = fields.Method("get_leaf")
    
    def get_item_type(self, obj):
        if obj.paetype == 1:
            return 'mod'
        elif obj.paetype == 2:
            return 'seq'
        elif obj.paetype == 3:
            return 'oum'
        else:
            return 'und'
        
    def get_leaf(self, obj):
        if obj.paetype == 1:
            return True
        else: 
            return False
    
    def get_loaded(self, obj):
        if obj.count == 0:
            return True
        else:
            return False
        
    class Meta:
        fields = ("id", "name", "id_parent", "pit", "leaf")
        ordered = True
    
class ModuleDetailsSchema(Schema):
    gid = fields.Integer()
    name = fields.String()
    mti = fields.Integer()
    mt =  fields.Method("get_item_type")   
    author = fields.String()
    mclass = fields.String()
    
    def get_item_type(self, obj):
        if obj.mti == 1:
            return 'EDProducer'
        elif obj.mti == 2:
            return 'EDAnalyzer'
        elif obj.mti == 3:
            return 'EDFilter'
        elif obj.mti == 4:
            return 'HLTProducer'
        elif obj.mti == 5:
            return 'HLTFilter'
        elif obj.mti == 6:
            return 'OutputModule'
        else:
            return 'und'
 
    class Meta:
        fields = ("gid", "name", "mt", "author", "mclass")
        ordered = True
        
class OutputModuleDetailsSchema(Schema):
    gid = fields.Integer()
    name = fields.String()
    mti = fields.Integer()
    mt =  fields.Method("get_item_type")   
    author = fields.String()
    mclass = fields.String()
    stream = fields.String()
    streamid = fields.Integer()
    
    def get_item_type(self, obj):
        return 'OutputModule'
 
    class Meta:
        fields = ("gid", "name", "mt", "author", "mclass", "stream", "streamid")
        ordered = True
                
class ModuleSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    
#-----------------------------------Parameters Schemas -------------------------  
        
class ParametersSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    paramtype = fields.String()
    value = fields.String()

class ParameterSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    moetype = fields.Integer()
    paramtype = fields.String()
    value = fields.String()
    order = fields.Integer()
    lvl = fields.Integer()
    default = fields.Integer()
    tracked = fields.Integer()
    gid = fields.Method("get_gid")
    mit = fields.Method("get_item_type")
    leaf = fields.Method("get_leaf")
    icon = fields.Method("get_icon")
    expanded = fields.Boolean()
    children = fields.Nested('self', many=True)
    
    def get_icon(self,obj):
        if obj.moetype == 1:
            return 'resources/param_2.ico'
        if obj.moetype == 2:
            return 'resources/PSet_2.ico'
        elif obj.moetype == 3:
            return 'resources/Vpset_2.ico'
        else:
            return ''
    
    def get_gid(self,obj):
        return obj.id
    
    def get_item_type(self, obj):
        if obj.moetype == 1:
            return 'par'
        elif obj.moetype == 2:
            return 'pas'
        elif obj.moetype == 3:
            return 'vps'
        else:
            return 'und'
        
    def get_leaf(self, obj):
        if obj.moetype == 1:
            return True
        else: 
            return False
    
    class Meta:
        fields = ("gid", "name", "value", "order", "lvl", "mit", "paramtype", "icon", "default", "tracked", "leaf", "expanded","children")
        ordered = True

#-----------------------------------Folder and Version Schemas -------------------------    
class FolderitemSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    new_name = fields.String()
    fit = fields.String()
    created = fields.Integer()
    gid = fields.Integer()
    leaf = fields.Method("get_leaf")
    icon = fields.Method("get_icon")
    expanded = fields.Boolean()
    children = fields.Nested('self', many=True)
    
    def get_icon(self,obj):
        if obj.fit == "cnf":
            return 'resources/Config.ico'
        else:
            return ''
    
    def get_leaf(self, obj):
        if obj.fit == "cnf":
            return True
        else: 
            return False
    
    class Meta:
        fields = ("gid", "new_name", "created", "leaf", "fit", "icon", "expanded", "children")
        ordered = True


class VersionSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    id_release = fields.String()
    created = fields.String()
    version = fields.Integer()
    ver = fields.Method("get_ver")
    gid = fields.Method("get_gid")
    creator = fields.String()
    processname = fields.String()
    description = fields.String()
    
    def get_gid(self,obj):
        return obj.id
    
    def get_ver(self,obj):
        return obj.version
    
    class Meta:
        fields = ("gid", "name", "ver", "created", "creator", "id_release", "processname", "description")
        ordered = True 
    
#-----------------------------------Services Schemas ------------------------- 

class ServiceSchema(Schema):

        gid = fields.Integer()
        template_id = fields.Integer()
        release_id = fields.Integer()
        name = fields.String()
        s_type = fields.String()
        icon = fields.Method("get_icon")
        expandable = fields.Method("get_exp")
        
        def get_icon(self,obj):
            return 'resources/Service.ico'
        
        def get_exp(self,obj):
            return False
        
        class Meta:
            fields = ("gid", "name", "template_id", "release_id", "s_type", "icon", "expandable")
            ordered = True 
            
#-----------------------------------Stream Schema -------------------------             
            
class StreamItemSchema(Schema):
#    id = fields.Integer()
    gid = fields.Integer()
    name = fields.String()
    fractodisk = fields.Integer()
    s_type = fields.String()
    leaf = fields.Method("get_leaf")
    icon = fields.Method("get_icon")
    children = fields.Nested('self', many=True)
    
    def get_icon(self,obj):
        if obj.s_type == 'str':
            return 'resources/Stream.ico'
        elif obj.s_type == 'dat':
            return 'resources/Dataset.ico'
        elif obj.s_type == 'evc':
            return 'resources/EventContent.ico'
        else:
            return ''
        
    def get_leaf(self, obj):
        if obj.s_type == 'str':
            return False
        else: 
            return True
        
    class Meta:
        fields = ("gid", "name", "fractodisk", "s_type", "leaf", "icon","children")
        ordered = True

#--------------------------Event content statements Schema --------------------             
            
class EvcStatementSchema(Schema):
    id = fields.Integer()
    gid = fields.Method("get_gid")
    classn = fields.String()
    modulel = fields.String()
    extran = fields.String()
    processn = fields.String()
    statementtype = fields.String()
    stype = fields.Method("get_stype")
    statementrank = fields.Integer()
    
    def get_gid(self,obj):
        return obj.id
    
    def get_stype(self,obj):
        if obj.statementtype == 0:
            return "drop"
        else:
            return "keep"
        
    class Meta:
        fields = ("gid", "classn", "modulel", "extran", "processn", "stype", "statementrank")
        ordered = True
            
#--------------------------ES Module Schema --------------------           
    
class ESModuleDetailsSchema(Schema):
    gid = fields.Integer()
    name = fields.String()
    mclass = fields.String()
    icon = fields.Method("get_icon")
    expandable = fields.Method("get_exp")

    def get_icon(self,obj):
        return 'resources/ESModule.ico'

    def get_exp(self,obj):
        return False
    
    class Meta:
        fields = ("gid", "name", "mclass", "icon", "expandable")
        ordered = True
        
        
class GlobalPsetSchema(Schema):
    
    gid = fields.Integer()
    name = fields.String()
    tracked = fields.Integer()
    icon = fields.Method("get_icon")
    expandable = fields.Method("get_exp")

    def get_icon(self,obj):
        return 'resources/PSet_2.ico'

    def get_exp(self,obj):
        return False
    
    class Meta:
        fields = ("gid", "name", "tracked", "icon", "expandable")
        ordered = True
        
class EDSourceSchema(Schema):
    gid = fields.Integer()
    name = fields.String()
    tclass = fields.String()
    icon = fields.Method("get_icon")
    expandable = fields.Method("get_exp")

    def get_icon(self,obj):
        return 'resources/Module_3.ico'

    def get_exp(self,obj):
        return False
    
    class Meta:
        fields = ("gid", "name", "tclass", "icon", "expandable")
        ordered = True
              
class ESSourceSchema(Schema):
    gid = fields.Integer()
    name = fields.String()
    tclass = fields.String()
    icon = fields.Method("get_icon")
    expandable = fields.Method("get_exp")

    def get_icon(self,obj):
        return 'resources/ESModule.ico'

    def get_exp(self,obj):
        return False
    
    class Meta:
        fields = ("gid", "name", "tclass", "icon", "expandable")
        ordered = True

        
class DstPathsTreeSchema(Schema):
#    id = fields.Integer()
    gid = fields.Integer()
    id_path = fields.Integer()
    vid = fields.Integer()
    name = fields.String()
    isEndPath = fields.Integer()
    pit = fields.String()
    icon = icon = fields.Method("get_icon")
    expandable = fields.Method("get_exp")
    
    def get_exp(self,obj):
        return False
    
    def get_icon(self,obj):
        if obj.isEndPath == 0:
            return 'resources/Path_3.ico'
        elif obj.isEndPath == 1:
            return 'resources/EndPath.ico'   
        
    class Meta:
        fields = ("gid", "vid", "icon", "id_path", "name", "pit", "expandable")
        ordered = True        