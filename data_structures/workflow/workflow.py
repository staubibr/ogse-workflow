import json
import os
from datetime import datetime

from components.factory import Factory
from components.logger import Logger
from components.json_object import JsonObject
from data_structures.metadata.model_atomic import ModelAtomic
from data_structures.metadata.model_coupled import ModelCoupled
from data_structures.scenario.scenario import Scenario
from util import tools


# TODO: SQL Injection (https://stackoverflow.com/questions/45128902/psycopg2-and-sql-injection-security)
# TODO: Error messaging and user feedback when wrong types in Cadmium
class Workflow(JsonObject):
    @property
    def metadata(self):
        return self.json["metadata"]

    @property
    def scenario(self):
        return self._scenario

    @scenario.setter
    def scenario(self, value):
        self._scenario = value

    @property
    def tasks(self):
        return self.json["tasks"]

    def __init__(self, json):
        super().__init__(json)

        self.scenario = Scenario(self.json["scenario"])

    def execute(self, db, experiment):
        Logger.info('Preparing workflow metadata for resulting coupled model...')
        self.metadata["identifier"] = db.schema
        self.metadata["creator"] = ["OGSE workflow engine"]
        self.metadata["created"] = datetime.today().strftime('%Y-%m-%d')

        Logger.info('Preparing tasks: injecting parameters, fix outputs, replacing steps...')
        for i, task in enumerate(self.tasks):
            task = tools.replace_tags(task, "@experiment", lambda v: tools.get_value(experiment, v.split(".")))
            task = tools.replace_tags(task, "@step", lambda v: self.tasks[int(v) - 1].output)

            self.tasks[i] = Factory.get_task(task)
            self.tasks[i].output = "step_{0}".format(i + 1) if self.tasks[i].output is None else self.tasks[i].output
            self.tasks[i].output = "{0}.{1}".format(db.schema, self.tasks[i].output)

        for t in self.tasks:
            Logger.info('Processing task {0}...'.format(t.name))
            t.execute(db)

        Logger.info('Cleaning up temporary tables...')
        for t in self.tasks:
            if t.is_temp:
                db.execute("DROP TABLE {0} CASCADE".format(t.output))

        Logger.info('Workflow execution done.')

    def get_full_metadata(self, lom_path):
        types = [ModelAtomic.from_library(lom_path, i_set.type).to_json() for i_set in self.scenario.model_sets]
        types.insert(0, ModelCoupled(self.metadata).to_json())

        return types;

    def write_metadata(self, lom_path, output):
        Logger.info('Assembling metadata for coupled model...')
        metadata = self.get_full_metadata(lom_path)

        Logger.info('Writing metadata file to disk...')
        with open(os.path.join(output, "metadata.json"), "w", encoding="utf8") as f:
            f.write(json.dumps(metadata))
