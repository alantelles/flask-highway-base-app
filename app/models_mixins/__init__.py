from app.models_mixins.desserializer import Desserializer
from app.models_mixins.serializer import Serializer
from app.models_mixins.timestamper import TimeStamper

class BaseModel(TimeStamper, Serializer, Desserializer):
    pass