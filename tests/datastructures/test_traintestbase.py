#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import logging
from ...datastructures.traintestbase import TrainTestBase


class TestInstantiateTrainTestBase(ut.TestCase):

    def test_error_on_number_of_transactions_not_integer(self):
        log_msg = ['ERROR:root:Attempt to instantiate data object with number'
                   ' of transactions not a positive integer.']
        err_msg = 'Number of transactions not a positive integer!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = TrainTestBase('foo', 2, {}, [])
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_number_of_transactions_too_small(self):
        log_msg = ['ERROR:root:Attempt to instantiate data object with number'
                   ' of transactions not a positive integer.']
        err_msg = 'Number of transactions not a positive integer!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ValueError, msg=err_msg) as err:
                _ = TrainTestBase(0, 2, {}, [])
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_number_of_corrupted_records_not_integer(self):
        log_msg = ['ERROR:root:Attempt to instantiate data object with number'
                   ' of corrupted records not an integer >= 0.']
        err_msg = 'Number of corrupted records not an integer >= 0!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = TrainTestBase(2, 'bar', {}, [])
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_number_of_corrupted_records_negative(self):
        log_msg = ['ERROR:root:Attempt to instantiate data object with number'
                   ' of corrupted records not an integer >= 0.']
        err_msg = 'Number of corrupted records not an integer >= 0!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ValueError, msg=err_msg) as err:
                _ = TrainTestBase(2, -1, {}, [])
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_last_unique_items_not_dictionary(self):
        log_msg = ['ERROR:root:Attempt to instantiate data object with last'
                   ' unique buys not of required type <dict>.']
        err_msg = 'Last unique items bought must be of type <dict>!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = TrainTestBase(2, 1, 'baz', [])
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_last_unique_items_empty_dictionary(self):
        log_msg = ['ERROR:root:Attempt to instantiate data object with empty'
                   ' <dict> of last unique items bought.']
        err_msg = 'Last unique items dictionary must not be empty!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ValueError, msg=err_msg) as err:
                _ = TrainTestBase(2, 1, {}, [])
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_last_unique_items_entry_not_dictionary(self):
        log_msg = ['ERROR:root:Attempt to instantiate data object with values'
                   ' in last unique item dictionary not of type <dict>.']
        err_msg = 'Last unique item values must be of type <dict>!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = TrainTestBase(2, 1, {1: 12.3}, [])
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_last_unique_items_entry_empty_dictionary(self):
        log_msg = ['ERROR:root:Attempt to instantiate data object with empty'
                   ' <dict> as entry of last unique items dictionary.']
        err_msg = 'Entries of last unique items must not be empty!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ValueError, msg=err_msg) as err:
                _ = TrainTestBase(2, 1, {1: {}}, [])
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_transactions_not_a_list(self):
        log_msg = ['ERROR:root:Attempt to instantiate data object with'
                  ' transactions not of required type <list>.']
        err_msg = 'Transactions must be of type <list>!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = TrainTestBase(2, 1, {1: {1: 23}}, 12)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_transactions_empty_list(self):
        log_msg = ['ERROR:root:Attempt to instantiate data object with empty'
                  ' transaction list.']
        err_msg = 'Transaction list must not be empty!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ValueError, msg=err_msg) as err:
                _ = TrainTestBase(2, 1, {1: {1: 23}}, [])
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_transaction_not_a_tuple(self):
        log_msg = ['ERROR:root:Attempt to instantiate data object with'
                   ' transactions not 3-tuples of strings.']
        err_msg = 'Transactions must be 3-tuples of strings!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = TrainTestBase(2, 1, {1: {1: 23}}, [2, 3])
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_transaction_tuple_too_long(self):
        log_msg = ['ERROR:root:Attempt to instantiate data object with'
                   ' transactions not 3-tuples of strings.']
        err_msg = 'Transactions must be 3-tuples of strings!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = TrainTestBase(2, 1, {1: {1: 23}}, [(1, 2, 2, 4)])
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_transaction_tuple_too_short(self):
        log_msg = ['ERROR:root:Attempt to instantiate data object with'
                   ' transactions not 3-tuples of strings.']
        err_msg = 'Transactions must be 3-tuples of strings!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = TrainTestBase(2, 1, {1: {1: 23}}, [(1, 2)])
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_transaction_tuple_not_strings(self):
        log_msg = ['ERROR:root:Attempt to instantiate data object with'
                   ' transactions not 3-tuples of strings.']
        err_msg = 'Transactions must be 3-tuples of strings!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = TrainTestBase(2, 1, {1: {1: 23}}, [(1, 2, 3)])
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)


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

    def test_cannot_set_number_of_transactions(self):
        with self.assertRaises(AttributeError):
            self.data.number_of_transactions = 123
        self.assertEqual(self.data.number_of_transactions, 21)

    def test_number_of_corrupted_records(self):
        self.assertEqual(self.data.number_of_corrupted_records, 4)

    def test_cannot_set_number_of_corrupted_records(self):
        with self.assertRaises(AttributeError):
            self.data.number_of_corrupted_records = 456
        self.assertEqual(self.data.number_of_corrupted_records, 4)

    def test_max_hold_out(self):
        self.assertEqual(self.data.max_hold_out, 2)

    def test_cannot_set_max_hold_out(self):
        with self.assertRaises(AttributeError):
            self.data.max_hold_out = 789
        self.assertEqual(self.data.max_hold_out, 2)


if __name__ == '__main__':
    ut.main()
