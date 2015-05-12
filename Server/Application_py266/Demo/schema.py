from marshmallow import Schema, fields, pprint
from collections import OrderedDict

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
    pit = fields.String()
    icon = icon = fields.Method("get_icon")
    
    def get_icon(self,obj):
            return 'resources/Path_3.ico'
    
    class Meta:
        fields = ("gid", "vid", "icon", "id_path", "name", "pit")
        ordered = True

class PathItemSchema(Schema):
#    id = fields.Integer()
    gid = fields.Integer()
    name = fields.String()
    id_pathid = fields.String()
    paetype = fields.Integer()
#    id_pathid = fields.Integer()
    id_parent = fields.Integer()
#    count = fields.Integer()
    pit = fields.Method("get_item_type")
    leaf = fields.Method("get_leaf")
    icon = fields.Method("get_icon")
#    loaded = fields.Boolean()
    expanded = fields.Boolean()
    children = fields.Nested('self', many=True)
    
    def get_icon(self,obj):
        if obj.paetype == 1:
            return 'resources/Module_3.ico'
        elif obj.paetype == 2:
            return 'resources/Sequence_2.ico'
        elif obj.paetype == 3:
            return 'oum'
        else:
            return ''
    
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
#    id_pathid = fields.Integer()
    id_parent = fields.Integer()
#    count = fields.Integer()
    pit = fields.Method("get_item_type")
    leaf = fields.Method("get_leaf")
#    loaded = fields.Method("get_loaded")
    
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
    
class ModuleSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    
class ResponseSchema(Schema):
    success = fields.Boolean()
    data = fields.Nested(ModuleSchema, many=True)
    class Meta:
        fields = ("success", "data")
        ordered = True
        
class ResponsePathTreeSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(PathsTreeSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True

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
#    count = fields.Integer()
    leaf = fields.Method("get_leaf")
    icon = fields.Method("get_icon")
#    loaded = fields.Boolean()
    expanded = fields.Boolean()
    children = fields.Nested('self', many=True)
    
    def get_icon(self,obj):
        if obj.moetype == 1:
            return 'resources/param_2.ico'
        if obj.moetype == 2:
            return 'resources/PSet_2.ico'
        elif obj.moetype == 3:
            return 'resources/PSet_2.ico'
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

#-----------------------------------Folder and Version Schemas --------------------------------------------------------------        

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
    created = fields.Integer()
    version = fields.Integer()
    ver = fields.Method("get_ver")
    gid = fields.Method("get_gid")
    creator = fields.String()
    
    def get_gid(self,obj):
        return obj.id
    
    def get_ver(self,obj):
        return obj.version
    
    class Meta:
        fields = ("gid", "name", "ver", "created", "creator", "id_release")
        ordered = True        
        

#-----------------------------------Responses Schemas -----------------------------------------------------------------------        

class ResponseVersionSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(VersionSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True 

class ResponseFolderitemSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(FolderitemSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True  

class ResponseParamSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(ParameterSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True    
 
class ResponseParamsSchema(Schema):
    success = fields.Boolean()
    data = fields.Nested(ParameterSchema, many=True)
    class Meta:
        fields = ("success", "data")
        ordered = True    
        
class ResponsePathsSchema(Schema):
    success = fields.Boolean()
    data = fields.Nested(PathsSchema, many=True)
    class Meta:
        fields = ("success", "data")
        ordered = True  

class ResponsePathItemSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(PathItemSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True  
        
class ResponsePathItemsSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(PathsItemSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True  
   
class ResponseModuleDetailsSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(ModuleDetailsSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True 