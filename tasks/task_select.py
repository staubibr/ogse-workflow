from components.task import Task, TaskParameters


class TaskSelectParams(TaskParameters):

    @property
    def where(self):
        """Object with criteria {field1: value1, field2: value2, etc} is returned as a single where clause."""
        w = []

        for key, value in self.json["where"].items():
            w.append(f"{key}='{value}'")  # postgres is matching numbers with or without quotes

        return " AND ".join(w)

    def __init__(self, json):
        super().__init__(json)


class TaskSelect(Task):
    """Executes a select statement and saves the results to a temporary table.

    Example:
    {
        "name": "select",
        "source": "alberta_csd_4326",
        "params": {
            "where": {
                "csduid": "@experiment:csduid"
            }
    }
    """

    def __init__(self, json):
        super().__init__(json)

    def execute(self, db):
        params = TaskSelectParams(self.params)

        if self.source is None:
            raise Exception("Select task requires a source parameter.")

        db.execute("CREATE TABLE {0} AS (SELECT * FROM {1} WHERE {2})".format(self.output, self.source, params.where))
