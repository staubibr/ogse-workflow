import decimal

from components.json_object import JsonObject
from util import tools


class ModelSet(JsonObject):
    @property
    def id(self):
        return self.json["id"]

    @property
    def type(self):
        return self.json["type"]

    @property
    def table(self):
        return self.json["table"]

    @property
    def properties(self):
        return self.json["properties"]

    @property
    def models(self):
        return self._models

    @models.setter
    def models(self, value):
        self._models = value

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

    def __init__(self, json):
        super().__init__(json)
        self._models = None
        self._index = {}

    def build(self, db):
        self.models = db.select("SELECT id, {0} FROM {1}.{2};".format(",".join(self.properties), db.schema, self.table))
        self.models = tools.traverse(self.models, lambda v: float(v) if isinstance(v, decimal.Decimal) else v)
        self.index = {m[0]: m for m in self.models}

    def set_cadmium_index(self, start):
        self.properties.insert(0, "cadmium_id")

        for m in self.models:
            m[0] = str(start)
            start = start + 1

        return start

    def to_json(self):
        return {
            "id": self.id,
            "type": self.type,
            "properties": self.properties,
            "models": self.models,
        }
