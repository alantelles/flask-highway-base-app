from app import db
from datetime import datetime

class TimeStampMixin(object):
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), default=None, onupdate=datetime.now)
    deleted_at = db.Column(db.DateTime(), default=None)

class SerializeOutput(object):

    forbidden_fields = []
    remap = {}
    process_key = {}
    
    def serialize_list(query_return):
        out = []
        for entry in query_return:
            out.append(entry.to_json())
            
        
        return out

    def serialize(self, force_fields=[]):
        out = dict.copy(self.__dict__)
        if '_sa_instance_state' in out:
            del out['_sa_instance_state']
        print(self.forbidden_fields)
        for ff in self.forbidden_fields:
            if ff not in force_fields:
                if ff in out:
                    del out[ff]

        for key in dict.copy(out):
            # IMPORTANT: process happens before remap
            # Your process keys should always use original field names
            if key in self.process_key:            
                fn = self.process_key[key]
                out[key] = fn(out[key])


            if key in self.remap:
                out[self.remap[key]] = out[key]
                del out[key]

        return out

    def json_serialize_list(items):
        singles = [int, bool, str, float]
        out = []
        for entry in items:
            if type(entry) in singles:
                out.append(entry)

            elif type(entry) == list:
                out.append(SerializeOutput.json_serialize_list(entry))

            elif type(entry) == dict:
                out.append(SerializeOutput.json_serialize_dict(entry))

            else:
                out.append(str(entry))

        return out


    def json_serialize_dict(items):
        singles = [int, bool, str, float]
        out = {}    
        for entry in items:
            val = items[entry]
            if type(entry) in singles:
                out[entry] = val

            elif type(entry) == list:
                out[entry] = SerializeOutput.json_serialize_list(val)

            elif type(entry) == dict:
                out[entry] = SerializeOutput.json_serialize_dict(val)

            else:
                out[entry] = str(entry)

        return out
            


    def to_json(self, force_fields=[]):
        out = self.serialize(force_fields)
        dump = {}
        singles = [int, bool, str, float]
        for key in out:
            val = out[key]
            if val:
                if type(val) in singles:
                    dump[key] = val

                elif type(val) == list:
                    dump[key] = SerializeOutput.json_serialize_list(val)
                    
                elif type(val) == dict:
                    dump[key] = SerializeOutput.json_serialize_dict(val)

                else:
                    dump[key] = str(val)

            else:
                dump[key] = None

            
        return dump