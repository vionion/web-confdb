from confdb_v2.queries import ConfDbQueries
from item_wrappers.FolderItem import *
from item_wrappers.ModuleDetails import *
from item_wrappers.Pathitem import *
from item_wrappers.Parameter import *
from item_wrappers.item_wrappers import *
from schemas.responseSchemas import *
from responses.responses import *
from marshmallow import Schema, fields, pprint
#from collections import OrderedDict
import string

class SummaryBuilder():
    def getPrescaleColumns(self, version, queries, db, log):
        if (version == None or db == None or queries == None):
            log.error('ERROR: getPrescaleColumns - input parameters error')

        try:

            #Retreive the Prescale template
            prescaleTemp = queries.getPrescaleTemplate(version.id_release,db, log)

            #Retreive the prescale
            prescale = queries.getPrescale(version.id, prescaleTemp.id ,db, log)

            #Retreive prescale labels
            prescaleLabels = queries.getPrescalelabels(prescale.id,db, log)

        except:
            log.error('ERROR: Query getSrvTemplateBySrv/getSrvTemplateParams Error')
            return None

        parValue = None
        if (prescaleLabels.valuelob == None or prescaleLabels.valuelob == ""):
            parValue = prescaleLabels.value

        else:
            parValue = prescaleLabels.valuelob

        parValue_list = parValue.split(",")

        parValue_list_clean = []
        columns = []

        i = 0
        for l in parValue_list:
            label = l.translate(None,' "{}')
            #parValue_list_clean.append(l)
            col = SummaryColumn(i,label,i)
            columns.append(col)
            i = i+1

        return columns

    def getL1Seeds(self, pats, id_rel, queries, db, log):
        if (pats == None or db == None or queries == None or id_rel == -2):
            log.error('ERROR: getL1Seeds - input parameters error')

        #---- Building l1 Seeds --------------------------------

        pathids = pats
        l1seedTemp = None
        l1seedTempParams = None

        pats_vals_dict = {}

        try:

            l1seedTemp = queries.getL1SeedsTemplate(id_rel ,db, log)

            if l1seedTemp is not None:
                l1seedTempParams = queries.getL1SeedsTempParams(l1seedTemp.id ,db, log)

        except:
            log.error('ERROR: Query getL1SeedsTemplate/getL1SeedsTempParams Error')
            return None


        try:
            l1s_modules = queries.getL1SeedsPathItems(pathids ,db, log)
        except:
            log.error('ERROR: Query getL1SeedsPathItems Error')
            return None


        l1seedTempParams_dict = {}
        for param in l1seedTempParams:
            l1seedTempParams_dict[param.name] = param

        l1seeds_dict = {}
        l1s_params_dict = {}
        l1s_ids = []

        for x in l1s_modules:
            l1s_ids.append(x.id_pae)
#            print 'ID_DSID:', str(x.id_datasetid)
            if x.id_pathid in l1seeds_dict.keys():
                l1seeds_dict[x.id_pathid].children.append(x)

            else:
                lc = ListContainer()
                lc.children.append(x)
                l1seeds_dict[x.id_pathid] = lc

        try:
            l1s_mod_params = queries.getL1SeedsParams(l1s_ids ,db, log)

        except Exception as e:
#            print "EXCEPTION: ", e.args[0]
            msg = 'ERROR: Query getL1SeedsParams Error: ' + e.args[0]
            log.error(msg)
            return None


        for x in l1s_mod_params:
