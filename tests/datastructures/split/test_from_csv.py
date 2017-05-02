#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import logging
from ....datastructures.split import from_csv


class BaseTests():

    def test_LogsWarningsOnCorruptedRecords(self):
        with self.assertLogs(level=logging.WARNING) as log:
            _ = from_csv(self.file, self.separator)
            self.assertEqual(log.output,
                             ['WARNING:root:Could not interpret transaction on'
                              ' line 2. Skipping.',
                              'WARNING:root:Transaction on line 3 contains'
                              ' empty fields. Skipping.',
                              'WARNING:root:Transaction on line 4 contains'
                              ' empty fields. Skipping.',
                              'WARNING:root:Could not interpret transaction on'
                               ' line 8. Skipping.',
                              'WARNING:root:Could not interpret transaction on'
                              ' line 26. Skipping.'])

    def test_TotalNumberOfRecords(self):
        with self.assertLogs(level=logging.WARNING) as log:
            n_rec, _, _, _ = from_csv(self.file, self.separator)
        self.assertEqual(n_rec, 21)

    def test_NumberOfCorruptedRecords(self):
        with self.assertLogs(level=logging.WARNING) as log:
            _, n_err, _, _ = from_csv(self.file, self.separator)
        self.assertEqual(n_err, 5)

    def test_LastUniqueUserList(self):
        should_be = ['4', '11', '10', '7']
        with self.assertLogs(level=logging.WARNING) as log:
            _, _, unique, _ = from_csv(self.file, self.separator)
        self.assertEqual(list(unique.keys()), should_be)

    def test_LastUniqueItemList(self):
        should_be = [['AC016EL50CPHALID-1749'],
                     ['CA189EL29AGOALID-170', 'LE629EL54ANHALID-345'],
                     ['OL756EL65HDYALID-4834'],
                     ['OL756EL55HAMALID-4744', 'AC016EL56BKHALID-943']]
        with self.assertLogs(level=logging.WARNING) as log:
            _, _, unique, _ = from_csv(self.file, self.separator)
        actually_is = [list(unique[user].keys()) for user in unique]
        self.assertEqual(actually_is, should_be)

    def test_LastUniqueTimes(self):
        with self.assertLogs(level=logging.WARNING) as log:
            _, _, unique, _ = from_csv(self.file, self.separator)

    def test_TransactionList(self):
        should_be = [('2012-03-06T23:26:35', '4', 'AC016EL50CPHALID-1749'),
                     ('2012-03-09T16:18:33', '11', 'CA189EL29AGOALID-170'),
                     ('2012-03-09T16:18:52', '11', 'LE629EL54ANHALID-345'),
                     ('2012-03-09T16:19:01', '10', 'OL756EL65HDYALID-4834'),
                     ('2012-03-09T16:20:14', '7', 'OL756EL55HAMALID-4744'),
                     ('2012-03-09T16:20:14', '7', 'OL756EL55HAMALID-4744'),
                     ('2012-03-09T16:20:14', '7', 'OL756EL55HAMALID-4744'),
                     ('2012-03-09T16:20:14', '7', 'OL756EL55HAMALID-4744'),
                     ('2012-03-09T16:20:14', '7', 'OL756EL55HAMALID-4744'),
                     ('2012-03-09T16:20:14', '7', 'OL756EL55HAMALID-4744'),
                     ('2012-03-09T16:20:14', '7', 'OL756EL55HAMALID-4744'),
                     ('2012-03-09T16:20:14', '7', 'OL756EL55HAMALID-4744'),
                     ('2012-03-09T16:20:14', '7', 'OL756EL55HAMALID-4744'),
                     ('2012-03-09T16:20:14', '7', 'AC016EL56BKHALID-943'),
                     ('2012-03-09T16:20:14', '7', 'AC016EL56BKHALID-943'),
                     ('2012-03-09T16:20:14', '7', 'AC016EL56BKHALID-943'),
                     ('2012-03-09T16:20:14', '7', 'AC016EL56BKHALID-943'),
                     ('2012-03-09T16:20:14', '7', 'AC016EL56BKHALID-943'),
                     ('2012-03-09T16:20:14', '7', 'AC016EL56BKHALID-943'),
                     ('2012-03-09T16:20:14', '7', 'AC016EL56BKHALID-943'),
                     ('2012-03-09T16:20:14', '7', 'AC016EL56BKHALID-943')]
        with self.assertLogs(level=logging.WARNING) as log:
            _, _, _, transactions = from_csv(self.file, self.separator)
        self.assertEqual(should_be, transactions)


class TestUserItemMatrixFromCsvSemicolonFile(ut.TestCase, BaseTests):
    def setUp(self):
        self.file = './bestPy/tests/data/data25semicolon.csv'
        self.separator = ';'


if __name__ == '__main__':
    ut.main()
