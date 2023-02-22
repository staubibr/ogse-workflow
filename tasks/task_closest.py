from components.task import Task, TaskParameters


class TaskClosestParams(TaskParameters):
    @property
    def table(self):
        return self.json["table"]

    @property
    def n(self):
        return self.json["n"]

    @property
    def field(self):
        return self.json["field"]

    def __init__(self, json):
        super().__init__(json)


class TaskClosest(Task):

    def __init__(self, json):
        super().__init__(json)

    def execute(self, db):
        params = TaskClosestParams(self.params)

        if self.source is None:
            raise Exception("closest task requires a source parameter.")



        # Build n to n table temporarily
        query = "SELECT a.id, b.id FROM {0} AS a CROSS JOIN LATERAL (SELECT id FROM {1} ORDER BY geom <-> a.geom limit {2}) AS b;"
        closest = db.select(query.format(self.source, params.table, params.n))

        # grab all records from n to n table
        # links = db.select("SELECT id, {0} FROM {1}.{2};".format(",".join(self.properties), db.schema, self.table))

        # copy table with empty fields
        fields = ["CAST(null AS numeric) AS {0}_{1}".format(params.field, i) for i in range(1, params.n + 1)]
        db.execute("CREATE TABLE {0} AS SELECT a.*, {1} FROM {2} a".format(self.output, ",".join(fields), self.source))

        i = 0

        while i < len(closest):
            values = ["{0}_{1}={2}".format(params.field, j % params.n + 1, closest[j][1]) for j in range(i, i + 3)]
            db.execute("UPDATE {0} SET {1} WHERE id = {2};".format(self.output, ",".join(values), closest[i][0]))
            i += 3


