#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import unittest as ut
from ....datastructures.auxiliary import TestDataFrom
from ....datastructures import TrainTest, Transactions


class TestTrainTest(ut.TestCase):

    def setUp(self):
        file = './bestPy/tests/data/data25sequential.csv'
        fmt = '%Y-%m-%d %H:%M:%S'
        self.data = TrainTest.from_csv(file, ';', fmt)

    def test_no_attribute_train_before_split(self):
        with self.assertRaises(AttributeError):
            _ = self.data.train

    def test_no_attribute_test_before_split(self):
        with self.assertRaises(AttributeError):
            _ = self.data.test

    def test_split_only_new_not_boolean(self):
        log_msg = ['ERROR:root:Attempt to set "only_new" to non-boolean type.']
        err_msg = 'Flag "only_new" can only be True or False!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                self.data.split(2, only_new='foo')
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_split_hold_out_not_integer(self):
        log_msg = ['ERROR:root:Attempt to set "hold_out" to non-integer type.']
        err_msg = 'Parameter "hold_out" must be an integer!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                self.data.split('bar')
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_split_hold_smaller_than_one(self):
        log_msg = ['WARNING:root:Attempt to set hold_out < 1. Resetting to 1.']
        with self.assertLogs(level=logging.WARNING) as log:
            self.data.split(-3)
        self.assertEqual(log.output, log_msg)

    def test_split_hold_out_greater_than_maximum(self):
        log_msg = ['WARNING:root:Hold_out > meaningful maximum of 2.'
                   ' Resetting to 2.',
                   'ERROR:root:Attempt to instantiate data object with number'
                   ' of valid transactions not a positive integer.']
        err_msg = 'Number of valid transactions not a positive integer!'
        with self.assertLogs(level=logging.WARNING) as log:
            with self.assertRaises(ValueError, msg=err_msg) as err:
                self.data.split(7)
        self.assertListEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_no_error_on_multiple_calls_to_split(self):
        self.data.split(2, only_new=False)
        self.data.split(1)

    def test_has_atrribute_test_after_split(self):
        self.data.split(1)
        self.assertTrue(hasattr(self.data, 'test'))

    def test_cannot_set_attribute_test_after_split(self):
        self.data.split(1)
        with self.assertRaises(AttributeError):
            self.data.test = 'foo'

    def test_other_instances_do_not_have_test_after_split(self):
        file = './bestPy/tests/data/data25sequential.csv'
        fmt = '%Y-%m-%d %H:%M:%S'
        other = TrainTest.from_csv(file, ';', fmt)
        self.data.split(1)
        self.assertFalse(hasattr(other, 'test'))

    def test_other_instances_have_different_test_after_split(self):
        file = './bestPy/tests/data/data25sequential.csv'
        fmt = '%Y-%m-%d %H:%M:%S'
        other = TrainTest.from_csv(file, ';', fmt)
        other.split(2, only_new=False)
        self.data.split(1)
        self.assertNotEqual(other.test.number_of_cases,
                            self.data.test.number_of_cases)

    def test_test_type(self):
        self.data.split(1)
        self.assertIsInstance(self.data.test, TestDataFrom)

    def test_test_data(self):
        should_be = {'12': {'SA848EL83DOYALID-2416', 'BL152EL82CRXALID-1817'},
                     '11': {'LE629EL54ANHALID-345', 'CA189EL29AGOALID-170'},
                     '7' : {'AC016EL56BKHALID-943', 'OL756EL55HAMALID-4744'}}
        with self.assertLogs(level=logging.ERROR):
            with self.assertRaises(ValueError):
                self.data.split(2, only_new=True)
        self.assertDictEqual(self.data.test.data, should_be)
        self.data.split(2, only_new=False)
        self.assertDictEqual(self.data.test.data, should_be)

    def test_test_only_new_true(self):
        self.data.split(1, only_new=True)
        self.assertTrue(self.data.test.only_new)

    def test_test_only_new_false(self):
        self.data.split(1, only_new=False)
        self.assertFalse(self.data.test.only_new)

    def test_test_hold_out(self):
        with self.assertLogs(level=logging.WARNING):
            with self.assertRaises(ValueError):
                self.data.split(2, only_new=True)
        self.assertEqual(self.data.test.hold_out, 2)
        self.data.split(2, only_new=False)
        self.assertEqual(self.data.test.hold_out, 2)

    def test_test_number_of_cases(self):
        self.data.split(1, only_new=True)
        self.assertEqual(self.data.test.number_of_cases, 6)
        self.data.split(1, only_new=False)
        self.assertEqual(self.data.test.number_of_cases, 6)

    def test_has_atrribute_train_after_split(self):
        self.data.split(1)
        self.assertTrue(hasattr(self.data, 'train'))

    def test_cannot_set_attribute_train_after_split(self):
        self.data.split(1)
        with self.assertRaises(AttributeError):
            self.data.train = 'bar'

    def test_other_instances_do_not_have_train_after_split(self):
        file = './bestPy/tests/data/data25sequential.csv'
        fmt = '%Y-%m-%d %H:%M:%S'
        other = TrainTest.from_csv(file, ';', fmt)
        self.data.split(1)
        self.assertFalse(hasattr(other, 'train'))

    def test_other_instances_have_different_train_after_split(self):
        file = './bestPy/tests/data/data25sequential.csv'
        fmt = '%Y-%m-%d %H:%M:%S'
        other = TrainTest.from_csv(file, ';', fmt)
        other.split(2, only_new=False)
        self.data.split(1)
        self.assertNotEqual(other.train.number_of_transactions,
                            self.data.train.number_of_transactions)

    def test_train_type(self):
         self.data.split(1)
         self.assertIsInstance(self.data.train, Transactions)

    def test_train_number_of_corrupted_records(self):
        self.data.split(1, only_new=True)
        self.assertEqual(self.data.train.number_of_corrupted_records, 0)
        self.data.split(1, only_new=False)
        self.assertEqual(self.data.train.number_of_corrupted_records, 0)

    def test_train_number_of_transactions_only_new(self):
        self.data.split(1)
        self.assertEqual(self.data.train.number_of_transactions, 12)

    def test_train_userIndex_of_only_new(self):
        should_be = {'12': 0, '11': 1, '7': 2}
        self.data.split(1)
        self.assertDictEqual(self.data.train.user.index_of, should_be)

    def test_train_itemIndex_of_only_new(self):
        should_be = {'SA848EL83DOYALID-2416': 0,
                     'CA189EL29AGOALID-170' : 1,
                     'OL756EL55HAMALID-4744': 2}
        self.data.split(1)
        self.assertDictEqual(self.data.train.item.index_of, should_be)

    def test_train_userID_of_only_new(self):
        should_be = {0: '12', 1: '11', 2: '7'}
        self.data.split(1)
        self.assertDictEqual(self.data.train.user.id_of, should_be)

    def test_train_itemID_of_only_new(self):
        should_be = {0: 'SA848EL83DOYALID-2416',
                     1: 'CA189EL29AGOALID-170',
                     2: 'OL756EL55HAMALID-4744'}
        self.data.split(1)
        self.assertDictEqual(self.data.train.item.id_of, should_be)

    def test_train_number_of_users_only_new(self):
        self.data.split(1)
        self.assertEqual(self.data.train.user.count, 3)

    def test_train_number_of_items_only_new(self):
        self.data.split(1)
        self.assertEqual(self.data.train.item.count, 3)

    def test_train_number_of_transactions_also_old(self):
        self.data.split(1, only_new=False)
        self.assertEqual(self.data.train.number_of_transactions, 19)

    def test_train_userIndex_of_also_old(self):
        should_be = {'12': 0, '11': 1, '7': 2}
        self.data.split(1, only_new=False)
        self.assertDictEqual(self.data.train.user.index_of, should_be)

    def test_train_itemIndex_of_also_old(self):
        should_be = {'SA848EL83DOYALID-2416': 0,
                     'CA189EL29AGOALID-170' : 1,
                     'OL756EL55HAMALID-4744': 2,
                     'AC016EL56BKHALID-943' : 3}
        self.data.split(1, only_new=False)
        self.assertDictEqual(self.data.train.item.index_of, should_be)

    def test_train_userID_of_also_old(self):
        should_be = {0: '12', 1: '11', 2: '7'}
        self.data.split(1, only_new=False)
        self.assertDictEqual(self.data.train.user.id_of, should_be)

    def test_train_itemID_of_also_old(self):
        should_be = {0: 'SA848EL83DOYALID-2416',
                     1: 'CA189EL29AGOALID-170',
                     2: 'OL756EL55HAMALID-4744',
                     3: 'AC016EL56BKHALID-943'}
        self.data.split(1, only_new=False)
        self.assertDictEqual(self.data.train.item.id_of, should_be)

    def test_train_number_of_users_also_old(self):
        self.data.split(1, only_new=False)
        self.assertEqual(self.data.train.user.count, 3)

    def test_train_number_of_items_also_old(self):
        self.data.split(1, only_new=False)
        self.assertEqual(self.data.train.item.count, 4)


if __name__ == '__main__':
    ut.main()
