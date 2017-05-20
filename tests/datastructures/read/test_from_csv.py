#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import logging
from ....datastructures.read import from_csv


class BaseTests():

    def test_logs_warnings_on_corrupted_records(self):
        log_msg = ['WARNING:root:Could not interpret transaction on'
                   ' line 2. Skipping.',
                   'WARNING:root:Transaction on line 3 contains'
                   ' empty fields. Skipping.',
                   'WARNING:root:Transaction on line 4 contains'
                   ' empty fields. Skipping.',
                   'WARNING:root:Could not interpret transaction on'
                   ' line 8. Skipping.',
                   'WARNING:root:Could not interpret transaction on'
                   ' line 26. Skipping.']
        with self.assertLogs(level=logging.WARNING) as log:
            _ = from_csv(self.file, self.separator)
            self.assertListEqual(log.output, log_msg)

    def test_integer_type_of_number_of_records(self):
        with self.assertLogs(level=logging.WARNING):
            n_rec, _, _, _, _ = from_csv(self.file, self.separator)
        self.assertIsInstance(n_rec, int)

    def test_correct_value_of_number_of_records(self):
        with self.assertLogs(level=logging.WARNING):
            n_rec, _, _, _, _ = from_csv(self.file, self.separator)
        self.assertEqual(n_rec, 21)

    def test_integer_type_of_number_of_corrupted_records(self):
        with self.assertLogs(level=logging.WARNING):
            _, n_err, _, _, _ = from_csv(self.file, self.separator)
        self.assertIsInstance(n_err, int)

    def test_correct_value_of_number_of_corrupted_records(self):
        with self.assertLogs(level=logging.WARNING):
            _, n_err, _, _, _ = from_csv(self.file, self.separator)
        self.assertEqual(n_err, 5)

    def test_dict_type_of_user_index(self):
        with self.assertLogs(level=logging.WARNING):
            _, _, user_i, _, _ = from_csv(self.file, self.separator)
        self.assertIsInstance(user_i, dict)

    def test_correct_value_of_user_index(self):
        should_be = {'4': 0, '11': 1, '10': 2, '7': 3}
        with self.assertLogs(level=logging.WARNING):
            _, _, user_i, _, _ = from_csv(self.file, self.separator)
        self.assertDictEqual(should_be, user_i)

    def test_dict_type_of_item_index(self):
        with self.assertLogs(level=logging.WARNING):
            _, _, _, item_j, _ = from_csv(self.file, self.separator)
        self.assertIsInstance(item_j, dict)

    def test_correct_value_of_item_index(self):
        should_be = {'AC016EL50CPHALID-1749': 0,
                     'CA189EL29AGOALID-170' : 1,
                     'LE629EL54ANHALID-345' : 2,
                     'OL756EL65HDYALID-4834': 3,
                     'OL756EL55HAMALID-4744': 4,
                     'AC016EL56BKHALID-943' : 5}
        with self.assertLogs(level=logging.WARNING):
            _, _, _, item_j, _ = from_csv(self.file, self.separator)
        self.assertDictEqual(should_be, item_j)

    def test_dict_type_of_user_item_counts(self):
        with self.assertLogs(level=logging.WARNING):
            _, _, _, _, counts = from_csv(self.file, self.separator)
        self.assertIsInstance(counts, dict)

    def test_correct_value_of_user_item_counts(self):
        should_be = {(0, 0): 1,
                     (1, 1): 1,
                     (1, 2): 1,
                     (2, 3): 1,
                     (3, 4): 9,
                     (3, 5): 8}
        with self.assertLogs(level=logging.WARNING):
            _, _, _, _, counts = from_csv(self.file, self.separator)
        self.assertDictEqual(should_be, counts)


class TestTransactionsFromCsvSemicolonFile(ut.TestCase, BaseTests):
    def setUp(self):
        self.file = './bestPy/tests/data/data25semicolon.csv'
        self.separator = ';'


class TestTransactionsFromCsvCommaFile(ut.TestCase, BaseTests):
    def setUp(self):
        self.file = './bestPy/tests/data/data25comma.csv'
        self.separator = ','


class TestTransactionsFromCsvSemicolonStream(ut.TestCase, BaseTests):
    def setUp(self):
        self.file = open('./bestPy/tests/data/data25semicolon.csv')
        self.separator = ';'


class TestTransactionsFromCsvCommaStream(ut.TestCase, BaseTests):
    def setUp(self):
        self.file = open('./bestPy/tests/data/data25comma.csv')
        self.separator = ','


class TestTrainTestFromCsvFileSeparator(ut.TestCase):

    def test_wrong_type_of_separator(self):
        log_msg = ['ERROR:root:Attempt to set separator argument to'
                   ' non-string type.']
        err_msg = 'Separator argument must be a string!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError):
                _ = from_csv('file', 12.3)
        self.assertEqual(log.output, log_msg)


if __name__ == '__main__':
    ut.main()
