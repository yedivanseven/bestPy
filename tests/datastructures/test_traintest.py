#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import logging
from ...datastructures.traintestbase import TestDataFrom
from ...datastructures import TrainTest, UserItemMatrix


class TestTrainTest(ut.TestCase):

    def setUp(self):
        file = './bestPy/tests/data/data25timestamp_fmt.csv'
        fmt = '%Y-%m-%d %H:%M:%S'
        with self.assertLogs(level=logging.WARNING):
            self.data = TrainTest.from_csv(file, ';', fmt)

    def test_no_attribute_train_before_split(self):
        with self.assertRaises(AttributeError):
            _ = self.data.train

    def test_no_attribute_test_before_split(self):
        with self.assertRaises(AttributeError):
            _ = self.data.test

    def test_has_atrribute_train_after_split(self):
        self.data.split(2)
        self.assertTrue(hasattr(self.data, 'train'))

    def test_has_atrribute_test_after_split(self):
        self.data.split(1)
        self.assertTrue(hasattr(self.data, 'test'))

    def test_test_type(self):
        self.data.split(2)
        self.assertIsInstance(self.data.test, TestDataFrom)

    def test_test_data(self):
        should_be = {'12': {'SA848EL83DOYALID-2416', 'BL152EL82CRXALID-1817'},
                     '7' : {'OL756EL55HAMALID-4744', 'AC016EL56BKHALID-943'}}
        self.data.split(2)
        self.assertDictEqual(self.data.test.data, should_be)

    def test_test_only_new_true(self):
        self.data.split(1, only_new=True)
        self.assertTrue(self.data.test.only_new)

    def test_test_only_new_false(self):
        self.data.split(1, only_new=False)
        self.assertFalse(self.data.test.only_new)

    def test_test_hold_out(self):
        self.data.split(2)
        self.assertEqual(self.data.test.hold_out, 2)

    def test_test_number_of_cases(self):
        self.data.split(1)
        self.assertEqual(self.data.test.number_of_cases, 5)

    def test_train_type(self):
         self.data.split(2)
         self.assertIsInstance(self.data.train, UserItemMatrix)

    def test_train_number_of_corrupted_records(self):
        self.data.split(1)
        self.assertEqual(self.data.train.number_of_corrupted_records, 0)

    def test_train_number_of_transactions(self):
        self.data.split(1)
        self.assertEqual(self.data.train.number_of_transactions, 9)

    def test_train(self):
        # TODO: continue testing the actual training data here!
        print('\nTODO: Continue testing the actual training data!')


if __name__ == '__main__':
    ut.main()
