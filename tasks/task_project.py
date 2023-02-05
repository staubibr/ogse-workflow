from components.task import Task, TaskParameters


class TaskProjectParams(TaskParameters):
    @property
    def srid(self):
        return self.json["srid"]

    def __init__(self, json):
        super().__init__(json)


class TaskProject(Task):

    def __init__(self, json):
        super().__init__(json)

    def execute(self, db):
        params = TaskProjectParams(self.params)

        if self.source is None:
            raise Exception("project task requires a source parameter.")

        db.execute("CREATE TABLE {0} AS (SELECT a.*, ST_Transform(geom, {1}) as proj_geom FROM {2} a)".format(self.output, params.srid, self.source))
        db.execute("ALTER TABLE {0} DROP COLUMN {1}".format(self.output, "geom"))
        db.execute("ALTER TABLE {0} RENAME COLUMN {1} TO {2}".format(self.output, "proj_geom", "geom"))

