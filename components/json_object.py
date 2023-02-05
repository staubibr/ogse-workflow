class JsonObject:
    @property
    def json(self):
        return self._json

    @json.setter
    def json(self, value):
        self._json = value

    def __init__(self, json):
        super().__init__()
        self.json = json

    def to_json(self):
        return self.json
