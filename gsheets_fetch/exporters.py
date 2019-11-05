import os
import csv
import json


class GSheetsExporter(object):

    default_filename_template = '{title} - {sheet}.{ext}'

    default_ext = NotImplemented

    def __init__(self, dirpath=None, filename_template=None, encoding='utf-8'):
        self.__raw_dirpath = None
        self.__dirpath = None
        self.encoding = encoding
        self.dirpath = dirpath
        self.filename_template = filename_template or self.default_filename_template

    @property
    def dirpath(self):
        return self.__dirpath

    @dirpath.setter
    def dirpath(self, value):
        raw_value = value or ''
        if raw_value:
            value = os.path.abspath(os.path.expanduser(raw_value))
            if not os.path.isdir(value):
                os.mkdir(value)
        self.__raw_dirpath = raw_value
        self.__dirpath = value

    def export(self, gsheets, **kwargs):
        for (title, sheet), rows in gsheets.itersheets(**kwargs):
            self._write(self._get_filename(title, sheet), rows)
            yield self._get_filename(title, sheet)

    def _get_filename(self, title, sheet):
        filename = self.filename_template.format(title=title, sheet=sheet, ext=self.default_ext)
        filename = os.path.join(self.dirpath, filename).replace('|', '_').replace('\'', '')
        if '.' not in filename:
            filename += '.' + self.default_ext
        return filename

    def _write(self, filename, rows, **kwargs):
        raise NotImplemented


class CsvGSheetsExporter(GSheetsExporter):

    default_ext = 'csv'

    def _write(self, filename, rows, **kwargs):
        with open(filename, 'w', newline='') as fd:
            csvfile = csv.writer(fd, dialect=kwargs.pop('dialect', 'excel'))
            for r in rows:
                csvfile.writerow(r)


class JsonGSheetsExporter(GSheetsExporter):

    default_ext = 'json'

    def _write(self, filename, rows, **kwargs):
        with open(filename, 'wb') as fd:
            # TODO: Test with Python 3
            data = dict(rows=[[c.encode(self.encoding) for c in r] for r in rows])
            json.dump(data, fd)


class TsvGSheetsExporter(GSheetsExporter):

    default_ext = 'tsv'

    def _write(self, filename, rows, **kwargs):
        with open(filename, 'w', newline='') as fd:
            csvfile = csv.writer(fd, dialect=csv.excel_tab)
            for r in rows:
                csvfile.writerow(r)


class TxtGSheetsExporter(GSheetsExporter):

    default_ext = 'txt'

    def _write(self, filename, rows, **kwargs):
        with open(filename, 'wb') as fd:
            fd.write(b'\n'.join([b''.join([c.encode(self.encoding) for c in r]) for r in rows]) + b'\n')
