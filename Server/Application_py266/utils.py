import external.bidict as bidict

class Counter(object):

    def __init__(self):
        self.__counter = 0

    def getNext(self):
        self.__counter += 1
        return self.__counter


class UniqueMapping(object):

    def __init__(self, counter):
        self.__counter = counter
        self.__dict = bidict.bidict()

    def put(self, item, unique = True):
        value = item.id
        if unique and value in self.__dict.inv:
            return self.__dict.inv[value]
        else:
            key = self.__counter.getNext()
            self.__dict[key] = value
            return key

    def get(self, key):
        if key in self.__dict:
            return self.__dict[key]
        else:
            return -2


class ModulesMapping(object):

    def __init__(self, counter):
        self.__counter = counter
        self.__dict = bidict.bidict()

    # Put for Path items
    def put(self, module, id_pathid, order, lvl):
        value = (module.id, id_pathid, order, lvl)
        if value in self.__dict.inv:
            return self.__dict.inv[value]
        else:
            key = self.__counter.getNext()
            self.__dict[key] = value
            return key

    # Put for Modules module_id + -1 + 0 + 0  -  UNUSED
    #def putModule(self, module):
    #    values = self.__dict.values()
    #    new_gid = -3
    #    for key, value in self.__dict.iteritems():
    #        vals_list = value.split(",")
    #        id_mod = vals_list[0]
    #        if id_mod == module.id:
    #            new_gid = key
    #            break
    #    new_value = module.id, -1, 0, 0
    #    if new_gid == -3:
    #        key = self.__counter.getNext()
    #        self.__dict[key] = new_value
    #        return key
    #    else:
    #        return new_gid

    def get(self, key):
        if key in self.__dict:
            return self.__dict[key][0]
        else:
            return -2


class SequencesMapping(object):

    def __init__(self, counter):
        self.__counter = counter
        self.__dict = bidict.bidict()

    def put(self, sequence, id_pathid, order, lvl):
        value = (sequence.id, id_pathid, order, lvl)
        if value in self.__dict.inv:
            return self.__dict.inv[value]
        else:
            key = self.__counter.getNext()
            self.__dict[key] = value
            return key

    def get(self, key):
        if self.__dict[key]:
            return self.__dict[key][0]
        else:
            return -2
