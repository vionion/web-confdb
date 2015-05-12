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