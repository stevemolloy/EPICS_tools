from analyse_stcmd import StCmdAnalyser


class IocFromStCmd:
    def __init__(self, filename):
        self.stcmd_analyser = StCmdAnalyser(filename)
        self.db_files = self.get_db_files()

    def get_db_files(self):
        return list(self.stcmd_analyser.template_dict.keys())


if __name__ == '__main__':
    ioc = IocFromStCmd('tests/st.cmd')

    for i in ioc.stcmd_analyser.template_dict:
        print(i)
