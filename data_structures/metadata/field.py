from data_structures.metadata.element import Element


class Field(Element):
    @property
    def name(self):
        return self.json["name"]

    @property
    def description(self):
        return self.json["description"]

    @property
    def type(self):
        return self.json["type"]

    @property
    def uom(self):
        return self.json["uom"]

    @property
    def scalar(self):
        return self.json["scalar"]

    def initialize(self):
        self.validate_element("name", True, False)
        self.validate_element("description", False, False)
        self.validate_element("type", True, False, ["nominal", "numerical", "ordinal"])
        self.validate_element("uom", False, False)
        self.validate_element("scalar", False, False)
