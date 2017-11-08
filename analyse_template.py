import re


class TemplateAnalyser:
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename) as f:
            self.contents = [line for line in f if not line.strip().startswith('#')]

    @property
    def records(self):
        records_start = [ind for ind, val in enumerate(self.contents) if val.startswith('record')]
        records_end = records_start[1:] + [None]
        records_list = [
            EpicsRecord(self.make_raw_record_string(inds=(start, end)))
            for start, end in zip(records_start, records_end)
        ]
        return records_list

    def make_raw_record_string(self, inds):
        list_of_lines = ''.join(self.contents[inds[0]:inds[1]]).split('\n')
        stripped_lines = [l.strip() for l in list_of_lines]
        return ''.join(stripped_lines)


class EpicsRecord:
    def __init__(self, raw_record_string):
        split_string = re.split('[{}]', raw_record_string)
        self.instantiation_string = split_string[0]
        self.body_string = split_string[1]

    @property
    def record_type(self):
        stripped_string = self.instantiation_string.replace('record(', '')
        return stripped_string.split(',')[0]

    @property
    def record_name(self):
        return self.instantiation_string.split('"')[1]
    
    @property
    def fields(self):
        raw_field_list = re.split('field|info', self.body_string)
        return [EpicsField(raw_field) for raw_field in raw_field_list if raw_field]


class EpicsField:
    def __init__(self, raw_string):
        assert(raw_string.startswith('('))
        assert(raw_string.endswith(')'))
        self.raw_string_split = raw_string.split(',', 1)

    @property
    def field_type(self):
        return self.raw_string_split[0][1:]

    @property
    def field_name(self):
        name_field = self.raw_string_split[1]
        name_field = name_field.replace('"', '')
        name_field = name_field.strip()
        return name_field[:-1]


if __name__ == '__main__':
    analyser = TemplateAnalyser('tests/one_record.template')
    print(analyser.records[0].fields)
