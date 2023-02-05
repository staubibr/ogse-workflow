from components.task import LoopTask, TaskParameters


class TaskMakePointParams(TaskParameters):
    @property
    def point(self):
        return self.json["point"]

    @property
    def attributes(self):
        return self.json["attributes"]

    def __init__(self, json):
        super().__init__(json)


class TaskMakePoint(LoopTask):

    def execute(self, db):
        params = [TaskMakePointParams(p) for p in self.params]

        if self.source is None:
            db.execute("CREATE TABLE {0} (id serial, geom geometry(Point, 4326))".format(self.output))
            values = ["(ST_GeomFromText('POINT({0} {1})', 4326))".format(p.point[0], p.point[1]) for p in params]
            db.execute("INSERT INTO {0} (geom) VALUES {1}".format(self.output, ",".join(values)))

        # TODO: Needs to be tested, this should send a single request with all points to create instead of multiple requests
        else:
            db.execute("CREATE TABLE {0} AS SELECT * FROM {1}".format(self.output, self.source))

            for p in params:
                columns = [k for k in p.attributes] + ["geom"]
                geom = "(ST_GeomFromText('POINT(%f %f)', 4326))".format(p.point[0], p.point[1])
                values = [v for k, v in p.attributes.items()] + [geom]
                db.execute("INSERT INTO {0} ({1}) VALUES {2}".format(self.output, ",".join(columns), ",".join(values)))
