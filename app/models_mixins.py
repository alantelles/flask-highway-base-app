from app import db
from datetime import datetime

class TimeStampMixin(object):
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), default=None, onupdate=datetime.now)
    deleted_at = db.Column(db.DateTime(), default=None)

class SerializeOutput(object):

    forbidden_fields = []

    def serialize(self, force_fields=[]):
        out = dict.copy(self.__dict__)
        del out['_sa_instance_state']
        for ff in self.forbidden_fields:
            print(ff)
            if ff not in force_fields:
                del out[ff]

        return out

    def to_json(self, force_fields=[]):
        out = self.serialize(force_fields)
        dump = {}
        serializables = [int, bool, str, float, list, dict]
        for key in out:
            val = out[key]
            if val:
                if type(val) in serializables:
                    dump[key] = val

                else:
                    dump[key] = str(val)

            else:
                dump[key] = None

        return dump