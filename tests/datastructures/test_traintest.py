#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
from ...datastructures.traintestbase import TestDataFrom
from ...datastructures import TrainTest, UserItemMatrix


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
                     '11': {'LE629EL54ANHALID-345', 'CA189EL29AGOALID-170'},
                     '7' : {'AC016EL56BKHALID-943', 'OL756EL55HAMALID-4744'}}
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
        self.data.split(2, only_new=True)
        self.assertEqual(self.data.test.hold_out, 2)
        self.data.split(2, only_new=False)
        self.assertEqual(self.data.test.hold_out, 2)

    def test_test_number_of_cases(self):
        self.data.split(1, only_new=True)
        self.assertEqual(self.data.test.number_of_cases, 6)
        self.data.split(1, only_new=False)
        self.assertEqual(self.data.test.number_of_cases, 6)

    def test_train_type(self):
         self.data.split(2)
         self.assertIsInstance(self.data.train, UserItemMatrix)

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
        self.assertDictEqual(self.data.train.userIndex_of, should_be)

    def test_train_itemIndex_of_only_new(self):
        should_be = {'SA848EL83DOYALID-2416': 0,
                     'CA189EL29AGOALID-170' : 1,
                     'OL756EL55HAMALID-4744': 2}
        self.data.split(1)
        self.assertDictEqual(self.data.train.itemIndex_of, should_be)

    def test_train_userID_of_only_new(self):
        should_be = {0: '12', 1: '11', 2: '7'}
        self.data.split(1)
        self.assertDictEqual(self.data.train.userID_of, should_be)

    def test_train_itemID_of_only_new(self):
        should_be = {0: 'SA848EL83DOYALID-2416',
                     1: 'CA189EL29AGOALID-170',
                     2: 'OL756EL55HAMALID-4744'}
        self.data.split(1)
        self.assertDictEqual(self.data.train.itemID_of, should_be)

    def test_train_number_of_users_only_new(self):
        self.data.split(1)
        self.assertEqual(self.data.train.number_of_users, 3)

    def test_train_number_of_items_only_new(self):
        self.data.split(1)
        self.assertEqual(self.data.train.number_of_items, 3)

    def test_train_count_buys_of_only_new(self):
        should_be = {(0, 0): 1, (1, 1): 1, (2, 2): 10}
        self.data.split(1)
        self.assertDictEqual(self.data.train._count_buys_of, should_be)

    def test_train_number_of_transactions_also_old(self):
        self.data.split(1, only_new=False)
        self.assertEqual(self.data.train.number_of_transactions, 19)

    def test_train_userIndex_of_also_old(self):
        should_be = {'12': 0, '11': 1, '7': 2}
        self.data.split(1, only_new=False)
        self.assertDictEqual(self.data.train.userIndex_of, should_be)

    def test_train_itemIndex_of_also_old(self):
        should_be = {'SA848EL83DOYALID-2416': 0,
                     'CA189EL29AGOALID-170' : 1,
                     'OL756EL55HAMALID-4744': 2,
                     'AC016EL56BKHALID-943' : 3}
        self.data.split(1, only_new=False)
        self.assertDictEqual(self.data.train.itemIndex_of, should_be)

    def test_train_userID_of_also_old(self):
        should_be = {0: '12', 1: '11', 2: '7'}
        self.data.split(1, only_new=False)
        self.assertDictEqual(self.data.train.userID_of, should_be)

    def test_train_itemID_of_also_old(self):
        should_be = {0: 'SA848EL83DOYALID-2416',
                     1: 'CA189EL29AGOALID-170',
                     2: 'OL756EL55HAMALID-4744',
                     3: 'AC016EL56BKHALID-943'}
        self.data.split(1, only_new=False)
        self.assertDictEqual(self.data.train.itemID_of, should_be)

    def test_train_number_of_users_also_old(self):
        self.data.split(1, only_new=False)
        self.assertEqual(self.data.train.number_of_users, 3)

    def test_train_number_of_items_also_old(self):
        self.data.split(1, only_new=False)
        self.assertEqual(self.data.train.number_of_items, 4)

    def test_train_count_buys_of_also_old(self):
        should_be = {(0, 0): 1, (1, 1): 1, (2, 2): 10, (2, 3): 7}
        self.data.split(1, only_new=False)


if __name__ == '__main__':
    ut.main()
