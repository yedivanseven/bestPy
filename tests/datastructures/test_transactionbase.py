#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import logging
from ...datastructures.transactionbase import TransactionBase


class TestTransactionBase(ut.TestCase):

    def setUp(self):
        file = './bestPy/tests/data/data25semicolon.csv'
        with self.assertLogs(level=logging.WARNING):
            self.data = TransactionBase.from_csv(file)

    def test_number_of_transactions(self):
        self.assertEqual(self.data.number_of_transactions, 21)

    def test_set_number_of_transactions(self):
        with self.assertRaises(AttributeError):
            self.data.number_of_transactions = 23
        self.assertEqual(self.data.number_of_transactions, 21)

    def test_number_of_corrupted_records(self):
        self.assertEqual(self.data.number_of_corrupted_records, 5)

    def test_set_number_of_corrupted_records(self):
        with self.assertRaises(AttributeError):
            self.data.number_of_corrupted_records = 8
        self.assertEqual(self.data.number_of_corrupted_records, 5)

    def test_userIndex_of(self):
        should_be = {'4': 0, '11': 1, '10': 2, '7': 3}
        self.assertEqual(self.data.userIndex_of, should_be)

    def test_set_userIndex_of(self):
        should_be = {'4': 0, '11': 1, '10': 2, '7': 3}
        with self.assertRaises(AttributeError):
            self.data.userIndex_of = 'foo'
        self.assertEqual(self.data.userIndex_of, should_be)

    def test_itemIndexof(self):
        should_be = {'AC016EL50CPHALID-1749': 0,
                     'CA189EL29AGOALID-170' : 1,
                     'LE629EL54ANHALID-345' : 2,
                     'OL756EL65HDYALID-4834': 3,
                     'OL756EL55HAMALID-4744': 4,
                     'AC016EL56BKHALID-943' : 5}
        self.assertEqual(self.data.itemIndex_of, should_be)

    def test_set_intemIndex_of(self):
        should_be = {'AC016EL50CPHALID-1749': 0,
                     'CA189EL29AGOALID-170' : 1,
                     'LE629EL54ANHALID-345' : 2,
                     'OL756EL65HDYALID-4834': 3,
                     'OL756EL55HAMALID-4744': 4,
                     'AC016EL56BKHALID-943' : 5}
        with self.assertRaises(AttributeError):
            self.data.itemIndex_of = 'bar'
        self.assertEqual(self.data.itemIndex_of, should_be)

    def test_count_buys_of(self):
        should_be = {(0, 0): 1,
                     (1, 1): 1,
                     (1, 2): 1,
                     (2, 3): 1,
                     (3, 4): 9,
                     (3, 5): 8}
        self.assertEqual(self.data._count_buys_of, should_be)

    def test_set_count_buys_of(self):
        should_be = {(0, 0): 1,
                     (1, 1): 1,
                     (1, 2): 1,
                     (2, 3): 1,
                     (3, 4): 9,
                     (3, 5): 8}
        with self.assertRaises(AttributeError):
            self.data._count_buys_of = 'baz'
        self.assertEqual(self.data._count_buys_of, should_be)


if __name__ == '__main__':
    ut.main()
