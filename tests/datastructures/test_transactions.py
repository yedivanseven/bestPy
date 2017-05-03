#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import logging
from ...datastructures.transactions import Transactions


class TestTransactions(ut.TestCase):

    def setUp(self):
        file = './bestPy/tests/data/data25comma.csv'
        with self.assertLogs(level=logging.WARNING):
            self.data = Transactions.from_csv(file, ',')

    def test_number_of_users(self):
        self.assertEqual(self.data.number_of_users, 4)

    def test_set_number_of_users(self):
        with self.assertRaises(AttributeError):
            self.data.number_of_users = 23
        self.assertEqual(self.data.number_of_users, 4)

    def test_number_of_items(self):
        self.assertEqual(self.data.number_of_items, 6)

    def test_set_number_of_items(self):
        with self.assertRaises(AttributeError):
            self.data.number_of_items = 45
        self.assertEqual(self.data.number_of_items, 6)

    def test_userID_of(self):
        should_be = {0: '4', 1: '11', 2: '10', 3: '7'}
        self.assertEqual(self.data.userID_of, should_be)

    def test_set_userID_of(self):
        should_be = {0: '4', 1: '11', 2: '10', 3: '7'}
        with self.assertRaises(AttributeError):
            self.data.userID_of = 'foo'
        self.assertEqual(self.data.userID_of, should_be)

    def test_itemID_of(self):
        should_be = {0: 'AC016EL50CPHALID-1749',
                     1: 'CA189EL29AGOALID-170',
                     2: 'LE629EL54ANHALID-345',
                     3: 'OL756EL65HDYALID-4834',
                     4: 'OL756EL55HAMALID-4744',
                     5: 'AC016EL56BKHALID-943'}
        self.assertEqual(self.data.itemID_of, should_be)

    def test_set_itemID_of(self):
        should_be = {0: 'AC016EL50CPHALID-1749',
                     1: 'CA189EL29AGOALID-170',
                     2: 'LE629EL54ANHALID-345',
                     3: 'OL756EL65HDYALID-4834',
                     4: 'OL756EL55HAMALID-4744',
                     5: 'AC016EL56BKHALID-943'}
        with self.assertRaises(AttributeError):
            self.data.itemID_of = 'bar'
        self.assertEqual(self.data.itemID_of, should_be)


if __name__ == '__main__':
    ut.main()
