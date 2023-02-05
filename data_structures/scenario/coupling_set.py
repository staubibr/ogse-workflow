from components.json_object import JsonObject


class CouplingSet(JsonObject):
    @property
    def table(self):
        return self.json["table"]

    @property
    def from_field(self):
        return self.json["from"]["field"]

    @property
    def from_model(self):
        return self.json["from"]["model"]

    @property
    def from_port(self):
        return self.json["from"]["port"]

    @property
    def to_field(self):
        return self.json["to"]["field"]

    @property
    def to_model(self):
        return self.json["to"]["model"]

    @property
    def to_port(self):
        return self.json["to"]["port"]

    @property
    def links(self):
        return self._links

    @links.setter
    def links(self, value):
        self._links = value

    def __init__(self, json):
        super().__init__(json)
        self._links = None

    def build(self, db, index):
        self.links = db.select("SELECT {0},{1} FROM {2}.{3};".format(self.from_field, self.to_field, db.schema, self.table))
        self.links = [list(l) for l in self.links]

        for c in self.links:
            c[0] = index[self.from_model].index[c[0]]
            c[1] = index[self.to_model].index[c[1]]

    def to_json(self):
        return {
            "from_model": self.from_model,
            "from_port": self.from_port,
            "to_model": self.to_model,
            "to_port": self.to_port,
            "couplings": [[c[0][0], c[1][0]] for c in self.links]
        }