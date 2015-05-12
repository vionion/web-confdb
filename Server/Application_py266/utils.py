class Counter(object):
    
    def __init__(self):
        self.counter = 0
    
    def getNext(self):
        self.counter += 1
        return self.counter

    
class ModulesDict(object):
    
    def __init__(self):
        self.modDict = {}
    
    def put(self, counter, module):
        mid = module.id
        if (mid in self.modDict.values()):
            return [k for k, v in self.modDict.iteritems() if v == mid][0]
        else:
            gid = counter.getNext()
            self.modDict[gid] = mid
            return gid
        
    def get(self,gid):
        if self.modDict.has_key(gid):
            return self.modDict.get(gid)
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
        
        
class SequencesDict(object):
    
    def __init__(self):
        self.seqDict = {}
    
    def put(self, counter, sequence):
        sid = sequence.id
        if(sid in self.seqDict.values()):
            return [k for k, v in self.seqDict.iteritems() if v == sid][0]
        else:
            gid = counter.getNext()
            self.seqDict[gid] = sid
            return gid
        
    def get(self,gid):
        if self.seqDict.has_key(gid):
            return self.seqDict.get(gid)
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
        