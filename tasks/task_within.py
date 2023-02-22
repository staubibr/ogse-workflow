from components.task import Task, TaskParameters


class TaskWithinParams(TaskParameters):
    @property
    def table(self):
        return self.json["table"]

    @property
    def join_field(self):
        return self.json["join_field"]

    def __init__(self, json):
        super().__init__(json)


class TaskWithin(Task):

    def __init__(self, json):
        super().__init__(json)

    def execute(self, db):
        params = TaskWithinParams(self.params)

        if self.source is None:
            raise Exception("within task requires a source parameter.")

        db.execute("CREATE TABLE {0} AS (SELECT DISTINCT ON (a.id) a.*, b.id as {1} FROM {2} a, {3} b WHERE ST_Within(a.geom, b.geom))".format(self.output, params.join_field, self.source, params.table))
