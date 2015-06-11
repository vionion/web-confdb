from confdb_queries.confdb_queries import ConfDbQueries
from item_wrappers.FolderItem import *
from item_wrappers.ModuleDetails import *
from item_wrappers.Pathitem import *
from item_wrappers.Parameter import *
from item_wrappers.item_wrappers import *
from schemas.responseSchemas import *
from responses.responses import *
from marshmallow import Schema, fields, pprint
from ordereddict import OrderedDict
import string        
  
class ParamsBuilder():
    
    def serviceParamsBuilder(self, sid=-2, queries=None, db=None):
        #params check
        if (sid == -2 or db == None or queries == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        print "SID: ", sid     
        
        queries = queries
        params = []
        id_p = sid #srvsMap.get(sid)    
        
        print "ID_P: ", id_p, sid
        
        #Retreive the module template
        template = queries.getSrvTemplateBySrv(id_p,db) 
        
        #Retreive template parameters
        tempelements = queries.getSrvTemplateParams(template.id,db)
        
        tempelements_dict = dict((x.id, x) for x in tempelements)
        print "TEMPLATE ELEMENTS LEN: ", len(tempelements)
        
        #Build template parameters
        temp_pset = {}
        temp_vpset = {}
        temp_parents = {}
        temp_parents[0]=-1
        
        #Build all the vpsets/psets 
        
        temp_params = []
        temp_params_dict = {}
        temp_params_name_dict = {}
        
        for p in tempelements:
#            print p.id
            parent = temp_parents.get(p.lvl)
            clvl = p.lvl+1
            item = Parameter(p.id, p.name, p.value, p.moetype, p.paramtype, parent, p.lvl, p.order, p.tracked)
            item.default = True
            
#            print item
            temp_params_name_dict[item.name] = item
            
            # It is a vpset
            if (item.moetype == 3):
                temp_parents[clvl] = p.id
                item.expanded = False
                temp_vpset[item.id] = item
        
            # It is a pset
            elif (item.moetype == 2):
                temp_parents[clvl] = p.id
                item.expanded = False
                temp_pset[item.id]=item
                if (temp_vpset.has_key(item.id_parent)):                
                    temp_vpset[item.id_parent].children.insert(item.order, item)

            # It is a param
            else:
                if(item.lvl == 0):
                    temp_params.insert(item.order,item)
                    temp_params.sort(key=lambda par: par.order)
                else:
                    tps = temp_pset[item.id_parent].children
                    tps.insert(item.order, item)
                    tps.sort(key=lambda par: par.order)
           
        #complete Pset construction
        temp_psets = temp_pset.values() #viewvalues() 
        for s in temp_psets:
            if (s.lvl != 0):
                if (temp_pset.has_key(s.id_parent)):
#                    pset[s.id_parent].children.insert(s.order, s)
                    tps = temp_pset[s.id_parent].children
                    tps.insert(s.order, s)
                    tps.sort(key=lambda par: par.order)

        #merge the psets created
        temp_psKeys = temp_pset.keys() #viewkeys()               
        
        for ss in temp_psKeys:
            s = temp_pset.get(ss)
            if(s.lvl==0):
                temp_params.insert(s.order, s)
#                params.sort(key=lambda par: par.order)
        
        #merge the vpsets created
        temp_vpsKeys = temp_vpset.keys() #viewkeys()               
        
        for ss in temp_vpsKeys:
            s = temp_vpset.get(ss)
            if(s.lvl==0):
                temp_params.insert(s.order, s)
        
        temp_params_dict = dict((x.id, x) for x in temp_params)
        
        #------------------------------------------------------------------------------------------------------------
        #Retreive all the parameters of the module
        elements = queries.getServiceParamElements(id_p, db)
        
        print "ELEMENTS: ", len(elements) 

        elements_dict = dict((x.id, x) for x in elements)

        pset = {}
        vpset = {}
        parents = {}
        
        parents[0]=-1
        #Build all the vpsets/psets 
        
        not_in = []
        params = []
        pset_name_dict = {}
        vpset_name_dict = {}
        params_mod_name_dict = {}
        
        for p in elements:
#            elem = p #elements_dict[p.id_moe]
            parent = parents.get(p.lvl)
            clvl = p.lvl+1
#            print "TYPE: ", type(elem.moetype), elem.moetype
            item = Parameter(p.id, p.name, p.value, p.moetype, p.paramtype, parent, p.lvl, p.order, p.tracked)
             
            params_mod_name_dict[item.name]=item
            #Set default
            if (temp_params_name_dict.has_key(item.name)):
                if temp_params_name_dict.get(item.name).value == item.value:
                    item.default = True
            
            # It is a vpset
            if (item.moetype == 3):
                parents[clvl] = p.id
                item.expanded = False
                vpset[item.id] = item
                vpset_name_dict[item.name]=item
        
            # It is a pset
            elif (item.moetype == 2):
                parents[clvl] = p.id
                item.expanded = False
                pset[item.id]=item
                pset_name_dict[item.name]=item
                if (vpset.has_key(item.id_parent)):                
                    vpset[item.id_parent].children.insert(item.order, item)

            # It is a param
            else:
                if(item.lvl == 0):
                    params.insert(item.order,item)
                    params.sort(key=lambda par: par.order)
                else:
                    tps = pset[item.id_parent].children
                    tps.insert(item.order, item)
                    tps.sort(key=lambda par: par.order)
        
        #Check ok temp params
        names = temp_params_name_dict.keys() #viewkeys()
        for pn in names:
            if (not(params_mod_name_dict.has_key(pn))): #The param is not in the module
                not_in.append(temp_params_name_dict.get(pn))
        
        
        #Fill the remaining params from Template
        print "LEN NOT_IN: ", len(not_in)
#        print not_in
        if (len(not_in) > 0):
            for n in not_in:
                if (n.lvl != 0):
                    if (n.id_parent in temp_vpset.keys()): #viewkeys()):
                        if(vpset_name_dict.has_key(temp_vpset.get(n.id_parent).name)):
                            vpset_name_dict.get(temp_vpset.get(n.id_parent).name).children.insert(n.order,n)

                    if (n.id_parent in temp_pset.keys()): #viewkeys()):
                        if(pset_name_dict.has_key(temp_pset.get(n.id_parent).name)):
                            pset_name_dict.get(temp_pset.get(n.id_parent).name).children.insert(n.order,n)
                    
                    else:
                        print "DOVE?: ", n.name," " ,n.id, " ",n.id_parent
        
        #complete Pset construction
        psets = pset.values() #viewvalues() 
        for s in psets:
            if (s.lvl != 0):
                if (pset.has_key(s.id_parent)):
#                    pset[s.id_parent].children.insert(s.order, s)
                    tps = pset[s.id_parent].children
                    tps.insert(s.order, s)
                    tps.sort(key=lambda par: par.order)

        #merge the psets created
        psKeys = pset.keys() #viewkeys() #pset.keys() #viewkeys()               
        
        for ss in psKeys:
            s = pset.get(ss)
            if(s.lvl==0):
                params.insert(s.order, s)
#                params.sort(key=lambda par: par.order)
        
        #merge the vpsets created
        vpsKeys = vpset.keys() #viewkeys()               
        
        for ss in vpsKeys:
            s = vpset.get(ss)
            if(s.lvl==0):
                params.insert(s.order, s)
        
        #Merge the remaining template params
        for p in not_in:
            if(p.lvl==0):
                tp = temp_params_dict.get(p.id)
                params.insert(tp.order, p)
                
        params.sort(key=lambda par: par.order)
        
        return params
    
#-------------------------------------------------------------------------------    
    def serviceTemplateParamsBuilder(self, sid=-2, queries=None, db=None):
        #params check
        if (sid == -2 or db == None or queries == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        print "SID: ", sid     
        
        queries = queries
        params = []
        id_p = sid #srvsMap.get(sid)    
        
        print "ID_P: ", id_p, sid
        
        #Retreive the module template
#        template = queries.getSrvTemplateBySrv(id_p,db) 
        
        #Retreive template parameters
        tempelements = queries.getSrvTemplateParams(id_p,db)
        
        tempelements_dict = dict((x.id, x) for x in tempelements)
        print "TEMPLATE ELEMENTS LEN: ", len(tempelements)
        
        #Build template parameters
        temp_pset = {}
        temp_vpset = {}
        temp_parents = {}
        temp_parents[0]=-1
        
        #Build all the vpsets/psets 
        
        temp_params = []
        temp_params_dict = {}
        temp_params_name_dict = {}
        
        for p in tempelements:
#            print p.id
            parent = temp_parents.get(p.lvl)
            clvl = p.lvl+1
            item = Parameter(p.id, p.name, p.value, p.moetype, p.paramtype, parent, p.lvl, p.order, p.tracked)
            item.default = True
            
#            print item
            temp_params_name_dict[item.name] = item
            
            # It is a vpset
            if (item.moetype == 3):
                temp_parents[clvl] = p.id
                item.expanded = False
                temp_vpset[item.id] = item
        
            # It is a pset
            elif (item.moetype == 2):
                temp_parents[clvl] = p.id
                item.expanded = False
                temp_pset[item.id]=item
                if (temp_vpset.has_key(item.id_parent)):                
                    temp_vpset[item.id_parent].children.insert(item.order, item)

            # It is a param
            else:
                if(item.lvl == 0):
                    temp_params.insert(item.order,item)
                    temp_params.sort(key=lambda par: par.order)
                else:
                    tps = temp_pset[item.id_parent].children
                    tps.insert(item.order, item)
                    tps.sort(key=lambda par: par.order)
           
        #complete Pset construction
        temp_psets = temp_pset.values() #viewvalues() 
        for s in temp_psets:
            if (s.lvl != 0):
                if (temp_pset.has_key(s.id_parent)):
#                    pset[s.id_parent].children.insert(s.order, s)
                    tps = temp_pset[s.id_parent].children
                    tps.insert(s.order, s)
                    tps.sort(key=lambda par: par.order)

        #merge the psets created
        temp_psKeys = temp_pset.keys() #viewkeys()               
        
        for ss in temp_psKeys:
            s = temp_pset.get(ss)
            if(s.lvl==0):
                temp_params.insert(s.order, s)
#                params.sort(key=lambda par: par.order)
        
        #merge the vpsets created
        temp_vpsKeys = temp_vpset.keys() #viewkeys()               
        
        for ss in temp_vpsKeys:
            s = temp_vpset.get(ss)
            if(s.lvl==0):
                temp_params.insert(s.order, s)
 
        temp_params.sort(key=lambda par: par.order)
        
        return temp_params    
    

    def moduleParamsBuilder(self, mid=-2, queries=None, db=None):
    
        params = []
        id_p = mid
        #Retreive the module template
        template = queries.getTemplateFromPae(id_p,db) 
        
        #Retreive template parameters
        tempelements = queries.getTemplateParams(template.id,db)
        
        tempelements_dict = dict((x.id, x) for x in tempelements)
        print "TEMPLATE ELEMENTS LEN: ", len(tempelements)
        
        #Build template parameters
        temp_pset = {}
        temp_vpset = {}
        temp_parents = {}
        temp_parents[0]=-1
        
        #Build all the vpsets/psets 
        
        temp_params = []
        temp_params_dict = {}
        temp_params_name_dict = {}
        
        for p in tempelements:
#            print p.id
            parent = temp_parents.get(p.lvl)
            clvl = p.lvl+1
            item = Parameter(p.id, p.name, p.value, p.moetype, p.paramtype, parent, p.lvl, p.order, p.tracked)
            item.default = True
            
#            print item
            temp_params_name_dict[item.name] = item
            
            # It is a vpset
            if (item.moetype == 3):
                temp_parents[clvl] = p.id
                item.expanded = False
                temp_vpset[item.id] = item
        
            # It is a pset
            elif (item.moetype == 2):
                temp_parents[clvl] = p.id
                item.expanded = False
                temp_pset[item.id]=item
                if (temp_vpset.has_key(item.id_parent)):                
                    temp_vpset[item.id_parent].children.insert(item.order, item)

            # It is a param
            else:
                if(item.lvl == 0):
                    temp_params.insert(item.order,item)
                    temp_params.sort(key=lambda par: par.order)
                else:
                    tps = temp_pset[item.id_parent].children
                    tps.insert(item.order, item)
                    tps.sort(key=lambda par: par.order)
           
        #complete Pset construction
        temp_psets = temp_pset.values() #viewvalues() 
        for s in temp_psets:
            if (s.lvl != 0):
                if (temp_pset.has_key(s.id_parent)):
#                    pset[s.id_parent].children.insert(s.order, s)
                    tps = temp_pset[s.id_parent].children
                    tps.insert(s.order, s)
                    tps.sort(key=lambda par: par.order)

        #merge the psets created
        temp_psKeys = temp_pset.keys() #viewkeys()               
        
        for ss in temp_psKeys:
            s = temp_pset.get(ss)
            if(s.lvl==0):
                temp_params.insert(s.order, s)
#                params.sort(key=lambda par: par.order)
        
        #merge the vpsets created
        temp_vpsKeys = temp_vpset.keys() #viewkeys()               
        
        for ss in temp_vpsKeys:
            s = temp_vpset.get(ss)
            if(s.lvl==0):
                temp_params.insert(s.order, s)
        
        temp_params_dict = dict((x.id, x) for x in temp_params)
        
        #------------------------------------------------------------------------------------------------------------
        #Retreive all the parameters of the module
        items = []
        
        items = queries.getModuleParamItems(id_p, db)
        
        itemsLen = len(items)
        
        print "ITEMS: ", itemsLen
#        
#        if(itemsLen > 100):
#            items = items[:100]
        
        moeIds = []
        for it in items:
            moeIds.append(int(it.id_moe))
            print it.id, it.id_pae, it.id_moe, it.lvl, it.order 
            
        moeIdsLen = len(moeIds)
        
        print "MOEIDS: ", moeIdsLen
        
        
        elements = queries.getModuleParamElements(moeIds, db)
        
        print "ELEMENTS: ", len(elements) 

#        items_dict = dict((x.id, x) for x in items)
        elements_dict = dict((x.id, x) for x in elements)

        pset = {}
        vpset = {}
        parents = {}
        
        parents[0]=-1
        #Build all the vpsets/psets 
        
        not_in = []
        params = []
        pset_name_dict = {}
        vpset_name_dict = {}
        params_mod_name_dict = {}
        
        for p in items:
#            print p.id_moe
            elem = elements_dict[p.id_moe]
            parent = parents.get(p.lvl)
            clvl = p.lvl+1
#            print "TYPE: ", type(elem.moetype), elem.moetype
            item = Parameter(p.id_moe, elem.name, elem.value, elem.moetype, elem.paramtype, parent, p.lvl, p.order, elem.tracked)
             
            params_mod_name_dict[item.name]=item
            #Set default
            if (temp_params_name_dict.has_key(item.name)):
                if temp_params_name_dict.get(item.name).value == item.value:
                    item.default = True
            
            # It is a vpset
            if (item.moetype == 3):
                parents[clvl] = p.id_moe
                item.expanded = False
                vpset[item.id] = item
                vpset_name_dict[item.name]=item
        
            # It is a pset
            elif (item.moetype == 2):
                parents[clvl] = p.id_moe
                item.expanded = False
                pset[item.id]=item
                pset_name_dict[item.name]=item
                if (vpset.has_key(item.id_parent)):                
                    vpset[item.id_parent].children.insert(item.order, item)

            # It is a param
            else:
                if(item.lvl == 0):
                    params.insert(item.order,item)
                    params.sort(key=lambda par: par.order)
                else:
                    tps = pset[item.id_parent].children
                    tps.insert(item.order, item)
                    tps.sort(key=lambda par: par.order)
        
        #Check ok temp params
        names = temp_params_name_dict.keys() #viewkeys()
        for pn in names:
            if (not(params_mod_name_dict.has_key(pn))): #The param is not in the module
                not_in.append(temp_params_name_dict.get(pn))
        
        
        #Fill the remaining params from Template
        print "LEN NOT_IN: ", len(not_in)
#        print not_in
        if (len(not_in) > 0):
            for n in not_in:
                if (n.lvl != 0):
                    if (n.id_parent in temp_vpset.keys()): #viewkeys()):
                        if(vpset_name_dict.has_key(temp_vpset.get(n.id_parent).name)):
                            vpset_name_dict.get(temp_vpset.get(n.id_parent).name).children.insert(n.order,n)

                    if (n.id_parent in temp_pset.keys()): #viewkeys()):
                        if(pset_name_dict.has_key(temp_pset.get(n.id_parent).name)):
                            pset_name_dict.get(temp_pset.get(n.id_parent).name).children.insert(n.order,n)
                    
                    else:
                        print "DOVE?: ", n.name," " ,n.id, " ",n.id_parent
        
        #complete Pset construction
        psets = pset.values() #viewvalues() 
        for s in psets:
            if (s.lvl != 0):
                if (pset.has_key(s.id_parent)):
#                    pset[s.id_parent].children.insert(s.order, s)
                    tps = pset[s.id_parent].children
                    tps.insert(s.order, s)
                    tps.sort(key=lambda par: par.order)

        #merge the psets created
        psKeys = pset.keys() #viewkeys() #pset.keys() #viewkeys()               
        
        for ss in psKeys:
            s = pset.get(ss)
            if(s.lvl==0):
                params.insert(s.order, s)
#                params.sort(key=lambda par: par.order)
        
        #merge the vpsets created
        vpsKeys = vpset.keys() #viewkeys()               
        
        for ss in vpsKeys:
            s = vpset.get(ss)
            if(s.lvl==0):
                params.insert(s.order, s)
        
        #Merge the remaining template params
        for p in not_in:
            if(p.lvl==0):
                tp = temp_params_dict.get(p.id)
                params.insert(tp.order, p)
                
        params.sort(key=lambda par: par.order)
        
        return params
    
    
#--------------------------------------------------------------------------------------
    def esModuleParamsBuilder(self, sid=-2, queries=None, db=None):
    
        #params check
        if (sid == -2 or db == None or queries == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        print "SID: ", sid     
        
        queries = queries
        params = []
        id_p = sid #srvsMap.get(sid)    
        
        print "ID_P: ", id_p, sid
        
        #Retreive the module template
        template = queries.getESMTemplateByEsm(id_p,db) 
        
        #Retreive template parameters
        tempelements = queries.getESMTemplateParams(template.id,db)
        
        tempelements_dict = dict((x.id, x) for x in tempelements)
        print "TEMPLATE ELEMENTS LEN: ", len(tempelements)
        
        #Build template parameters
        temp_pset = {}
        temp_vpset = {}
        temp_parents = {}
        temp_parents[0]=-1
        
        #Build all the vpsets/psets 
        
        temp_params = []
        temp_params_dict = {}
        temp_params_name_dict = {}
        
        for p in tempelements:
#            print p.id
            parent = temp_parents.get(p.lvl)
            clvl = p.lvl+1
            item = Parameter(p.id, p.name, p.value, p.moetype, p.paramtype, parent, p.lvl, p.order, p.tracked)
            item.default = True
            
#            print item
            temp_params_name_dict[item.name] = item
            
            # It is a vpset
            if (item.moetype == 3):
                temp_parents[clvl] = p.id
                item.expanded = False
                temp_vpset[item.id] = item
        
            # It is a pset
            elif (item.moetype == 2):
                temp_parents[clvl] = p.id
                item.expanded = False
                temp_pset[item.id]=item
                if (temp_vpset.has_key(item.id_parent)):                
                    temp_vpset[item.id_parent].children.insert(item.order, item)

            # It is a param
            else:
                if(item.lvl == 0):
                    temp_params.insert(item.order,item)
                    temp_params.sort(key=lambda par: par.order)
                else:
                    tps = temp_pset[item.id_parent].children
                    tps.insert(item.order, item)
                    tps.sort(key=lambda par: par.order)
           
        #complete Pset construction
        temp_psets = temp_pset.values() #viewvalues() 
        for s in temp_psets:
            if (s.lvl != 0):
                if (temp_pset.has_key(s.id_parent)):
#                    pset[s.id_parent].children.insert(s.order, s)
                    tps = temp_pset[s.id_parent].children
                    tps.insert(s.order, s)
                    tps.sort(key=lambda par: par.order)

        #merge the psets created
        temp_psKeys = temp_pset.keys() #viewkeys()               
        
        for ss in temp_psKeys:
            s = temp_pset.get(ss)
            if(s.lvl==0):
                temp_params.insert(s.order, s)
#                params.sort(key=lambda par: par.order)
        
        #merge the vpsets created
        temp_vpsKeys = temp_vpset.keys() #viewkeys()               
        
        for ss in temp_vpsKeys:
            s = temp_vpset.get(ss)
            if(s.lvl==0):
                temp_params.insert(s.order, s)
        
        temp_params_dict = dict((x.id, x) for x in temp_params)
        
        #------------------------------------------------------------------------------------------------------------
        #Retreive all the parameters of the module
        elements = queries.getESModParams(id_p, db)
        
        print "ELEMENTS: ", len(elements) 

        elements_dict = dict((x.id, x) for x in elements)

        pset = {}
        vpset = {}
        parents = {}
        
        parents[0]=-1
        #Build all the vpsets/psets 
        
        not_in = []
        params = []
        pset_name_dict = {}
        vpset_name_dict = {}
        params_mod_name_dict = {}
        
        for p in elements:
#            elem = p #elements_dict[p.id_moe]
            parent = parents.get(p.lvl)
            clvl = p.lvl+1
#            print "TYPE: ", type(elem.moetype), elem.moetype
            item = Parameter(p.id, p.name, p.value, p.moetype, p.paramtype, parent, p.lvl, p.order, p.tracked)
             
            params_mod_name_dict[item.name]=item
            #Set default
            if (temp_params_name_dict.has_key(item.name)):
                if temp_params_name_dict.get(item.name).value == item.value:
                    item.default = True
            
            # It is a vpset
            if (item.moetype == 3):
                parents[clvl] = p.id
                item.expanded = False
                vpset[item.id] = item
                vpset_name_dict[item.name]=item
        
            # It is a pset
            elif (item.moetype == 2):
                parents[clvl] = p.id
                item.expanded = False
                pset[item.id]=item
                pset_name_dict[item.name]=item
                if (vpset.has_key(item.id_parent)):                
                    vpset[item.id_parent].children.insert(item.order, item)

            # It is a param
            else:
                if(item.lvl == 0):
                    params.insert(item.order,item)
                    params.sort(key=lambda par: par.order)
                else:
                    tps = pset[item.id_parent].children
                    tps.insert(item.order, item)
                    tps.sort(key=lambda par: par.order)
        
        #Check ok temp params
        names = temp_params_name_dict.keys() #viewkeys()
        for pn in names:
            if (not(params_mod_name_dict.has_key(pn))): #The param is not in the module
                not_in.append(temp_params_name_dict.get(pn))
        
        
        #Fill the remaining params from Template
        print "LEN NOT_IN: ", len(not_in)
#        print not_in
        if (len(not_in) > 0):
            for n in not_in:
                if (n.lvl != 0):
                    if (n.id_parent in temp_vpset.keys()): #viewkeys()):
                        if(vpset_name_dict.has_key(temp_vpset.get(n.id_parent).name)):
                            vpset_name_dict.get(temp_vpset.get(n.id_parent).name).children.insert(n.order,n)

                    if (n.id_parent in temp_pset.keys()): #viewkeys()):
                        if(pset_name_dict.has_key(temp_pset.get(n.id_parent).name)):
                            pset_name_dict.get(temp_pset.get(n.id_parent).name).children.insert(n.order,n)
                    
                    else:
                        print "DOVE?: ", n.name," " ,n.id, " ",n.id_parent
        
        #complete Pset construction
        psets = pset.values() #viewvalues() 
        for s in psets:
            if (s.lvl != 0):
                if (pset.has_key(s.id_parent)):
#                    pset[s.id_parent].children.insert(s.order, s)
                    tps = pset[s.id_parent].children
                    tps.insert(s.order, s)
                    tps.sort(key=lambda par: par.order)

        #merge the psets created
        psKeys = pset.keys() #viewkeys() #pset.keys() #viewkeys()               
        
        for ss in psKeys:
            s = pset.get(ss)
            if(s.lvl==0):
                params.insert(s.order, s)
#                params.sort(key=lambda par: par.order)
        
        #merge the vpsets created
        vpsKeys = vpset.keys() #viewkeys()               
        
        for ss in vpsKeys:
            s = vpset.get(ss)
            if(s.lvl==0):
                params.insert(s.order, s)
        
        #Merge the remaining template params
        for p in not_in:
            if(p.lvl==0):
                tp = temp_params_dict.get(p.id)
                params.insert(tp.order, p)
                
        params.sort(key=lambda par: par.order)
        
        return params
    
    def gpsetParamsBuilder(self, sid=-2, queries=None, db=None):
        #params check
        if (sid == -2 or db == None or queries == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        print "SID: ", sid     
        
        queries = queries
        params = []
        id_p = sid #srvsMap.get(sid)    
        
        print "ID_P: ", id_p, sid

        #Retreive all the parameters of the module
        elements = queries.getGpsetElements(id_p, db)
        
        print "ELEMENTS: ", len(elements) 

        elements_dict = dict((x.id, x) for x in elements)

        pset = {}
        vpset = {}
        parents = {}
        
        parents[0]=-1
        #Build all the vpsets/psets 
        
        not_in = []
        params = []
        pset_name_dict = {}
        vpset_name_dict = {}
        params_mod_name_dict = {}
        
        for p in elements:
#            elem = p #elements_dict[p.id_moe]
            parent = parents.get(p.lvl)
            clvl = p.lvl+1
#            print "TYPE: ", type(elem.moetype), elem.moetype
            item = Parameter(p.id, p.name, p.value, p.moetype, p.paramtype, parent, p.lvl, p.order, p.tracked)
            
            # It is a vpset
            if (item.moetype == 3):
                parents[clvl] = p.id
                item.expanded = False
                vpset[item.id] = item
                vpset_name_dict[item.name]=item
        
            # It is a pset
            elif (item.moetype == 2):
                parents[clvl] = p.id
                item.expanded = False
                pset[item.id]=item
                pset_name_dict[item.name]=item
                if (vpset.has_key(item.id_parent)):                
                    vpset[item.id_parent].children.insert(item.order, item)

            # It is a param
            else:
                if(item.lvl == 0):
                    params.insert(item.order,item)
                    params.sort(key=lambda par: par.order)
                else:
                    tps = pset[item.id_parent].children
                    tps.insert(item.order, item)
                    tps.sort(key=lambda par: par.order)
        
        #complete Pset construction
        psets = pset.values() #viewvalues() 
        for s in psets:
            if (s.lvl != 0):
                if (pset.has_key(s.id_parent)):
#                    pset[s.id_parent].children.insert(s.order, s)
                    tps = pset[s.id_parent].children
                    tps.insert(s.order, s)
                    tps.sort(key=lambda par: par.order)

        #merge the psets created
        psKeys = pset.keys() #viewkeys() #pset.keys() #viewkeys()               
        
        for ss in psKeys:
            s = pset.get(ss)
            if(s.lvl==0):
                params.insert(s.order, s)
#                params.sort(key=lambda par: par.order)
        
        #merge the vpsets created
        vpsKeys = vpset.keys() #viewkeys()               
        
        for ss in vpsKeys:
            s = vpset.get(ss)
            if(s.lvl==0):
                params.insert(s.order, s)
                
        params.sort(key=lambda par: par.order)
        
        return params
    
    def outputModuleParamsBuilder(self, sid=-2, queries=None, db=None):
        #params check
        if (sid == -2 or db == None or queries == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        print "SID: ", sid     
        
        queries = queries
        params = []
        id_p = sid #srvsMap.get(sid)    
        
        print "ID_P: ", id_p, sid

        #Retreive all the parameters of the module
        elements = queries.getOUMElements(id_p, db)
        
        print "ELEMENTS: ", len(elements) 

        elements_dict = dict((x.id, x) for x in elements)

        pset = {}
        vpset = {}
        parents = {}
        
        parents[0]=-1
        #Build all the vpsets/psets 
        
        not_in = []
        params = []
        pset_name_dict = {}
        vpset_name_dict = {}
        params_mod_name_dict = {}
        
        for p in elements:
#            elem = p #elements_dict[p.id_moe]
            parent = parents.get(p.lvl)
            clvl = p.lvl+1
#            print "TYPE: ", type(elem.moetype), elem.moetype
            item = Parameter(p.id, p.name, p.value, p.moetype, p.paramtype, parent, p.lvl, p.order, p.tracked)
             
#            params_mod_name_dict[item.name]=item
#            #Set default
#            if (temp_params_name_dict.has_key(item.name)):
#                if temp_params_name_dict.get(item.name).value == item.value:
#                    item.default = True
            
            # It is a vpset
            if (item.moetype == 3):
                parents[clvl] = p.id
                item.expanded = False
                vpset[item.id] = item
                vpset_name_dict[item.name]=item
        
            # It is a pset
            elif (item.moetype == 2):
                parents[clvl] = p.id
                item.expanded = False
                pset[item.id]=item
                pset_name_dict[item.name]=item
                if (vpset.has_key(item.id_parent)):                
                    vpset[item.id_parent].children.insert(item.order, item)

            # It is a param
            else:
                if(item.lvl == 0):
                    params.insert(item.order,item)
                    params.sort(key=lambda par: par.order)
                else:
                    tps = pset[item.id_parent].children
                    tps.insert(item.order, item)
                    tps.sort(key=lambda par: par.order)
        
        #complete Pset construction
        psets = pset.values() #viewvalues() 
        for s in psets:
            if (s.lvl != 0):
                if (pset.has_key(s.id_parent)):
#                    pset[s.id_parent].children.insert(s.order, s)
                    tps = pset[s.id_parent].children
                    tps.insert(s.order, s)
                    tps.sort(key=lambda par: par.order)

        #merge the psets created
        psKeys = pset.keys() #viewkeys() #pset.keys() #viewkeys()               
        
        for ss in psKeys:
            s = pset.get(ss)
            if(s.lvl==0):
                params.insert(s.order, s)
#                params.sort(key=lambda par: par.order)
        
        #merge the vpsets created
        vpsKeys = vpset.keys() #viewkeys()               
        
        for ss in vpsKeys:
            s = vpset.get(ss)
            if(s.lvl==0):
                params.insert(s.order, s)
        
        #Merge the remaining template params
#        for p in not_in:
#            if(p.lvl==0):
#                tp = temp_params_dict.get(p.id)
#                params.insert(tp.order, p)
                
        params.sort(key=lambda par: par.order)
        
        return params 
    def edSourceParamsBuilder(self, sid=-2, queries=None, db=None):
    
        #params check
        if (sid == -2 or db == None or queries == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        print "SID: ", sid     
        
        queries = queries
        params = []
        id_p = sid #srvsMap.get(sid)    
        
        print "ID_P: ", id_p, sid
        
        #Retreive the module template
        template = queries.getEDSTemplateByEds(id_p,db) 
        
        #Retreive template parameters
        tempelements = queries.getEDSTemplateParams(template.id,db)
        
        tempelements_dict = dict((x.id, x) for x in tempelements)
        print "TEMPLATE ELEMENTS LEN: ", len(tempelements)
        
        #Build template parameters
        temp_pset = {}
        temp_vpset = {}
        temp_parents = {}
        temp_parents[0]=-1
        
        #Build all the vpsets/psets 
        
        temp_params = []
        temp_params_dict = {}
        temp_params_name_dict = {}
        
        for p in tempelements:
#            print p.id
            parent = temp_parents.get(p.lvl)
            clvl = p.lvl+1
            item = Parameter(p.id, p.name, p.value, p.moetype, p.paramtype, parent, p.lvl, p.order, p.tracked)
            item.default = True
            
#            print item
            temp_params_name_dict[item.name] = item
            
            # It is a vpset
            if (item.moetype == 3):
                temp_parents[clvl] = p.id
                item.expanded = False
                temp_vpset[item.id] = item
        
            # It is a pset
            elif (item.moetype == 2):
                temp_parents[clvl] = p.id
                item.expanded = False
                temp_pset[item.id]=item
                if (temp_vpset.has_key(item.id_parent)):                
                    temp_vpset[item.id_parent].children.insert(item.order, item)

            # It is a param
            else:
                if(item.lvl == 0):
                    temp_params.insert(item.order,item)
                    temp_params.sort(key=lambda par: par.order)
                else:
                    tps = temp_pset[item.id_parent].children
                    tps.insert(item.order, item)
                    tps.sort(key=lambda par: par.order)
           
        #complete Pset construction
        temp_psets = temp_pset.values() #viewvalues() 
        for s in temp_psets:
            if (s.lvl != 0):
                if (temp_pset.has_key(s.id_parent)):
#                    pset[s.id_parent].children.insert(s.order, s)
                    tps = temp_pset[s.id_parent].children
                    tps.insert(s.order, s)
                    tps.sort(key=lambda par: par.order)

        #merge the psets created
        temp_psKeys = temp_pset.keys() #viewkeys()               
        
        for ss in temp_psKeys:
            s = temp_pset.get(ss)
            if(s.lvl==0):
                temp_params.insert(s.order, s)
#                params.sort(key=lambda par: par.order)
        
        #merge the vpsets created
        temp_vpsKeys = temp_vpset.keys() #viewkeys()               
        
        for ss in temp_vpsKeys:
            s = temp_vpset.get(ss)
            if(s.lvl==0):
                temp_params.insert(s.order, s)
        
        temp_params_dict = dict((x.id, x) for x in temp_params)
        
        #------------------------------------------------------------------------------------------------------------
        #Retreive all the parameters of the module
        elements = queries.getEDSourceParams(id_p, db)
        
        print "ELEMENTS: ", len(elements) 

        elements_dict = dict((x.id, x) for x in elements)

        pset = {}
        vpset = {}
        parents = {}
        
        parents[0]=-1
        #Build all the vpsets/psets 
        
        not_in = []
        params = []
        pset_name_dict = {}
        vpset_name_dict = {}
        params_mod_name_dict = {}
        
        for p in elements:
#            elem = p #elements_dict[p.id_moe]
            parent = parents.get(p.lvl)
            clvl = p.lvl+1
#            print "TYPE: ", type(elem.moetype), elem.moetype
            item = Parameter(p.id, p.name, p.value, p.moetype, p.paramtype, parent, p.lvl, p.order, p.tracked)
             
            params_mod_name_dict[item.name]=item
            #Set default
            if (temp_params_name_dict.has_key(item.name)):
                if temp_params_name_dict.get(item.name).value == item.value:
                    item.default = True
            
            # It is a vpset
            if (item.moetype == 3):
                parents[clvl] = p.id
                item.expanded = False
                vpset[item.id] = item
                vpset_name_dict[item.name]=item
        
            # It is a pset
            elif (item.moetype == 2):
                parents[clvl] = p.id
                item.expanded = False
                pset[item.id]=item
                pset_name_dict[item.name]=item
                if (vpset.has_key(item.id_parent)):                
                    vpset[item.id_parent].children.insert(item.order, item)

            # It is a param
            else:
                if(item.lvl == 0):
                    params.insert(item.order,item)
                    params.sort(key=lambda par: par.order)
                else:
                    tps = pset[item.id_parent].children
                    tps.insert(item.order, item)
                    tps.sort(key=lambda par: par.order)
        
        #Check ok temp params
        names = temp_params_name_dict.keys() #viewkeys()
        for pn in names:
            if (not(params_mod_name_dict.has_key(pn))): #The param is not in the module
                not_in.append(temp_params_name_dict.get(pn))
        
        
        #Fill the remaining params from Template
        print "LEN NOT_IN: ", len(not_in)
#        print not_in
        if (len(not_in) > 0):
            for n in not_in:
                if (n.lvl != 0):
                    if (n.id_parent in temp_vpset.keys()): #viewkeys()):
                        if(vpset_name_dict.has_key(temp_vpset.get(n.id_parent).name)):
                            vpset_name_dict.get(temp_vpset.get(n.id_parent).name).children.insert(n.order,n)

                    if (n.id_parent in temp_pset.keys()): #viewkeys()):
                        if(pset_name_dict.has_key(temp_pset.get(n.id_parent).name)):
                            pset_name_dict.get(temp_pset.get(n.id_parent).name).children.insert(n.order,n)
                    
                    else:
                        print "DOVE?: ", n.name," " ,n.id, " ",n.id_parent
        
        #complete Pset construction
        psets = pset.values() #viewvalues() 
        for s in psets:
            if (s.lvl != 0):
                if (pset.has_key(s.id_parent)):
#                    pset[s.id_parent].children.insert(s.order, s)
                    tps = pset[s.id_parent].children
                    tps.insert(s.order, s)
                    tps.sort(key=lambda par: par.order)

        #merge the psets created
        psKeys = pset.keys() #viewkeys() #pset.keys() #viewkeys()               
        
        for ss in psKeys:
            s = pset.get(ss)
            if(s.lvl==0):
                params.insert(s.order, s)
#                params.sort(key=lambda par: par.order)
        
        #merge the vpsets created
        vpsKeys = vpset.keys() #viewkeys()               
        
        for ss in vpsKeys:
            s = vpset.get(ss)
            if(s.lvl==0):
                params.insert(s.order, s)
        
        #Merge the remaining template params
        for p in not_in:
            if(p.lvl==0):
                tp = temp_params_dict.get(p.id)
                params.insert(tp.order, p)
                
        params.sort(key=lambda par: par.order)
        
        return params
    
    def esSourceParamsBuilder(self, sid=-2, queries=None, db=None):
    
        #params check
        if (sid == -2 or db == None or queries == None):
            print ("PARAMETERS EXCEPTION HERE")
            
        print "SID: ", sid     
        
        queries = queries
        params = []
        id_p = sid #srvsMap.get(sid)    
        
        print "ID_P: ", id_p, sid
        
        #Retreive the module template
        template = queries.getESSTemplateByEss(id_p,db) 
        
        #Retreive template parameters
        tempelements = queries.getESSTemplateParams(template.id,db)
        
        tempelements_dict = dict((x.id, x) for x in tempelements)
        print "TEMPLATE ELEMENTS LEN: ", len(tempelements)
        
        #Build template parameters
        temp_pset = {}
        temp_vpset = {}
        temp_parents = {}
        temp_parents[0]=-1
        
        #Build all the vpsets/psets 
        
        temp_params = []
        temp_params_dict = {}
        temp_params_name_dict = {}
        
        for p in tempelements:
#            print p.id
            parent = temp_parents.get(p.lvl)
            clvl = p.lvl+1
            item = Parameter(p.id, p.name, p.value, p.moetype, p.paramtype, parent, p.lvl, p.order, p.tracked)
            item.default = True
            
#            print item
            temp_params_name_dict[item.name] = item
            
            # It is a vpset
            if (item.moetype == 3):
                temp_parents[clvl] = p.id
                item.expanded = False
                temp_vpset[item.id] = item
        
            # It is a pset
            elif (item.moetype == 2):
                temp_parents[clvl] = p.id
                item.expanded = False
                temp_pset[item.id]=item
                if (temp_vpset.has_key(item.id_parent)):                
                    temp_vpset[item.id_parent].children.insert(item.order, item)

            # It is a param
            else:
                if(item.lvl == 0):
                    temp_params.insert(item.order,item)
                    temp_params.sort(key=lambda par: par.order)
                else:
                    tps = temp_pset[item.id_parent].children
                    tps.insert(item.order, item)
                    tps.sort(key=lambda par: par.order)
           
        #complete Pset construction
        temp_psets = temp_pset.values() #viewvalues() 
        for s in temp_psets:
            if (s.lvl != 0):
                if (temp_pset.has_key(s.id_parent)):
#                    pset[s.id_parent].children.insert(s.order, s)
                    tps = temp_pset[s.id_parent].children
                    tps.insert(s.order, s)
                    tps.sort(key=lambda par: par.order)

        #merge the psets created
        temp_psKeys = temp_pset.keys() #viewkeys()               
        
        for ss in temp_psKeys:
            s = temp_pset.get(ss)
            if(s.lvl==0):
                temp_params.insert(s.order, s)
#                params.sort(key=lambda par: par.order)
        
        #merge the vpsets created
        temp_vpsKeys = temp_vpset.keys() #viewkeys()               
        
        for ss in temp_vpsKeys:
            s = temp_vpset.get(ss)
            if(s.lvl==0):
                temp_params.insert(s.order, s)
        
        temp_params_dict = dict((x.id, x) for x in temp_params)
        
        #------------------------------------------------------------------------------------------------------------
        #Retreive all the parameters of the module
        elements = queries.getESSourceParams(id_p, db)
        
        print "ELEMENTS: ", len(elements) 

        elements_dict = dict((x.id, x) for x in elements)

        pset = {}
        vpset = {}
        parents = {}
        
        parents[0]=-1
        #Build all the vpsets/psets 
        
        not_in = []
        params = []
        pset_name_dict = {}
        vpset_name_dict = {}
        params_mod_name_dict = {}
        
        for p in elements:
#            elem = p #elements_dict[p.id_moe]
            parent = parents.get(p.lvl)
            clvl = p.lvl+1
#            print "TYPE: ", type(elem.moetype), elem.moetype
            item = Parameter(p.id, p.name, p.value, p.moetype, p.paramtype, parent, p.lvl, p.order, p.tracked)
             
            params_mod_name_dict[item.name]=item
            #Set default
            if (temp_params_name_dict.has_key(item.name)):
                if temp_params_name_dict.get(item.name).value == item.value:
                    item.default = True
            
            # It is a vpset
            if (item.moetype == 3):
                parents[clvl] = p.id
                item.expanded = False
                vpset[item.id] = item
                vpset_name_dict[item.name]=item
        
            # It is a pset
            elif (item.moetype == 2):
                parents[clvl] = p.id
                item.expanded = False
                pset[item.id]=item
                pset_name_dict[item.name]=item
                if (vpset.has_key(item.id_parent)):                
                    vpset[item.id_parent].children.insert(item.order, item)

            # It is a param
            else:
                if(item.lvl == 0):
                    params.insert(item.order,item)
                    params.sort(key=lambda par: par.order)
                else:
                    tps = pset[item.id_parent].children
                    tps.insert(item.order, item)
                    tps.sort(key=lambda par: par.order)
        
        #Check ok temp params
        names = temp_params_name_dict.keys() #viewkeys()
        for pn in names:
            if (not(params_mod_name_dict.has_key(pn))): #The param is not in the module
                not_in.append(temp_params_name_dict.get(pn))
        
        
        #Fill the remaining params from Template
        print "LEN NOT_IN: ", len(not_in)
#        print not_in
        if (len(not_in) > 0):
            for n in not_in:
                if (n.lvl != 0):
                    if (n.id_parent in temp_vpset.keys()): #viewkeys()):
                        if(vpset_name_dict.has_key(temp_vpset.get(n.id_parent).name)):
                            vpset_name_dict.get(temp_vpset.get(n.id_parent).name).children.insert(n.order,n)

                    if (n.id_parent in temp_pset.keys()): #viewkeys()):
                        if(pset_name_dict.has_key(temp_pset.get(n.id_parent).name)):
                            pset_name_dict.get(temp_pset.get(n.id_parent).name).children.insert(n.order,n)
                    
                    else:
                        print "DOVE?: ", n.name," " ,n.id, " ",n.id_parent
        
        #complete Pset construction
        psets = pset.values() #viewvalues() 
        for s in psets:
            if (s.lvl != 0):
                if (pset.has_key(s.id_parent)):
#                    pset[s.id_parent].children.insert(s.order, s)
                    tps = pset[s.id_parent].children
                    tps.insert(s.order, s)
                    tps.sort(key=lambda par: par.order)

        #merge the psets created
        psKeys = pset.keys() #viewkeys() #pset.keys() #viewkeys()               
        
        for ss in psKeys:
            s = pset.get(ss)
            if(s.lvl==0):
                params.insert(s.order, s)
#                params.sort(key=lambda par: par.order)
        
        #merge the vpsets created
        vpsKeys = vpset.keys() #viewkeys()               
        
        for ss in vpsKeys:
            s = vpset.get(ss)
            if(s.lvl==0):
                params.insert(s.order, s)
        
        #Merge the remaining template params
        for p in not_in:
            if(p.lvl==0):
                tp = temp_params_dict.get(p.id)
                params.insert(tp.order, p)
                
        params.sort(key=lambda par: par.order)
        
        return params
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    