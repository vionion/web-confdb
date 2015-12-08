# File data_builder.py Description:
#
# Class: DataBuilder

import itertools
import re
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

    indent_module = '  '
    indent_parameter = '  '

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
            try:
                template_params = self.params_builder.gpsetParamsBuilder(gpset.id, self.queries, self.database, self.logger)
            except Exception as e:
                msg = 'ERROR: Query gpsetParamsBuilder Error: ' + e.args[0]
                self.logger.error(msg)
                return result

            result = result + "process." + gpset.name + ' = cms.PSet('
            if template_params:
                result += '\n' + ',\n'.join(self.emitParameter(p) for p in template_params) + '\n)\n'
            else:
                result += ' )\n'

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
            result = result + self.indent_module + stream.name + " = cms.vstring( "

            new_result = ""
            for dataset in datasets:
                if(stream.id == relations_dict.get(dataset.id)):
                    new_result = new_result + "'" + dataset.name + "'" + ",\n" + self.indent_module + self.indent_parameter

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
            result = result + self.indent_module + dataset.name + " = cms.vstring( "

            paths = None
            try:
                paths = self.queries.getDatasetPathids(self.version.id, dataset.id, self.database)
            except Exception as e:
                msg = 'ERROR: Query getDatasetPathids Error: ' + e.args[0]
                self.logger.error(msg)
                return result

            paths.sort(key=lambda par: par.name)
            if len(paths) == 0:
                result = result + "\n" + self.indent_module + self.indent_parameter
            elif len(paths) < 255:
                for path in paths:
                    result = result + "'" + path.name + "'" + ",\n" + self.indent_module + self.indent_parameter
            else:
                result = result + "*( "
                for path in paths:
                    result = result + "'" + path.name + "'" + ",\n" + self.indent_module + self.indent_parameter
                result = result[:-6] + "),\n" + self.indent_module + self.indent_parameter
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
            try:
                template     = self.queries.getEDSTemplateByEds(edsource.id, self.database)
                tempelements = self.queries.getEDSTemplateParams(template.id, self.database)
            except Exception as e:
                msg = 'ERROR: EDSources Query Error: ' + e.args[0]
                self.logger.error(msg)
                return ""

            params = self.params_builder.buildParameterStructure(self.logger, tempelements, set_default = True)
            result = result + self.emitModule('source', 'Source', edsource.name, params)

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
                template_params = self.params_builder.esSourceParamsBuilder(module.id, self.queries, self.database, self.logger)
                result = result + self.emitModule(module.name, 'ESSource', template.name, template_params)

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
                template_params = self.params_builder.esModuleParamsBuilder(module.id, self.queries, self.database, self.logger)
                result = result + self.emitModule(module.name, 'ESProducer', template.name, template_params)

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
                template_params = self.params_builder.serviceParamsBuilder(service.id, self.queries, self.database, self.logger)
                result = result + self.emitModule(template.name, 'Service', template.name, template_params)

        return result + "\n"


    def getModules(self):
        result = ""

        modules = []
        templates = {}
        parameters = {}

        try:
            t1 = Timer()
            modules = self.queries.getModules(self.version.id, self.database, self.logger)
            t1.stop()
            self.logger.info('getModules: getModules(...) [%.1fs]' % t1.elapsed)

            t1 = Timer()
            templates = dict((module.id_templ, None) for module in modules)
            for id in templates:
                templates[id] = self.queries.getTemplateParams(id, self.database, self.logger)
            t1.stop()
            self.logger.info('getModules: getTemplateParams(...) [%.1fs]' % t1.elapsed)

            t1 = Timer()
            parameters = dict((module.id, None) for module in modules)
            for id in parameters:
                parameters[id] = self.queries.getModuleParamItemsOne(id, self.database, self.logger)
            t1.stop()
            self.logger.info('getModules: getModuleParamItemsOne(...) [%.1fs]' % t1.elapsed)

        except Exception as e:
            msg = 'ERROR: getModules: ' + e.args[0]
            self.logger.error(msg)
            return None

        t2 = Timer()
        t3 = Timer()

        for module in modules:
            t2.start()
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
            t2.stop()

            # build the text representation
            t3.start()
            result = result + self.emitModule(module.name, module.mtype, module.temp_name, template_params)
            t3.stop()

        self.logger.info('getModules: building the parameter structure [%.1fs]' % t2.elapsed)
        self.logger.info('getModules: emitting the python representation [%.1fs]' % t3.elapsed)

        return result + '\n'


    def getOutputModules(self):

        result = ""

        endpaths = None

        try:
            endpaths = self.queries.getEndPaths(self.version.id, self.database, self.logger)
        except Exception as e:
            msg = 'ERROR: Query getEndPaths Error: ' + e.args[0]
            self.logger.error(msg)
            return result

        for path in endpaths:
            outmodule = self.queries.getOumStreamid(path.id, self.database, self.logger)
            if outmodule == None:
                continue
            stream = self.queries.getStreamid(outmodule.id_streamid, self.database, self.logger)
            template_params = self.params_builder.outputModuleParamsBuilder(stream.id, self.queries, self.database, self.logger)
            result = result + self.emitModule('hltOutput'+ stream.name, 'OutputModule', 'ShmStreamConsumer', template_params)

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
        try:
            paths    = self.queries.getPaths(self.version.id, self.database, self.logger)
            endpaths = self.queries.getEndPaths(self.version.id, self.database, self.logger)
        except Exception as e:
            msg = 'ERROR: getSchedule: error querying database: ' + e.args[0]
            self.logger.error(msg)
            return 'process.HLTSchedule = cms.Schedule( )'

        if not paths and not endpaths:
            return 'process.HLTSchedule = cms.Schedule( )'

        string = ', '.join('process.' + path.name for path in itertools.chain(paths, endpaths))
        if len(paths) + len(endpaths) > 255:
            string = '*( ' + string + ' )'

        return 'process.HLTSchedule = cms.Schedule( ' + string + ' )'


    ## -- Helper Functions -- ##
    delimiter = [ re.compile(', *'), re.compile('", *"'), re.compile("', *'") ]

    def decode_string(self, value):
        if value is None or value == '':
            return ''
        elif len(value) > 1 and ((value[0] == '"' and value[-1] == '"') or (value[0] == "'" and value[-1] == '"')):
            return value[1:-1]
        else:
            return value

    def decode_bool(self, value):
        if value == '0':
            return False
        elif value == '1':
            return True
        else:
            # FIXME raise an exception ?
            return False

    def decode_uint32(self, value):
        return int(value) % 2**32

    def decode_uint64(self, value):
        return int(value) % 2**64

    def decode_vstring(self, value):
        if value[0] == '{' and value[-1] == '}':
            value = value[1:-1].strip()
            if len(value) == 0:
                return []
            if len(value) == 1:
                return [ value ]
            if value[0] == '"' and value[-1] == '"':
                value = value[1:-1]
                d = self.delimiter[1]
            elif value[0] == "'" and value[-1] == '"':
                value = value[1:-1]
                d = self.delimiter[2]
            else:
                d = self.delimiter[0]
            return d.split(value)
        else:
            self.logger.warning('found scalar value "%s" in place of a vector' % value)
            return [ value ]

    def format_string(self, value):
        return '"' + value + '"'

    def decode_vector(self, scalar, value):
        if value[0] == '{' and value[-1] == '}':
            value = value[1:-1].strip()
            if len(value) == 0:
                return []
            return [ scalar(v) for v in self.delimiter[0].split(value) ]
        else:
            self.logger.warning('found scalar value "%s" in place of a vector' % value)
            return [ scalar(value) ]

    def format_vector(self, scalar, value):
        string = ' ' + ', '.join(scalar(v) for v in value) + ' '
        if len(value) > 255:
            string = ' *(' + string + ') '
        return string

    def format_double(self, value):
        string = format(value)
        if not '.' in string:
            if 'e' in string:
                string = string.replace('e', '.0e')
            else:
                string = string + '.0'
        return string


    def emitParameter(self, parameter):
        level   = parameter.lvl
        indent  = self.indent_module + self.indent_parameter * level
        name    = parameter.name
        tracked = '' if parameter.tracked else 'untracked.'
        type    = parameter.paramtype

        if type in ( 'vstring', 'VInputTag' ):
            # FIXME - a VInputTag should e amitted as a tuple of InputTags, not as a tuple of strings 
            value  = self.decode_vstring(parameter.value)
            string = self.format_vector(self.format_string, value)
        elif type in ( 'vint32', 'vint64' ):
            value  = self.decode_vector(int, parameter.value)
            string = self.format_vector(format, value)
        elif type in ( 'vuint32', ):
            value  = self.decode_vector(self.decode_uint32, parameter.value)
            string = self.format_vector(format, value)
        elif type in ( 'vuint64', ):
            value  = self.decode_vector(self.decode_uint64, parameter.value)
            string = self.format_vector(format, value)
        elif type in ( 'vdouble', ):
            value  = self.decode_vector(float, parameter.value)
            string = self.format_vector(self.format_double, value)
        elif type in ( 'VPSet', ):
            string = '\n' + ',\n'.join(self.emitParameter(v) for v in parameter.children) + '\n' + indent
            if len(parameter.children) > 255:
                string = ' *(' + string + ') '
        elif type in ( 'string', 'InputTag', 'FileInPath' ):
            value = self.decode_string(parameter.value)
            string = ' ' + self.format_string(value) + ' '
        elif type in ( 'bool', ):
            value = self.decode_bool(parameter.value)
            string = ' ' + format(value) + ' '
        elif type in ( 'int32', 'int64' ):
            value = int(parameter.value)
            string = ' ' + format(value) + ' '
        elif type in ( 'uint32', ):
            value = self.decode_uint32(parameter.value)
            if parameter.value[0:2] == '0x':
                string = ' 0x' + format(value, '08x') + ' '
            else:
                string = ' ' + format(value) + ' '
        elif type in ( 'uint64', ):
            value = self.decode_uint64(parameter.value)
            if parameter.value[0:2] == '0x':
                string = ' 0x' + format(value, '016x') + ' '
            else:
                string = ' ' + format(value) + ' '
        elif type in ( 'double', ) :
            value = float(parameter.value)
            string = ' ' + self.format_double(value) + ' '
        elif type in ( 'PSet', ) :
            string = '\n' + ',\n'.join(self.emitParameter(v) for v in parameter.children) + '\n' + indent
        else:
            string = parameter.value

        if name is not None:
            return indent + name + ' = cms.' + tracked + type + '(' + string + ')'
        else:
            return indent + 'cms.' + tracked + type + '(' + string + ')'


    def emitModule(self, module_name, module_type, module_class, parameters):
        string = 'process.' + module_name + ' = cms.' + module_type + '( "' + module_class + '"'
        if parameters:
            string += ',\n' + ',\n'.join(self.emitParameter(p) for p in parameters) + '\n)\n'
        else:
            string += ' )\n'
        return string


    def emitPathItem(self, item):
        if item.operator == 0:
            string = "process." + item.name + " + "
        elif item.operator == 2:
            string = "cms.ignore(process." + item.name + ")" + " + "
        elif item.operator == 1:
            string = "~process." + item.name + " + "
        return string


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


