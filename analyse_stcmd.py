from pathlib import PurePath
from collections import defaultdict


class StCmdAnalyser:
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename) as f:
            self.contents = [line.replace('\n', '') for line in f]
        self.contents = [line for line in self.contents if line]

    @property
    def epics_env_vars(self):
        retval = dict()
        for line in self.contents:
            if not line.startswith('epicsEnvSet'):
                continue
            value_pair = self.parse_envset(line)
            retval[value_pair[0].replace(',', '')] = value_pair[1]
        return retval

    @staticmethod
    def parse_envset(line):
        line = line.replace('epicsEnvSet(', '')
        line = line.replace('"', '')
        line = line.replace(')', '')
        pairs = line.split()
        return pairs
    
    @property
    def dbloadrecord_cmds(self):
        return [line for line in self.contents if line.startswith('dbLoadRecords')]

    @property
    def templates(self):
        template_dict = defaultdict(list)
        for line in self.dbloadrecord_cmds:
            template_dict[self.filename_from_command(line)].append(self.substring_from_command(line))
        return template_dict

    @staticmethod
    def filename_from_command(cmd_str):
        cmd_str = cmd_str.replace('dbLoadRecords("', '')
        path = PurePath(cmd_str.split('"')[0])
        return path.as_posix()

    def substring_from_command(self, cmd_str):
        retval = dict()
        substitute_str = cmd_str.split('"')[-2]
        for item in substitute_str.replace(',', ' ').split():
            pair = item.split('=')
            if len(pair) == 1:
                pair.append('')
            pair[1] = pair[1].replace('$(', '').replace(')', '')
            try:
                retval[pair[0]] = self.epics_env_vars[pair[1]]
            except KeyError:
                retval[pair[0]] = pair[1]
        return retval
