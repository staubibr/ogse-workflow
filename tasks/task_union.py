from components.task import TaskParameters, Task

class TaskUnionParams(TaskParameters):
    @property
    def where(self):
        if "where" not in self.json:
            return ""

        return "WHERE {0} IN ({1})".format(self.json["where"]["field"], ",".join(self.json["where"]["value"]))

    def __init__(self, json):
        super().__init__(json)


class TaskUnion(Task):

    def __init__(self, json):
        super().__init__(json)

    def execute(self, db):
        params = TaskUnionParams(self.params)

        if self.source is None:
            raise Exception("project task requires a source parameter.")

        db.execute("CREATE TABLE {0} AS SELECT ST_Union(geom) AS geom FROM {1} {2} ".format(self.output, self.source, params.where))
        db.execute("ALTER TABLE {0} ADD COLUMN id SERIAL PRIMARY KEY;".format(self.output))
