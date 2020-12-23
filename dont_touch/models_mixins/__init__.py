from dont_touch.models_mixins.desserializer import Desserializer
from dont_touch.models_mixins.serializer import Serializer
from dont_touch.models_mixins.timestamper import TimeStamper

class BaseModel(TimeStamper, Serializer, Desserializer):
    pass