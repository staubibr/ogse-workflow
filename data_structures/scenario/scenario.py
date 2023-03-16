import json
import os

from components.json_object import JsonObject
from components.logger import Logger
from data_structures.scenario.coupling_set import CouplingSet
from data_structures.scenario.model_set import ModelSet


class Scenario(JsonObject):
    @property
    def model_sets(self):
        return self._models

    @model_sets.setter
    def model_sets(self, value):
        self._models = value

    @property
    def coupling_sets(self):
        return self._couplings

    @coupling_sets.setter
    def coupling_sets(self, value):
        self._couplings = value

    def __init__(self, json):
        super().__init__(json)

        self.model_sets = [ModelSet(i) for i in self.json["models"]] if "models" in self.json else None
        self.coupling_sets = [CouplingSet(c) for c in self.json["couplings"]] if "couplings" in self.json else None

    def build(self, db):
        Logger.info('Building scenario file from workflow results...')
        cadmium_id = 1
        index = {m_set.id: m_set for m_set in self.model_sets}

        Logger.info('Building instance sets...')
        for i_set in self.model_sets:
            i_set.build(db)

        Logger.info('Building couplings sets...')
        for c_set in self.coupling_sets:
            c_set.build(db, index)

        # id = 0

        Logger.info('Preparing instances and couplings for Cadmium...')
        for i_set in self.model_sets:
            i_set.properties.insert(0, "cadmium_id")

            # cadmium needs the id to be a string.
            for m in i_set.models:
                # id = id + 1
                m[0] = str(m[0])
                # m[0] = str(id)

            # cadmium_id = i_set.set_cadmium_index(cadmium_id)

        Logger.info('Scenario preparation done.')

    def to_json(self):
        return {
            "instances": [i_set.to_json() for i_set in self.model_sets],
            "couplings": [c_set.to_json() for c_set in self.coupling_sets],
        }
