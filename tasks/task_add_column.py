from components.task import TaskParameters, LoopTask


class TaskAddColumnsParams(TaskParameters):
    @property
    def name(self):
        return self.json["name"]

    @property
    def type(self):
        return self.json["type"]

    def __init__(self, json):
        super().__init__(json)


class TaskAddColumns(LoopTask):

    def __init__(self, json):
        super().__init__(json)

    def execute(self, db):
        params = [TaskAddColumnsParams(p) for p in self.params]

        if self.source is None:
            raise Exception("project task requires a source parameter.")

        db.execute("CREATE TABLE {0} AS SELECT * FROM {1}".format(self.output, self.source))

        for p in params:
            db.execute("ALTER TABLE {0} ADD COLUMN {1} {2}".format(self.output, p.name, p.type))
