import json

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