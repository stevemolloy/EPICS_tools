import re


class TemplateAnalyser:
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename) as f:
            self.contents = [
                line
                for line in f
                if not line.strip().startswith('#')
            ]

    @property
    def records(self):
        records_start = [
            ind
            for ind, val in enumerate(self.contents)
            if val.startswith('record')
        ]
        records_end = records_start[1:]
        records_list = [
            EpicsRecord(self.make_raw_record_string(inds=(start, end)))
            for start, end in zip(records_start[:-1], records_end)
        ]
        records_list.append(EpicsRecord(self.make_raw_record_string(inds=(records_start[-1], None))))
        return records_list

    def make_raw_record_string(self, inds):
        list_of_lines = ''.join(self.contents[inds[0]:inds[1]]).split('\n')
        stripped_lines = [l.strip() for l in list_of_lines]
        return ''.join(stripped_lines)

    def __repr__(self):
        repr_str = ''
        for rec in self.records:
            repr_str += rec.__repr__() + '\n'
        return repr_str


class EpicsRecord:
    def __init__(self, raw_record_string):
        split_string = re.split('[{}]', raw_record_string)
        self.instantiation_string = split_string[0]
        self.body_string = split_string[1]
        self.record_type = self.get_record_type()
        self.record_name = self.get_record_name()

    def __repr__(self):
        repr_str = 'record('
        repr_str += self.get_record_type()
        repr_str += ', "' + self.record_name + '") {\n'
        for field in self.fields:
            repr_str += '\t' + field.__repr__() + '\n'
        repr_str += '}'
        return repr_str

    def get_record_type(self):
        stripped_string = self.instantiation_string.replace('record(', '')
        return stripped_string.split(',')[0]

    def get_record_name(self):
        return str(self.instantiation_string.split('"')[1])

    @property
    def fields(self):
        raw_field_list = re.split('field', self.body_string)
        ret_list = [EpicsField(raw_field)
                    for raw_field in raw_field_list
                    if raw_field and 'info' not in raw_field]
        for raw_field in raw_field_list:
            if 'info' in raw_field:
                info_split = raw_field.split('info')
                ret_list.append(EpicsField(info_split[0]))
                ret_list.append(EpicsInfo(info_split[1]))
        return ret_list


class EpicsField:
    is_field = True
    is_info = False

    def __init__(self, raw_string):
        assert(raw_string.startswith('('))
        assert(raw_string.endswith(')'))
        self.raw_string_split = raw_string.split(',', 1)

    def __repr__(self):
        return 'field(' + self.field_type + ', "' + self.field_name + '")'

    @property
    def field_type(self):
        return self.raw_string_split[0][1:]

    @property
    def field_name(self):
        name_field = self.raw_string_split[1]
        name_field = name_field.replace('"', '')
        name_field = name_field.strip()
        return name_field[:-1]


class EpicsInfo(EpicsField):
    is_field = False
    is_info = True

    def __repr__(self):
        return 'info(' + self.field_type + ', "' + self.field_name + '")'


if __name__ == '__main__':
    from collections import Counter

    SIS8300bpm = TemplateAnalyser('tests/SIS8300bpm.template')
    SIS8300bpmN = TemplateAnalyser('tests/SIS8300bpmN.template')
    SIS8300 = TemplateAnalyser('tests/SIS8300.template')
    SIS8300N = TemplateAnalyser('tests/SIS8300N.template')

    print(SIS8300.filename)
    type_ctr = Counter(record.record_type for record in SIS8300.records)
    for record_type in type_ctr.most_common():
        print(record_type)
    print([rec.record_name for rec in SIS8300.records])
