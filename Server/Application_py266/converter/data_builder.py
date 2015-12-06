# File data_builder.py Description:
#
# Class: DataBuilder

import itertools
from confdb_queries.confdb_queries import ConfDbQueries
from item_wrappers.FolderItem import *
from item_wrappers.ModuleDetails import *
from item_wrappers.Pathitem import *
from item_wrappers.Parameter import *
from item_wrappers.item_wrappers import *
from schemas.responseSchemas import *
from responses.responses import *
from marshmallow import Schema, fields, pprint
#from ordereddict import OrderedDict
from marshmallow.ordereddict import OrderedDict
from exposed.exposed import *
from utils import *

class DataBuilder(object):

    queries = ConfDbQueries()
    params_builder = ParamsBuilder()

    def __init__(self, database, version, logger):
        self.database = database
        self.version  = version
        self.logger   = logger

    def getGlobalPsets(self):
        result = ""

        psets = None

        try:
            psets = self.queries.getConfGPsets(self.version.id, self.database, self.logger)
        except Exception as e:
            msg = 'ERROR: Query getConfGPsets Error: ' + e.args[0]
            self.logger.error(msg)
            return result

        template_params = None

        for gpset in psets:
            result = result + "process." + gpset.name + ' = cms.PSet(\n'

            try:
                template_params = self.params_builder.gpsetParamsBuilder(gpset.id, self.queries, self.database, self.logger)
            except Exception as e:
                msg = 'ERROR: Query gpsetParamsBuilder Error: ' + e.args[0]
                self.logger.error(msg)
                return result

            new_result = self.createParameterString(template_params)
            if new_result == "":
                result = result[:-2] + " )\n"
            else:
                result = result + new_result

        if result == "":
            return result
        else:
            return result + "\n"


    def getStreams(self):

        result = "process.streams = cms.PSet(\n"

        streams = None
        datasets = None
        relations = None

        try:
            streams   = self.queries.getConfStreams(self.version.id, self.database)
            datasets  = self.queries.getConfDatasets(self.version.id, self.database)
            relations = self.queries.getConfStrDatRels(self.version.id, self.database)
        except Exception as e:
            msg = 'ERROR: Steams Query Error: ' + e.args[0]
            self.logger.error(msg)
            return result

        relations_dict = dict((x.id_datasetid, x.id_streamid) for x in relations)

        streams.sort(key=lambda par: par.name)
        datasets.sort(key=lambda par: par.name)

        for stream in streams:
            result = result + self.getTab(2) + stream.name + " = cms.vstring( "
            new_result = ""
            for dataset in datasets:
                if(stream.id == relations_dict.get(dataset.id)):
                    new_result = new_result + "'" + dataset.name + "'" + ",\n" + self.getTab(4)

            if new_result != "":
                result = result + new_result[:-6] + " ),\n"
            else:
                result = result + " ),\n"

        result = result[:-2] + "\n)\n"

        return result + "\n"


    def getDatasetsPaths(self):

        result = "process.datasets = cms.PSet(\n"

        try:
            datasets = self.queries.getConfDatasets(self.version.id, self.database)
            datasets.sort(key=lambda par: par.name)
        except Exception as e:
            msg = 'ERROR: Steams Query Error: ' + e.args[0]
            self.logger.error(msg)
            return result

        for dataset in datasets:
            result = result + self.getTab(2) + dataset.name + " = cms.vstring( "

            paths = None
            try:
                paths = self.queries.getDatasetPathids(self.version.id, dataset.id, self.database)
            except Exception as e:
                msg = 'ERROR: Query getDatasetPathids Error: ' + e.args[0]
                self.logger.error(msg)
                return result

            paths.sort(key=lambda par: par.name)
            if len(paths) == 0:
                result = result + "\n" + self.getTab(4)
            elif len(paths) < 255:
                for path in paths:
                    result = result + "'" + path.name + "'" + ",\n" + self.getTab(4)
            else:
                result = result + "*( "
                for path in paths:
                    result = result + "'" + path.name + "'" + ",\n" + self.getTab(4)
                result = result[:-6] + "),\n" + self.getTab(4)
            result = result[:-6] + " ),\n"
        result = result[:-2] + "\n)\n"

        return result + "\n"


    def getEDSources(self):

        result = ""

        modules = None
        templates = None
        conf2eds = None

        try:
            modules   = self.queries.getConfEDSource(self.version.id, self.database)
            templates = self.queries.getEDSTemplates(self.version.id_release, self.database)
            conf2eds  = self.queries.getConfToEDSRel(self.version.id, self.database)
        except Exception as e:
            msg = 'ERROR: EDSources Query Error: ' + e.args[0]
            self.logger.error(msg)
            return result

        templates_dict = dict((x.id, x) for x in templates)
        conf2eds_dict = dict((x.id_edsource, x.order) for x in conf2eds)

        edsources = []

        for m in modules:
            if (templates_dict.has_key(m.id_template) and conf2eds_dict.has_key(m.id)):
                temp = templates_dict.get(m.id_template)
                c2e = conf2eds_dict.get(m.id)
                eds = EDSource(m.id, m.id_template, temp.name, c2e)
                eds.gid = m.id
            if (eds != None):
                edsources.append(eds)

        edsources.sort(key=lambda par: par.order)

        template = None
        tempelements = None

        for edsource in edsources:
            result = result + 'process.source = cms.Source( "'  + edsource.name + '",\n'

            try:
                template     = self.queries.getEDSTemplateByEds(edsource.id, self.database)
                tempelements = self.queries.getEDSTemplateParams(template.id, self.database)
            except Exception as e:
                msg = 'ERROR: EDSources Query Error: ' + e.args[0]
                self.logger.error(msg)
                return ""
            for tempel in tempelements:
                tracked, val = self.buildParamValue(tempel, 4, 6)
                result = result + self.getTab(4) + tempel.name + " = cms." + tracked + tempel.paramtype + val
            result = result[:-2] + "\n)\n\n"

        return result


    def getESSource(self):

        result = ""

        modules = None
        templates = None
        conf2ess = None

        try:
            modules =   self.queries.getConfESSource(self.version.id, self.database)
            templates = self.queries.getESSTemplates(self.version.id_release, self.database)
            conf2ess =  self.queries.getConfToESSRel(self.version.id, self.database)
        except Exception as e:
            msg = 'ERROR: ESSource Query Error: ' + e.args[0]
            self.logger.error(msg)
            return result

        templates_dict = dict((x.id, x) for x in templates)
        modules_dict = dict((x.id, x) for x in modules)
        conf2ess_dict = dict((x.id_essource, x.order) for x in conf2ess)

        for module in modules:
            if (templates_dict.has_key(module.id_template) and conf2ess_dict.has_key(module.id)):
                template = templates_dict.get(module.id_template)
                result = result + "process." + module.name + ' = cms.ESSource( "' + template.name + '",\n'
                template_params = self.params_builder.esSourceParamsBuilder(module.id, self.queries, self.database, self.logger)
                new_result = self.createParameterString(template_params)
                if new_result == "":
                    result = result[:-2] + " )\n"
                else:
                    result = result + new_result

        return result + "\n"


    def getESModules(self):

        result = ""

        modules = None
        templates = None
        conf2esm = None

        try:
            modules   = self.queries.getConfESModules(self.version.id, self.database)
            templates = self.queries.getESMTemplates(self.version.id_release, self.database)
            conf2esm  = self.queries.getConfToESMRel(self.version.id, self.database)
        except Exception as e:
            msg = 'ERROR: ESModules Query Error: ' + e.args[0]
            self.logger.error(msg)
            return result

        templates_dict = dict((x.id, x) for x in templates)
        modules_dict = dict((x.id, x) for x in modules)
        conf2esm_dict = dict((x.id_esmodule, x.order) for x in conf2esm)

        for module in modules:
            if (templates_dict.has_key(module.id_template) and conf2esm_dict.has_key(module.id)):
                template = templates_dict.get(module.id_template)
                result = result + "process." + module.name + ' = cms.ESProducer( "' + template.name + '",\n'
                template_params = self.params_builder.esModuleParamsBuilder(module.id, self.queries, self.database, self.logger)
                new_result = self.createParameterString(template_params)
                if new_result == "":
                    result = result[:-2] + " )\n"
                else:
                    result = result + new_result

        return result + "\n"


    def getServices(self):

        result = ""

        services = None
        templates = None

        try:
            services  = self.queries.getConfServices(self.version.id, self.database)
            templates = self.queries.getRelSrvTemplates(self.version.id_release, self.database)
        except Exception as e:
            msg = 'ERROR: Services Query Error: ' + e.args[0]
            self.logger.error(msg)
            return result

        templates_dict = dict((x.id, x) for x in templates)

        for service in services:
            if (templates_dict.has_key(service.id_template)):
                template = templates_dict.get(service.id_template)
                result = result + "process." + template.name + ' = cms.Service( "' + template.name + '",\n'
                template_params = self.params_builder.serviceParamsBuilder(service.id, self.queries, self.database, self.logger)
                new_result = self.createParameterString(template_params)
                if new_result == "":
                    result = result[:-2] + " )\n"
                else:
                    result = result + new_result

        return result + "\n"


    def getModules(self):
        result = ""

        modules = []
        templates = {}
        parameters = {}

        try:
            modules = self.queries.getModules(self.version.id, self.database, self.logger)

            templates = dict((module.id_templ, None) for module in modules)
            for id in templates:
                templates[id] = self.queries.getTemplateParams(id, self.database, self.logger)

            parameters = dict((module.id, None) for module in modules)
            for id in parameters:
                parameters[id] = self.queries.getModuleParamItemsOne(id, self.database, self.logger)

        except Exception as e:
            msg = 'ERROR: getModules: ' + e.args[0]
            self.logger.error(msg)
            return None

        for module in modules:
            # retrieve the template (default) parameters
            t_params = self.params_builder.buildParameterStructure(self.logger, templates[module.id_templ], set_default = True)

            # retreive the module parameters
            m_params = self.params_builder.buildParameterStructure(self.logger, parameters[module.id], set_default = False)

            # merge the template (default) and module parameters
            params = {}
            for p in t_params:
                params[p.name] = p
            for p in m_params:
                params[p.name] = p
            template_params = sorted(params.values(), key = lambda p: p.order)

            # build the text representation
            result = result + "process." + module.name + " = cms." + module.mtype + '( "' + module.temp_name + '",\n'
            new_result = self.createParameterString(template_params)
            if new_result == "":
                result = result[:-2] + " )\n"
            else:
                result = result + new_result

        return result + "\n"


    def getOutputModules(self):

        result = ""

        endPaths = None

        try:
            endPaths = self.queries.getEndPaths(self.version.id, self.database, self.logger)
        except Exception as e:
            msg = 'ERROR: Query getEndPaths Error: ' + e.args[0]
            self.logger.error(msg)
            return result

        for path in endPaths:
            outmodule = self.queries.getOumStreamid(path.id, self.database, self.logger)
            if outmodule == None:
                continue
            stream = self.queries.getStreamid(outmodule.id_streamid, self.database, self.logger)
            result = result + "process.hltOutput"+ stream.name + ' = cms.OutputModule( "ShmStreamConsumer",\n'
            template_params = self.params_builder.outputModuleParamsBuilder(stream.id, self.queries, self.database, self.logger)
            new_result = self.createParameterString(template_params)
            if new_result == "":
                result = result[:-2] + " )\n"
            else:
                result = result + new_result

        return result + "\n"


    def skipSequence(self, counter, items, level):
        while(counter < len(items) and items[counter].lvl >= level):
            counter = counter + 1
        return counter


    def getSequenceChildren(self, counter, written_sequences, items, elements_dict, level):
        children = []
        result = ""
        while(counter < len(items) and items[counter].lvl == level):
            elem = elements_dict[items[counter].id_pae]
            item = Pathitem(items[counter].id_pae, elem.name, items[counter].id_pathid, elem.paetype, items[counter].id_parent, items[counter].lvl, items[counter].order, items[counter].operator)
            children.append(item)
            counter = counter + 1
            if item.paetype == 2:
                if item.name in written_sequences:
                    counter = self.skipSequence(counter, items, item.lvl+1)
                else:
                    new_result, counter, new_children, written_sequences = self.getSequenceChildren(counter, written_sequences, items, elements_dict, item.lvl+1)
                    result = result + new_result + "process." + item.name + " = cms.Sequence( "
                    for child in new_children:
                        result += self.emitPathItem(child)
                    result = result[:-2] + ")\n"
                    written_sequences.add(item.name)

        return result, counter, children, written_sequences


    def getSequences(self):

        result = ""

        """ unused
        idgen = Counter()
        seqsMap = SequencesMapping(idgen)
        modsMap = ModulesMapping(idgen)
        """

        paths = None

        try:
            paths    = self.queries.getPaths(self.version.id, self.database, self.logger)
            endpaths = self.queries.getEndPaths(self.version.id, self.database, self.logger)
        except Exception as e:
            msg = 'ERROR: Query getPaths Error: ' + e.args[0]
            self.logger.error(msg)
            return result

        written_sequences = set()

        elements = None
        items = None

        for path in itertools.chain(paths, endpaths):
            try:
                elements = self.queries.getCompletePathSequences(path.id, self.version.id, self.database, self.logger)
                items    = self.queries.getCompletePathSequencesItems(path.id, self.version.id, self.database, self.logger)
            except Exception as e:
                msg = 'ERROR: Sequences Query Error: ' + e.args[0]
                self.logger.error(msg)
                return result

            elements_dict = dict((element.id, element) for element in elements)

            counter = 0

            while counter < len(items):
                elem = elements_dict[items[counter].id_pae]
                item = Pathitem(items[counter].id_pae, elem.name, items[counter].id_pathid, elem.paetype, items[counter].id_parent, items[counter].lvl, items[counter].order, items[counter].operator)
                counter = counter + 1
                if item.paetype == 2:
                    if item.name in written_sequences:
                        counter = self.skipSequence(counter, items, item.lvl+1)
                    else:
                        new_result, counter, new_children, written_sequences = self.getSequenceChildren(counter, written_sequences, items, elements_dict, item.lvl+1)
                        result = result + new_result + "process." + item.name + " = cms.Sequence( "
                        for child in new_children:
                            result += self.emitPathItem(child)
                        result = result[:-2] + ")\n"
                        written_sequences.add(item.name)

        return result + "\n"


    def getPaths(self):
        result = ""

        try:
            paths = self.queries.getPaths(self.version.id, self.database, self.logger)
        except Exception as e:
            msg = 'ERROR: Query getPaths Error: ' + e.args[0]
            self.logger.error(msg)
            return result

        for path in paths:
            result = result + "process." + path.name + " = " + "cms.Path( "

            try:
                elements = self.queries.getPathElements(path.id, self.version.id, self.database, self.logger)
                items    = self.queries.getPathItems(path.id, self.version.id, self.database, self.logger)
            except Exception as e:
                msg = 'ERROR: Paths Query Error: ' + e.args[0]
                self.logger.error(msg)
                return None

            elements_dict = dict((element.id, element) for element in elements)
            pathitems = []

            # emit only the top-level items
            for item in items:
                elem = elements_dict[item.id_pae]
                if item.lvl > 0:
                    continue
                pathitem = Pathitem(item.id_pae, elem.name, item.id_pathid, elem.paetype, item.id_parent, item.lvl, item.order, item.operator)
                pathitems.append(pathitem)

            pathitems.sort(key = lambda pathitem: pathitem.order)
            for pathitem in pathitems:
                result += self.emitPathItem(pathitem)
            result = result[:-2] + ")\n"

        return result + "\n"


    def getEndPaths(self):
        result = ""

        try:
            paths = self.queries.getEndPaths(self.version.id, self.database, self.logger)
        except Exception as e:
            msg = 'ERROR: Query getPaths Error: ' + e.args[0]
            self.logger.error(msg)
            return result

        for path in paths:
            result = result + "process." + path.name + " = " + "cms.EndPath( "

            try:
                elements = self.queries.getPathElements(path.id, self.version.id, self.database, self.logger)
                items    = self.queries.getPathItems(path.id, self.version.id, self.database, self.logger)
            except Exception as e:
                msg = 'ERROR: Paths Query Error: ' + e.args[0]
                self.logger.error(msg)
                return None

            elements_dict = dict((element.id, element) for element in elements)
            pathitems = []

            # emit only the top-level items...
            for item in items:
                element = elements_dict[item.id_pae]
                if item.lvl > 0:
                    continue
                pathitem = Pathitem(item.id_pae, element.name, item.id_pathid, element.paetype, item.id_parent, item.lvl, item.order, item.operator)
                pathitems.append(pathitem)

            # ...and the OutputMoules
            outputmodule = self.queries.getOumStreamid(path.id, self.database, self.logger)
            if (outputmodule != None):
                stream = self.queries.getStreamid(outputmodule.id_streamid, self.database, self.logger)
                pathitem = Pathitem(outputmodule.id_streamid, "hltOutput"+stream.name, outputmodule.id_pathid, 3, -1, 0, outputmodule.order)
                pathitems.append(pathitem)

            pathitems.sort(key = lambda item: item.order)
            for pathitem in pathitems:
                result += self.emitPathItem(pathitem)
            result = result[:-2] + ")\n"

        return result + "\n"


    def getSchedule(self):

        text = ''
        try:
            paths    = self.queries.getPaths(self.version.id, self.database, self.logger)
            endPaths = self.queries.getEndPaths(self.version.id, self.database, self.logger)
        except Exception as e:
            msg = 'ERROR: getSchedule: error querying database: ' + e.args[0]
            self.logger.error(msg)
            return "process.HLTSchedule = cms.Schedule( )"

        for path in paths:
            text = text + "process." + path.name + ", "
        for path in endPaths:
            text = text + "process." + path.name + ", "

        if text == "":
            return "process.HLTSchedule = cms.Schedule( )"

        else:
            result = "process.HLTSchedule = cms.Schedule( *(" + text
            return result[:-2] + " ))"


    ## -- Helper Functions -- ##

    def createParameterString(self, template_params):
        result = ""
        for template_param in template_params:
            tracked = '' if template_param.tracked else 'untracked.'

            if template_param.paramtype == "VPSet":
                result = result + self.getTab(4) + template_param.name + " = cms." + tracked
                new_result = self.buildVPSetChildren(template_param, 6, 8)
                if len(template_param.children) < 255:
                    result = result + "VPSet(\n"
                    if new_result == "\n":
                        result =  result + self.getTab(4) + "),\n"
                    else:
                        result = result + new_result + self.getTab(4) + "),\n"
                else:
                    result = result +"VPSet(  *(\n" + new_result + self.getTab(4) + ") ),\n"

            elif template_param.paramtype == "PSet":
                new_result = self.buildPsetChildren(template_param, 6, 8)

                if len(template_param.children) < 255:
                    result = result + self.getTab(4) + template_param.name + " = cms." + tracked + "PSet(\n"
                    if new_result == "\n":
                        result = result[:-1] + "  ),\n"
                    else:
                        result = result + new_result + self.getTab(4) + "),\n"
                else:
                    result = result + self.getTab(4) + template_param.name + " = cms." + tracked + "PSet(  *(\n"
                    result = result + new_result + self.getTab(4) + ") ),\n"

            else:
                tracked, val = self.buildParamValue(template_param, 4, 6)
                result = result + self.getTab(4) + template_param.name + " = cms." + tracked + template_param.paramtype + val

        if result == "":
            return result
        else:
            return result[:-2] + "\n)\n"

    def buildVPSetChildren(self, template_param, pset_tab, param_tab):
        result = ""
        psets = template_param.children

        for pset in psets:
            tracked = '' if pset.tracked else 'untracked.'
            if pset.paramtype == "VPSet":
                result = result + self.getTab(pset_tab) + pset.name + " = cms." + tracked
                new_result = self.buildVPSetChildren(template_param, pset_tab+2, param_tab+2)
                if len(pset.children) < 255:
                    result = result + "VPSet(\n"
                    if new_result == "\n":
                        result =  result + self.getTab(pset_tab) + "),\n"
                    else:
                        result = result + new_result + self.getTab(pset_tab) + "),\n"
                else:
                    result = result +"VPSet(  *(\n" + new_result + self.getTab(pset_tab) + ") ),\n"
            else:
                new_result = self.buildPsetChildren(pset, pset_tab+2, param_tab+2)
                if len(pset.children) < 255:
                    pset_name = "cms." + tracked + "PSet(\n" if (pset.name == None) else pset.name + " = cms." + tracked + "PSet(\n"
                    result = result + self.getTab(pset_tab) + pset_name
                    if new_result == "\n":
                        result = result[:-1] + "  ),\n"
                    else:
                        result = result + new_result + self.getTab(pset_tab) + "),\n"
                else:
                    pset_name = "cms." + tracked + "PSet( *(\n" if (pset.name == None) else pset.name + " = cms." + tracked + "PSet( *(\n"
                    result = result + self.getTab(pset_tab) + pset_name
                    result = result + new_result + self.getTab(pset_tab) + "),\n"

        result = result[:-2] + "\n"
        return result

    def buildPsetChildren(self, template_params, pset_tab, param_tab):
        result = ""
        params = template_params.children

        for param in params:
            tracked = '' if param.tracked else 'untracked.'
            if param.paramtype == "VPSet":
                result = result + self.getTab(pset_tab) + param.name + " = cms." + tracked
                new_result = self.buildVPSetChildren(template_param, pset_tab+2, param_tab+2)
                if len(param.children) < 255:
                    result = result + "VPSet(\n"
                    if new_result == "\n":
                        result =  result + self.getTab(pset_tab) + "),\n"
                    else:
                        result = result + new_result + self.getTab(pset_tab) + "),\n"
                else:
                    result = result +"VPSet(  *(\n" + new_result + self.getTab(pset_tab) + ") ),\n"
            elif param.paramtype == "PSet":
                new_result = self.buildPsetChildren(param, pset_tab+2, param_tab+2)
                if len(param.children) < 255:
                    pset_name = "cms." + tracked + "PSet(\n" if (param.name == None) else param.name + " = cms.PSet(\n"
                    result = result + self.getTab(pset_tab) + pset_name
                    if new_result == "\n":
                        result = result[:-1] + "  ),\n"
                    else:
                        result = result + new_result + self.getTab(pset_tab) + "),\n"
                else:
                    pset_name = "cms." + tracked + "PSet( *(\n" if (param.name == None) else param.name + " = cms.PSet( *(\n"
                    result = result + self.getTab(pset_tab) + pset_name
                    result = result + new_result + self.getTab(pset_tab) + "),\n"
            else:
                tracked, val = self.buildParamValue(param, pset_tab, param_tab)
                result = result + self.getTab(pset_tab) + param.name + " = cms." + tracked + param.paramtype + val
        result = result[:-2] + "\n"
        return result

    def modifyTemplateParameters(self, templateparams, params):
        data = []
        counter = 0
        for templateparam in templateparams:
            data.append(templateparam)
            for param in params:
                if templateparam.name == param.name:
                    data[counter] = param
            counter = counter + 1
        return data

    def checkIfInTemplate(self, templateparams, params):
        flag = False
        for param in params:
            for templateparam in templateparams:
                if param.name == templateparam.name:
                    flag = True
                    break
                else:
                    flag = False
            if flag == False:
                return False
        return True

    def buildParamValue(self, template_params, pset_tab, param_tab):

        tracked = '' if template_params.tracked else 'untracked.'
        val = ""

        if (template_params.paramtype == "vstring"):
            if template_params.value == None or template_params.value[1:-1].strip() == "":
                val = '(  ),\n'
            else:
                elems = template_params.value[1:-1].split(",")
                value = ""
                for elem in elems:
                    value = value + elem + ",\n" + self.getTab(param_tab) if '"' in elem else value + '"' + elem + '"' + ",\n" + self.getTab(param_tab)
                if len(elems) < 255:
                    val = val + '(' + value[:- (len(self.getTab(param_tab)) + 2)] + '),\n'
                else:
                    val = val + '( *(' + value[:- (len(self.getTab(param_tab)) + 2)] + ') ),\n'

        elif (template_params.paramtype == "vint32"):
            if template_params.value == None:
                val = '( ' + str(template_params.value) + ' ),\n'
            else:
                if len(template_params.value[1:-1].split(",")) < 255:
                    val = '(' + template_params.value[1:-1] + '),\n'
                else:
                    val = '( *(' + template_params.value[1:-1] + ') ),\n'

        elif (template_params.paramtype == "vuint32"):
            if template_params.value == None:
                val = '( ' + str(template_params.value) + ' ),\n'
            else:
                if len(template_params.value[1:-1].split(",")) < 255:
                    val = '(' + template_params.value[1:-1] + '),\n'
                else:
                    val = '( *(' + template_params.value[1:-1] + ') ),\n'

        elif (template_params.paramtype == "vdouble"):
            values = [ v.strip() for v in template_params.value[1:-1].split(",") if len(v.strip()) ]
            text = ', '.join(self.format_double(float(v)) for v in values)
            if len(values) < 255:
                val = '( ' +  text + ' ),\n'
            else:
                val = '( *( ' + text + ' ) ),\n'

        elif (template_params.paramtype == "VInputTag"):
            val = '( ' + ','.join( "'%s'" % it.strip() for it in template_params.value[2:-2].split(',') if it) + ' ),\n'

        elif (template_params.paramtype == "string"):
            if template_params.value == None or template_params.value == "" or template_params.value == "none" or template_params.value == "None":
                val = '( "" ),\n'
            else:
                val = '( "' + template_params.value.strip('"') + '" ),\n'

        elif (template_params.paramtype == "FileInPath"):
            if template_params.value == None or template_params.value == "" or template_params.value == "none" or template_params.value == "None":
                val = '( "" ),\n'
            else:
                val = '( "' + template_params.value.replace("'","").replace('"',"") + '" ),\n'

        elif (template_params.paramtype == "bool"):
            if template_params.value == None:
                val = '( ' + str(template_params.value) + ' ),\n'
            else:
                val = '( True ),\n' if (int(template_params.value)) else '( False ),\n'

        elif (template_params.paramtype == "uint64"):
            if template_params.value == None:
                val = '( ' + str(template_params.value) + ' ),\n'
            else:
                val = '( ' + hex(int(template_params.value)).replace("-","") + ' ),\n'

        elif (template_params.paramtype == "double"):
            if template_params.value == None:
                val = '( ' + str(template_params.value) + ' ),\n'
            else:
                val = '( ' + self.format_double(float(template_params.value)) + ' ),\n'

        elif(template_params.paramtype == "InputTag"):
            if template_params.value == None:
                val = '( ' + str(template_params.value) + ' ),\n'
            else:
                if template_params.value == '""':
                    val = '( ' + template_params.value + ' ),\n'
                else:
                    val = '( '
                    for elem in template_params.value.split(":"):
                        val = val + "'" + elem + "', "
                    val = val[:-2] + ' ),\n'

        else:
            if (template_params.value != None):
                val = '( ' + template_params.value + ' ),\n'
            else:
                val = '( ' + str(template_params.value) + ' ),\n'

        return tracked, val


    @staticmethod
    def getRequestedVersion(ver, cnf, db):

        ver_id = -1
        version = None
        queries = DataBuilder.queries

        if((ver == -2) and (cnf == -2)):
            print "VER CNF ERROR"

        elif(cnf != -2 and cnf != -1):
            configs = queries.getConfVersions(cnf, db)
            configs.sort(key=lambda par: par.version, reverse=True)
            ver_id = configs[0].id
            version = queries.getVersion(ver_id, db)

        elif(ver != -2):
            ver_id = ver
            version = queries.getVersion(ver, db)

        return version

    @staticmethod
    def getTab(n):
        return "\t".expandtabs(n)


    @staticmethod
    def format_double(value):
        string = format(value)
        if not '.' in string:
            if 'e' in string:
                string = string.replace('e', '.0e')
            else:
                string = string + '.0'
        return string

    @staticmethod
    def emitPathItem(item):
        if item.operator == 0:
            string = "process." + item.name + " + "
        elif item.operator == 2:
            string = "cms.ignore(process." + item.name + ")" + " + "
        elif item.operator == 1:
            string = "~process." + item.name + " + "
        return string

