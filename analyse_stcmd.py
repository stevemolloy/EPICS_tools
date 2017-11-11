from pathlib import PurePath
from collections import defaultdict
import re


class StCmdAnalyser:
    regex = r"([\w-]+)\=(\w*)(\$\(\w+\))?(.*)"

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
        return [line
                for line in self.contents
                if line.startswith('dbLoadRecords')]

    @property
    def templates(self):
        template_dict = defaultdict(list)
        for line in self.dbloadrecord_cmds:
            fname = self.filename_from_command(line)
            substitutions = self.substitutions_from_command(line)
            template_dict[fname].append(substitutions)
        return template_dict

    @staticmethod
    def filename_from_command(cmd_str):
        cmd_str = cmd_str.replace('dbLoadRecords("', '')
        path = PurePath(cmd_str.split('"')[0])
        return path.as_posix()

    def substitutions_from_command(self, cmd_str):
        inval = cmd_str.split('"')[-2]
        return self.parse_substitutions(inval.replace(',', '\n'))

    def parse_substitutions(self, subs):
        matches = re.finditer(self.regex, subs)

        retval = dict()
        for match in matches:
            val = ''
            if match.group(2):
                val += match.group(2)
            if match.group(3):
                val += self.epics_env_vars[match.group(3)[2:-1]]
            if match.group(4):
                val += match.group(4)
            retval[match.group(1)] = val

        return retval
