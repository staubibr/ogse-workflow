from components.task import TaskParameters, LoopTask


class TaskRingParams(TaskParameters):
    @property
    def id(self):
        return self.json["id"]

    @property
    def min(self):
        return self.json["min"]

    @property
    def max(self):
        return self.json["max"]

    def __init__(self, json):
        super().__init__(json)


class TaskRing(LoopTask):

    def __init__(self, json):
        super().__init__(json)

    def execute(self, db):
        params = [TaskRingParams(p) for p in self.params]

        if self.source is None:
            raise Exception("project task requires a source parameter.")

        db.execute("CREATE TABLE {0} AS SELECT a.*, ST_Difference(ST_Buffer(a.geom, {1}), ST_Buffer(a.geom, {2})) AS ring_geom FROM {3} a".format(self.output, params[0].max, params[0].min, self.source))
        db.execute("ALTER TABLE {0} ADD COLUMN ring_id SERIAL PRIMARY KEY;".format(self.output))

        for p in params[1:]:
            db.execute("INSERT INTO {0} SELECT a.*, ST_Difference(ST_Buffer(a.geom, {1}), ST_Buffer(a.geom, {2})) AS ring_geom FROM {3} a".format(self.output, p.max, p.min, self.source))

        db.execute("ALTER TABLE {0} DROP COLUMN {1}".format(self.output, "geom"))
        db.execute("ALTER TABLE {0} RENAME COLUMN {1} TO {2}".format(self.output, "ring_geom", "geom"))
        db.execute("ALTER TABLE {0} DROP COLUMN {1}".format(self.output, "id"))
        db.execute("ALTER TABLE {0} RENAME COLUMN {1} TO {2}".format(self.output, "ring_id", "id"))
