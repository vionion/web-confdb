# File inverter.py Description:
# 
# Class: Inverter

from utils import * 
from marshmallow.ordereddict import OrderedDict

import re

class BaseItem(object):
    id = 0
    name = ''
    children = []
    def __init__(self, id, name, children):
        self.id = id
        self.name = name
        self.children = children

class GlobalPsetObject(BaseItem):
    gpset_tracked = 0
    def __init__(self, id, name, tracked, children):
        self.gpset_tracked = tracked
        super(GlobalPsetObject, self).__init__(id, name, children)

class StreamObject(BaseItem):
    def __init__(self, id, name, children):
        super(StreamObject, self).__init__(id, name, children)

class DatasetObject(BaseItem):
    def __init__(self, id, name, children):
        super(DatasetObject, self).__init__(id, name, children)

class EventContentObject(BaseItem):
    def __init__(self, id, name, children):
        super(EventContentObject, self).__init__(id, name, children)

class ComponentObject(BaseItem):  ## Used for EdSource - EsSource - EsModule - Service - Output Module
    template = ''
    def __init__(self, id, name, template, children):
        self.template = template
        super(ComponentObject, self).__init__(id, name, children)

class ModuleObject(BaseItem):
    template = ''
    module_type = ''
    operator = 0
    def __init__(self, id, name, template, module_type, children):
        self.template = template
        self.module_type = module_type
        super(ModuleObject, self).__init__(id, name, children)

class SequenceObject(BaseItem):
    def __init__(self, id, name, children):
        super(SequenceObject, self).__init__(id, name, children)

class PathObject(BaseItem):
    def __init__(self, id, name, children):
        super(PathObject, self).__init__(id, name, children)

class EndPathObject(BaseItem):
    def __init__(self, id, name, children):
        super(EndPathObject, self).__init__(id, name, children)

class ScheduleObject(BaseItem):
    def __init__(self, id, name, children):
        super(ScheduleObject, self).__init__(id, name, children)

class Basic_Parameter(object):
    id = 0
    name = ''
    tracked = 0
    moetype = 0
    def __init__(self, id, name, tracked, moetype):
        self.id = id
        self.name = name
        self.tracked = tracked
        self.moetype = moetype
        
class Parameter(Basic_Parameter):
    ptype = ''
    value = ''
    moetype = 0

    def __init__(self, id, name, tracked, ptype, value, moetype):
        self.ptype = ptype
        self.value = value
        super(Parameter, self).__init__(id, name, tracked, moetype)

class Parameter_Set(Basic_Parameter):
    children = []

    def __init__(self, id, name, tracked, children, moetype):
        self.children = children
        super(Parameter_Set, self).__init__(id, name, tracked, moetype)

class EventContent_Parameter(object):
    def __init__(self, id, name, ptype, moduleElement, extraName, processName):
        self.id = id
        self.name = name
        self.ptype = ptype
        self.moduleElement = moduleElement
        self.extraName = extraName
        self.processName = processName

class Configuration(object):
    def __init__(self, id, config_name, global_pset_dict, streams_dict, datasets_dict, eventContent_dict, eventContentParams_dict, edSources_dict, esSources_dict,
        esModules_dict, services_dict, modules_dict, endPathModules, parameters_dict, sequences_dict, paths_dict, endPaths_dict, schedule_dict):
        self.id = id
        self.config_name = config_name
        self.global_pset_dict = global_pset_dict
        self.streams_dict = streams_dict
        self.datasets_dict = datasets_dict
        self.eventContent_dict = eventContent_dict
        self.eventContentParams_dict = eventContentParams_dict
        self.edSources_dict = edSources_dict
        self.esSources_dict = esSources_dict
        self.esModules_dict = esModules_dict
        self.services_dict = services_dict
        self.modules_dict = modules_dict
        self.endPathModules = endPathModules
        self.parameters_dict = parameters_dict
        self.sequences_dict = sequences_dict
        self.paths_dict = paths_dict
        self.endPaths_dict = endPaths_dict
        self.schedule_dict = schedule_dict

