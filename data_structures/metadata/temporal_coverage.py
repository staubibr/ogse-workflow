from data_structures.metadata.element import Element


class TemporalCoverage(Element):
    @property
    def start(self):
        return self.json["start"]

    @property
    def end(self):
        return self.json["end"]

    @property
    def scheme(self):
        return self.json["scheme"]

    def initialize(self):
        self.validate_element("start", True, False)
        self.validate_element("end", True, False)
        self.validate_element("scheme", True, False)
