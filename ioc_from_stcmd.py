import re
import os
from pathlib import PurePath, Path
from collections.abc import MutableMapping

from analyse_stcmd import StCmdAnalyser
from analyse_template import TemplateAnalyser
from utilities import remove_envvars


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
        ret_dict = DynamicDict(
            zip(self.db_files, [
                filename
                if Path(filename).exists() else None
                for filename in self.db_files
            ])
        )

        return ret_dict


class DynamicDict(MutableMapping):
    def __init__(self, *args, **kw):
        self._storage = dict(*args, **kw)

    def __len__(self):
        return len(self._storage)

    def __getitem__(self, item):
        value = self._storage[item]
        if type(value) is TemplateAnalyser:
            return value
        try:
            self._storage[item] = TemplateAnalyser(item)
        except FileNotFoundError:
            pass
        return self._storage[item]

    def __delitem__(self, key):
        self._storage.pop(key)

    def __iter__(self):
        return self._storage.items()

    def __setitem__(self, key, value):
        self._storage.__setitem__(key, value)

    def items(self):
        for key in self._storage:
            yield key, self.__getitem__(key)


if __name__ == "__main__":
    envvar_list = [
        'SIS8300',
        'BPM',
        'ADCORE',
        'MRFIOC2',
    ]
    os.chdir('tests')
    with remove_envvars(envvar_list):
        ioc = IocFromStCmd('st.cmd')
        for k, v in ioc.templates.items():
            print(v)
