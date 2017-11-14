import re
import os
from pathlib import PurePath, Path

from analyse_stcmd import StCmdAnalyser
from analyse_template import TemplateAnalyser


class IocFromStCmd:
    def __init__(self, filename):
        self.stcmd_analyser = StCmdAnalyser(filename)
        self.db_files = self.get_db_files()
        self.templates = self.get_templates()

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

    def get_templates(self):
        return dict(
            zip(self.db_files, [
                TemplateAnalyser(filename)
                if Path(filename).exists() else None
                for filename in self.db_files
            ])
        )
