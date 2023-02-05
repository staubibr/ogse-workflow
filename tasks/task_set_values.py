from components.task import TaskParameters, LoopTask


class TaskSetValuesParams(TaskParameters):
    @property
    def column(self):
        return self.json["column"]

    @property
    def value(self):
        return self.json["value"]

    @property
    def use_quotes(self):
        return self.json["use_quotes"]

    @property
    def where(self):
        return "WHERE {0} = {1}".format(self.json["where"]["field"], self.json["where"]["value"]) if "where" in self.json else ""

    def __init__(self, json):
        super().__init__(json)


class TaskSetValues(LoopTask):

    def __init__(self, json):
        super().__init__(json)

    def get_sql_value(self, v):
        return "'%s'" % v if isinstance(v, str) else "%s" % str(v)

    def get_sql_array(self, values):
        value = ",".join([self.get_sql_value(v) for v in values])

        return "'{%s}'" % value

    def execute(self, db):
        params = [TaskSetValuesParams(p) for p in self.params]

        if self.source is None:
            raise Exception("project task requires a source parameter.")

        db.execute("CREATE TABLE {0} AS SELECT * FROM {1}".format(self.output, self.source))

        for p in params:
            if isinstance(p.value, list):
                value = self.get_sql_array(p.value)
            else:
                value = self.get_sql_value(p.value)

            db.execute("UPDATE {0} SET {1} = {2} {3}".format(self.output, p.column, value, p.where))
