from data_structures.metadata.element import Element
from data_structures.metadata.spatial_coverage import SpatialCoverage
from data_structures.metadata.temporal_coverage import TemporalCoverage


class ModelDCMI(Element):
    @property
    def identifier(self):
        return self.json["identifier"]

    @property
    def title(self):
        return self.json["title"]

    @property
    def alternative(self):
        return self.json["alternative"]

    @property
    def creator(self):
        return self.json["creator"]

    @property
    def contributor(self):
        return self.json["contributor"]

    @property
    def language(self):
        return self.json["language"]

    @property
    def description(self):
        return self.json["description"]

    @property
    def subject(self):
        return self.json["subject"]

    @property
    def spatial_coverage(self):
        return self._spatial_coverage

    @property
    def temporal_coverage(self):
        return self._temporal_coverage

    @property
    def license(self):
        return self.json["license"]

    @property
    def created(self):
        return self.json["created"]

    @property
    def modified(self):
        return self.json["modified"]

    def __init__(self, json):
        super().__init__(json)

        if "spatial coverage" in self.json and self.json["spatial coverage"] is not None:
            self._spatial_coverage = [SpatialCoverage(sc) for sc in self.json["spatial coverage"]]

        if "temporal coverage" in self.json and self.json["temporal coverage"] is not None:
            self._temporal_coverage = [TemporalCoverage(tc) for tc in self.json["temporal coverage"]]

    def initialize(self):
        self.validate_element("identifier", True, False)
        self.validate_element("title", True, False)
        self.validate_element("alternative", False, True)
        self.validate_element("creator", False, True)
        self.validate_element("contributor", False, True)
        self.validate_element("language", False, True)
        self.validate_element("description", False, False)
        self.validate_element("subject", False, True)
        self.validate_element("spatial coverage", False, True)
        self.validate_element("temporal coverage", False, True)
        self.validate_element("license", False, True)
        self.validate_element("created", True, False)
        self.validate_element("modified", False, True)
