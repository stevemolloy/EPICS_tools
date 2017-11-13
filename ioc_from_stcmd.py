import re
import os
from pathlib import PurePath

from analyse_stcmd import StCmdAnalyser


class IocFromStCmd:
    def __init__(self, filename):
        self.stcmd_analyser = StCmdAnalyser(filename)
        self.db_files = self.get_db_files()

    def get_db_files(self):
        # print(os.environ.get('BPM'))
        return self.get_filename_envvars()

    def get_filename_envvars(self):
        envvars = []
        filenames = list(self.stcmd_analyser.template_dict.keys())
        regex = r"\$\((\w+)\)"
        for filename in filenames:
            matches = re.finditer(regex, filename)
            for match in matches:
                if match.group(1) in os.environ:
                    envvars.append(re.sub(regex, os.environ[match.group(1)], filename))
                else:
                    envvars.append(PurePath(filename).name)
        return envvars


if __name__ == '__main__':
    ioc = IocFromStCmd('tests/st.cmd')

    for i in ioc.stcmd_analyser.template_dict:
        print(i)
