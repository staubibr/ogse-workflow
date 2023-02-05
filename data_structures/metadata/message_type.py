from data_structures.metadata.element import Element
from data_structures.metadata.field import Field


class MessageType(Element):
    @property
    def identifier(self):
        return self.json["identifier"]

    @property
    def field(self):
        return self._field

    def __init__(self, json):
        super().__init__(json)
        self._field = [Field(j) for j in self.json["field"]]

    def initialize(self):
        self.validate_element("identifier", True, False)
        self.validate_element("field", True, True)
