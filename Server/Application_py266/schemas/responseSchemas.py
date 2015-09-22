from marshmallow import Schema, fields, pprint
#from collections import OrderedDict
#from ordereddict import OrderedDict
from marshmallow.ordereddict import OrderedDict
from schemas import *

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

class ResponsePathDetailsSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(PathDetailsSchema, many=True)
    class Meta:
        fields = ("success", "children")
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
        
class ResponseServiceSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(ServiceSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True         
        
class ResponseStreamItemSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(StreamItemSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True 
        
class ResponseEvcStatementSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(EvcStatementSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True         
        
class ResponseESModuleDetailsSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(ESModuleDetailsSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True        
        
class ResponseOutputModuleDetailsSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(OutputModuleDetailsSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True            
        
class ResponseGlobalPsetSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(GlobalPsetSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True       
        
class ResponseEDSourceSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(EDSourceSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True  
        
class ResponseESSourceSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(ESSourceSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True  

class ResponseDstPathsTreeSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(DstPathsTreeSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True        
        
#------------------ Summary Responses ------------------        
class ResponseSummaryColumnSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(SummaryColumnSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True
        
class ResponseSummaryItemSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(SummaryItemSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True
        
#------------ Url Response Schema -------------------------        
class ResponseUrlStringSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(UrlStringSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True        

#----------- Added By Husam ------------------------------
class ResponseFileEndPathsTreeSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(FileEndPathsTreeSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True

class ResponseFilePathsTreeSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(FilePathsTreeSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True

class ResponseFileModulesSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(FileModulesSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True

class ResponseFilePathItemSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(FilePathItemSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True  

class ResponseFileParamSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(FileParameterSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True    

class ResponseFileDstPathsTreeSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(FileDstPathsTreeSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True        

        
class ResponseFileEvcStatementSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(FileEvcStatementSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True       

class ResponseFileModuleDetailsSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(FileModuleDetailsSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True

class ResponseFileVersionSchema(Schema):
    success = fields.Boolean()
    children = fields.Nested(FileVersionSchema, many=True)
    class Meta:
        fields = ("success", "children")
        ordered = True 
