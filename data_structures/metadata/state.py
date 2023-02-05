from data_structures.metadata.element import Element


class State(Element):
    @property
    def description(self):
        return self.json["description"]

    @property
    def message_type(self):
        return self.json["message type"]

    def initialize(self):
        self.validate_element("description", False, False)
        self.validate_element("message type", True, False)
