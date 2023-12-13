"""Schema for serializing/deserializing a EventsModel"""

from data.events.models.events_model import EventsModel
from shared.utils.schema.base_schema import BaseSchema


class EventsSchema(BaseSchema):
    class Meta:
        model = EventsModel
        load_instance = True
