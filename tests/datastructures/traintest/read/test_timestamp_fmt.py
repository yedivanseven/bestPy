#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import datetime as dt
import logging
from .....datastructures.traintest.read import from_csv


class TestTrainTestFromCsvFileTimestampFmt(ut.TestCase):

    def setUp(self):
        self.file = './bestPy/tests/data/data25timestamp_fmt.csv'
        self.separator = ';'
        self.fmt = '%Y-%m-%d %H:%M:%S'

    def test_logs_warnings_on_corrupted_timestamps(self):
        log_msg = ['WARNING:root:Failed to read timestamp. Check that it'
                   ' adheres to the given format "%Y-%m-%d %H:%M:%S".',
                   'WARNING:root:Could not interpret timestamp on'
                   ' line 2. Skipping.',
                   'WARNING:root:Failed to read timestamp. Check that it'
                   ' adheres to the given format "%Y-%m-%d %H:%M:%S".',
                   'WARNING:root:Could not interpret timestamp on'
                   ' line 5. Skipping.',
                   'WARNING:root:Failed to read timestamp. Check that it'
                   ' adheres to the given format "%Y-%m-%d %H:%M:%S".',
                   'WARNING:root:Could not interpret timestamp on'
                   ' line 11. Skipping.',
                   'WARNING:root:Failed to read timestamp. Check that it'
                   ' adheres to the given format "%Y-%m-%d %H:%M:%S".',
                   'WARNING:root:Could not interpret timestamp on'
                   ' line 17. Skipping.']
        with self.assertLogs(level=logging.WARNING) as log:
            _, _, _, _ = from_csv(self.file, self.separator, self.fmt)
        self.assertListEqual(log.output, log_msg)

    def test_total_number_of_records(self):
        with self.assertLogs(level=logging.WARNING):
            n_rec, _, _, _ = from_csv(self.file, self.separator, self.fmt)
        self.assertEqual(n_rec, 21)

    def test_number_of_corrupted_records(self):
        with self.assertLogs(level=logging.WARNING):
            _, n_err, _, _ = from_csv(self.file, self.separator, self.fmt)
        self.assertEqual(n_err, 4)

    def test_datetimes(self):
        should_be = ['2012-03-06T23:26:35', '2012-03-09T16:18:02',
                     '2012-03-09T16:18:02', '2012-03-09T16:18:52',
                     '2012-03-09T16:19:01', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14']
        with self.assertLogs(level=logging.WARNING):
            _, _, _, transacts = from_csv(self.file, self.separator, self.fmt)
        datetimes = [transact[0] for transact in transacts]
        self.assertListEqual(datetimes, should_be)


if __name__ == '__main__':
    ut.main()
