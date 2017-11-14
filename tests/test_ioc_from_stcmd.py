import unittest
from pathlib import Path

from utilities import remove_envvars, add_envvars
from ioc_from_stcmd import IocFromStCmd


class IocFromStCmdTester(unittest.TestCase):
    def test_basic_initialisation(self):
        ioc = IocFromStCmd('st.cmd')
        self.assertIsInstance(ioc, IocFromStCmd)

    def test_filenames_with_no_OSenvvars(self):
        envvar_list = [
            'SIS8300',
            'BPM',
            'ADCORE',
            'MRFIOC2',
        ]
        with remove_envvars(envvar_list):
            ioc = IocFromStCmd('st.cmd')
            self.assertEqual(
                ioc.db_files, [
                    'SIS8300.template',
                    'SIS8300N.template',
                    'SIS8300bpm.template',
                    'SIS8300bpmN.template',
                    'NDStdArrays.template',
                    'NDTimeSeries.template',
                    'NDTimeSeriesN.template',
                    'NDFFT.template',
                    'evr-mtca-300.db',
                    'evr-softEvent.template',
                    'evr-pulserMap.template',
                ]
            )

    def test_filenames_with_OSenvvars(self):
        envvar_dict = dict([
            ('SIS8300', 'sisfolder'),
            ('BPM', 'bpmfolder'),
            ('ADCORE', 'adcorefolder'),
            ('MRFIOC2', 'mrfioc2folder'),
        ])
        with add_envvars(envvar_dict):
            ioc = IocFromStCmd('st.cmd')
            self.assertEqual(
                ioc.db_files, [
                    'sisfolder/db/SIS8300.template',
                    'sisfolder/db/SIS8300N.template',
                    'bpmfolder/db/SIS8300bpm.template',
                    'bpmfolder/db/SIS8300bpmN.template',
                    'adcorefolder/db/NDStdArrays.template',
                    'adcorefolder/db/NDTimeSeries.template',
                    'adcorefolder/db/NDTimeSeriesN.template',
                    'adcorefolder/db/NDFFT.template',
                    'mrfioc2folder/db/evr-mtca-300.db',
                    'mrfioc2folder/db/evr-softEvent.template',
                    'mrfioc2folder/db/evr-pulserMap.template',
                ]
            )

    def test_files_can_be_found(self):
        envvar_list = [
            'SIS8300',
            'BPM',
            'ADCORE',
            'MRFIOC2',
        ]
        with remove_envvars(envvar_list):
            ioc = IocFromStCmd('st.cmd')
            for file in ioc.db_files:
                if file != 'evr-mtca-300.db' and file != 'evr-softEvent.template' and file != 'evr-pulserMap.template':
                    self.assertTrue(Path(file).exists(), msg=f'{file} does not exist')
                    self.assertTrue(Path(file).is_file(), msg=f'{file} is not a file')
