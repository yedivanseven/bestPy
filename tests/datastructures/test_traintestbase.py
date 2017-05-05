#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import logging
from ...datastructures.traintestbase import TrainTestBase, TestDataFrom
from ...datastructures.traintestbase import FileFrom


class TestTrainTestBase(ut.TestCase):

    def setUp(self):
        file = './bestPy/tests/data/data25timestamp_fmt.csv'
        fmt = '%Y-%m-%d %H:%M:%S'
        with self.assertLogs(level=logging.WARNING):
            self.data = TrainTestBase.from_csv(file, ';', fmt)

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


class TestTestDataFrom(ut.TestCase):

    def setUp(self):
        self.data = {'12': {'SA848EL83DOYALID-2416', 'BL152EL82CRXALID-1817'},
                      '7': {'AC016EL56BKHALID-943', 'OL756EL55HAMALID-4744'}}
        self.hold_out = 2
        self.only_new = False
        self.test = TestDataFrom(self.data, self.hold_out, self.only_new)

    def test_data(self):
        self.assertDictEqual(self.test.data, self.data)

    def test_set_data(self):
        with self.assertRaises(AttributeError):
            self.test.data = 'foo'
        self.assertDictEqual(self.test.data, self.data)

    def test_hold_out(self):
        self.assertEqual(self.test.hold_out, self.hold_out)

    def test_set_hold_out(self):
        with self.assertRaises(AttributeError):
            self.test.hold_out = 'bar'
        self.assertEqual(self.test.hold_out, self.hold_out)

    def test_only_new(self):
        self.assertEqual(self.test.only_new, self.only_new)

    def test_set_only_new(self):
        with self.assertRaises(AttributeError):
            self.test.only_new = 'baz'
        self.assertEqual(self.test.only_new, self.only_new)

    def test_number_of_cases(self):
        self.assertEqual(self.test.number_of_cases, 2)

    def test_set_number_of_cases(self):
        with self.assertRaises(AttributeError):
            self.test.number_of_cases = 'foz'
        self.assertEqual(self.test.number_of_cases, 2)


class TestFileFrom(ut.TestCase):

    def setUp(self):
        str_generator = (str(i) for i in range(11))
        int_generator = (i for i in range(2))
        self.str_stream = FileFrom(str_generator)
        self.int_stream = FileFrom(int_generator)
        self.no_stream = FileFrom(12.3)

    def test_read_like_file_str_works(self):
        should_be = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        actual = []
        with self.str_stream as file:
            for line in file:
                actual.append(line)
        self.assertListEqual(should_be, actual)

    def test_read_like_file_int_fails(self):
        log_msg = ['ERROR:root:Line read from file-like object is not a'
                   ' string. Was it created from a string iterator?']
        err_msg = 'Line read from file-like object is not a string!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg):
                with self.int_stream as file:
                    for line in file:
                        _ = line
        self.assertListEqual(log.output, log_msg)

    def test_readline_like_file_fails(self):
        log_msg = ['ERROR:root:Failed to read line from file-like object.'
                   ' Was it created from an iterator?']
        err_msg = 'Object was not created from an iterator!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg):
                with self.no_stream as file:
                    for line in file:
                        _ = line
        self.assertListEqual(log.output, log_msg)


if __name__ == '__main__':
    ut.main()
