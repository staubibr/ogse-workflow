from data_structures.metadata.element import Element


class Port(Element):
    @property
    def type(self):
        return self.json["type"]

    @property
    def name(self):
        return self.json["name"]

    @property
    def message_type(self):
        return self.json["message type"]

    @message_type.setter
    def message_type(self, value):
        self.json["message type"] = value

    def initialize(self):
        self.validate_element("type", True, False, ["input", "output"])
        self.validate_element("name", True, False)
        self.validate_element("message type", True, False)
