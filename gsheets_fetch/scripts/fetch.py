# scripts/fetch.py

import argparse
import json

from gsheets_fetch.client import GSheets

from gsheets_fetch.exporters import CsvGSheetsExporter, JsonGSheetsExporter, TxtGSheetsExporter


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('spreadsheet_id')
    parser.add_argument('-d', '--dirpath', default=argparse.SUPPRESS,
                        help='Directory to save output files if different than the current working directory.')
    parser.add_argument('-f', '--filename_template', default=argparse.SUPPRESS,
                        help='Template for output filenames.')
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', default=False,
                        help='Flag to suppress showing downloaded filepaths.')
    parser.add_argument('--secrets', dest='client_secrets_filename', default='credentials.json',
                        help='Custom Google OAuth2 client secretes JSON filepath.')
    parser.add_argument('--storage', dest='storage_filename', default='token.pickle',
                        help='Custom Google OAuth2 storage filepath.')
    parser.add_argument('--sheet-ids', nargs='+', type=int, dest='sheet_ids', default=argparse.SUPPRESS)
    parser.add_argument('--sheet-names', nargs='+', type=str, dest='sheet_names', default=argparse.SUPPRESS)
    parser.add_argument('--sheet-name-patterns', nargs='+', type=str, dest='sheet_name_patterns',
                        default=argparse.SUPPRESS)
    parser.add_argument('--exclude-sheet-ids', nargs='+', type=int, dest='exclude_sheet_ids',
                        default=argparse.SUPPRESS)
    parser.add_argument('--exclude-sheet-names', nargs='+', type=str, dest='exclude_sheet_names',
                        default=argparse.SUPPRESS)
    parser.add_argument('--exclude-sheet-name-patterns', nargs='+', type=str,
                        dest='exclude_sheet_name_patterns', default=argparse.SUPPRESS)
    file_type_group = parser.add_mutually_exclusive_group()
    file_type_group.add_argument('--text', dest='as_text', action='store_true', default=False,
                                 help='Flag if files should be saved as plaintext instead of CSV.')
    file_type_group.add_argument('--json', dest='as_json', action='store_true', default=False,
                                 help='Flag if files should be saved as JSON instead of CSV.')
    parser.add_argument('--info', dest='show_info', action='store_true', default=False,
                        help='Show information about the spreadsheet and exit.')

    args = parser.parse_args()

    kwargs = vars(args)
    if kwargs.pop('as_json', False):
        kwargs['exporter_cls'] = JsonGSheetsExporter
    elif kwargs.pop('as_text', False):
        kwargs['exporter_cls'] = TxtGSheetsExporter
    spreadsheet_id = kwargs.pop('spreadsheet_id')

    fetch(spreadsheet_id, **kwargs)


def fetch(spreadsheet_id, client_secrets_filename=None, storage_filename=None,
          dirpath=None, filename_template=None, exporter_cls=None,
          show_info=False, quiet=False, **kwargs):

    gs = GSheets(spreadsheet_id=spreadsheet_id,
                 client_secrets=client_secrets_filename,
                 storage=storage_filename)

    if show_info:
        metadata = gs.get_metadata(**kwargs)
        json_metadata = json.dumps(metadata)
        print(json_metadata)
    else:
        exporter_cls = exporter_cls or CsvGSheetsExporter
        exporter = exporter_cls(dirpath=dirpath, filename_template=filename_template)
        for filename in exporter.export(gs, **kwargs):
            if not quiet:
                print(filename)
