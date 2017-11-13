import re
import os
from pathlib import PurePath

from analyse_stcmd import StCmdAnalyser


class IocFromStCmd:
    def __init__(self, filename):
        self.stcmd_analyser = StCmdAnalyser(filename)
        self.db_files = self.get_db_files()

    @property
    def filenames(self):
        return self.stcmd_analyser.template_dict.keys()

    def get_db_files(self):
        envvars = []
        regex = r"\$\((\w+)\)"
        for filename in self.filenames:
            matches = re.finditer(regex, filename)
            for match in matches:
                if match.group(1) in os.environ:
                    envvars.append(re.sub(regex, os.environ[match.group(1)], filename))
                else:
                    envvars.append(PurePath(filename).name)
        return envvars
