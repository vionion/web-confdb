import traceback
from item_wrappers.Parameter import *

class ParamsBuilder():

    @staticmethod
    def buildParameters(session, logger, query, module_id, set_default=False, id_field=None):
        # check the input parameters
        if (module_id == -2 or session == None or query == None):
            logger.error('ERROR: buildParameters - input parameters error\n' + ''.join(traceback.format_stack()))

        try:
            # retreive all the parameters of the module
            elements = query(module_id, session, logger)
        except Exception as e:
            logger.error('ERROR: query %s(%s, ...): %s' % (query.__name__, module_id, e))
            return None

        return ParamsBuilder.buildParameterStructure(logger, elements, set_default=set_default, id_field=id_field)

    @staticmethod
    def buildParameterStructure(logger, elements, module_id=-1, set_default=False, id_field=None):
        # build all the parameters, PSets and VPSets
        params  = []
        level   = 0
        stack   = [ params ]
        parents = [ None ]
        prev    = None

        for p in elements:
            # build the next element
            if (p.valuelob == None or p.valuelob == "") and (p.moetype == 1):   # XXX why valuelob == "" ?  why moetype == 1 ?
                value = p.value
            else:
                value = p.valuelob

            if p.lvl > (len(stack)-1):
                assert p.lvl == len(stack)
                assert stack[-1]
                stack.append(stack[-1][-1].children)
                parents.append(prev)

            while p.lvl < (len(stack)-1):
                # stack[-1].sort(key = lambda p: p.order)
                stack.pop()
                prev = parents.pop()
            item = Parameter(module_id, p.id, p.name, value, p.moetype, p.paramtype, parents[-1], p.lvl, p.order, p.tracked, p.hex)
            if hasattr(p, "default"):
                item.default = p.default
            else:
                item.default = set_default
            if id_field is not None and hasattr(p, id_field):
                if item.default:
                    item.id_field_templ = getattr(p, id_field)
                else:
                    item.id_field_module = getattr(p, id_field)
            # the parameter is a PSet or VPSet
            if item.moetype == 3 or item.moetype == 2:
                item.expanded = False

            stack[-1].append(item)

            # remember the last elements as the possible next parent
            prev = p.id

        while stack:
            # stack[-1].sort(key = lambda p: p.order)
            stack.pop()

        return params


    @staticmethod
    def buildFromTemplateAndModule(session, logger, queries, module_id, id_field_module=None, id_field_template=None):
        # check the input parameters
        if (module_id == -2 or session == None or queries == None):
            logger.error('ERROR: buildFromTemplateAndModule - input parameters error\n' + ''.join(traceback.format_stack()))

        # queries = (get_template_by_module_id, get_template_parameters, get_module_parameters)
        (get_template_by_module_id, get_template_parameters, get_module_parameters) = queries

        # template DB queries
        template = None

        try:
            # find the module template
            template = get_template_by_module_id(module_id, session, logger)
        except Exception as e:
            logger.error('ERROR: query %s(%s, ...): %s' % (get_template_by_module_id.__name__, module_id, e))
            return None

        if template is None:
            logger.error('ERROR: query %s(%s, ...) did not return any values' % (get_template_by_module_id.__name__, module_id))
            return None

        # retrieve the template (default) parameters
        t_params = ParamsBuilder.buildParameters(session, logger, get_template_parameters, template.id, set_default=True, id_field=id_field_template)

        # retreive the module parameters
        m_params = ParamsBuilder.buildParameters(session, logger, get_module_parameters, module_id, set_default=False, id_field=id_field_module)

        # merge the template (default) and module parameters
        parameters = {}
        for p in t_params:
            parameters[p.name] = p
        for p in m_params:
            parameters[p.name] = p

        return sorted(parameters.values(), key = lambda p: p.order)


    @staticmethod
    def serviceParamsBuilder(id, queries, session, logger):
        q = ( queries.getSrvTemplateBySrv,
              queries.getSrvTemplateParams,
              queries.getServiceParamElements )
        return ParamsBuilder.buildFromTemplateAndModule(session, logger, q, id, id_field_module='id_service', id_field_template='id_srvtemplate')

    @staticmethod
    def serviceTemplateParamsBuilder(id, queries, session, logger):
        return ParamsBuilder.buildParameters(session, logger, queries.getSrvTemplateParams, id, set_default=True, id_field='id_srvtemplate')

    @staticmethod
    def moduleParamsBuilder(mid, queries, session, logger):
        q = ( queries.getTemplateFromPae,
              queries.getTemplateParams,
              queries.getModuleParamItemsOne )
        return ParamsBuilder.buildFromTemplateAndModule(session, logger, q, mid, id_field_module='id_moe', id_field_template='id_modtemp')

    @staticmethod
    def esModuleParamsBuilder(id, queries, session, logger):
        q = ( queries.getESMTemplateByEsm,
              queries.getESMTemplateParams,
              queries.getESModParams )
        return ParamsBuilder.buildFromTemplateAndModule(session, logger, q, id, id_field_module='id_esmodule', id_field_template='id_esmtemplate')

    @staticmethod
    def gpsetParamsBuilder(id, queries, session, logger):
        return ParamsBuilder.buildParameters(session, logger, queries.getGpsetElements, id, id_field='id_gpset')

    @staticmethod
    def outputModuleParamsBuilder(id, queries, session, logger):
        return ParamsBuilder.buildParameters(session, logger, queries.getOUMElements, id, id_field='id_streamid')

    @staticmethod
    def edSourceParamsBuilder(id, queries, session, logger):
        q = ( queries.getEDSTemplateByEds,
              queries.getEDSTemplateParams,
              queries.getEDSourceParams )
        return ParamsBuilder.buildFromTemplateAndModule(session, logger, q, id, id_field_module='id_edsource', id_field_template='id_edstemplate')

    @staticmethod
    def esSourceParamsBuilder(id, queries, session, logger):
        q = ( queries.getESSTemplateByEss,
              queries.getESSTemplateParams,
              queries.getESSourceParams )
        return ParamsBuilder.buildFromTemplateAndModule(session, logger, q, id, id_field_module='id_essource', id_field_template='id_esstemplate')

