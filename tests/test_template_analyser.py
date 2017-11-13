import unittest

from analyse_template import TemplateAnalyser, EpicsInfo


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
        record = self.analyser.records[0]
        fields = record.fields
        self.assertEqual(fields[0].field_type, 'DTYP')
        self.assertEqual(fields[1].field_type, 'INP')
        self.assertEqual(fields[2].field_type, 'SCAN')

    def test_field_names(self):
        record = self.analyser.records[0]
        fields = record.fields
        self.assertEqual(fields[0].field_name, "asynInt32")
        self.assertEqual(fields[1].field_name, "@asyn($(PORT),$(ADDR),$(TIMEOUT))BPM_FW_VERSION")
        self.assertEqual(fields[2].field_name, "I/O Intr")

    def test_record_repr(self):
        self.assertEqual(
            self.analyser.records[0].__repr__(),
            'record(longin, "$(P)$(R)BPMFWVersion_RBV") {\n' +
            '\tfield(DTYP, "asynInt32")\n' +
            '\tfield(INP, "@asyn($(PORT),$(ADDR),$(TIMEOUT))BPM_FW_VERSION")\n' +
            '\tfield(SCAN, "I/O Intr")\n' +
            '}'
        )


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
        fourth_record = self.analyser.records[4]
        field_list = fourth_record.fields
        self.assertEqual(field_list[0].is_field, True)
        self.assertEqual(field_list[1].is_field, True)
        self.assertEqual(field_list[2].is_field, True)
        self.assertEqual(field_list[3].is_field, True)
        self.assertEqual(field_list[4].is_field, True)
        self.assertEqual(field_list[5].is_field, True)
        self.assertEqual(field_list[6].is_field, False)
        self.assertEqual(field_list[6].is_info, True)

    def test_number_of_records_with_info(self):
        counter = 0
        records = self.analyser.records
        for record in records:
            if any(isinstance(field, EpicsInfo) for field in record.fields):
                counter += 1
        self.assertEqual(counter, 15)

    def test_record_repr_with_info(self):
        rec = self.analyser.records
        fourth_record = rec[4]
        another_record = rec[-4]

        self.assertEqual(
            fourth_record.__repr__(),
            'record(longout, "$(P)$(R)NearIQM") {\n' +
            '\tfield(DTYP, "asynInt32")\n' +
            '\tfield(OUT, "@asyn($(PORT),$(ADDR),$(TIMEOUT))BPM_NEARIQ_M")\n' +
            '\tfield(DRVH, "255")\n' +
            '\tfield(DRVL, "0")\n' +
            '\tfield(PINI, "YES")\n' +
            '\tfield(VAL, "4")\n' +
            '\tinfo(autosaveFields, "VAL")\n' +
            '}'
        )
        self.assertEqual(
            another_record.__repr__(),
            'record(longout, "$(P)$(R)SelfTrigIQSamples") {\n' +
            '\tfield(DTYP, "asynInt32")\n' +
            '\tfield(OUT, "@asyn($(PORT),$(ADDR),$(TIMEOUT))BPM_SELF_TRIG_IQ_SAMPLES")\n' +
            '\tfield(VAL, "0")\n' +
            '\tfield(PINI, "YES")\n' +
            '\tinfo(autosaveFields, "VAL")\n' +
            '}'
        )

    def test_whole_file_repr(self):
        analyser_repr = self.analyser.__repr__()
        analyser_repr = ''.join(analyser_repr).replace('\n', '').replace('\t', '')

        with open('SIS8300bpm.template') as f:
            file_str = [line.replace(' ', '') for line in f if line and not line.startswith('#')]
        file_str = ''.join(file_str).replace('\n', '')

        self.assertEqual(analyser_repr.replace(' ', ''), file_str.replace('\t', ''))
