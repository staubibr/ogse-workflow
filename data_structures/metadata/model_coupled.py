from datetime import datetime

from data_structures.metadata.coupling import Coupling
from data_structures.metadata.model_common import ModelCommon
from data_structures.metadata.submodel import SubModel


class ModelCoupled(ModelCommon):
    @property
    def submodel(self):
        return self._submodel

    @property
    def coupling(self):
        return self._coupling

    def __init__(self, json):
        super().__init__(json)

        if "submodel" in self.json and self.json["submodel"] is not None:
            self._submodel = [SubModel(sm) for sm in self.json["submodel"]]

        if "coupling" in self.json and self.json["coupling"] is not None:
            self._coupling = [Coupling(c) for c in self.json["coupling"]]

    def initialize(self):
        super().initialize()
        self.validate_element("submodel", False, True)
        self.validate_element("coupling", False, True)
