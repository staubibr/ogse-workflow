from components.task import Task, TaskParameters


class TaskCentroidParams(TaskParameters):

    def __init__(self, json):
        super().__init__(json)


class TaskCentroid(Task):

    def __init__(self, json):
        super().__init__(json)

    def execute(self, db):
        params = TaskCentroidParams(self.params)

        if self.source is None:
            raise Exception("centroid task requires a source parameter.")

        db.execute("CREATE TABLE {0} AS SELECT a.*, ST_Centroid(a.geom) as centroid FROM {1} a".format(self.output, self.source))

        db.execute("ALTER TABLE {0} DROP COLUMN {1}".format(self.output, "geom"))
        db.execute("ALTER TABLE {0} RENAME COLUMN {1} TO {2}".format(self.output, "centroid", "geom"))
