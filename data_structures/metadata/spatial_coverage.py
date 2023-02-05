from data_structures.metadata.element import Element
from data_structures.metadata.extent import Extent


class SpatialCoverage(Element):
    @property
    def placename(self):
        return self.json["placename"]

    @property
    def extent(self):
        return self._extent

    def __init__(self, json):
        super().__init__(json)

        if "extent" in self.json and self.json["extent"] is not None:
            self._extent = [Extent(e) for e in self.json["extent"]]

    def initialize(self):
        self.validate_element("placename", False, True)
        self.validate_element("extent", False, True)
