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


class FullFileAnalyserTest(unittest.TestCase):
    def setUp(self):
        self.analyser = TemplateAnalyser('SIS8300bpm.template')

    def test_file_has_record_list(self):
        self.assertEqual(len(self.analyser.records), 48)

    def test_record_types(self):
        records = self.analyser.records
        self.assertEqual(records[0].record_type, "longin")
        self.assertEqual(records[4].record_type, "longout")
        self.assertEqual(records[10].record_type, "longin")
        self.assertEqual(records[11].record_type, "mbbo")
        self.assertEqual(records[12].record_type, "mbbi")
        self.assertEqual(records[-12].record_type, "ai")
        self.assertEqual(records[-5].record_type, "bi")
        self.assertEqual(records[-2].record_type, "bo")
        self.assertEqual(records[-1].record_type, "seq")

    def test_record_names(self):
        records = self.analyser.records
        self.assertEqual(records[0].record_name, "$(P)$(R)BPMFWVersion_RBV")
        self.assertEqual(records[4].record_name, "$(P)$(R)NearIQM")
        self.assertEqual(records[10].record_name, "$(P)$(R)NumBPMSamples_RBV")
        self.assertEqual(records[11].record_name, "$(P)$(R)MemMux")
        self.assertEqual(records[12].record_name, "$(P)$(R)MemMux_RBV")
        self.assertEqual(records[-12].record_name, "$(P)$(R)FilterGain_RBV")
        self.assertEqual(records[-5].record_name, "$(P)$(R)SelfTrigChRef_RBV")
        self.assertEqual(records[-2].record_name, "$(P)$(R)BPM:Enable")
        self.assertEqual(records[-1].record_name, "$(P)$(R)BPM:EnableSeq")

    def test_first_record_types(self):
        first_record = self.analyser.records[0]
        field_list = first_record.fields
        self.assertEqual(len(field_list), 3)
        self.assertEqual(field_list[0].field_type, 'DTYP')
        self.assertEqual(field_list[1].field_type, 'INP')
        self.assertEqual(field_list[2].field_type, 'SCAN')

    def test_first_record_names(self):
        first_record = self.analyser.records[0]
        field_list = first_record.fields
        self.assertEqual(len(field_list), 3)
        self.assertEqual(field_list[0].field_name, "asynInt32")
        self.assertEqual(field_list[1].field_name, "@asyn($(PORT),$(ADDR),$(TIMEOUT))BPM_FW_VERSION")
        self.assertEqual(field_list[2].field_name, "I/O Intr")

    def test_fourth_record_types(self):
        first_record = self.analyser.records[4]
        field_list = first_record.fields
        self.assertEqual(len(field_list), 7)
        self.assertEqual(field_list[0].field_type, 'DTYP')
        self.assertEqual(field_list[1].field_type, 'OUT')
        self.assertEqual(field_list[2].field_type, 'DRVH')
        self.assertEqual(field_list[3].field_type, 'DRVL')
        self.assertEqual(field_list[4].field_type, 'PINI')
        self.assertEqual(field_list[5].field_type, 'VAL')
        self.assertEqual(field_list[6].field_type, 'autosaveFields')

    def test_fourth_record_names(self):
        first_record = self.analyser.records[4]
        field_list = first_record.fields
        self.assertEqual(len(field_list), 7)
        self.assertEqual(field_list[0].field_name, "asynInt32")
        self.assertEqual(field_list[1].field_name, "@asyn($(PORT),$(ADDR),$(TIMEOUT))BPM_NEARIQ_M")
        self.assertEqual(field_list[2].field_name, "255")
        self.assertEqual(field_list[3].field_name, "0")
        self.assertEqual(field_list[4].field_name, "YES")
        self.assertEqual(field_list[5].field_name, "4")
        self.assertEqual(field_list[6].field_name, "VAL")

    def test_fourth_record_contains_info(self):
        first_record = self.analyser.records[4]
        field_list = first_record.fields
        self.assertEqual(field_list[0].is_field, True)
        self.assertEqual(field_list[1].is_field, True)
        self.assertEqual(field_list[2].is_field, True)
        self.assertEqual(field_list[3].is_field, True)
        self.assertEqual(field_list[4].is_field, True)
        self.assertEqual(field_list[5].is_field, True)
        self.assertEqual(field_list[6].is_field, False)
        self.assertEqual(field_list[6].is_info, True)
