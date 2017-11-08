import unittest

from analyse_template import TemplateAnalyser


class BasicTemplateAnalyserTest(unittest.TestCase):
    def test_nonexistent_filename(self):
        with self.assertRaises(FileNotFoundError):
            TemplateAnalyser('blah_blah_blah')

    def test_file_of_comments_has_is_empty(self):
        analyser = TemplateAnalyser('only_comments.template')
        self.assertListEqual(analyser.contents, [])


class OneRecordFileAnalyserTest(unittest.TestCase):
    def setUp(self):
        self.analyser = TemplateAnalyser('one_record.template')

    def test_file_has_contents(self):
        self.assertEqual(len(self.analyser.contents), 5)

    def test_file_has_a_record(self):
        contents = self.analyser.contents
        self.assertRegex(contents[0], 'record\(.*,.*\).*\{.*\\n')
        self.assertRegex(contents[1], 'field\(.*,.*\)')
        self.assertRegex(contents[2], 'field\(.*,.*\)')
        self.assertRegex(contents[3], 'field\(.*,.*\)')
        self.assertEqual(contents[4], '}')

    def test_file_has_record_list(self):
        self.assertEqual(len(self.analyser.records), 1)

    def test_record_name(self):
        record = self.analyser.records[0]
        self.assertEqual(record.record_name, "$(P)$(R)BPMFWVersion_RBV")

    def test_record_type(self):
        record = self.analyser.records[0]
        self.assertEqual(record.record_type, "longin")

    def test_file_has_3_fields(self):
        analyser = TemplateAnalyser('one_record.template')
        self.assertEqual(len(analyser.records[0].fields), 3)

    def test_field_types(self):
        analyser = TemplateAnalyser('one_record.template')
        record = analyser.records[0]
        fields = record.fields
        self.assertEqual(fields[0].field_type, 'DTYP')
        self.assertEqual(fields[1].field_type, 'INP')
        self.assertEqual(fields[2].field_type, 'SCAN')

    def test_field_names(self):
        analyser = TemplateAnalyser('one_record.template')
        record = analyser.records[0]
        fields = record.fields
        self.assertEqual(fields[0].field_name, "asynInt32")
        self.assertEqual(fields[1].field_name, "@asyn($(PORT),$(ADDR),$(TIMEOUT))BPM_FW_VERSION")
        self.assertEqual(fields[2].field_name, "I/O Intr")
