from data_structures.metadata.element import Element


class SubModel(Element):
    @property
    def identifier(self):
        return self.json["identifier"]

    @property
    def model_type(self):
        return self.json["model type"]

    def validate(self):
        self.validate_element("identifier", True, False)
        self.validate_element("model type", True, False)
