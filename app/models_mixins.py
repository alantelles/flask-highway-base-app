from app import db
from datetime import datetime
import json

class TimeStampMixin(object):
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), default=None, onupdate=datetime.now)
    deleted_at = db.Column(db.DateTime(), default=None)
    
class Desserializer(object):
    # class name should change to
    # Desserializer
    
    accept_only = []
    remap_input = {}
    process_input_key = {}
    
    def from_json(self, body, force_accept=[]):
        body = json.loads(body)
        for key in dict.copy(body):
            if len(self.accept_only):
                if key not in self.accept_only and key not in force_accept:
                    del body[key]
        
            if key in self.remap_input:
                new = self.remap_input[key]
                
                if key in body:
                    body[new] = body[key]
                    del body[key]
               
        for key in body:
            if key in self.process_input_key:
                fn = self.process_input_key[key]
                body[key] = fn(body[key])
        
        for key in body:    
            setattr(self, key, body[key])
        

class Serializer(object):
    # class name should change to 
    # Serializer

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
                out.append(Serializer.json_serialize_list(entry))

            elif type(entry) == dict:
                out.append(Serializer.json_serialize_dict(entry))

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
                out[entry] = Serializer.json_serialize_list(val)

            elif type(entry) == dict:
                out[entry] = Serializer.json_serialize_dict(val)

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
                    dump[key] = Serializer.json_serialize_list(val)
                    
                elif type(val) == dict:
                    dump[key] = Serializer.json_serialize_dict(val)

                else:
                    dump[key] = str(val)

            else:
                dump[key] = None

            
        return dump

class BaseModel(TimeStampMixin, Serializer, Desserializer):
    pass