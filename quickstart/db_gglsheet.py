import logging
import logging.config
import pathlib

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from typing import List


class DbGGlSheet(object):
    """
    It processes data from the list of events
    and saves it to Google Sheet
    
    Methods:
        process_events(ev_list:List, ev_src:str, ev_type:str = None, ev_info:str = None)
    """

    def __init__(self, logger=None):
        current_dir = pathlib.Path(__file__).parent
        if logger is None:
            logfile = current_dir.joinpath('config/logging.conf')
            logging.config.fileConfig(logfile)
            logger = logging.getLogger('dbg')
        self.logger = logger
        self.logger.debug('DbGGlSheet.__init__')

        # Initialize Google Sheets

        # If modifying these scopes, delete the file token.json.
        # SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
        SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

        store = file.Storage(current_dir.joinpath('config/token.json'))
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(current_dir.joinpath('config/credentials.json'), SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('sheets', 'v4', http=creds.authorize(Http()), cache_discovery=False)

    def create(self, title):
        """Create new sheet with title
        
        Arguments:
            title {str} -- sheet title
        
        Returns:
            str -- SheetId
        """
        service = self.service
        # [START sheets_create]
        spreadsheet = {'properties': {'title': title}}
        spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
        self.logger.debug('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))
        # [END sheets_create]
        return spreadsheet.get('spreadsheetId')

    def append_values(self, spreadsheet_id, range_name, value_input_option, _values):
        service = self.service
        self.logger.debug('DbGGlSheet.append_values SpreadsheetID: {}, RangeName: {}'.format(
            spreadsheet_id, range_name))
        # [START sheets_append_values]
        values = [
            [
                # Cell values ...
            ],
            # Additional rows ...
        ]
        # [START_EXCLUDE silent]
        values = _values
        # [END_EXCLUDE]
        body = {'values': values}
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name, valueInputOption=value_input_option, body=body).execute()
        print('{0} cells appended.'.format(result.get('updates').get('updatedCells')))
        # [END sheets_append_values]
        return result

    def process_events(self, ev_list: List, ev_src: str, ev_type: str = None, ev_info: str = None) -> int:
        """
        Processes event list:
            - Saves data to table of events
            -

        Arguments:
            ev_list {List} -- List of events with following structure
                {'IPAddr': '51.136.19.83',
                 'EventTime': datetime.datetime(2018, 9, 8, 19, 16, 29)}
            ev_src {str} -- Source of events (syslog, ....)
            ev_type {str} -- Optional parameter, if needed
            ev_info {str} -- [description] (default: {None})
        
        Returns:
            int -- error code (0 if OK)
        """
        retVal = -1
        if (not ev_list):
            return 0

        return retVal


if __name__ == "__main__":
    pass
