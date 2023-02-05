from data_structures.metadata.element import Element


class Coupling(Element):
    @property
    def from_model(self):
        return self.json["from model"]

    @property
    def from_port(self):
        return self.json["from port"]

    @property
    def to_model(self):
        return self.json["to model"]

    @property
    def to_port(self):
        return self.json["to port"]

    def validate(self):
        self.validate_element("from model", True, False)
        self.validate_element("from port", True, False)
        self.validate_element("to model", True, False)
        self.validate_element("to port", True, False)
