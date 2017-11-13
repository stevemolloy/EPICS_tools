from pathlib import PurePath
from collections import defaultdict
import re


class StCmdAnalyser:
    verbose_regex = r"""
        ([\w-]+)        # Group #1. LHS of equality. Alphanums + "_" + "-"
        \=              # The  equals sign
        ([\w-]*)        # Group #2. Any chars prefixing an env var substitution
        (\$\([\w-]+\))? # Group #3. An env var substitution. e.g. $(PORT)
        (.*)            # Group #4. Any chars suffixing an env var substitution
    """

    def __init__(self, filename):
        with open(filename) as f:
            self.contents = [line.replace('\n', '') for line in f]
        self.contents = [line for line in self.contents if line]
        self.epics_env_vars = self.get_epics_env_vars()
        self.dbloadrecord_cmds = self.get_dbloadrecord_cmds()

    def get_epics_env_vars(self):
        retval = dict()
        for line in self.contents:
            if not line.startswith('epicsEnvSet'):
                continue
            value_pair = self.parse_envset(line)
            retval[value_pair[0].replace(',', '')] = value_pair[1]
        return retval

    @staticmethod
    def parse_envset(line):
        line = re.sub(r'(epicsEnvSet\(|"|\))', '', line)
        return line.split()

    def get_dbloadrecord_cmds(self):
        return [line
                for line in self.contents
                if line.startswith('dbLoadRecords')]

    @property
    def template_dict(self):
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
        matches = re.finditer(self.verbose_regex, subs, re.VERBOSE)

        retval = dict()
        for match in matches:
            val = ''
            prefix, subst, suffix = match.group(2), match.group(3), match.group(4)
            if prefix:
                val += prefix
            if subst:
                val += self.epics_env_vars[subst[2:-1]]
            if suffix:
                val += suffix
            retval[match.group(1)] = val

        return retval


if __name__ == '__main__':
    analyser = StCmdAnalyser('tests/st.cmd')
    print(analyser.dbloadrecord_cmds)
