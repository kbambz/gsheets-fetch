import unittest
import os.path

from gsheets_fetch.scripts import fetch
from gsheets_fetch import TxtGSheetsExporter


class TestFetch(unittest.TestCase):

    @property
    def target_file(self):
        if hasattr(self, '_target_file'):
            return self._target_file
        else:
            return None

    @target_file.setter
    def target_file(self, value):
        if value:
            value = os.path.join('tmp', value)
            if os.path.isfile(value):
                os.remove(value)
        self._target_file = value

    @classmethod
    def setUpClass(cls):
        try:
            os.mkdir('tmp')
        except FileExistsError:
            pass

    @classmethod
    def tearDownClass(cls):
        os.rmdir('tmp')

    def setUp(self):
        self.spreadsheet_id = '1oJVL8pxdUvbdtD39NASTctzljX-wosUb4nKZhyFYBCs'
        self.default_kwargs = dict(dirpath='tmp',
                                   client_secrets_filename='credentials.json',
                                   storage_filename='token.pickle',
                                   show_info=False,
                                   quiet=True)

    def tearDown(self):
        if self.target_file:
            os.remove(self.target_file)

    def test_fetch_sheet_csv(self):
        self.target_file = 'GSheets Fetch Test - Data1.csv'
        fetch(self.spreadsheet_id, **self.default_kwargs)
        self.assertTrue(os.path.isfile(self.target_file))

    def test_fetch_sheet_text(self):
        self.target_file = 'GSheets Fetch Test - Data1.txt'
        fetch(self.spreadsheet_id, exporter_cls=TxtGSheetsExporter, **self.default_kwargs)
        self.assertTrue(os.path.isfile(self.target_file))


if __name__ == '__main__':
    unittest.main()
