import datetime
import logging
import logging.config
import pathlib
import pytest
import unittest

import sheetid
from db_gglsheet import DbGGlSheet


class Test_DbGGlSheet(unittest.TestCase):

    def setUp(self):
        current_dir = pathlib.Path(__file__).parent
        logfile = current_dir.joinpath('config/logging.conf')
        logging.config.fileConfig(logfile)
        self.syslog_fname_test = current_dir.joinpath('files/inp_system.tst')

        self.logger = logging.getLogger('dbg')
        self.db_ggl_sheet = DbGGlSheet(self.logger)
        logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

    @unittest.skip("just temporary")
    @pytest.mark.short
    def test_create(self):
        self.logger.debug('START TEST test_create')
        sheetID = self.db_ggl_sheet.create("Hola Ho")
        self.logger.debug('END TEST test_create sheetID: {}'.format(sheetID))

    @unittest.skip("just temporary")
    @pytest.mark.short
    def test_append_values(self):
        self.logger.debug('START TEST test_append_values')
        values = [[1, 2], [3, 6]]
        self.append_values(values)

    def append_values(self, values):
        RANGE_NAME = 'Event'
        self.logger.debug('START TEST test_append_values')
        self.logger.debug('Values : {}'.format(values))
        self.db_ggl_sheet.append_values(sheetid.SPREADSHEET_ID, RANGE_NAME, 'USER_ENTERED', values)

    def test_append_event_list(self):
        ev_list = [{
            'IPAddr': '51.136.19.83',
            'EventTime': datetime.datetime(2018, 9, 8, 19, 16, 29).isoformat(' ')
        }, {
            'IPAddr': '51.136.19.83',
            'EventTime': datetime.datetime(2018, 9, 8, 19, 16, 29).isoformat(' ')
        }, {
            'IPAddr': '2a03:2880:f007:0001:face:b00c:0000:0001',
            'EventTime': datetime.datetime(2018, 9, 8, 19, 47, 30).isoformat(' ')
        }, {
            'IPAddr': '2a03:2880:f007:0001:face:b00c:0000:0001',
            'EventTime': datetime.datetime(2017, 10, 8, 20, 47, 30).isoformat(' ')
        }]
        values = []
        for ev in ev_list:
            values.append([ev['EventTime'], ev['IPAddr']])
        self.append_values(values)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
