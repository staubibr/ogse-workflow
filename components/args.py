import os
from argparse import ArgumentParser, ArgumentTypeError


class Args:
    @property
    def workflow(self):
        return self.args.workflow

    @property
    def output(self):
        return self.args.output

    @property
    def experiment(self):
        return self.args.experiment

    def validate(self):
        if not os.path.isdir(self.output):
            raise ArgumentTypeError("output path provided (%s) is not a folder." % self.output)
        if not os.access(self.output, os.W_OK):
            raise ArgumentTypeError("output path provided (%s) is not accessible." % self.output)
        if not os.path.exists(self.output):
            raise ArgumentTypeError("output path provided (%s) does not exist." % self.output)
        if not os.path.exists(self.workflow):
            raise ArgumentTypeError("workflow file provided (%s) does not exist." % self.workflow)
        if not os.path.exists(self.experiment):
            raise ArgumentTypeError("file provided (%s) does not exist." % self.experiment)

    def __init__(self):
        parser = ArgumentParser(description='This script executes a spatial analysis workflow to generate instances sets and relations sets from geojson data.')
        parser.add_argument('--experiment', dest='experiment', type=str, help='Path to the experiment file', required=False)
        parser.add_argument('--workflow', dest='workflow', type=str, help='Path to the workflow configuration file', required=True)
        parser.add_argument('--output', dest='output', type=str, help='Path to the output folder', required=True)

        self.args = parser.parse_args()
        self.validate()