#            print 'ID_DSID:', str(x.id_datasetid)
            if x.id_pae in l1s_params_dict.keys():
                l1s_params_dict[x.id_pae].children.append(x)

            else:
                lc = ListContainer()
                lc.children.append(x)
                l1s_params_dict[x.id_pae] = lc

        for p in pats:
            p_mods = l1seeds_dict.get(p)
            tech = 0
            expression = ""

            if p_mods is None:
                msg = 'WARNING: No Level 1 seeds for: ' + str(p)
                log.error(msg)

            #the paths has one l1seeds module
            elif len(p_mods.children) == 1:
                module = p_mods.children[0]

                if module.operator == 2:
                    msg = 'WARNING: L1 Seed Module ignored: ' + module.name + 'in Path: '+ str(p)
                    log.error(msg)

                elif module.operator == 0:
                    m_params = l1s_params_dict[module.id_pae].children
                    m_params_dict = {}
                    for param in m_params:
                        m_params_dict[param.name] = param

                    if m_params_dict.has_key('L1TechTriggerSeeding'):
                        tech = m_params_dict.get('L1TechTriggerSeeding').value

                    else:
                        tech = l1seedTempParams_dict.get('L1TechTriggerSeeding').value

                    if m_params_dict.has_key('L1SeedsLogicalExpression'):
                        par = m_params_dict.get('L1SeedsLogicalExpression')
                        val = ""
                        if par.valuelob is not None:
                            val = par.valuelob
                        else:
                            val = par.value
                        expression = val #m_params_dict.get('L1SeedsLogicalExpression').value
#                        print " has MODULE EXPRESSION: ",expression

                    else:
                        par = l1seedTempParams_dict.get('L1SeedsLogicalExpression')
                        val = ""
                        if par.valuelob is not None:
                            val = par.valuelob
                        else:
                            val = par.value
                        expression = val
#                        expression = l1seedTempParams_dict.get('L1SeedsLogicalExpression').value


            #the paths has more than one l1seeds module
            elif len(p_mods.children) > 1:
                p_mods_len = len(p_mods.children)
                module = p_mods.children[0]

                if module.operator == 2:
                    msg = 'WARNING: L1 Seed Module ignored: ' + module.name + 'in Path: '+ str(p)
                    log.error(msg)

                elif module.operator == 0:
                    m_params = l1s_params_dict[module.id_pae].children
                    m_params_dict = {}
                    for param in m_params:
                        m_params_dict[param.name] = param

                    if m_params_dict.has_key('L1TechTriggerSeeding'):
                        tech = m_params_dict.get('L1TechTriggerSeeding').value

                    else:
                        tech = l1seedTempParams_dict.get('L1TechTriggerSeeding').value

                    if m_params_dict.has_key('L1SeedsLogicalExpression'):
                        par = m_params_dict.get('L1SeedsLogicalExpression')
                        val = ""
                        if par.valuelob is not None:
                            val = par.valuelob
                        else:
                            val = par.value
                        expression = val #m_params_dict.get('L1SeedsLogicalExpression').value
#                        print " has MODULE EXPRESSION: ",expression

                    else:
                        par = l1seedTempParams_dict.get('L1SeedsLogicalExpression')
                        val = ""
                        if par.valuelob is not None:
                            val = par.valuelob
                        else:
                            val = par.value
                        expression = val
#                        expression = l1seedTempParams_dict.get('L1SeedsLogicalExpression').value

                i = 1
                for i in range(1,p_mods_len):
                    module = p_mods.children[i]

                    if module.operator == 2:
                        msg = 'WARNING: L1 Seed Module ignored: ' + module.name + 'in Path: '+ str(p)
                        log.error(msg)

                    elif module.operator == 0:
                        m_params = l1s_params_dict[module.id_pae].children
                        m_params_dict = {}
                        for param in m_params:
                            m_params_dict[param.name] = param

                        if m_params_dict.has_key('L1TechTriggerSeeding'):
                            tech = m_params_dict.get('L1TechTriggerSeeding').value

                        else:
                            tech = l1seedTempParams_dict.get('L1TechTriggerSeeding').value

                        if m_params_dict.has_key('L1SeedsLogicalExpression'):
                            par = m_params_dict.get('L1SeedsLogicalExpression')
                            val = ""
                            if par.valuelob is not None:
                                val = par.valuelob
                            else:
                                val = par.value
                            expression = expression + " AND " + val  #m_params_dict.get('L1SeedsLogicalExpression').value
    #                        print " has MODULE EXPRESSION: ",expression

                        else:
                            par = l1seedTempParams_dict.get('L1SeedsLogicalExpression')
                            val = ""
                            if par.valuelob is not None:
                                val = par.valuelob
                            else:
                                val = par.value
                            expression = expression + " AND " + val
    #                        expression = l1seedTempParams_dict.get('L1SeedsLogicalExpression').value

