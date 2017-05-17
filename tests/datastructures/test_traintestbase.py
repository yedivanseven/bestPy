#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import logging
from ...datastructures.traintestbase import TrainTestBase


class TestTrainTestBase(ut.TestCase):

    def setUp(self):
        file = './bestPy/tests/data/data25timestamp_fmt.csv'
        fmt = '%Y-%m-%d %H:%M:%S'
        with self.assertLogs(level=logging.WARNING):
            self.data = TrainTestBase.from_csv(file, ';', fmt)

    def test_has_attribute_number_of_transactions(self):
        self.assertTrue(hasattr(self.data, 'number_of_transactions'))

    def test_number_of_transactions(self):
        self.assertEqual(self.data.number_of_transactions, 21)

    def test_set_number_of_transactions(self):
        with self.assertRaises(AttributeError):
            self.data.number_of_transactions = 123
        self.assertEqual(self.data.number_of_transactions, 21)

    def test_number_of_corrupted_records(self):
        self.assertEqual(self.data.number_of_corrupted_records, 4)

    def test_set_number_of_corrupted_records(self):
        with self.assertRaises(AttributeError):
            self.data.number_of_corrupted_records = 456
        self.assertEqual(self.data.number_of_corrupted_records, 4)

    def test_max_hold_out(self):
        self.assertEqual(self.data.max_hold_out, 2)

    def test_set_max_hold_out(self):
        with self.assertRaises(AttributeError):
            self.data.max_hold_out = 789
        self.assertEqual(self.data.max_hold_out, 2)


if __name__ == '__main__':
    ut.main()
