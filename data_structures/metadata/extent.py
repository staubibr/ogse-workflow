from data_structures.metadata.element import Element


class Extent(Element):
    @property
    def reference(self):
        return self.json["reference"]

    @property
    def x_min(self):
        return self.json["x min"]

    @property
    def x_max(self):
        return self.json["x max"]

    @property
    def y_min(self):
        return self.json["y min"]

    @property
    def y_max(self):
        return self.json["y max"]

    @y_max.setter
    def y_max(self, value):
        self.json["y max"] = value

    def initialize(self):
        self.validate_element("reference", True, False)
        self.validate_element("x min", True, False)
        self.validate_element("x max", True, False)
        self.validate_element("y min", True, False)
        self.validate_element("y max", True, False)