class Inverter(object):

    idgen = None

    temp_dict = None
    path_names_dict = None
    parameters_dict = None
    module_names_dict = None
    sequence_names_dict = None
    outputModules_names_dict = None

    eventContentParams_dict = None

    config_name = None
    global_pset_dict = None
    streams_dict = None
    datasets_dict = None
    eventContent_dict = None
    edSources_dict = None
    esSources_dict = None
    esModules_dict = None
    services_dict = None
    modules_dict = None
    endPathModules = None
    sequences_dict = None
    paths_dict = None
    endPaths_dict = None
    schedule_dict = None

    def readConfig(self, file, config_id, log):

        self.idgen = Counter()
        self.temp_dict = OrderedDict()
        self.parameters_dict = OrderedDict()
        self.eventContentParams_dict = OrderedDict()

        try:
            self.createConfigName(file)
        except Exception as e:
            msg = 'Error In Creating Configuration Name: ' + e.args[0]
            log.error(msg)

        try:
            self.createGlobalPsets(file)
        except Exception as e:
            msg = 'Error In Creating Global PSets: ' + e.args[0]
            log.error(msg)

        try:
            self.createStreams(file)
        except Exception as e:
            msg = 'Error In Creating Streams: ' + e.args[0]
            log.error(msg)

        try:
            self.createDatasets(file)
        except Exception as e:
            msg = 'Error In Creating Datasets: ' + e.args[0]
            log.error(msg)

        self.createEventContents(file)

        try:
            self.createEDSources(file)
        except Exception as e:
            msg = 'Error In Creating EdSources: ' + e.args[0]
            log.error(msg)
        
        try:
            self.createESSources(file)
        except Exception as e:
            msg = 'Error In Creating EsSources: ' + e.args[0]
            log.error(msg)

        try:
            self.createESModules(file)
        except Exception as e:
            msg = 'Error In Creating EsModules: ' + e.args[0]
            log.error(msg)

        try:
            self.createServices(file)
        except Exception as e:
            msg = 'Error In Creating Services: ' + e.args[0]
            log.error(msg)

        try:
            self.createModules(file)
        except Exception as e:
            msg = 'Error In Creating Modules: ' + e.args[0]
            log.error(msg)

        try:
            self.createEndPathModules(file)
        except Exception as e:
            msg = 'Error In Creating Output Modules: ' + e.args[0]
            log.error(msg)

        try:
            self.createSequences(file)
        except Exception as e:
            msg = 'Error In Creating Sequences: ' + e.args[0]
            log.error(msg)

        try:
            self.createPaths(file)
        except Exception as e:
            msg = 'Error In Creating Paths: ' + e.args[0]
            log.error(msg)

        try:
            self.createEndPaths(file)
        except Exception as e:
            msg = 'Error In Creating EndPaths: ' + e.args[0]
            log.error(msg)

        try:
            self.createSchedule(file)
        except Exception as e:
            msg = 'Error In Creating Schedule: ' + e.args[0]
            log.error(msg)

        # self.testConfigName()
        # self.testGlobalPsets()
        # self.testStreams()
        # self.testDatasets()
        # self.testContentEvents()
        # self.testStreamsAndDataSets()
        # self.testEdSources()
        # self.testEsSources()
        # self.testEsModules()
        # self.testServices()
        # self.testModules()
        # self.testEndPathModules()
        # self.testSequences()
        # self.testPaths()
        # self.testEndPaths()
        # self.testSchedule()

        config_object = Configuration(config_id, self.config_name, self.global_pset_dict, self.streams_dict, self.datasets_dict, self.eventContent_dict, self.eventContentParams_dict, self.edSources_dict, self.esSources_dict, self.esModules_dict,
                                        self.services_dict,  self.modules_dict, self.endPathModules, self.parameters_dict, self.sequences_dict, self.paths_dict, self.endPaths_dict, self.schedule_dict)

        file.close

        return config_object

    def createConfigName(self, file):
        self.config_name = ""

        for line in file:
            if "tableName" in line:
                self.config_name = line.split("cms.string('")[1].split("')")[0]
                break

    def createGlobalPsets(self, file):
        file.seek(0)
        self.global_pset_dict = OrderedDict()

        gpset_found = False 
        
        gpset_id = None
        gpset_name = None
        gpset_tracked = None

        parameter_list = list()

        parameter_id = None
        parameter_name = ""
        parameter_tracked = 0
        parameter_ptype = ""
        parameter_value = ""
        parameter_value_found = False

        vpset_count = 0 
        vpset_space_count = 0
        vpset_id = None
        vpset_name = ""
        vpset_tracked = 0
        vpset_children = list()

        pset_count = 0
        pset_space_count = 0
        pset_id = None
        pset_name = ""
        pset_tracked = 0
        pset_children = list()

        pset_vpset_holder = []
        current_obj = None

        for line in file:
            if "process.streams" in line:
                break

            if "process." in line and "process.HLTConfigVersion" not in line:
                gpset_found = True
                gpset_id = self.idgen.getNext()
                gpset_name = line.split("process.")[1].split(" = ")[0]
                gpset_tracked = 0 if "untracked" in line else 1
                if ")" not in line: 
                    continue
                else:
                    gpset_found = False
                    gpset_object = GlobalPsetObject(gpset_id, gpset_name, gpset_tracked, parameter_list)
                    self.global_pset_dict[gpset_id] = gpset_object
                    parameter_list = list()

            if line == ")\n" and gpset_found:
                gpset_found = False
                gpset_object = GlobalPsetObject(gpset_id, gpset_name, gpset_tracked, parameter_list)
                self.global_pset_dict[gpset_id] = gpset_object
                parameter_list = list()

            if ("cms.VPSet" in line or "cms.untracked.VPSet" in line) and gpset_found:
                vpset_id = self.idgen.getNext()
                if " = " in line:
                    vpset_name = line.split(" = ")[0].replace(" ", "")
                    vpset_space_count = len(line) - len(line.lstrip())
                else:
                    vpset_name = ""
                    vpset_space_count = len(line) - len(line.lstrip())
                vpset_tracked = 0 if "untracked" in line else 1
                vpset = Parameter_Set(vpset_id, vpset_name, vpset_tracked, list(), 3)
                self.parameters_dict[vpset_id] = vpset
                pset_vpset_holder.append([vpset_id,vpset_space_count,'vpset'])
                if current_obj != None:
                    pset_vpset_obj = self.parameters_dict.get(current_obj[0])
                    pset_vpset_obj.children.append(vpset_id)
                    current_obj = [vpset_id, 'vpset']
                else:
                    parameter_list.append(vpset_id)
                    current_obj = [vpset_id, 'vpset']
                if ")" in line:
                    pset_vpset_holder.pop()
                    vpset_children = list()
                    if len(pset_vpset_holder) > 0:
                        current_obj = [pset_vpset_holder[-1][0],pset_vpset_holder[-1][2]]
                    else:
                        current_obj = None
                continue

            elif ("cms.PSet" in line or "cms.untracked.PSet" in line) and gpset_found:
                pset_id = self.idgen.getNext()
                if " = " in line:
                    pset_name = line.split(" = ")[0].replace(" ", "")
                    pset_space_count = len(line) - len(line.lstrip())
                else:
                    pset_name = ""
                    pset_space_count = len(line) - len(line.lstrip())
                pset_tracked = 0 if "untracked" in line else 1
                pset = Parameter_Set(pset_id, pset_name, pset_tracked, list(), 2)
                self.parameters_dict[pset_id] = pset
                pset_vpset_holder.append([pset_id,pset_space_count,'pset'])
                if current_obj != None:
                    pset_vpset_obj = self.parameters_dict.get(current_obj[0])
                    pset_vpset_obj.children.append(pset_id)
                    current_obj = [pset_id, 'pset']
                else:
                    parameter_list.append(pset_id)
                    current_obj = [pset_id, 'pset']
                if ")" in line:
                    pset_vpset_holder.pop()
                    pset_children = list()
                    if len(pset_vpset_holder) > 0:
                        current_obj = [pset_vpset_holder[-1][0],pset_vpset_holder[-1][2]]
                    else:
                        current_obj = None
                continue

            if ")" in line and line != ")\n" and parameter_value_found and gpset_found:
                parameter_value_found = False
                parameter_value = parameter_value + " }"
                parameter = Parameter(parameter_id, parameter_name, parameter_tracked, parameter_ptype, parameter_value, 1)
                self.parameters_dict[parameter_id] = parameter
                if current_obj == None:
                    parameter_list.append(parameter_id)
                else:                        
                    if current_obj[1] == 'vpset':
                        vpset_children.append(parameter_id)
                    elif current_obj[1] == 'pset':
                        pset_children.append(parameter_id)

            elif ")" in line and line != ")\n" and len(pset_vpset_holder) > 0 and parameter_value_found == False and len(line) - len(line.lstrip()) == pset_vpset_holder[-1][1]:
                pset_vpset_obj = pset_vpset_holder.pop()
                pset_vpset_id = pset_vpset_obj[0]
                pset_vpset = self.parameters_dict.get(pset_vpset_id)

                if current_obj[1] == 'vpset':
                    pset_vpset.children = pset_vpset.children + vpset_children
                    vpset_children = list()
                elif current_obj[1] == 'pset':
                    pset_vpset.children = pset_vpset.children + pset_children
                    pset_children = list()

                self.parameters_dict[pset_vpset_id] = pset_vpset

                if len(pset_vpset_holder) > 0:
                    current_obj = [pset_vpset_holder[-1][0],pset_vpset_holder[-1][2]]
                else:
                    current_obj = None

            elif gpset_found and parameter_value_found == False:
                parameter_id = self.idgen.getNext()
                parameter_name = line.split(" = ")[0].replace(" ", "")
                parameter_tracked = 0 if "untracked" in line else 1
                parameter_ptype = line.split("(")[0].split(".")[-1]
                if (re.findall('"([^"]*)"', line)[0] if '"' in line else re.findall("'([^']*)'", line)) != [] and (parameter_ptype == "vstring" or parameter_ptype == "vint32" or parameter_ptype == "vuint32" or parameter_ptype == "vdouble" or parameter_ptype == "VInputTag"):
                    parameter_value_found = True
                    parameter_value = "{ " + re.findall('"([^"]*)"', line)[0] if '"' in line else re.findall("'([^']*)'", line)[0]
                    if ")" in line:
                        parameter_value_found = False
                        parameter_value = parameter_value + " }"
                        parameter = Parameter(parameter_id, parameter_name, parameter_tracked, parameter_ptype, parameter_value, 1)
                        self.parameters_dict[parameter_id] = parameter
                        if current_obj == None:
                            parameter_list.append(parameter_id)
                        else:                        
                            if current_obj[1] == 'vpset':
                                vpset_children.append(parameter_id)
                            elif current_obj[1] == 'pset':
                                pset_children.append(parameter_id)
                    else:
                        continue 
                else:
                    parameter_value = line[line.find("(")+1:line.find(")")].replace(" ", "")
                    parameter = Parameter(parameter_id, parameter_name, parameter_tracked, parameter_ptype, parameter_value, 1)
                    self.parameters_dict[parameter_id] = parameter
                    if current_obj == None:
                        parameter_list.append(parameter_id)
                    else:                        
                        if current_obj[1] == 'vpset':
                            vpset_children.append(parameter_id)
                        elif current_obj[1] == 'pset':
                            pset_children.append(parameter_id)

            elif gpset_found and parameter_value_found and re.findall('"([^"]*)"', line)[0] if '"' in line else re.findall("'([^']*)'", line) != []:
                parameter_value = parameter_value + ', ' + re.findall('"([^"]*)"', line)[0] if '"' in line else re.findall("'([^']*)'", line)[0]

    def createStreams(self, file):
        file.seek(0)
        self.streams_dict = OrderedDict()

        streams = False
        stream_found = False 

        stream_id = None
        stream_name = None
        stream_children = list()

        data_set = None
        data_set_id = None

        for line in file:
            if "process.streams" in line:
                streams = True
                continue

            if line == ")\n" and streams:
                streams = False
                stream_found = False
                continue

            if "cms.vstring" in line and streams:
                stream_found = True 
                stream_id = self.idgen.getNext()
                stream_name = line.split(" = ")[0].replace("  ", "")

            if stream_found and re.findall("'([^']*)'", line) != []:
                data_set = re.findall("'([^']*)'", line)[0]
                data_set_id = self.idgen.getNext()
                self.temp_dict[data_set] = data_set_id
                stream_children.append(data_set_id)

            if " )" in line and stream_found:
                stream_found = False 
                stream_object = StreamObject(stream_id, stream_name, stream_children)
                self.streams_dict[stream_id] = stream_object
                stream_children = list()

    def createDatasets(self, file):
        file.seek(0)
        self.datasets_dict = OrderedDict()
        self.path_names_dict = OrderedDict()

        datasets = False
        dataset_found = False

        dataset_id = None
        dataset_name = None
        dataset_children = list()

        path = None
        path_id = None

        for line in file:
            if "process.datasets" in line:
                datasets = True
                continue

            if line == ")\n" and datasets:
                datasets = False
                dataset_found = False
                continue

            if ")+cms.vstring" in line and datasets:
                paths = line.split(")+cms.vstring(")
                path = paths[0].replace(" ", "")
                path_id = self.idgen.getNext()
                if path not in self.path_names_dict:
                    self.path_names_dict[path] = path_id
                else:
                    path_id = self.path_names_dict.get(path)
                dataset_children.append(path_id)
                path = paths[1].replace(" ", "").replace(",","")
                path_id = self.idgen.getNext()
                if path not in self.path_names_dict:
                    self.path_names_dict[path] = path_id
                else:
                    path_id = self.path_names_dict.get(path)
                dataset_children.append(path_id)

            elif "cms.vstring" in line and datasets:
                dataset_found = True 
                dataset_name = line.split(" = ")[0].replace(" ", "")
                dataset_id = self.temp_dict.get(dataset_name)
                del self.temp_dict[dataset_name]

            if dataset_found and re.findall("'([^']*)'", line) != []:
                path = re.findall("'([^']*)'", line)[0]
                path_id = self.idgen.getNext()
                if path not in self.path_names_dict:
                    self.path_names_dict[path] = path_id
                else:
                    path_id = self.path_names_dict.get(path)
                dataset_children.append(path_id)

            if (") )" in line or ")" in line) and dataset_found:
                dataset_found = False 
                dataset_object = DatasetObject(dataset_id, dataset_name, dataset_children)
                self.datasets_dict[dataset_id] = dataset_object
                dataset_children = list()

    def createEDSources(self, file):
        self.edSources_dict = OrderedDict()
        self.createComponentAndParameters("process.source", self.edSources_dict, file)

    def createESSources(self, file):
        self.esSources_dict = OrderedDict()
        self.createComponentAndParameters("cms.ESSource", self.esSources_dict, file)

    def createESModules(self, file):
        self.esModules_dict = OrderedDict()
        self.createComponentAndParameters("cms.ESProducer", self.esModules_dict, file)

    def createServices(self, file):
        self.services_dict = OrderedDict()
        self.createComponentAndParameters("cms.Service", self.services_dict, file)

    def createModules(self, file):
        file.seek(0)
        self.modules_dict = OrderedDict()
        self.module_names_dict = OrderedDict()

        module_found = False

        module_id = None
        module_name = ""
        module_template = ""
        module_type = ""

        parameter_list = list()

        parameter_id = None
        parameter_name = ""
        parameter_tracked = 0
        parameter_ptype = ""
        parameter_value = ""
        parameter_value_found = False

        vpset_count = 0 
        vpset_space_count = 0
        vpset_id = None
        vpset_name = ""
        vpset_tracked = 0
        vpset_children = list()

        pset_count = 0
        pset_space_count = 0
        pset_id = None
        pset_name = ""
        pset_tracked = 0
        pset_children = list()

        pset_vpset_holder = []
        current_obj = None

        for line in file:
            if "cms.EDProducer" in line or "cms.EDAnalyzer" in line or "cms.EDFilter" in line:
                module_found = True
                module_id = self.idgen.getNext()
                module_name = line.split(" = ")[0].split(".")[1]
                module_template = re.findall('"([^"]*)"', line)[0] if '"' in line else re.findall("'([^']*)'", line)[0]
                module_type = line.split("cms.")[1].split("(")[0]
                if ")" not in line: 
                    continue
                else:
                    module_found = False
                    module_object = ModuleObject(module_id, module_name, module_template, module_type, parameter_list)
                    self.modules_dict[module_id] = module_object
                    self.module_names_dict[module_name] = module_id
                    parameter_list = list()


            if line == ")\n" and module_found:
                module_found = False
                module_object = ModuleObject(module_id, module_name, module_template, module_type, parameter_list)
                self.modules_dict[module_id] = module_object
                self.module_names_dict[module_name] = module_id
                parameter_list = list()

            if ("cms.VPSet" in line or "cms.untracked.VPSet" in line) and module_found:
                vpset_id = self.idgen.getNext()
                if " = " in line:
                    vpset_name = line.split(" = ")[0].replace(" ", "")
                    vpset_space_count = len(line) - len(line.lstrip())
                else:
                    vpset_name = ""
                    vpset_space_count = len(line) - len(line.lstrip())
                vpset_tracked = 0 if "untracked" in line else 1
                vpset = Parameter_Set(vpset_id, vpset_name, vpset_tracked, list(), 3)
                self.parameters_dict[vpset_id] = vpset
                pset_vpset_holder.append([vpset_id,vpset_space_count,'vpset'])
                if current_obj != None:
                    pset_vpset_obj = self.parameters_dict.get(current_obj[0])
                    pset_vpset_obj.children.append(vpset_id)
                    current_obj = [vpset_id, 'vpset']
                else:
                    parameter_list.append(vpset_id)
                    current_obj = [vpset_id, 'vpset']
                if ")" in line:
                    pset_vpset_holder.pop()
                    vpset_children = list()
                    if len(pset_vpset_holder) > 0:
                        current_obj = [pset_vpset_holder[-1][0],pset_vpset_holder[-1][2]]
                    else:
                        current_obj = None
                continue

            elif ("cms.PSet" in line or "cms.untracked.PSet" in line) and module_found:
                pset_id = self.idgen.getNext()
                if " = " in line:
                    pset_name = line.split(" = ")[0].replace(" ", "")
                    pset_space_count = len(line) - len(line.lstrip())
                else:
                    pset_name = ""
                    pset_space_count = len(line) - len(line.lstrip())
                pset_tracked = 0 if "untracked" in line else 1
                pset = Parameter_Set(pset_id, pset_name, pset_tracked, list(), 2)
                self.parameters_dict[pset_id] = pset
                pset_vpset_holder.append([pset_id,pset_space_count,'pset'])
                if current_obj != None:
                    pset_vpset_obj = self.parameters_dict.get(current_obj[0])
                    pset_vpset_obj.children.append(pset_id)
                    current_obj = [pset_id, 'pset']
                else:
                    parameter_list.append(pset_id)
                    current_obj = [pset_id, 'pset']
                if ")" in line:
                    pset_vpset_holder.pop()
                    pset_children = list()
                    if len(pset_vpset_holder) > 0:
                        current_obj = [pset_vpset_holder[-1][0],pset_vpset_holder[-1][2]]
                    else:
                        current_obj = None
                continue

            if ")" in line and line != ")\n" and parameter_value_found and module_found:
                parameter_value_found = False
                parameter_value = parameter_value + " }"
                parameter = Parameter(parameter_id, parameter_name, parameter_tracked, parameter_ptype, parameter_value, 1)
                self.parameters_dict[parameter_id] = parameter
                if current_obj == None:
                    parameter_list.append(parameter_id)
                else:                        
                    if current_obj[1] == 'vpset':
                        vpset_children.append(parameter_id)
                    elif current_obj[1] == 'pset':
                        pset_children.append(parameter_id)

            elif ")" in line and line != ")\n" and len(pset_vpset_holder) > 0 and parameter_value_found == False and len(line) - len(line.lstrip()) == pset_vpset_holder[-1][1]:
                pset_vpset_obj = pset_vpset_holder.pop()
                pset_vpset_id = pset_vpset_obj[0]
                pset_vpset = self.parameters_dict.get(pset_vpset_id)

                if current_obj[1] == 'vpset':
                    pset_vpset.children = pset_vpset.children + vpset_children
                    vpset_children = list()
                elif current_obj[1] == 'pset':
                    pset_vpset.children = pset_vpset.children + pset_children
                    pset_children = list()

                self.parameters_dict[pset_vpset_id] = pset_vpset

                if len(pset_vpset_holder) > 0:
                    current_obj = [pset_vpset_holder[-1][0],pset_vpset_holder[-1][2]]
                else:
                    current_obj = None

            elif module_found and parameter_value_found == False:
                parameter_id = self.idgen.getNext()
                parameter_name = line.split(" = ")[0].replace(" ", "")
                parameter_tracked = 0 if "untracked" in line else 1
                parameter_ptype = line.split("(")[0].split(".")[-1]
                if (re.findall('"([^"]*)"', line)[0] if '"' in line else re.findall("'([^']*)'", line)) != [] and (parameter_ptype == "vstring" or parameter_ptype == "vint32" or parameter_ptype == "vuint32" or parameter_ptype == "vdouble" or parameter_ptype == "VInputTag"):
                    parameter_value_found = True
                    parameter_value = "{ " + re.findall('"([^"]*)"', line)[0] if '"' in line else re.findall("'([^']*)'", line)[0]
                    if ")" in line:
                        parameter_value_found = False
                        parameter_value = parameter_value + " }"
                        parameter = Parameter(parameter_id, parameter_name, parameter_tracked, parameter_ptype, parameter_value, 1)
                        self.parameters_dict[parameter_id] = parameter
                        if current_obj == None:
                            parameter_list.append(parameter_id)
                        else:                        
                            if current_obj[1] == 'vpset':
                                vpset_children.append(parameter_id)
                            elif current_obj[1] == 'pset':
                                pset_children.append(parameter_id)
                    else:
                        continue 
                else:
                    parameter_value = line[line.find("(")+1:line.find(")")][1:-1]
                    parameter = Parameter(parameter_id, parameter_name, parameter_tracked, parameter_ptype, parameter_value, 1)
                    self.parameters_dict[parameter_id] = parameter
                    if current_obj == None:
                        parameter_list.append(parameter_id)
                    else:                        
                        if current_obj[1] == 'vpset':
                            vpset_children.append(parameter_id)
                        elif current_obj[1] == 'pset':
                            pset_children.append(parameter_id)

            elif module_found and parameter_value_found and re.findall('"([^"]*)"', line)[0] if '"' in line else re.findall("'([^']*)'", line) != []:
                parameter_value = parameter_value + ', ' + re.findall('"([^"]*)"', line)[0] if '"' in line else re.findall("'([^']*)'", line)[0]

    def createEndPathModules(self, file):
        self.endPathModules = OrderedDict()
        self.outputModules_names_dict = OrderedDict()
        self.createComponentAndParameters("cms.OutputModule", self.endPathModules, file)

    def createSequences(self, file):
        file.seek(0)
        self.sequences_dict = OrderedDict()
        self.sequence_names_dict = OrderedDict()

        sequence_id = None
        sequence_name = None
        sequence_children = list()

        for line in file:
            if "cms.Sequence" in line:
                sequence_id = self.idgen.getNext()
                sequence_name = line.split(" = ")[0].split(".")[1]
                children = line.split("cms.Sequence( ")[1].split(" )")[0].split(" + ")
                for child in children:
                    child_name = child.replace("process.","")
                    if child_name in self.module_names_dict:
                        child_id = self.module_names_dict.get(child_name)
                        sequence_children.append([child_id,'mod'])
                        if "~" in child:
                            self.modules_dict.get(child_id).operator = 1
                        elif "ignore" in child:
                            self.modules_dict.get(child_id).operator = 2                        
                    elif child_name in self.sequence_names_dict:
                        child_id = self.sequence_names_dict.get(child_name)
                        sequence_children.append([child_id,'seq'])
                sequence = SequenceObject(sequence_id, sequence_name, sequence_children)
                self.sequences_dict[sequence_id] = sequence
                self.sequence_names_dict[sequence_name] = sequence_id
                sequence_children = list()

    def createPaths(self, file):
        file.seek(0)
        self.paths_dict = OrderedDict()

        path_id = None
        path_name = None
        path_children = list()

        for line in file:
            if "cms.Path" in line:
                path_name = line.split(" = ")[0].split(".")[1]
                if path_name in self.path_names_dict:
                    path_id = self.path_names_dict.get(path_name)
                else:
                    path_id = self.idgen.getNext()
                children = line.split("cms.Path( ")[1].split(" )")[0].split(" + ")
                for child in children:
                    child_name = child.replace("process.","")
                    if child_name in self.module_names_dict:
                        child_id = self.module_names_dict.get(child_name)
                        path_children.append([child_id,'mod'])
                        if "~" in child:
                            self.modules_dict.get(child_id).operator = 1
                        elif ".ignore" in child:
                            self.modules_dict.get(child_id).operator = 2
                    elif child_name in self.sequence_names_dict:
                        child_id = self.sequence_names_dict.get(child_name)
                        path_children.append([child_id,'seq'])
                path = PathObject(path_id, path_name, path_children)
                self.paths_dict[path_id] = path
                path_children = list()

    def createEndPaths(self, file):
        file.seek(0)
        self.endPaths_dict = OrderedDict()

        endPath_id = None
        endPath_name = None
        endPath_children = list()

        for line in file:
            if "cms.EndPath" in line:
                endPath_id = self.idgen.getNext()
                endPath_name = line.split(" = ")[0].split(".")[1]
                children = line.split("cms.EndPath( ")[1].split(" )")[0].split(" + ")
                for child in children:
                    child_name = child.replace("process.","")
                    if child_name in self.module_names_dict:
                        child_id = self.module_names_dict.get(child_name)
                        endPath_children.append([child_id,'mod'])
                        if "~" in child:
                            self.modules_dict.get(child_id).operator = 1
                        elif ".ignore" in child:
                            self.modules_dict.get(child_id).operator = 2
                    elif child_name in self.outputModules_names_dict:
                        child_id = self.outputModules_names_dict.get(child_name)
                        endPath_children.append([child_id,'oum'])
                    elif child_name in self.sequence_names_dict:
                        child_id = self.sequence_names_dict.get(child_name)
                        endPath_children.append([child_id,'seq'])
                endPath = EndPathObject(endPath_id, endPath_name, endPath_children)
                self.endPaths_dict[endPath_id] = endPath
                endPath_children = list()

    def createSchedule(self, file):
        file.seek(0)
        self.schedule_dict = OrderedDict()

        schedule_id = None
        schedule_name = None
        schedule_children = list()

        for line in file:
            if "cms.Schedule" in line:
                schedule_id = self.idgen.getNext()
                schedule_name = line.split(" = ")[0].split(".")[1]
                if ("*" not in line):
                    schedule_children = line.split("cms.Schedule( ")[1].split(" )")[0].split(" + ")
                else:
                    schedule_children = line.split("cms.Schedule( *(")[1].split(" )")[0].split(" + ")
                schedule = ScheduleObject(schedule_id, schedule_name, schedule_children)
                self.schedule_dict[schedule_id] = schedule

    def createEventContents(self, file):
        file.seek(0)
        self.eventContent_dict = OrderedDict()

        endpath_found = False
        eventContent_found = False

        eventContent_id = None
        eventContent_name = ""

        eventContent_param_list = list()

        eventContent_param_id = None
        eventContent_param_name = ""
        eventContent_param_type = ""
        eventContent_param_ModuleElement = ""
        eventContent_param_ExtraName = ""
        eventContent_param_ProcessName = ""

        for line in file:
            if "cms.OutputModule" in line:
                endpath_found = True
                eventContent_name = 'hltEventContent' + line.split(" = ")[0].split(".")[1].replace('hltOutput',"")
                continue

            if endpath_found and 'outputCommands' in line:
                eventContent_found = True
                eventContent_id = self.idgen.getNext()
                eventContent_param_id = self.idgen.getNext()
                eventContent_Param = EventContent_Parameter(eventContent_param_id, "*", "drop", "*", "*", "*")
                self.eventContentParams_dict[eventContent_param_id] = eventContent_Param
                eventContent_param_list.append(eventContent_param_id)

            elif endpath_found and eventContent_found:
                eventContent_param_id = self.idgen.getNext()
                eventContent_param_name = line.split("_")[0].split("p ")[1]
                eventContent_param_type = "drop" if "drop" in line else "keep"
                eventContent_param_ModuleElement = line.split("_")[1]
                eventContent_param_ExtraName = line.split("_")[2]
                eventContent_param_ProcessName = line.split("_")[3].split('"')[0]
                eventContent_Param = EventContent_Parameter(eventContent_param_id, eventContent_param_name, eventContent_param_type, eventContent_param_ModuleElement, eventContent_param_ExtraName, eventContent_param_ProcessName)
                self.eventContentParams_dict[eventContent_param_id] = eventContent_Param
                eventContent_param_list.append(eventContent_param_id)

            if ")" in line and endpath_found and eventContent_found:
                endpath_found = False
                eventContent_found = False
                eventContent_object = EventContentObject(eventContent_id, eventContent_name, eventContent_param_list)
                self.eventContent_dict[eventContent_id] = eventContent_object
                eventContent_param_list = list()

            elif line == ")\n" and endpath_found and eventContent_found == False:
                endpath_found = False
                eventContent_found = False
                eventContent_name = ""
                eventContent_param_list = list()

    #--------------------------- HELPER FUNCTIONS -----------------------#

    def createComponentAndParameters(self, pattern, object_dict, file):
        file.seek(0)

        object_found = False

        object_id = None
        object_name = ""
        object_template = ""

        parameter_list = list()

        parameter_id = None
        parameter_name = ""
        parameter_tracked = 0
        parameter_ptype = ""
        parameter_value = ""
        parameter_value_found = False

        vpset_count = 0 
        vpset_space_count = 0
        vpset_id = None
        vpset_name = ""
        vpset_tracked = 0
        vpset_children = list()

        pset_count = 0
        pset_space_count = 0
        pset_id = None
        pset_name = ""
        pset_tracked = 0
        pset_children = list()

        pset_vpset_holder = []
        current_obj = None

        for line in file:
            if pattern in line:
                object_found = True
                object_id = self.idgen.getNext()
                object_name = line.split(" = ")[0].split(".")[1]
                object_template = re.findall('"([^"]*)"', line)[0] if '"' in line else re.findall("'([^']*)'", line)[0]
                if ")" not in line: 
                    continue
                else:
                    object_found = False
                    component_object = ComponentObject(object_id, object_name, object_template, parameter_list)
                    object_dict[object_id] = component_object
                    if pattern == "cms.OutputModule":
                        self.outputModules_names_dict[object_name] = object_id
                    parameter_list = list()

            if line == ")\n" and object_found:
                object_found = False
                component_object = ComponentObject(object_id, object_name, object_template, parameter_list)
                object_dict[object_id] = component_object
                if pattern == "cms.OutputModule":
                    self.outputModules_names_dict[object_name] = object_id
                parameter_list = list()

            if ("cms.VPSet" in line or "cms.untracked.VPSet" in line) and object_found:
                vpset_id = self.idgen.getNext()
                if " = " in line:
                    vpset_name = line.split(" = ")[0].replace(" ", "")
                    vpset_space_count = len(line) - len(line.lstrip())
                else:
                    vpset_name = ""
                    vpset_space_count = len(line) - len(line.lstrip())
                vpset_tracked = 0 if "untracked" in line else 1
                vpset = Parameter_Set(vpset_id, vpset_name, vpset_tracked, list(), 3)
                self.parameters_dict[vpset_id] = vpset
                pset_vpset_holder.append([vpset_id,vpset_space_count,'vpset'])
                if current_obj != None:
                    pset_vpset_obj = self.parameters_dict.get(current_obj[0])
                    pset_vpset_obj.children.append(vpset_id)
                    current_obj = [vpset_id, 'vpset']
                else:
                    parameter_list.append(vpset_id)
                    current_obj = [vpset_id, 'vpset']
                if ")" in line:
                    pset_vpset_holder.pop()
                    vpset_children = list()
                    if len(pset_vpset_holder) > 0:
                        current_obj = [pset_vpset_holder[-1][0],pset_vpset_holder[-1][2]]
                    else:
                        current_obj = None
                continue

            elif ("cms.PSet" in line or "cms.untracked.PSet" in line) and object_found:
                pset_id = self.idgen.getNext()
                if " = " in line:
                    pset_name = line.split(" = ")[0].replace(" ", "")
                    pset_space_count = len(line) - len(line.lstrip())
                else:
                    pset_name = ""
                    pset_space_count = len(line) - len(line.lstrip())
                pset_tracked = 0 if "untracked" in line else 1
                pset = Parameter_Set(pset_id, pset_name, pset_tracked, list(), 2)
                self.parameters_dict[pset_id] = pset
                pset_vpset_holder.append([pset_id,pset_space_count,'pset'])
                if current_obj != None:
                    pset_vpset_obj = self.parameters_dict.get(current_obj[0])
                    pset_vpset_obj.children.append(pset_id)
                    current_obj = [pset_id, 'pset']
                else:
                    parameter_list.append(pset_id)
                    current_obj = [pset_id, 'pset']
                if ")" in line:
                    pset_vpset_holder.pop()
                    pset_children = list()
                    if len(pset_vpset_holder) > 0:
                        current_obj = [pset_vpset_holder[-1][0],pset_vpset_holder[-1][2]]
                    else:
                        current_obj = None
                continue

            if (")" in line or ") )" in line) and line != ")\n" and parameter_value_found and object_found:
                if re.findall('"([^"]*)"', line)[0] if '"' in line else re.findall("'([^']*)'", line) != []:
                    parameter_value = parameter_value + ', ' + re.findall('"([^"]*)"', line)[0] if '"' in line else re.findall("'([^']*)'", line)[0]
                parameter_value_found = False
                parameter_value = parameter_value + " }"
                parameter = Parameter(parameter_id, parameter_name, parameter_tracked, parameter_ptype, parameter_value, 1)
                self.parameters_dict[parameter_id] = parameter
                if current_obj == None:
                    parameter_list.append(parameter_id)
                else:                        
                    if current_obj[1] == 'vpset':
                        vpset_children.append(parameter_id)
                    elif current_obj[1] == 'pset':
                        pset_children.append(parameter_id)

            elif ")" in line and line != ")\n" and len(pset_vpset_holder) > 0 and parameter_value_found == False and len(line) - len(line.lstrip()) == pset_vpset_holder[-1][1]:
                pset_vpset_obj = pset_vpset_holder.pop()
                pset_vpset_id = pset_vpset_obj[0]
                pset_vpset = self.parameters_dict.get(pset_vpset_id)

                if current_obj[1] == 'vpset':
                    pset_vpset.children = pset_vpset.children + vpset_children
                    vpset_children = list()
                elif current_obj[1] == 'pset':
                    pset_vpset.children = pset_vpset.children + pset_children
                    pset_children = list()

                self.parameters_dict[pset_vpset_id] = pset_vpset

                if len(pset_vpset_holder) > 0:
                    current_obj = [pset_vpset_holder[-1][0],pset_vpset_holder[-1][2]]
                else:
                    current_obj = None

            elif object_found and parameter_value_found == False:
                parameter_id = self.idgen.getNext()
                parameter_name = line.split(" = ")[0].replace(" ", "")
                parameter_tracked = 0 if "untracked" in line else 1
                parameter_ptype = line.split("(")[0].split(".")[-1]
                if (re.findall('"([^"]*)"', line)[0] if '"' in line else re.findall("'([^']*)'", line)) != [] and (parameter_ptype == "vstring" or parameter_ptype == "vint32" or parameter_ptype == "vuint32" or parameter_ptype == "vdouble" or parameter_ptype == "VInputTag"):
                    parameter_value_found = True
                    parameter_value = "{ " + re.findall('"([^"]*)"', line)[0] if '"' in line else re.findall("'([^']*)'", line)[0]
                    if ")" in line:
                        parameter_value_found = False
                        parameter_value = parameter_value + " }"
                        parameter = Parameter(parameter_id, parameter_name, parameter_tracked, parameter_ptype, parameter_value, 1)
                        self.parameters_dict[parameter_id] = parameter
                        if current_obj == None:
                            parameter_list.append(parameter_id)
                        else:                        
                            if current_obj[1] == 'vpset':
                                vpset_children.append(parameter_id)
                            elif current_obj[1] == 'pset':
                                pset_children.append(parameter_id)
                    else:
                        continue 
                else:
                    parameter_value = line[line.find("(")+1:line.find(")")].replace(" ", "")
                    parameter = Parameter(parameter_id, parameter_name, parameter_tracked, parameter_ptype, parameter_value, 1)
                    self.parameters_dict[parameter_id] = parameter
                    if current_obj == None:
                        parameter_list.append(parameter_id)
                    else:                        
                        if current_obj[1] == 'vpset':
                            vpset_children.append(parameter_id)
                        elif current_obj[1] == 'pset':
                            pset_children.append(parameter_id)

            elif object_found and parameter_value_found and re.findall('"([^"]*)"', line)[0] if '"' in line else re.findall("'([^']*)'", line) != []:
                parameter_value = parameter_value + ', ' + re.findall('"([^"]*)"', line)[0] if '"' in line else re.findall("'([^']*)'", line)[0]


    #--------------------------- TESTING ZONE -----------------------#

    def testConfigName(self):
        print "CONFIG NAME: , ", self.config_name

    def testGlobalPsets(self):
        if len(self.global_pset_dict) == 0:
            print "No Global PSets Were Found !"
        else:
            for key in self.global_pset_dict:
                print "---------------"
                print "GPSET NAME: ", self.global_pset_dict[key].name, self.global_pset_dict[key].id
                for param in self.global_pset_dict[key].children:
                    x = self.parameters_dict.get(param)
                    if isinstance(x,Parameter):
                        print x.id, x.name, x.tracked, x.ptype, x.value 
                    else:
                        print x.id, x.name, x.tracked, x.children
                        if x.children is not None:
                            self.printChildren(x.children)

    def testStreams(self):
        if len(self.streams_dict) == 0:
            print "No Streams Were Found !"
        else:
            for key in self.streams_dict:
                print "-------------"
                print "STREAM NAME: ", self.streams_dict[key].name, self.streams_dict[key].id
                print self.streams_dict[key].children
                # for param in self.streams_dict[key].children:
                #     print param

    def testDatasets(self):
        if len(self.datasets_dict) == 0:
            print "No Datasets Were Found !"
        else:
            for key in self.datasets_dict:
                print "--------------"
                print "DATASET NAME: ", self.datasets_dict[key].name, self.datasets_dict[key].id
                print self.datasets_dict[key].children
                for child in self.datasets_dict[key].children:
                    print "CHILD: ", child
                    print self.paths_dict.get(child).name
                    break

    def testContentEvents(self):
        if len(self.eventContent_dict) == 0:
            print "No ContentEvents Were Found !"
        else:
            for key in self.eventContent_dict:
                print "--------------"
                print "CONTENT EVENT NAME: ", self.eventContent_dict[key].name, self.eventContent_dict[key].id
                print self.eventContent_dict[key].children
                # for param in self.datasets_dict[key].children:
                #     print param

    def testStreamsAndDataSets(self):
        if len(self.streams_dict) == 0:
            print "No Streams Were Found !"
        elif len(self.datasets_dict) == 0:
            print "No Datasets Were Found !"
        else:
            for key in self.streams_dict:
                print "-------------"
                print "STREAM NAME: ", self.streams_dict[key].name
                for param in self.streams_dict[key].children:
                    print self.datasets_dict[param].name

    def testEdSources(self):
        if len(self.edSources_dict) == 0:
            print "No EdSources Were Found !"
        else:
            for key in self.edSources_dict:
                print "---------------"
                print "EDSOURCE NAME: ", self.edSources_dict[key].name, self.edSources_dict[key].template, self.edSources_dict[key].id
                for param in self.edSources_dict[key].children:
                    x = self.parameters_dict.get(param)
                    print x.name, x.tracked, x.ptype, x.value 

    def testEsSources(self):
        if len(self.esSources_dict) == 0:
            print "No EsSources Were Found !"
        else:
            for key in self.esSources_dict:
                print "---------------"
                print "ESSOURCE NAME: ", self.esSources_dict[key].name, self.esSources_dict[key].template, self.esSources_dict[key].id
                for param in self.esSources_dict[key].children:
                    x = self.parameters_dict.get(param)
                    if isinstance(x,Parameter):
                        print x.id, x.name, x.tracked, x.ptype, x.value 
                    else:
                        print x.id, x.name, x.tracked, x.children
                        if x.children is not None:
                            self.printChildren(x.children)

    def testEsModules(self):
        if len(self.esModules_dict) == 0:
            print "No EsModules Were Found !"
        else:
            for key in self.esModules_dict:
                print "---------------"
                print "ESMODULE NAME: ", self.esModules_dict[key].name, self.esModules_dict[key].template, self.esModules_dict[key].id
                for param in self.esModules_dict[key].children:
                    x = self.parameters_dict.get(param)
                    if isinstance(x,Parameter):
                        print x.id, x.name, x.tracked, x.ptype, x.value 
                    else:
                        print x.id, x.name, x.tracked, x.children
                        if x.children is not None:
                            self.printChildren(x.children)

    def testServices(self):
        if len(self.services_dict) == 0:
            print "No Services Were Found !"
        else:
            for key in self.services_dict:
                print "---------------"
                print "SERVICE NAME: ", self.services_dict[key].name, self.services_dict[key].template, self.services_dict[key].id
                for param in self.services_dict[key].children:
                    x = self.parameters_dict.get(param)
                    if isinstance(x,Parameter):
                        print x.id, x.name, x.tracked, x.ptype, x.value 
                    else:
                        print x.id, x.name, x.tracked, x.children
                        if x.children is not None:
                            self.printChildren(x.children)

    def testModules(self):
        if len(self.modules_dict) == 0:
            print "No Modules Were Found !"
        else:
            for key in self.modules_dict:
                print "---------------"
                print "Module NAME: ", self.modules_dict[key].name, self.modules_dict[key].template, self.modules_dict[key].module_type, self.modules_dict[key].id
                for param in self.modules_dict[key].children:
                    x = self.parameters_dict.get(param)
                    if isinstance(x,Parameter):
                        print x.id, x.name, x.tracked, x.ptype, x.value 
                    else:
                        print x.id, x.name, x.tracked, x.children
                        if x.children is not None:
                            self.printChildren(x.children)

    def testEndPathModules(self):
        if len(self.endPathModules) == 0:
            print "No EndPath Modules Were Found !"
        else:
            for key in self.endPathModules:
                print "---------------"
                print "Output Module  NAME: ", self.endPathModules[key].name, self.endPathModules[key].template, self.endPathModules[key].id
                for param in self.endPathModules[key].children:
                    x = self.parameters_dict.get(param)
                    if isinstance(x,Parameter):
                        print x.id, x.name, x.tracked, x.ptype, x.value 
                    else:
                        print x.id, x.name, x.tracked, x.children
                        if x.children is not None:
                            self.printChildren(x.children)

    def printChildren(self, children):
        for param in children:
            x = self.parameters_dict.get(param)
            if isinstance(x,Parameter):
                print x.id, x.name, x.tracked, x.ptype, x.value 
            else:
                print x.id, x.name, x.tracked, x.children
                if x.children is not None:
                    self.printChildren(x.children)

    def testSequences(self):
        if len(self.sequences_dict) == 0:
            print "No Sequences Were Found !"
        else:
            for key in self.sequences_dict:
                print "---------------"
                print "SEQUENCE NAME: ", self.sequences_dict[key].name, self.sequences_dict[key].id
                for param in self.sequences_dict[key].children:
                    if param[0] in self.modules_dict and param[1] == 'mod':
                        print self.modules_dict.get(param[0]).name
                    elif param[0] in self.sequences_dict and param[1] == 'seq':
                        print self.sequences_dict.get(param[0]).name
                        self.printPathChildren(self.sequences_dict.get(param[0]).children)

    def testPaths(self):
        if len(self.paths_dict) == 0:
            print "No Paths Were Found !"
        else:
            for key in self.paths_dict:
                print "---------------"
                print "PATH NAME: ", self.paths_dict[key].name, self.paths_dict[key].id
                for param in self.paths_dict[key].children:
                    if param[0] in self.modules_dict and param[1] == 'mod':
                        print self.modules_dict.get(param[0]).name
                    elif param[0] in self.sequences_dict and param[1] == 'seq':
                        print self.sequences_dict.get(param[0]).name
                        self.printPathChildren(self.sequences_dict.get(param[0]).children)

    def printPathChildren(self, children):
        for param in children:
            if param[1] == 'mod':
                print self.modules_dict.get(param[0]).name
            elif param[1] == 'seq':
                print self.sequences_dict.get(param[0]).name
                self.printPathChildren(self.sequences_dict.get(param[0]).children)       

    def testEndPaths(self):
        if len(self.endPaths_dict) == 0:
            print "No EndPaths Were Found !"
        else:
            for key in self.endPaths_dict:
                print "---------------"
                print "ENDPATH NAME: ", self.endPaths_dict[key].name, self.endPaths_dict[key].id
                for param in self.endPaths_dict[key].children:
                    if param[0] in self.modules_dict and param[1] == 'mod':
                        print self.modules_dict.get(param[0]).name
                    elif param[0] in self.endPathModules and param[1] == 'oum':
                        print self.endPathModules.get(param[0]).name
                    elif param[0] in self.sequences_dict and param[1] == 'seq':
                        print self.sequences_dict.get(param[0]).name
                        self.printPathChildren(self.sequences_dict.get(param[0]).children)

    def testSchedule(self):
        if len(self.schedule_dict) == 0:
            print "No Schedule Was Found !"
        else:
            for key in self.schedule_dict:
                print "---------------"
                print "Schedule NAME: ", self.schedule_dict[key].name, self.schedule_dict[key].id
                for param in self.schedule_dict[key].children:
                    print param
