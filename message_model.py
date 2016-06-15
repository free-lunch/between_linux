import json
import collections

class Message():
    def __init__(self, message):
        self.dict = collections.defaultdict()
        self.type = None
        self.nested_dict_iter(message, self.dict)
        self.type = self.__getType__()


    def nested_dict_iter(self, nested, d):
        for key, value in nested.iteritems():
            if isinstance(value, collections.Mapping):
                self.nested_dict_iter(value, d)
            elif isinstance(value, list):
                self.nested_dict_iter(value[0], d)
            else:
                if not key in d:
                    d[key] = value
                else:
                    # For duplicated key
                    if type(d[key]) == 'list':
                        d[key].append(value)
                    else:
                        d[key] = [d[key], value]

    def __getType__(self):
        if 'content' in self.dict:
            return 'MESSAGE'
        elif 'type' in self.dict:
            if 'T_STICKER_V2' in self.dict['type']:
                return 'STICKER'
        elif 'action' in self.dict:
            if self.dict['type'] == 'EA_MODIFY':
                return 'MODIFY'
        else :
            return 'UNKNOWN'


    def getType(self):
        return self.type

    def getValue(self, key):
        if key in self.dict:
            return self.dict[key]
        else:
            raise KeyError('Invalid key : ' + key)
