class Counter(object):
    
    def __init__(self):
        self.counter = 0
    
    def getNext(self):
        self.counter += 1
        return self.counter

#value string: "id,id_pathid,order,lvl"     
class ModulesDict(object):
    
    def __init__(self):
        self.modDict = {}
    
    # Put for Path items
    def putItem(self, counter, module, id_pathid, order,lvl):
        mid = module.id
        value = str(mid)+","+str(id_pathid)+","+str(order)+","+str(lvl)
        if (value in self.modDict.values()):
            return [k for k, v in self.modDict.iteritems() if v == value][0]
        else:
            gid = counter.getNext()
            self.modDict[gid] = value
            return gid
    
    # Put for Modules module_id + -1 + 0 + 0
    def putModule(self, counter, module):
        mid = module.id
        values = self.modDict.values()
        new_gid = -3 
        for key, value in self.modDict.iteritems():
            vals_list = value.split(",")
            id_mod = vals_list[0]
            if id_mod == mid:
                new_gid = key
                break
        new_value = str(mid)+","+str(-1)+","+str(0)+","+str(0)
        if new_gid == -3:
            gid = counter.getNext()
            self.modDict[gid] = new_value
            return gid
        
        else:
            return new_gid 
        
    def get(self,gid):
        if self.modDict.has_key(gid):
            value = self.modDict.get(gid)
            vals_list = value.split(",")
            id_mod = vals_list[0]
            return int(id_mod)
        else:
            return -2

class AllModulesDict(object):
    
    def __init__(self):
        self.allmodDict = {}
    
    def put(self, counter, module):
        mid = module.id
        if (mid in self.allmodDict.values()):
            return [k for k, v in self.allmodDict.iteritems() if v == mid][0]
        else:
            gid = counter.getNext()
            self.allmodDict[gid] = mid
            return gid
        
    def get(self,gid):
        if self.allmodDict.has_key(gid):
            return self.allmodDict.get(gid)
        else:
            return -2
        
class OutputModulesDict(object):
    
    def __init__(self):
        self.oumodDict = {}
    
    def put(self, counter, module):
        mid = module.id
        if (mid in self.oumodDict.values()):
            return [k for k, v in self.oumodDict.iteritems() if v == mid][0]
        else:
            gid = counter.getNext()
            self.oumodDict[gid] = mid
            return gid
        
    def get(self,gid):
        if self.oumodDict.has_key(gid):
            return self.oumodDict.get(gid)
        else:
            return -2
        
#value string: "id,id_pathid,order,lvl"        
class SequencesDict(object):
    
    def __init__(self):
        self.seqDict = {}
    
    def put(self, counter, sequence, id_pathid, order,lvl):
        sid = sequence.id
        value = str(sid)+","+str(id_pathid)+","+str(order)+","+str(lvl)
        if(value in self.seqDict.values()):
            return [k for k, v in self.seqDict.iteritems() if v == value][0]
        else:
            gid = counter.getNext()
            self.seqDict[gid] = value
            return gid
        
    def get(self,gid):
        if self.seqDict.has_key(gid):
            value = self.seqDict.get(gid)
            vals_list = value.split(",")
            id_seq = vals_list[0]
            return int(id_seq)
        else:
            return -2
 

class PathsDict(object):
    
    def __init__(self):
        self.patDict = {}
    
    def put(self, counter, path):
        pid = path.id
        if(pid in self.patDict.values()):
            return [k for k, v in self.patDict.iteritems() if v == pid][0]
        else:
            gid = counter.getNext()
            self.patDict[gid] = pid
            return gid
        
    def get(self,gid):
        if self.patDict.has_key(gid):
            return self.patDict.get(gid)
        else:
            return -2
    
#-----------------------------------------------------------------

class FolderItemCounter(object):
    
    def __init__(self):
        self.counter = 0
    
    def getNext(self):
        self.counter += 1
        return self.counter

    
class ConfigsDict(object):
    
    def __init__(self):
        self.cnfDict = {}
    
    def put(self, counter, config):
        cid = config.id
        if (cid in self.cnfDict.values()):
            return [k for k, v in self.cnfDict.iteritems() if v == cid][0]
        else:
            gid = counter.getNext()
            self.cnfDict[gid] = cid
            return gid
        
    def get(self,gid):
        if(self.cnfDict.has_key(gid)):
            return self.cnfDict.get(gid)
        else:
            return -2
    
