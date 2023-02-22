from tasks.task_add_column import TaskAddColumns
from tasks.task_intersection import TaskIntersection
from tasks.task_within import TaskWithin
from tasks.task_project import TaskProject
from tasks.task_ring import TaskRing
from tasks.task_set_values import TaskSetValues
from tasks.task_make_point import TaskMakePoint
from tasks.task_union import TaskUnion
from tasks.task_centroid import TaskCentroid
from tasks.task_closest import TaskClosest


class Factory:
    tasks = {}

    @staticmethod
    def register(name, task):
        if name in Factory.tasks:
            raise Exception("A task with the name {0} is already registered with the factory.".format(name))

        Factory.tasks[name] = task

    @staticmethod
    def get_task(json):
        if "name" not in json:
            raise Exception("Factory cannot instantiate task, no task name was provided.")

        return Factory.tasks[json["name"]](json)


Factory.register("project", TaskProject)
Factory.register("ring", TaskRing)
Factory.register("add_column", TaskAddColumns)
Factory.register("set_values", TaskSetValues)
Factory.register("intersection", TaskIntersection)
Factory.register("within", TaskWithin)
Factory.register("make_point", TaskMakePoint)
Factory.register("union", TaskUnion)
Factory.register("centroid", TaskCentroid)
Factory.register("closest", TaskClosest)
