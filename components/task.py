from components.json_object import JsonObject
from util import tools
from components.logger import Logger


class TaskParameters(JsonObject):
    def __init__(self, json):
        super().__init__(json)

    def __iter__(self):
        return self


class Task(JsonObject):
    @property
    def name(self):
        return self.json["name"]

    @property
    def loop(self):
        return self.json["loop"] if "loop" in self.json else None

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, value):
        self._params = value

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, value):
        self._output = value

    @property
    def is_temp(self):
        return "output" not in self.json

    @property
    def source(self):
        return self.json["source"] if "source" in self.json else None

    @source.setter
    def source(self, value):
        self.json["source"] = value

    def __init__(self, json):
        super().__init__(json)
        self.output = json["output"] if "output" in json else None
        self.params = json["params"] if "params" in json else None

    def execute(self, db):
        raise Exception("process function not implemented for task {0}.".format(self.name))


class LoopTask(Task):
    def __init__(self, json):
        super().__init__(json)

        if self.loop is None:
            self.params = [self.params]
        else:
            Logger.info('Injecting looped experiment parameters...')
            self.params = [tools.replace_tags(self.params, "@iterator", lambda v: tools.get_value(l, v.split("."))) for l in self.loop]
