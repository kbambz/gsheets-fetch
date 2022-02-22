import unittest
import os.path

from gsheets_fetch.scripts import fetch


class TestFetch(unittest.TestCase):

    def test_fetch_sheet(self):
        target_file = 'GSheets Fetch Test - Data1.csv'

        if os.path.isfile(target_file):
            os.remove(target_file)

        spreadsheet_id = '1oJVL8pxdUvbdtD39NASTctzljX-wosUb4nKZhyFYBCs'
        fetch(spreadsheet_id,
              dirpath='.', filename_template=None, exporter_cls=None,
              client_secrets_filename='credentials.json', storage_filename='token.pickle',
              show_info=False, quiet=True)

        self.assertTrue(os.path.isfile(target_file))
        os.remove(target_file)


if __name__ == '__main__':
    unittest.main()
