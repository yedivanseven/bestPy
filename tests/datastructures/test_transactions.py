#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import logging
import scipy
from ...datastructures import Transactions
from ...datastructures.help import IndexFrom, MatrixFrom


class TestInstantiateTransactions(ut.TestCase):

    def setUp(self):
        file = './bestPy/tests/data/data25comma.csv'
        with self.assertLogs(level=logging.WARNING):
             self.data = Transactions.from_csv(file, ',')

    def test_error_on_wrong_type_of_number_of_transactions(self):
        log_msg = ['ERROR:root:Attempt to instantiate data object with number'
                   ' of valid transactions not a positive integer.']
        err_msg = 'Number of valid transactions not a positive integer!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = Transactions(12.3, 0, 1, 1, 1)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_non_positive_number_of_transactions(self):
        log_msg = ['ERROR:root:Attempt to instantiate data object with number'
                   ' of valid transactions not a positive integer.']
        err_msg = 'Number of valid transactions not a positive integer!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ValueError, msg=err_msg) as err:
                _ = Transactions(0, 0, 1, 1, 1)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_wrong_type_of_number_of_corrupted_records(self):
        log_msg = ['ERROR:root:Attempt to instantiate data object with number'
                   ' of corrupted records not an integer >= 0.']
        err_msg = 'Number of corrupted records not an integer >= 0!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = Transactions(2, 'foo', 1, 1, 1)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_non_positive_number_of_corrupted_records(self):
        log_msg = ['ERROR:root:Attempt to instantiate data object with number'
                   ' of corrupted records not an integer >= 0.']
        err_msg = 'Number of corrupted records not an integer >= 0!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ValueError, msg=err_msg) as err:
                _ = Transactions(1, -1, 1, 1, 1)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)


class TestTransactions(ut.TestCase):

    def setUp(self):
        file = './bestPy/tests/data/data25comma.csv'
        with self.assertLogs(level=logging.WARNING):
             self.data = Transactions.from_csv(file, ',')

    def test_has_attribute_number_of_transactions(self):
        self.assertTrue(hasattr(self.data, 'number_of_transactions'))

    def test_cannot_set_attribute_number_of_transactions(self):
        with self.assertRaises(AttributeError):
            self.data.number_of_transactions = 12.3
        self.assertEqual(self.data.number_of_transactions, 21)

    def test_type_of_attribute_number_of_transactions(self):
        self.assertIsInstance(self.data.number_of_transactions, int)

    def test_correct_value_of_attribute_number_of_transactions(self):
        self.assertEqual(self.data.number_of_transactions, 21)

    def test_has_attribute_number_of_corrupted_records(self):
        self.assertTrue(hasattr(self.data, 'number_of_corrupted_records'))

    def test_cannot_set_attribute_number_of_corrupted_records(self):
        with self.assertRaises(AttributeError):
            self.data.number_of_corrupted_records = 'foo'
        self.assertEqual(self.data.number_of_corrupted_records, 5)

    def test_type_of_attribute_number_of_corrupted_records(self):
        self.assertIsInstance(self.data.number_of_corrupted_records, int)

    def test_correct_value_of_attribute_number_of_corrupted_records(self):
        self.assertEqual(self.data.number_of_corrupted_records, 5)

    def test_has_attribute_number_of_userItem_pairs(self):
        self.assertTrue(hasattr(self.data, 'number_of_userItem_pairs'))

    def test_cannot_set_attribute_number_of_userItem_pairs(self):
        with self.assertRaises(AttributeError):
            self.data.number_of_userItem_pairs = 'bar'
        self.assertEqual(self.data.number_of_userItem_pairs, 6)

    def test_type_of_attribute_number_of_userItem_pairs(self):
        self.assertIsInstance(self.data.number_of_userItem_pairs, int)

    def test_correct_value_of_attribute_number_of_userItem_pairs(self):
        self.assertEqual(self.data.number_of_userItem_pairs, 6)

    def test_has_attribute_user(self):
        self.assertTrue(hasattr(self.data, 'user'))

    def test_cannot_set_attribute_user(self):
        with self.assertRaises(AttributeError):
            self.data.user = 45.6

    def test_type_of_attribute_user(self):
        self.assertIsInstance(self.data.user, IndexFrom)

    def test_correct_value_of_user(self):
        should_be = {'4': 0, '11': 1, '10': 2, '7': 3}
        self.assertDictEqual(self.data.user.index_of, should_be)

    def test_has_attribute_item(self):
        self.assertTrue(hasattr(self.data, 'item'))

    def test_cannot_set_attribute_item(self):
        with self.assertRaises(AttributeError):
            self.data.item = 'baz'

    def test_type_of_attribute_item(self):
        self.assertIsInstance(self.data.item, IndexFrom)

    def test_correct_value_of_item(self):
        should_be = {'AC016EL50CPHALID-1749': 0,
                     'CA189EL29AGOALID-170' : 1,
                     'LE629EL54ANHALID-345' : 2,
                     'OL756EL65HDYALID-4834': 3,
                     'OL756EL55HAMALID-4744': 4,
                     'AC016EL56BKHALID-943' : 5}
        self.assertDictEqual(self.data.item.index_of, should_be)

    def test_has_attribute_matrix(self):
        self.assertTrue(hasattr(self.data, 'matrix'))

    def test_cannot_set_attribute_matrix(self):
        with self.assertRaises(AttributeError):
            self.data.item = 7.89

    def test_type_of_attribute_matrix(self):
        self.assertIsInstance(self.data.matrix, MatrixFrom)

    def test_correct_value_of_matrix(self):
        should_be = [[1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 9.0, 8.0]]
        actually_is = self.data.matrix.by_col.toarray().tolist()
        self.assertListEqual(should_be, actually_is)

    def test_users_who_bought(self):
        should_be = [[0], [1], [1], [2], [3], [3]]
        actual = [self.data.users_who_bought(i).tolist() for i in range(6)]
        self.assertListEqual(should_be, actual)


if __name__ == '__main__':
    ut.main()
