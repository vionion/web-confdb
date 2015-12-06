import traceback
from item_wrappers.Parameter import *

class ParamsBuilder():

    @staticmethod
    def buildParameters(session, logger, query, module_id, set_default = False):
        # check the input parameters
        if (module_id == -2 or session == None or query == None):
            logger.error('ERROR: buildParameters - input parameters error\n' + ''.join(traceback.format_stack()))

        elements = None

        try:
            # retreive all the parameters of the module
            elements = query(module_id, session, logger)
        except Exception as e:
            logger.error('ERROR: query %s(%s, ...): %s' % (query.__name__, module_id, e))
            return None

        return ParamsBuilder.buildParameterStructure(logger, elements, set_default)


    @staticmethod
    def buildParameterStructure(logger, elements, set_default = False):
        # build all the parameters, PSets and VPSets
        params      = []
        pset        = {}
        vpset       = {}
        parents     = {}
        parents[0]  = -1

        for p in elements:
            parent = parents.get(p.lvl)
            clvl = p.lvl+1
            parValue = None
            if (p.valuelob == None or p.valuelob == "") and (p.moetype == 1):
                parValue = p.value
            else:
                parValue = p.valuelob

            item = Parameter(p.id, p.name, parValue, p.moetype, p.paramtype, parent, p.lvl, p.order, p.tracked)
            item.default = set_default

            # the parameter is a VPSet
            if (item.moetype == 3):
                parents[clvl] = p.id
                item.expanded = False
                vpset[item.id] = item

            # the parameter is a PSet
            elif (item.moetype == 2):
                parents[clvl] = p.id
                item.expanded = False
                pset[item.id]=item
                if (vpset.has_key(item.id_parent)):
                    vpset[item.id_parent].children.insert(item.order, item)

            # the parameter is a simple value
            else:
                if (item.lvl == 0):
                    params.insert(item.order,item)
                    params.sort(key=lambda par: par.order)
                elif item.id_parent:
                    tps = pset[item.id_parent].children
                    tps.insert(item.order, item)
                    tps.sort(key=lambda par: par.order)
                else:
                    logger.error('parameter %s has level %d but not parent' % (item.name, item.lvl))

        # complete the construction of the PSet
        psets = pset.values()
        for s in psets:
            if (s.lvl != 0):
                if (pset.has_key(s.id_parent)):
                    tps = pset[s.id_parent].children
                    tps.insert(s.order, s)
                    tps.sort(key=lambda par: par.order)

        # merge the PSets
        psKeys = pset.keys()
        for ss in psKeys:
            s = pset.get(ss)
            if(s.lvl==0):
                params.insert(s.order, s)

        # merge the VPSets
        vpsKeys = vpset.keys()
        for ss in vpsKeys:
            s = vpset.get(ss)
            if(s.lvl==0):
                params.insert(s.order, s)

        params.sort(key=lambda par: par.order)

        return params


    @staticmethod
    def buildFromTemplateAndModule(session, logger, queries, module_id):
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
        t_params = ParamsBuilder.buildParameters(session, logger, get_template_parameters, template.id, set_default = True)

        # retreive the module parameters
        m_params = ParamsBuilder.buildParameters(session, logger, get_module_parameters,   module_id,   set_default = False)

        # merge the template (default) and module parameters
        parameters = {}
        for p in t_params:
            parameters[p.name] = p
        for p in m_params:
            parameters[p.name] = p

        return sorted(parameters.values(), key = lambda p: p.order)


    @staticmethod
    def serviceParamsBuilder(sid = -2, queries = None, db = None, log = None):
        q = ( queries.getSrvTemplateBySrv,
              queries.getSrvTemplateParams,
              queries.getServiceParamElements )
        return ParamsBuilder.buildFromTemplateAndModule(db, log, q, sid)

    @staticmethod
    def serviceTemplateParamsBuilder(sid = -2, queries = None, db = None, log = None):
        return ParamsBuilder.buildParameters(db, log, queries.getSrvTemplateParams, sid, set_default = True)

    @staticmethod
    def moduleParamsBuilder(mid = -2, queries = None, db = None, log = None):
        q = ( queries.getTemplateFromPae,
              queries.getTemplateParams,
              queries.getModuleParamItemsOne )
        return ParamsBuilder.buildFromTemplateAndModule(db, log, q, mid)

    @staticmethod
    def esModuleParamsBuilder(sid = -2, queries = None, db = None, log = None):
        q = ( queries.getESMTemplateByEsm,
              queries.getESMTemplateParams,
              queries.getESModParams )
        return ParamsBuilder.buildFromTemplateAndModule(db, log, q, sid)

    @staticmethod
    def gpsetParamsBuilder(sid = -2, queries = None, db = None, log = None):
        return ParamsBuilder.buildParameters(db, log, queries.getGpsetElements, sid)

    @staticmethod
    def outputModuleParamsBuilder(sid = -2, queries = None, db = None, log = None):
        return ParamsBuilder.buildParameters(db, log, queries.getOUMElements, sid)

    @staticmethod
    def edSourceParamsBuilder(sid = -2, queries = None, db = None, log = None):
        q = ( queries.getEDSTemplateByEds,
              queries.getEDSTemplateParams,
              queries.getEDSourceParams )
        return ParamsBuilder.buildFromTemplateAndModule(db, log, q, sid)

    @staticmethod
    def esSourceParamsBuilder(sid = -2, queries = None, db = None, log = None):
        q = ( queries.getESSTemplateByEss,
              queries.getESSTemplateParams,
              queries.getESSourceParams )
        return ParamsBuilder.buildFromTemplateAndModule(db, log, q, sid)

