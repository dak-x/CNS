import json
class DB:
    def __init__(self, filename):
        with open(filename, 'r') as fp:
            self.database = dict(json.load(fp))
            self.cache = []
            self.cache_dict = dict()

    def fetch_record(self, name):
        return self.database.get(name,-1)

    def fetch_fields(self,name,fields,cacheFlag=False):
        name = name.lower()
        if(cacheFlag and (name in self.cache)):
            print('Returned from Cache!!')
            record = self.cache_dict.get(name)
        else:
            record = self.fetch_record(name)
        ans=[]
        if(record==-1):
            return -1
        if(len(self.cache)==4):
            del self.cache_dict[self.cache[0]]
            self.cache.pop(0)
        if(name not in self.cache):
            self.cache.append(name)
            self.cache_dict[name] = record
        print('Cache Status:', self.cache)
        for field in fields:
            ans.append(self.database[name].get(field,''))
        return ans



    