class FoldersDict(object):
    
    def __init__(self):
        self.folDict = {}
    
    def put(self, counter, folder):
        fid = folder.id
        if(fid in self.folDict.values()):
            return [k for k, v in self.folDict.iteritems() if v == fid][0]
        else:
            gid = counter.getNext()
            self.folDict[gid] = fid
            return gid
        
    def get(self,gid):
        if self.folDict.has_key(gid):
            return self.folDict.get(gid)
        else:
            return -2
#-----------------------------------------------------------------

class ServicesDict(object):
    
    def __init__(self):
        self.srvDict = {}
    
    def put(self, counter, service):
        sid = service.id
        if (sid in self.srvDict.values()):
            return [k for k, v in self.srvDict.iteritems() if v == sid][0]
        else:
            gid = counter.getNext()
            self.srvDict[gid] = sid
            return gid
        
    def get(self,gid):
        if self.srvDict.has_key(gid):
            return self.srvDict.get(gid)
        else:
            return -2
        
#-----------------------------------------------------------------

class StreamItemCounter(object):
    
    def __init__(self):
        self.counter = 0
    
    def getNext(self):
        self.counter += 1
        return self.counter

class StreamsDict(object):
    
    def __init__(self):
        self.strDict = {}
    
    def put(self, counter, stream):
        sid = stream.id
        if (sid in self.strDict.values()):
            return [k for k, v in self.strDict.iteritems() if v == sid][0]
        else:
            gid = counter.getNext()
            self.strDict[gid] = sid
            return gid
        
    def get(self,gid):
        if self.strDict.has_key(gid):
            return self.strDict.get(gid)
        else:
            return -2
        
class DatasetsDict(object):
    
    def __init__(self):
        self.datDict = {}
    
    def put(self, counter, dataset):
        sid = dataset.id
        if (sid in self.datDict.values()):
            return [k for k, v in self.datDict.iteritems() if v == sid][0]
        else:
            gid = counter.getNext()
            self.datDict[gid] = sid
            return gid
        
    def get(self,gid):
        if self.datDict.has_key(gid):
            return self.datDict.get(gid)
        else:
            return -2 
        
class EvcoDict(object):
    
    def __init__(self):
        self.evcDict = {}
    
    def put(self, counter, evco):
        sid = evco.id
        if (sid in self.evcDict.values()):
            return [k for k, v in self.evcDict.iteritems() if v == sid][0]
        else:
            gid = counter.getNext()
            self.evcDict[gid] = sid
            return gid
        
    def putDouble(self, counter, evco):
        sid = evco.id
        gid = counter.getNext()
        self.evcDict[gid] = sid
        return gid    
        
    def get(self,gid):
        if self.evcDict.has_key(gid):
            return self.evcDict.get(gid)
        else:
            return -2         
        
#-----------------------------------------------------------------

class GpsetsDict(object):
    
    def __init__(self):
        self.gpsDict = {}
    
    def put(self, counter, gps):
        sid = gps.id
        if (sid in self.gpsDict.values()):
            return [k for k, v in self.gpsDict.iteritems() if v == sid][0]
        else:
            gid = counter.getNext()
            self.gpsDict[gid] = sid
            return gid
        
    def get(self,gid):
        if self.gpsDict.has_key(gid):
            return self.gpsDict.get(gid)
        else:
            return -2

#-----------------------------------------------------------------
class SummaryItemCounter(object):
    
    def __init__(self):
        self.counter = 0
    
    def getNext(self):
        self.counter += 1
        return self.counter



class SummaryitemsDict(object):
    
    def __init__(self):
        self.sumDict = {}
    
    def put(self, counter, item, sit):
        sid = item.id
        value = sit + "_" + str(sid)
        if (value in self.sumDict.values()):
            return [k for k, v in self.sumDict.iteritems() if v == value][0]
        else:
            gid = counter.getNext()
            self.sumDict[gid] = value
            return gid
        
    def get(self,gid):
        if self.sumDict.has_key(gid):
            val = self.sumDict.get(gid)
            vals_list = value.split("_")
            id_sid = vals_list[1]
            return int(id_sid)
        else:
            return -2
