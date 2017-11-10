class StCmdAnalyser:
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename) as f:
            self.contents = [line.replace('\n', '') for line in f]
        self.contents = [line for line in self.contents if line]

    @property
    def epics_env_sets(self):
        retval = dict()
        for line in self.contents:
            if not line.startswith('epicsEnvSet'):
                continue
            value_pair = self.parse_envset(line)
            retval[value_pair[0]] = value_pair[1]
        return retval

    @staticmethod
    def parse_envset(line):
        line = line.replace('epicsEnvSet(', '')
        line = line.replace('"', '')
        line = line.replace(')', '')
        pairs = line.split()
        return pairs
