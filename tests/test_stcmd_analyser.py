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
        self.assertEqual(len(self.analyser.epics_env_sets), 43)
        self.assertIsInstance(self.analyser.epics_env_sets, dict)
