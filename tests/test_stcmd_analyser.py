import unittest

from analyse_stcmd import StCmdAnalyser


class StCmdAnalyserTester(unittest.TestCase):
    def setUp(self):
        self.analyser = StCmdAnalyser('st.cmd')

    def test_basic_instantiation(self):
        with self.assertRaises(FileNotFoundError):
            StCmdAnalyser('blah_blah_blah')
        self.assertEqual(self.analyser.filename, 'st.cmd')
        self.assertGreater(len(self.analyser.contents), 0)

    def test_no_empty_lines(self):
        for line in self.analyser.contents:
            self.assertNotEqual(line, '\n')

    def test_no_linefeeds(self):
        for line in self.analyser.contents:
            self.assertNotIn('\n', line)

    def test_finding_envset_lines(self):
        self.assertEqual(len(self.analyser.epics_env_vars), 43)
        self.assertIsInstance(self.analyser.epics_env_vars, dict)
        self.assertEqual(self.analyser.epics_env_vars['PORT'], 'BPM')
        self.assertEqual(self.analyser.epics_env_vars['BPMCH14'], 'REFPHA')
        self.assertEqual(self.analyser.epics_env_vars['EVR_PCIFUNCTION'], '0x0')

    def test_find_dbloadrecord_lines(self):
        self.assertEqual(len(self.analyser.dbloadrecord_cmds), 85)

    def test_finding_template_files(self):
        a = self.analyser
        self.assertEqual(len(a.templates), 11)

    def test_listing_substitutions(self):
        a = self.analyser
        self.assertEqual(a.templates['$(MRFIOC2)/db/evr-mtca-300.db'],
                         [{'DEVICE': 'EVR', 'SYS': 'BPM', 'Link-Clk-SP': '88.0525'}])
        self.assertEqual(a.templates["$(SIS8300)/db/SIS8300.template"],
                         [{'P': 'BPM:', 'R': '', 'PORT': 'BPM', 'ADDR': '0', 'TIMEOUT': '1'}])
        self.assertEqual(a.templates["$(SIS8300)/db/SIS8300N.template"],
                         [
                             {'P': 'BPM:', 'R': 'AI0', 'PORT': 'BPM', 'ADDR': '0', 'TIMEOUT': '1', 'NAME': 'AI0'},
                             {'P': 'BPM:', 'R': 'AI1', 'PORT': 'BPM', 'ADDR': '1', 'TIMEOUT': '1', 'NAME': 'AI1'},
                             {'P': 'BPM:', 'R': 'AI2', 'PORT': 'BPM', 'ADDR': '2', 'TIMEOUT': '1', 'NAME': 'AI2'},
                             {'P': 'BPM:', 'R': 'AI3', 'PORT': 'BPM', 'ADDR': '3', 'TIMEOUT': '1', 'NAME': 'AI3'},
                             {'P': 'BPM:', 'R': 'AI4', 'PORT': 'BPM', 'ADDR': '4', 'TIMEOUT': '1', 'NAME': 'AI4'},
                             {'P': 'BPM:', 'R': 'AI5', 'PORT': 'BPM', 'ADDR': '5', 'TIMEOUT': '1', 'NAME': 'AI5'},
                             {'P': 'BPM:', 'R': 'AI6', 'PORT': 'BPM', 'ADDR': '6', 'TIMEOUT': '1', 'NAME': 'AI6'},
                             {'P': 'BPM:', 'R': 'AI7', 'PORT': 'BPM', 'ADDR': '7', 'TIMEOUT': '1', 'NAME': 'AI7'},
                             {'P': 'BPM:', 'R': 'AI8', 'PORT': 'BPM', 'ADDR': '8', 'TIMEOUT': '1', 'NAME': 'AI8'},
                             {'P': 'BPM:', 'R': 'AI9', 'PORT': 'BPM', 'ADDR': '9', 'TIMEOUT': '1', 'NAME': 'AI9'},
                         ])
