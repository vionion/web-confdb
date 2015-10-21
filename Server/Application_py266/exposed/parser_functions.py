# Class: Parser_Functions

from confdb_queries.confdb_queries import ConfDbQueries
from item_wrappers.FolderItem import *
from item_wrappers.ModuleDetails import *
from item_wrappers.Pathitem import *
from item_wrappers.Parameter import *
from item_wrappers.item_wrappers import *
from schemas.responseSchemas import *
from responses.responses import *
from marshmallow import Schema, fields, pprint
#from collections import OrderedDict
#from ordereddict import OrderedDict
from marshmallow.ordereddict import OrderedDict
from params_builder import ParamsBuilder
from summary_builder import SummaryBuilder
import string
import re
from utils import * 

class Parser_Functions(object):
    summaryItemCounter = Counter()

    def getGPsetsFromFile(self, config_id, config_dict=None):
        config_obj = config_dict.get(int(config_id))
        resp = Response()
        resp.children = []

        for key in config_obj.global_pset_dict:
            gpset = GlobalPset(config_obj.global_pset_dict[key].id, config_obj.global_pset_dict[key].name, int(config_obj.global_pset_dict[key].gpset_tracked))
            gpset.gid = config_obj.global_pset_dict[key].id

            if (gpset is not None):
                resp.children.append(gpset)

        schema = ResponseGlobalPsetSchema()
        
        resp.success = True

        output = schema.dump(resp)
            
        return output.data

    def getGPsetsItemsFromFile(self, config_id, gPsetId, config_dict=None):
        config_obj = config_dict.get(int(config_id))

        gpset = config_obj.global_pset_dict.get(gPsetId)

        gpsetItems = self.getComponentItems(config_obj, gpset.children, 0)

        resp = Response()
        resp.children = gpsetItems
        schema = ResponseFileParamSchema()
        
        resp.success = True

        output = schema.dump(resp)
            
        return output.data

    def getStreamsFromFile(self, config_id, config_dict=None):
        config_obj = config_dict.get(int(config_id))
        streams_data = {}

        for key in config_obj.streams_dict:
            stream_obj = Streamitem(config_obj.streams_dict[key].id,-1,config_obj.streams_dict[key].name,"str")
            stream_obj.gid = config_obj.streams_dict[key].id
            streams_data[config_obj.streams_dict[key].id] = stream_obj
            for event in config_obj.eventContent_dict:
                if config_obj.eventContent_dict[event].name.replace("hltEventContent","") == config_obj.streams_dict[key].name:
                    event_obj = Streamitem(config_obj.eventContent_dict[event].id,-1,config_obj.eventContent_dict[event].name,"evc")   
                    event_obj.gid = config_obj.eventContent_dict[event].id
                    streams_data.get(config_obj.streams_dict[key].id).children.append(event_obj)
            for param in config_obj.streams_dict[key].children:
                if param in config_obj.datasets_dict:
                    dataset_obj = Streamitem(config_obj.datasets_dict[param].id,-1,config_obj.datasets_dict[param].name,"dat")   
                    dataset_obj.gid = config_obj.datasets_dict[param].id
                    streams_data.get(config_obj.streams_dict[key].id).children.append(dataset_obj)

        resp = Response()
        
        resp.children = streams_data.values()
        resp.children.sort(key=lambda par: par.name)
        schema = ResponseStreamItemSchema()
        
        resp.success = True

        output = schema.dump(resp)
            
        return output.data

    def getDataSetItemsFromFile(self, config_id, dataSet_id,config_dict=None):
        config_obj = config_dict.get(int(config_id))

        paths = []
        path = None

        dataset = config_obj.datasets_dict.get(dataSet_id)

        i = 0

        for child in dataset.children:
            path_object = config_obj.paths_dict.get(child)
            if path_object is not None:
                path = PathObj(path_object.id, path_object.id, path_object.name, 'pat')
                path.vid = config_id
                path.order = i
                path.gid = path_object.id

            if (path is not None):
                paths.append(path) 

        paths.sort(key=lambda par: par.order)
        resp = Response()
        resp.children = paths
        schema = ResponseFileDstPathsTreeSchema()
        
        resp.success = True

        output = schema.dump(resp)
            
        return output.data

    def getEvcoStatementsFromFile(self, config_id, evco_id, config_dict=None):
        config_obj = config_dict.get(int(config_id))

        statements = []

        evco = config_obj.eventContent_dict.get(evco_id)

        i = 0

        for child in evco.children:
            param = config_obj.eventContentParams_dict.get(child)
            statement = None
            if param is not None:
                statement = FileEvcoParameter(param.id, param.ptype, param.name, param.moduleElement, param.extraName, param.processName)
                statement.gid = param.id
                statement.statementrank = i
                i = i + 1

            if statement is not None:
                statements.append(statement)

        statements.sort(key=lambda par: par.statementrank)
        
        resp = Response()
        resp.children = statements
        schema = ResponseFileEvcStatementSchema()
        
        resp.success = True
         #params 

        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)
        
        return output.data 


    def getEdSourceFromFile(self, config_id, config_dict=None):
        config_obj = config_dict.get(int(config_id))
        edSources = []

        for key in config_obj.edSources_dict:
            ed_source = EDSource(config_obj.edSources_dict[key].id, config_obj.edSources_dict[key].template, "Source", config_obj.edSources_dict[key].name)
            ed_source.gid = config_obj.edSources_dict[key].id
            if (ed_source != None):
                edSources.append(ed_source) 
            
        edSources.sort(key=lambda par: par.order)
        resp = Response()
        resp.children = [] 
        
        resp.children.extend(edSources)
        schema = ResponseEDSourceSchema()
        
        resp.success = True

        output = schema.dump(resp)
            
        return output.data

    def getEdSourceItemsFromFile(self, config_id, source_id, config_dict=None):
        config_obj = config_dict.get(int(config_id))

        edSource = config_obj.edSources_dict.get(source_id)

        edSourceItems = self.getComponentItems(config_obj, edSource.children, 0)

        resp = Response()
        resp.children = edSourceItems
        schema = ResponseFileParamSchema()
        
        resp.success = True

        output = schema.dump(resp)
            
        return output.data

    def getEsSourcesFromFile(self, config_id, config_dict=None):
        config_obj = config_dict.get(int(config_id))
        esSources = []

        for key in config_obj.esSources_dict:
            es_source = ESSource(config_obj.esSources_dict[key].id, config_obj.esSources_dict[key].id, config_obj.esSources_dict[key].name, config_obj.esSources_dict[key].name)
            es_source.gid = config_obj.esSources_dict[key].id

            if (es_source != None):
                esSources.append(es_source) 

        esSources.sort(key=lambda par: par.order)
        resp = Response()
        resp.children = [] 
        
        resp.children.extend(esSources)
        schema = ResponseESSourceSchema()
        
        resp.success = True

        output = schema.dump(resp)
            
        return output.data

    def getEsSourceItemsFromFile(self, config_id, esSource_id, config_dict=None):
        config_obj = config_dict.get(int(config_id))

        esSource = config_obj.esSources_dict.get(esSource_id)

        esSourceItems = self.getComponentItems(config_obj, esSource.children, 0)

        resp = Response()
        resp.children = esSourceItems
        schema = ResponseFileParamSchema()
        
        resp.success = True

        output = schema.dump(resp)
            
        return output.data

    def getEsModulesFromFile(self, config_id, config_dict=None):
        config_obj = config_dict.get(int(config_id))
        esModules = []

        for key in config_obj.esModules_dict:
            es_module = ESModuleDetails(config_obj.esModules_dict[key].id, config_obj.esModules_dict[key].id, config_obj.esModules_dict[key].name, config_obj.esModules_dict[key].template)
            es_module.gid = config_obj.esModules_dict[key].id

            if (es_module != None):
                esModules.append(es_module) 

        esModules.sort(key=lambda par: par.order)
        resp = Response()
        resp.children = [] 
        
        resp.children.extend(esModules)
        schema = ResponseESModuleDetailsSchema()
        
        resp.success = True

        output = schema.dump(resp)
            
        return output.data

    def getEsModulesItemsFromFile(self, config_id, esModule_id, config_dict=None):
        config_obj = config_dict.get(int(config_id))

        esModule = config_obj.esModules_dict.get(esModule_id)

        esModuleItems = self.getComponentItems(config_obj, esModule.children, 0)

        resp = Response()
        resp.children = esModuleItems
        schema = ResponseFileParamSchema()
        
        resp.success = True

        output = schema.dump(resp)
            
        return output.data

    def getServiceFromFile(self, config_id, config_dict=None):
        config_obj = config_dict.get(int(config_id))
        services = []

        for key in config_obj.services_dict:
            service = Service(config_obj.services_dict[key].id, config_obj.services_dict[key].id, config_obj.services_dict[key].id, config_obj.services_dict[key].name, "")
            service.gid = config_obj.services_dict[key].id

            if (service != None):
                services.append(service) 

        resp = Response()
        resp.children = [] 
        
        resp.children.extend(services)
        schema = ResponseServiceSchema()
        
        resp.success = True

        output = schema.dump(resp)
            
        return output.data

    def getServiceItemsFromFile(self, config_id, service_id, config_dict=None):
        config_obj = config_dict.get(int(config_id))

        service = config_obj.services_dict.get(service_id)

        serviceItems = self.getComponentItems(config_obj, service.children, 0)

        resp = Response()
        resp.children = serviceItems
        schema = ResponseFileParamSchema()
        
        resp.success = True

        output = schema.dump(resp)
            
        return output.data

    def getModulesFromFile(self, config_id, config_dict=None):
        config_obj = config_dict.get(int(config_id))
        modules = []

        for key in config_obj.modules_dict:
            module = FileModuleDetails(config_obj.modules_dict[key].id, config_obj.modules_dict[key].name, config_obj.modules_dict[key].module_type, config_obj.modules_dict[key].template)
            module.gid = config_obj.modules_dict[key].id 

            if (module != None):
                modules.append(module) 

        resp = Response()
        resp.children = [] 
        
        resp.children.extend(modules)
        schema = ResponseFileModulesSchema()
        
        resp.success = True

        output = schema.dump(resp)
            
        return output.data

    def getModDetailsFromFile(self, config_id, module_id, config_dict=None):
        config_obj = config_dict.get(int(config_id))

        module = config_obj.modules_dict.get(module_id)

        moduleDetail = ModuleDetails(module_id, module.name, module.module_type, "", module.template)
        moduleDetail.gid = module_id

        resp = Response()
        schema = ResponseFileModuleDetailsSchema()

        resp.success = True
        resp.children = []
        resp.children.append(moduleDetail)
        
        output = schema.dump(resp)

        return output.data


    def getModuleItemsFromFile(self, config_id, module_id, config_dict=None):
        config_obj = config_dict.get(int(config_id))

        module = config_obj.modules_dict.get(module_id)

        if module == None:
            module = config_obj.endPathModules.get(module_id)

        moduleItems = self.getComponentItems(config_obj, module.children, 0)

        resp = Response()
        resp.children = moduleItems
        schema = ResponseFileParamSchema()
        
        resp.success = True

        output = schema.dump(resp)
            
        return output.data

    def getEndPathsFromFile(self, config_id, config_dict=None):
        config_obj = config_dict.get(int(config_id))
        endPaths = []
        i = 0

        for key in config_obj.endPaths_dict:
            endPath = PathObj(config_obj.endPaths_dict[key].id, config_obj.endPaths_dict[key].id, config_obj.endPaths_dict[key].name, 'pat')
            endPath.vid = config_id
            endPath.order = i
            endPath.gid = config_obj.endPaths_dict[key].id
            i = i+1
            if (endPath != None):
                endPaths.append(endPath) 

        endPaths.sort(key=lambda par: par.order)
        resp = Response()
        resp.children = endPaths
        schema = ResponseFileEndPathsTreeSchema()
        
        resp.success = True

        output = schema.dump(resp)
            
        return output.data

    def getEndPathItemsFromFile(self, config_id, endPath_id=-1, config_dict=None):
        config_obj = config_dict.get(int(config_id))
        endPathItems = []
        i = 0

        endPath = config_obj.endPaths_dict.get(endPath_id)

        for child in endPath.children:
            endPathItem = None
            if child[0] in config_obj.modules_dict and child[1] == 'mod':
                endPathItem = FilePathitem(config_obj.modules_dict.get(child[0]).id, config_obj.modules_dict.get(child[0]).name, endPath_id, 1, i, config_obj.modules_dict.get(child[0]).operator)
                endPathItem.gid = config_obj.modules_dict.get(child[0]).id
            elif child[0] in config_obj.endPathModules and child[1] == 'oum':
                endPathItem = FilePathitem(config_obj.endPathModules.get(child[0]).id, config_obj.endPathModules.get(child[0]).name, endPath_id, 3, i)
                endPathItem.gid = config_obj.endPathModules.get(child[0]).id
            elif child[0] in config_obj.sequences_dict and child[1] == 'seq':
                endPathItem = FilePathitem(config_obj.sequences_dict.get(child[0]).id, config_obj.sequences_dict.get(child[0]).name, endPath_id, 2, i)
                i = i + 1
                endPathItem.children, i = self.buildPathItemChildren(config_obj.sequences_dict.get(child[0]).children, i, config_id, endPath_id)
                endPathItem.gid = config_obj.sequences_dict.get(child[0]).id

            endPathItem.vid = config_id    
            i = i+1

            if endPathItem is not None:
                endPathItems.append(endPathItem)

        endPathItems.sort(key=lambda par: par.order)

        resp = Response()
        resp.children= endPathItems
        schema = ResponseFilePathItemSchema()
        
        resp.success = True

        output = schema.dump(resp)
            
        return output.data

    def getOutmodDetails(self, config_id, outputModule_id, config_dict=None):
        config_obj = config_dict.get(int(config_id))

        outputModule = config_obj.endPathModules.get(outputModule_id)

        outputModuleDetail = OutputModuleDetails(outputModule.id, outputModule.name, "", "", outputModule.name.replace("hltOutput",""), outputModule_id)
        outputModuleDetail.gid = outputModule_id

        resp = Response()
        schema = ResponseOutputModuleDetailsSchema()

        resp.success = True
        resp.children = []
        resp.children.append(outputModuleDetail)
        
        output = schema.dump(resp)

        return output.data

    def getComponentItems(self, config_obj, children, i):
        items = []

        for key in children:
            param = config_obj.parameters_dict.get(key)
            item = None
            if param.moetype == 1:
                item = FileParameter(param.id, param.name, param.value, 1, param.ptype, i, param.tracked)
            else:
                ptype = "VPSet" if param.moetype == 3 else "PSet"
                item = FileParameter(param.id, param.name, "", param.moetype, ptype, i, param.tracked)
                if param.children is not None:
                    i = i + 1
                    item.children, i = self.buildComponentChildren(param.children, i, config_obj)

            i = i + 1

            if item is not None:
                items.append(item)

        items.sort(key=lambda par: par.order)

        return items

    def buildComponentChildren(self, children, i, config_obj, config_dict=None):
        moduleItems = []

        for key in children:
            param = config_obj.parameters_dict.get(key)
            moduleItem = None
            if param.moetype == 1:
                moduleItem = FileParameter(param.id, param.name, param.value, param.moetype, param.ptype, i, param.tracked)
            else:
                ptype = "VPSet" if param.moetype == 3 else "PSet"
                moduleItem = FileParameter(param.id, param.name, "", param.moetype, ptype, i, param.tracked)
                if param.children is not None:
                    i = i + 1
                    moduleItem.children, i = self.buildComponentChildren(param.children, i, config_obj)

            i = i + 1

            if moduleItem is not None:
                moduleItems.append(moduleItem)

        return moduleItems, i
    
    def getPathsFromFile(self, config_id, config_dict=None):
        config_obj = config_dict.get(int(config_id))
        paths = []
        i = 0

        for key in config_obj.paths_dict:
            path = PathObj(config_obj.paths_dict[key].id, config_obj.paths_dict[key].id, config_obj.paths_dict[key].name, 'pat')
            path.vid = config_id
            path.order = i
            path.gid = config_obj.paths_dict[key].id
            i = i+1
            if (path is not None):
                paths.append(path) 

        paths.sort(key=lambda par: par.order)
        resp = Response()
        resp.children = paths
        schema = ResponseFilePathsTreeSchema()
        
        resp.success = True

        output = schema.dump(resp)
            
        return output.data

    def getPathItemsFromFile(self, config_id, path_id=-1, config_dict=None):
        config_obj = config_dict.get(int(config_id))
        pathItems = []
        i = 0

        path = config_obj.paths_dict.get(path_id)

        for child in path.children:
            pathItem = None
            if child[0] in config_obj.modules_dict and child[1] == 'mod':
                pathItem = FilePathitem(config_obj.modules_dict.get(child[0]).id, config_obj.modules_dict.get(child[0]).name, path_id, 1, i, config_obj.modules_dict.get(child[0]).operator)
                pathItem.gid = config_obj.modules_dict.get(child[0]).id
            elif child[0] in config_obj.sequences_dict and child[1] == 'seq':
                pathItem = FilePathitem(config_obj.sequences_dict.get(child[0]).id, config_obj.sequences_dict.get(child[0]).name, path_id, 2, i)
                i = i + 1
                pathItem.children, i = self.buildPathItemChildren(config_obj.sequences_dict.get(child[0]).children, i, config_id, path_id)
                pathItem.gid = config_obj.sequences_dict.get(child[0]).id

            pathItem.vid = config_id    
            i = i+1

            if pathItem is not None:
                pathItems.append(pathItem)

        pathItems.sort(key=lambda par: par.order)

        resp = Response()
        resp.children= pathItems
        schema = ResponseFilePathItemSchema()
        
        resp.success = True

        output = schema.dump(resp)
            
        return output.data

    def getPathDetailsFromFile(self, config_id, path_id=-1, config_dict=None):
        config_obj = config_dict.get(int(config_id))

        pathDetail = None

        path = config_obj.paths_dict.get(path_id)

        if path == None:
            path = config_obj.endPaths_dict.get(path_id)
        path_found = False
        path_values = []
        path_labels = []

        for key in config_obj.services_dict:
            service = config_obj.services_dict.get(key)
            if service.name == "PrescaleService":
                for child in service.children:
                    param = config_obj.parameters_dict.get(child)
                    if param.name == "prescaleTable":
                        for paramChild in param.children:
                            paramChildName = config_obj.parameters_dict.get(config_obj.parameters_dict.get(paramChild).children[0]).value.replace('"','')
                            if paramChildName == path.name:
                                path_found = True
                                path_values = config_obj.parameters_dict.get(config_obj.parameters_dict.get(paramChild).children[1]).value.replace("{",'').replace("}","").split(",")
                    elif param.name == "lvl1Labels":
                        path_labels = param.value.replace("{",'').replace("}","").split(",")

        if path_found:
            pathDetail = PathDetails(path_id, path.name, path_labels, path_values, "", "")
        else:
            path_values = [1] * len(path_labels)
            pathDetail = PathDetails(path_id, path.name, path_labels, path_values, "", "")


        resp = Response()
        resp.children = []
        resp.children.append(pathDetail)
        schema = ResponsePathDetailsSchema()
        
        resp.success = True

        output = schema.dump(resp)
            
        return output.data

    def buildPathItemChildren(self, children, i, config_id, path_id, config_dict=None):
        config_obj = config_dict.get(int(config_id))
        children_list = []

        for child in children:
            if child[0] in config_obj.modules_dict and child[1] == 'mod':
                pathItem = FilePathitem(config_obj.modules_dict.get(child[0]).id, config_obj.modules_dict.get(child[0]).name, path_id, 1, i, config_obj.modules_dict.get(child[0]).operator)
                pathItem.gid = config_obj.modules_dict.get(child[0]).id
            elif child[0] in config_obj.sequences_dict and child[1] == 'seq':
                pathItem = FilePathitem(config_obj.sequences_dict.get(child[0]).id, config_obj.sequences_dict.get(child[0]).name, path_id, 2, i)
                i = i + 1
                pathItem.children, i = self.buildPathItemChildren(config_obj.sequences_dict.get(child[0]).children, i, config_id, path_id)
                pathItem.gid = config_obj.sequences_dict.get(child[0]).id

            pathItem.vid = config_id
            i = i + 1

            if pathItem is not None:
                children_list.append(pathItem)

        children_list.sort(key=lambda par: par.order)

        return children_list, i

    def getSummaryColumnsFromFile(self, config_id, config_dict=None):
        config_obj = config_dict.get(int(config_id))
        columns = []

        path_labels = []

        for key in config_obj.services_dict:
            service = config_obj.services_dict.get(key)
            if service.name == "PrescaleService":
                for child in service.children:
                    param = config_obj.parameters_dict.get(child)
                    if param.name == "lvl1Labels":
                        path_labels = param.value.replace("{",'').replace("}","").split(",")

        i = 0
        for label in path_labels:
            col = SummaryColumn(i,label,i)
            columns.append(col)
            i = i+1

        resp = Response()
        resp.children = columns
        schema = ResponseSummaryColumnSchema()
        
        resp.success = True

        output = schema.dump(resp)
            
        return output.data

    def getSummaryItemsFromFile(self, config_id, config_dict=None):
        config_obj = config_dict.get(int(config_id))
        items = {}

        paths = {}

        prescale_table = {}
        path_labels = None

        trigger_path = {}

        for key in config_obj.services_dict:
            service = config_obj.services_dict.get(key)
            if service.name == "PrescaleService":
                for child in service.children:
                    param = config_obj.parameters_dict.get(child)
                    if param.name == "prescaleTable":
                        for paramChild in param.children:
                            if hasattr(config_obj.parameters_dict.get(paramChild), 'children') and len(config_obj.parameters_dict.get(paramChild).children) > 1:
                                paramChildName = config_obj.parameters_dict.get(config_obj.parameters_dict.get(paramChild).children[0]).value.replace('"','')
                                path_values = config_obj.parameters_dict.get(config_obj.parameters_dict.get(paramChild).children[1]).value.replace("{",'').replace("}","").split(",")
                                prescale_table[paramChildName] = path_values
                    elif param.name == "lvl1Labels":
                        path_labels = param.value.replace("{",'').replace("}","").split(",")

        for key in config_obj.streams_dict:
            stream = config_obj.streams_dict[key]
            stream_id = self.summaryItemCounter.getNext()
            summaryItemStream = Summaryitem(stream.id,stream.name,"str",False,'resources/Stream.ico')
            summaryItemStream.gid = stream_id
            items[stream_id] = summaryItemStream
            mod_found = False

            for elem in config_obj.endPaths_dict:
                for mod in config_obj.endPaths_dict[elem].children:
                    if mod[0] in config_obj.modules_dict and mod[1] == 'mod':
                        mod_temp = config_obj.modules_dict.get(mod[0]).template
                        if mod_temp == "TriggerResultsFilter":
                            for modChild in config_obj.modules_dict.get(mod[0]).children:
                                if config_obj.parameters_dict.get(modChild).name == "triggerConditions":
                                    trf_expression = config_obj.parameters_dict.get(modChild).value.translate(None,'"{}')
                                    expressions = trf_expression.split(',')
                                    prescale = 1
                                    for e in expressions:
                                        parts = e.split('/')

                                        if len(parts) == 2:
                                            pre_str = parts[1]
                                            pre_str = pre_str.translate(None,' "')
                                            prescale = int(pre_str)

                                        part_one = parts[0]
                                        part_one = part_one.translate(None,'()"')
                                        terms = part_one.split(' OR ')
                                        for ter in terms:
                                            ter = ter.translate(None,' () "')
                                            trigger_path[ter] = prescale

                    elif mod[0] in config_obj.endPathModules and mod[1] == 'oum':
                        mod_name = config_obj.endPathModules.get(mod[0]).name
                        if mod_name.replace("hltOutput", "") != stream.name:
                            trigger_path = {}
                        else:
                            mod_found = True
                            break
                if mod_found:
                    break

            for param in stream.children:
                paths = {}
                if param in config_obj.datasets_dict:
                    dataset = config_obj.datasets_dict[param]
                    dataset_id = self.summaryItemCounter.getNext()
                    summaryItemDataset = Summaryitem(dataset.id,dataset.name,"dat",False, 'resources/Dataset.ico')
                    summaryItemDataset.gid = dataset_id

                    for par in dataset.children:
                        path = config_obj.paths_dict.get(par)
                        path_id = self.summaryItemCounter.getNext()
                        if path is not None:
                            summaryItemPath = Summaryitem(path.id,path.name,"pat",True,'resources/Path_3.ico')
                            LV1_value = ""
                            if "ignore" in path.name:
                                LV1_value = ""
                            else:
                                LV1_value = self.checkPathChildren(path.children,LV1_value,1, config_obj)
                                LV1_value = "Level_1_Seeds_Expression###" + LV1_value
                            
                            if trigger_path == {}:
                                if path.name in prescale_table:
                                    values = prescale_table.get(path.name)
                                    if path_labels is not None:
                                        for counter in xrange(len(path_labels)):
                                            val = path_labels[counter] + "###" + values[counter]
                                            summaryItemPath.values.append(val)
                                else:
                                    if path_labels is not None:
                                        for counter in xrange(len(path_labels)):
                                            val = path_labels[counter] + "###" + "1"
                                            summaryItemPath.values.append(val)
                                summaryItemPath.values.append(LV1_value)
                                summaryItemPath.gid = path_id
                                paths[summaryItemPath.gid] = summaryItemPath
                            else:
                                if path.name in trigger_path:
                                    prescale = trigger_path.get(path.name)
                                    if path.name in prescale_table:
                                        values = prescale_table.get(path.name)
                                        if path_labels is not None:
                                            for counter in xrange(len(path_labels)):
                                                val = path_labels[counter] + "###" + str(int(values[counter]) * prescale)
                                                summaryItemPath.values.append(val)
                                    else:
                                        if path_labels is not None:
                                            for counter in xrange(len(path_labels)):
                                                val = path_labels[counter] + "###" + "1"
                                                summaryItemPath.values.append(val)
                                    summaryItemPath.values.append(LV1_value)
                                    summaryItemPath.gid = path_id
                                    paths[summaryItemPath.gid] = summaryItemPath

                        if len(paths) > 0:
                            summaryItemDataset.children = paths.values()

                    items.get(stream_id).children.append(summaryItemDataset)

        resp = Response()
        resp.children = []
        resp.children = items.values()

        resp.children.sort(key=lambda par: par.name)
        schema = ResponseSummaryItemSchema()
        
        resp.success = True

        output = schema.dump(resp)
            
        return output.data

    def checkPathChildren(self, children, LV1_value, count, config_obj):
        L1TechTrigger = False
        for m in children:
            if m[0] in config_obj.modules_dict and m[1] == 'mod':
                module = config_obj.modules_dict.get(m[0]) 
                if module.template == "HLTLevel1GTSeed":
                    for c in module.children:
                        moduleParamChild = config_obj.parameters_dict.get(c)
                        if moduleParamChild.name == "L1SeedsLogicalExpression":
                            if count == 1:
                                LV1_value = LV1_value + moduleParamChild.value.translate(None,'"').translate(None,"'")
                                count = count + 1
                            else:
                                LV1_value = LV1_value + " AND " + moduleParamChild.value.translate(None,'"').translate(None,"'")

                        elif moduleParamChild.name == "L1TechTriggerSeeding":
                            if moduleParamChild.value == "False":
                                L1TechTrigger = False
                            else:
                                L1TechTrigger
            elif m[0] in config_obj.sequences_dict and m[1] == 'seq':
                sequence = config_obj.sequences_dict.get(m[0])
                self.checkPathChildren(sequence.children,LV1_value,count, config_obj)       

        if L1TechTrigger == False:
            return LV1_value
        else:
            # PUT CODE FOR LEVEL1_SEED_EXPRESSION
            return LV1_value 

    def getCnfDetailsFromFile(self, config_id, config_dict=None):
        config_obj = config_dict.get(int(config_id))

        version = FileVersion(config_id, config_obj.config_name)
        
        resp = Response()
        schema = ResponseFileVersionSchema()
        resp.success = True
        resp.children = []
        resp.children.append(version)
        
        output = schema.dump(resp)
        #assert isinstance(output.data, OrderedDict)

        return output.data