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

Logger.info('Connecting to database...')
db.connect("service", "service", "postgres", "localhost", "5432")

Logger.info('Creating database schema...')
db.execute("CREATE SCHEMA {0}".format(db.schema))

try:
    workflow = Workflow(j_workflow)
    workflow.execute(db, j_experiment)
    workflow.scenario.build(db)

except Exception as ex:
    Logger.error(str(ex))
    db.rollback()
    Logger.info('Dropping database schema...')
    db.execute("DROP SCHEMA {0} CASCADE".format(db.schema))
    raise ex

finally:
    # db.execute("DROP SCHEMA {0} CASCADE".format(db.schema))
    db.close()

# Writing to sample.json
workflow.scenario.write(args.output)

# TODO: Maybe OGSE should have a common config file to hold these folders.
workflow.write_metadata("D:\\4. Development\\ogse-files\\models\\", args.output)

Logger.info('Workflow execution done.')
