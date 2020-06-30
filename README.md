# gsheets-fetch

## Setup
From command line:
```console
$ pip install -e git+git@github.com:kbambz/gsheets-fetch.git#egg=gsheets_fetch --upgrade
```

In requirements file (e.g., `pip install -r requirements.txt`):
```
-e git+git@github.com:kbambz/gsheets-fetch.git#egg=gsheets_fetch
```

**You will need a credentials file to access private sheets!** You can download a credentials.json file for simple read-only access by following the instructions at https://developers.google.com/sheets/api/quickstart/python.

[![How to get credentials.json](https://i.imgur.com/iIh4Kge.png "How to get credentials.json")](https://developers.google.com/sheets/api/quickstart/python)

For advanced usage (e.g., read and write), you'll need to enable [Google Sheets API](https://console.developers.google.com/apis/library/sheets.googleapis.com) and [Google Drive API](https://console.developers.google.com/apis/library/drive.googleapis.com) on your own project and create a new credentials.json file for an OAuth Credentials. If you already created a token.pickle file with read-only permissions, simply delete the storage file (e.g., `rm token.pickle`) and re-run the fetch command to reprompt the authorization flow. 

## Usage
```console
$ gsheets-fetch --help
usage: gsheets-fetch [-h] [-d DIRPATH] [-f FILENAME_TEMPLATE] [-q]
                     [--secrets CLIENT_SECRETS_FILENAME]
                     [--storage STORAGE_FILENAME]
                     [--sheet-ids SHEET_IDS [SHEET_IDS ...]]
                     [--sheet-names SHEET_NAMES [SHEET_NAMES ...]]
                     [--sheet-name-patterns SHEET_NAME_PATTERNS [SHEET_NAME_PATTERNS ...]]
                     [--exclude-sheet-ids EXCLUDE_SHEET_IDS [EXCLUDE_SHEET_IDS ...]]
                     [--exclude-sheet-names EXCLUDE_SHEET_NAMES [EXCLUDE_SHEET_NAMES ...]]
                     [--exclude-sheet-name-patterns EXCLUDE_SHEET_NAME_PATTERNS [EXCLUDE_SHEET_NAME_PATTERNS ...]]
                     [--text | --json] [--info]
                     spreadsheet_id

positional arguments:
  spreadsheet_id

optional arguments:
  -h, --help            show this help message and exit
  -d DIRPATH, --dirpath DIRPATH
                        Directory to save output files if different than the
                        current working directory.
  -f FILENAME_TEMPLATE, --filename_template FILENAME_TEMPLATE
                        Template for output filenames.
  -q, --quiet           Flag to suppress showing downloaded filepaths.
  --secrets CLIENT_SECRETS_FILENAME
                        Custom Google OAuth2 client secretes JSON filepath.
  --storage STORAGE_FILENAME
                        Custom Google OAuth2 storage filepath.
  --sheet-ids SHEET_IDS [SHEET_IDS ...]
  --sheet-names SHEET_NAMES [SHEET_NAMES ...]
  --sheet-name-patterns SHEET_NAME_PATTERNS [SHEET_NAME_PATTERNS ...]
  --exclude-sheet-ids EXCLUDE_SHEET_IDS [EXCLUDE_SHEET_IDS ...]
  --exclude-sheet-names EXCLUDE_SHEET_NAMES [EXCLUDE_SHEET_NAMES ...]
  --exclude-sheet-name-patterns EXCLUDE_SHEET_NAME_PATTERNS [EXCLUDE_SHEET_NAME_PATTERNS ...]
  --text                Flag if files should be saved as plaintext instead of
                        CSV.
  --json                Flag if files should be saved as JSON instead of CSV.
  --info                Show information about the spreadsheet and exit.
  ```

### Destination Filename Template Usage

`-f FILENAME_TEMPLATE, --filename_template FILENAME_TEMPLATE`

If no destination filename is provided, the template defaults to `{title} - {sheet}.{ext}`, where `{title}` is the name of the spreadsheet and `{sheet}` is the name of the sheet, with any backslashes `\` removed and pipes (`|`) replaced with underscores (`_`). These keywords can also be used to create your own dynamic filename for one or more sheet downloads.

## Develop
```shell
virtualenv venv -p `which python3`
. venv/bin/activate

pip install -e . --upgrade
```