#
#                        if m_params_dict.has_key('L1SeedsLogicalExpression'):
#                            expression = expression + " AND " + m_params_dict.get('L1SeedsLogicalExpression').value
#
#                        else:
#                            expression = expression + " AND " + l1seedTempParams_dict.get('L1SeedsLogicalExpression').value
                    i = i+1

            expression = expression.translate(None,'"')
            sv = "Level_1_Seeds_Expression" + "###" + expression
            pats_vals_dict[p] = sv

        return pats_vals_dict



#

    def getSmartPrescales(self, ver_id, id_rel, streams, queries, db, log):
        if (db == None or queries == None or streams == None):
            log.error('ERROR: getSmartPrescaler - input parameters error')


        pathidsToOum = None
        triggResFilters = None
        triggerConditions = None

        smart_prescales_dict = {}

        try:

            #get Pathids of the EndPaths
            pathidsToOum = queries.getPathidToOum(streams,db, log)

        except:
            log.error('ERROR: Query getPathidToOum Error')
            return None


        pathidsToOum_dict = dict((x.id_pathid, x.id_streamid) for x in pathidsToOum)


        try:

            #get Smart Prescale modules
            triggResFilters = queries.getSmartPrescaleModule(ver_id, id_rel, pathidsToOum_dict.keys(),db, log)

        except Exception as e:
            msg = 'ERROR: Query getSmartPrescaleModule Error: ' + e.args[0]
            log.error(msg)
            return None

        tr_list = []
        triggResFilters_dict = dict((x.id_pathid, x) for x in triggResFilters)
        for t in triggResFilters:
            tr_list.append(t.id_pae)

        try:

            #get Smart Prescale Expression
            triggerConditions = queries.getSmartPrescaleExpressions(tr_list,db, log)

        except:
            log.error('ERROR: Query getSrvTemplateBySrv/getSrvTemplateParams Error')
            return None

        triggerConditions_dict = dict((x.id_pae, x) for x in triggerConditions) #TO DO - iS WRONG

        for t in triggResFilters:

            if t.operator == 0:

                if pathidsToOum_dict.has_key(t.id_pathid):
                    stream = pathidsToOum_dict[t.id_pathid]

                    if triggerConditions_dict.has_key(t.id_pae):
                        tc = triggerConditions_dict[t.id_pae]

                        sp = SmartPrescale(stream)

                        trf_expression = ""
                        if tc.valuelob is not None:
                            val = tc.valuelob
                        else:
                            val = tc.value
                        trf_expression = val
                        trf_expression = trf_expression.translate(None,'"{}')
#                    trf_expression = trf_expression.strip('"')
#                    trf_expression = trf_expression.strip('{')
#                    trf_expression = trf_expression.strip('}')

                        expressions = trf_expression.split(',')

                        prescale = 1

                        for e in expressions:
                            prescale = 1
                            parts = e.split('/')

                            if len(parts) == 2:
                                pre_str = parts[1]
                                pre_str = pre_str.translate(None,' "')
                                prescale = int(pre_str)

                            part_one = parts[0]
                            part_one = part_one.translate(None,'()"')
#                           part_one = part_one.strip('"')
                            terms = part_one.split(' OR ')

                            for ter in terms:

                                ter = ter.translate(None,' () "')
#                            print "TERM: ",ter,"PRE: ",prescale
                                sp.children[ter] = prescale

                                #logmsg = "SMART PRESCALE: " + str(ter) + " " + str(prescale)
                                #log.error(logmsg)
                        smart_prescales_dict[stream] = sp

        return smart_prescales_dict
