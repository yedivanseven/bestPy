#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import logging
from ....datastructures.read import from_csv
from ....datastructures.traintestbase import FileFrom

class TestUserItemMatrixFromCsvList(ut.TestCase):

    def setUp(self):
        self.list = iter(('1331072795;4;AC016EL50CPHALID-1749',
                          '1331074425;1;AC016EL67BJWALID-932;',
                          '1331306282;;SA848EL83DOYALID-2416',
                          '1331306282;12;',
                          '1331306313;11;CA189EL29AGOALID-170',
                          '1331306332;11;LE629EL54ANHALID-345',
                          '1331306341;10;OL756EL65HDYALID-4834',
                          '1331306414;7',
                          '1331306414;7;OL756EL55HAMALID-4744',
                          '1331306414;7;OL756EL55HAMALID-4744',
                          '1331306414;7;OL756EL55HAMALID-4744',
                          '1331306414;7;OL756EL55HAMALID-4744',
                          '1331306414;7;OL756EL55HAMALID-4744',
                          '1331306414;7;OL756EL55HAMALID-4744',
                          '1331306414;7;OL756EL55HAMALID-4744',
                          '1331306414;7;OL756EL55HAMALID-4744',
                          '1331306414;7;OL756EL55HAMALID-4744',
                          '1331306414;7;AC016EL56BKHALID-943',
                          '1331306414;7;AC016EL56BKHALID-943',
                          '1331306414;7;AC016EL56BKHALID-943',
                          '1331306414;7;AC016EL56BKHALID-943',
                          '1331306414;7;AC016EL56BKHALID-943',
                          '1331306414;7;AC016EL56BKHALID-943',
                          '1331306414;7;AC016EL56BKHALID-943',
                          '1331306414;7;AC016EL56BKHALID-943',
                          '\n'))
        self.file = FileFrom(self.list)
        self.user_i_should_be = {'4': 0, '11': 1, '10': 2, '7': 3}
        self.item_j_should_be = {'AC016EL50CPHALID-1749': 0,
                                 'CA189EL29AGOALID-170' : 1,
                                 'LE629EL54ANHALID-345' : 2,
                                 'OL756EL65HDYALID-4834': 3,
                                 'OL756EL55HAMALID-4744': 4,
                                 'AC016EL56BKHALID-943' : 5}
        self.counts_should_be = {(0, 0): 1,
                                 (1, 1): 1,
                                 (1, 2): 1,
                                 (2, 3): 1,
                                 (3, 4): 9,
                                 (3, 5): 8}

    def test_LogsWarningsOnCorruptedRecords(self):
        with self.assertLogs(level=logging.WARNING) as log:
            _ = from_csv(self.file)
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
            n_rec, _, _, _, _ = from_csv(self.file)
            self.assertEqual(n_rec, 21)

    def test_NumberOfCorruptedRecords(self):
        with self.assertLogs(level=logging.WARNING) as log:
            _, n_err, _, _, _ = from_csv(self.file)
            self.assertEqual(n_err, 5)

    def test_UserIndexDict(self):
        with self.assertLogs(level=logging.WARNING) as log:
            _, _, user_i, _, _ = from_csv(self.file)
            self.assertEqual(self.user_i_should_be, user_i)

    def test_ItemIndexDict(self):
        with self.assertLogs(level=logging.WARNING) as log:
            _, _, _, item_j, _ = from_csv(self.file)
            self.assertEqual(self.item_j_should_be, item_j)

    def test_UserItemCountsDict(self):
        with self.assertLogs(level=logging.WARNING) as log:
            _, _, _, _, counts = from_csv(self.file)
            self.assertEqual(self.counts_should_be, counts)

if __name__ == '__main__':
    ut.main()
