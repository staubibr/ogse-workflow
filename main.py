import json
import os

from components.args import Args
from components.db import DB
from components.logger import Logger
from data_structures.workflow.workflow import Workflow


# TODO: All task queries must be done with safe queries (use %s instead of {0})

args = Args()

# for path in os.listdir(args.output):
#    if os.path.isfile(os.path.join(args.output, path)):
#        os.remove(os.path.join(args.output, path))

Logger.init("ogse-workflow", os.path.join(args.output, "log.log"))

Logger.info('Reading workflow file ({0})...'.format(args.workflow))
f_workflow = open(args.workflow, 'r')
j_workflow = json.load(f_workflow)
f_workflow.close()

Logger.info('Reading experiment file ({0})...'.format(args.experiment))
f_experiment = open(args.experiment, 'r')
j_experiment = json.load(f_experiment)
f_experiment.close()

db = DB()

db.connect("service", "service", "postgres", "localhost", "5432")

try:
    workflow = Workflow(j_workflow)
    workflow.execute(db, j_experiment)
    workflow.scenario.build(db)

except Exception as ex:
    db.rollback()
    db.close()

    Logger.error(str(ex))
    raise ex

workflow.write_geojson(args.output, db)
workflow.write_scenario(args.output)
workflow.write_metadata("D:\\4. Development\\ogse-files\\models\\", args.output)
db.close()

Logger.info('Workflow execution done.')
