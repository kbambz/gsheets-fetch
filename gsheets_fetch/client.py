from __future__ import print_function
from __future__ import unicode_literals

import os.path
import re
import pickle

try:
    from itertools import izip as zip
except ImportError:  # will be 3.x series
    pass

from googleapiclient.discovery import build as build_service
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class GSheets(object):

    def __init__(self, spreadsheet_id=None, **kwargs):
        kwargs.setdefault('scopes', ['https://www.googleapis.com/auth/spreadsheets.readonly'])
        credentials = self._get_credentials(**kwargs)
        self._service = self._get_service(credentials)
        self.spreadsheet_id = spreadsheet_id

    def get_metadata(self, spreadsheet_id=None, **kwargs):
        """Return metadata from the GSheets API about the target spreadsheet.

        Returns a dict with two keys:
            - "properties" is a one-item dict containing the value of the spreadsheet's
                    name under key "title"
            - "sheets" is a list of dicts containing the integer sheet ID ("sheetId")
                    and string sheet name ("title") for each sheet in the spreadsheet

        Example:
            >>> gs = GSheets(spreadsheet_id='2n4cf8IIq8-BKv2Wm4V7dcuiyLy_rICeM-sPcuTxGMb7')
            >>> gs.get_metadata()
            {'properties': {'title': 'My Spreadsheet'},
             'sheets': [{u'properties': {'sheetId': 0, 'title': 'Sheet1'}},
                        {u'properties': {'sheetId': 329009455,
                                         'title': '>>> RAW DATA'}}]}
        """
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id
        metadata = self._service.spreadsheets().get(
            spreadsheetId=spreadsheet_id,
            fields='properties.title,sheets(properties.title,properties.sheetId)'
        ).execute()

        metadata.setdefault('url', f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}')
        if 'sheets' in metadata:
            metadata['sheets'] = self._filter_sheets(metadata['sheets'], **kwargs)

        return metadata

    def get_sheets_values(self, sheet_names, spreadsheet_id=None):
        return self._service.spreadsheets().values().batchGet(
            spreadsheetId=spreadsheet_id or self.spreadsheet_id,
            ranges=sheet_names,
            fields='valueRanges(range,values)'
        ).execute().get('valueRanges')

    def itersheets(self, spreadsheet_id=None, **kwargs):
        spreadsheet_id = spreadsheet_id or self.spreadsheet_id
        metadata = self.get_metadata(spreadsheet_id=spreadsheet_id, **kwargs)
        title = metadata['properties']['title']
        sheet_names = [sheet['properties']['title'] for sheet in metadata['sheets']]
        results = self.get_sheets_values(sheet_names, spreadsheet_id=spreadsheet_id)
        for name, vr in zip(sheet_names, results):
            yield (title, name), vr['values']

    def _filter_sheets(self, sheets_metadata,
                       sheet_names=None,
                       sheet_ids=None,
                       sheet_name_patterns=None,
                       exclude_sheet_names=None,
                       exclude_sheet_ids=None,
                       exclude_sheet_name_patterns=None,
                       **kwargs):
        f = Filter(include_names=sheet_names,
                   include_ids=sheet_ids,
                   include_name_patterns=sheet_name_patterns,
                   exclude_names=exclude_sheet_names,
                   exclude_ids=exclude_sheet_ids,
                   exclude_name_patterns=exclude_sheet_name_patterns,
                   name_func=lambda s: s['properties']['title'],
                   id_func=lambda s: s['properties']['sheetId'])
        return f(sheets_metadata)

    @staticmethod
    def _get_credentials(client_secrets='credentials.json', storage='token.pickle', scopes=None):
        credentials = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(storage):
            with open(storage, 'rb') as token:
                credentials = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(client_secrets, scopes)
                credentials = flow.run_local_server()
            # Save the credentials for the next run
            with open(storage, 'wb') as token:
                pickle.dump(credentials, token)

        return credentials

    @staticmethod
    def _get_service(credentials):
        return build_service('sheets', 'v4', credentials=credentials)

    def __del__(self):
        self.cleanup()

    def cleanup(self):
        # Temp workaround to https://github.com/googleapis/google-api-python-client/issues/618
        self._service._http.http.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.cleanup()


class Filter(object):

    def __init__(self,
                 include_names=None,
                 include_ids=None,
                 include_name_patterns=None,
                 exclude_names=None,
                 exclude_ids=None,
                 exclude_name_patterns=None,
                 name_func=lambda o: getattr(o, 'name'),
                 id_func=lambda o: getattr(o, 'id')):
        self.include_ids = include_ids
        self.include_names = include_names
        self.include_name_patterns = include_name_patterns
        self.exclude_ids = exclude_ids
        self.exclude_names = exclude_names
        self.exclude_name_patterns = exclude_name_patterns
        self.id_func = id_func
        self.name_func = name_func

    def has_include_rules(self):
        return (self.include_names is not None or
                self.include_ids is not None or
                self.include_name_patterns)

    def __call__(self, items):
        if self.has_include_rules():
            names = set(self.include_names or [])
            ids = set([int(item_id) for item_id in self.include_ids or []])
            name_patterns = self.include_name_patterns or []
            items = [i for i in items if (self.name_func(i) in names or
                                          self.id_func(i) in ids or
                                          any([re.search(p, self.name_func(i))
                                               for p in name_patterns]))]
        else:
            items = [i for i in items]

        if self.exclude_names:
            names = set(self.exclude_names)
            items = filter(lambda i: self.name_func(i) not in names, items)
        if self.exclude_ids:
            ids = set([int(item_id) for item_id in self.exclude_ids or []])
            items = filter(lambda i: self.id_func(i) not in ids, items)
        if self.exclude_name_patterns:
            items = filter(lambda i: not any([re.search(p, self.name_func(i))
                                              for p in self.exclude_name_patterns]), items)
        if isinstance(items, filter):
            items = list(items)

        return items
