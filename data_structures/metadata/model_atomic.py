import json
import os

from data_structures.metadata.model_common import ModelCommon
from data_structures.metadata.state import State


class ModelAtomic(ModelCommon):
    @property
    def time(self):
        return self.json["time"]

    @property
    def state(self):
        return self._state

    def __init__(self, json):
        super().__init__(json)

        if "state" in self.json and self.json["state"] is not None:
            self._state = State(self.json["state"])

    def initialize(self):
        super().initialize()
        self.validate_element("time", True, False)
        self.validate_element("state", False, False)

    @staticmethod
    def from_library(path, uuid):
        if not os.path.exists(os.path.join(path, uuid, "model.json")):
            raise Exception("Missing file: model metadata file {0} is missing.".format(uuid))

        f_metadata = open(os.path.join(path, uuid, "model.json"), 'r')
        j_metadata = json.load(f_metadata)
        f_metadata.close()

        return ModelAtomic(j_metadata)
