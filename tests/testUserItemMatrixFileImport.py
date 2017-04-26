#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import logging
from ..datastructures.read import from_csv

class TestUserItemMatrixFileImport(ut.TestCase):

    def setUp(self):
        self.file = './data/head100.csv'

    def test_LogsWarningOnReadingCorruptedRecords(self):
        with self.assertLogs(level=logging.WARNING) as log:
            n_rec, n_err, user_i, itme_j, counts = from_csv(self.file)
            self.assertEqual(log.output,
                             ['WARNING:root:Could not interpret transaction '
                              'on line 101. Skipping.'])

    def test_TotalNumberOfRecordsReadFromFile(self):
        with self.assertLogs(level=logging.WARNING) as log:
            n_rec, n_err, user_i, itme_j, counts = from_csv(self.file)
            self.assertEqual(n_rec, 100)

    def test_NumberOfCorruptedRecordsReadFromFile(self):
        with self.assertLogs(level=logging.WARNING) as log:
            n_rec, n_err, user_i, itme_j, counts = from_csv(self.file)
            self.assertEqual(n_err, 1)

if __name__ == '__main__':
    ut.main()
