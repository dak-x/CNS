import json
class DB:
    def __init__(self, filename):
        with open(filename, 'r') as fp:
            self.database = dict(json.load(fp))

    def fetch_record(self, name):
        return self.database.get(name,-1)

    def fetch_fields(self,name,fields):
        record = self.fetch_record(name)
        ans=[]
        if(record==-1):
            return ans
        for field in fields:
            ans.append(self.database[name].get(field,None))
        return ans



    