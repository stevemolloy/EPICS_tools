import re
import os
from pathlib import PurePath

from analyse_stcmd import StCmdAnalyser


class IocFromStCmd:
    def __init__(self, filename):
        self.stcmd_analyser = StCmdAnalyser(filename)
        self.db_files = self.get_db_files()

    @property
    def raw_filenames(self):
        return self.stcmd_analyser.template_dict.keys()

    def get_db_files(self):
        envvars = []
        regex = r"\$\((\w+)\)"
        for filename in self.raw_filenames:
            for match in re.finditer(regex, filename):
                if match.group(1) in os.environ:
                    envvars.append(
                        re.sub(regex, os.environ[match.group(1)], filename)
                    )
                else:
                    envvars.append(PurePath(filename).name)
        return envvars
