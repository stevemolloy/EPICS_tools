import unittest

from ioc_from_stcmd import IocFromStCmd

class IocFromStCmdTester(unittest.TestCase):
    def setUp(self):
        self.ioc = IocFromStCmd('st.cmd')

    def test_basic_initialisation(self):
        self.assertIsInstance(self.ioc, IocFromStCmd)

    def test_filenames_of_interest(self):
        self.assertEqual(
            self.ioc.db_files, [
                '$(SIS8300)/db/SIS8300.template',
                '$(SIS8300)/db/SIS8300N.template',
                '$(BPM)/db/SIS8300bpm.template',
                '$(BPM)/db/SIS8300bpmN.template',
                '$(ADCORE)/db/NDStdArrays.template',
                '$(ADCORE)/db/NDTimeSeries.template',
                '$(ADCORE)/db/NDTimeSeriesN.template',
                '$(ADCORE)/db/NDFFT.template',
                '$(MRFIOC2)/db/evr-mtca-300.db',
                '$(MRFIOC2)/db/evr-softEvent.template',
                '$(MRFIOC2)/db/evr-pulserMap.template',
            ]
        )
