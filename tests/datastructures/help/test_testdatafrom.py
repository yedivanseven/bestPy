#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import unittest as ut
from ....datastructures.help import TestDataFrom


class TestInstantiationOfTestDataFrom(ut.TestCase):

    def test_wrong_data_type(self):
        log_msg = ['ERROR:root:Attempt to set non-dictionary type as'
                   ' test data.']
        err_msg = 'Test data must be of type <dict>!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = TestDataFrom(1, 2, True)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_wrong_value_type_in_data(self):
        log_msg = ['ERROR:root:Attempt to initialize test-data object from'
                  ' dictionary with values not of type <set>.']
        err_msg = 'Test data values must be of type <set>!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = TestDataFrom({1: 'baz'}, 1, True)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_empty_value_set_in_data(self):
        log_msg = ['ERROR:root:Attempt to initialize test-data object from'
                  ' dictionary with empty set as values.']
        err_msg = 'Test data values must not be empty sets!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ValueError, msg=err_msg) as err:
                _ = TestDataFrom({1: set({})}, 1, True)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_wrong_hold_out_type(self):
        log_msg = ['ERROR:root:Attempt to set non-integer type as'
                   ' "hold_out".']
        err_msg = '"hold_out" must be of type <int>!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = TestDataFrom({1: {'foo'}}, 'bar', False)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_wrong_hold_out_value(self):
        log_msg = ['ERROR:root:Attempt to set argument "hold_out" to value'
                   ' other than the number of held-out items.']
        err_msg = '"hold_out" differs from no. of held-out items!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ValueError, msg=err_msg) as err:
                _ = TestDataFrom({1: {'foo'}}, 2, False)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_wrong_only_new_type(self):
        log_msg = ['ERROR:root:Attempt to set non-boolean type as'
                   ' "only_new".']
        err_msg = '"only_new" must be of type <bool>!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = TestDataFrom({1: {'foo'}}, 1, 'baz')
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)


class TestTestDataFrom(ut.TestCase):

    def setUp(self):
        self.data = {'12': {'SA848EL83DOYALID-2416', 'BL152EL82CRXALID-1817'},
                      '7': {'AC016EL56BKHALID-943', 'OL756EL55HAMALID-4744'}}
        self.hold_out = 2
        self.only_new = False
        self.test = TestDataFrom(self.data, self.hold_out, self.only_new)

    def test_has_attribute_data(self):
        self.assertTrue(hasattr(self.test, 'data'))

    def test_type_of_attribute_data(self):
        self.assertIsInstance(self.test.data, dict)

    def test_correct_value_of_attribute_data(self):
        self.assertDictEqual(self.test.data, self.data)

    def test_cannot_set_attribute_data(self):
        with self.assertRaises(AttributeError):
            self.test.data = 'foo'
        self.assertDictEqual(self.test.data, self.data)

    def test_has_attribute_hold_out(self):
        self.assertTrue(hasattr(self.test, 'hold_out'))

    def test_type_of_attribute_hold_out(self):
        self.assertIsInstance(self.test.hold_out, int)

    def test_correct_value_of_attribute_hold_out(self):
        self.assertEqual(self.test.hold_out, self.hold_out)

    def test_cannot_set_attribute_hold_out(self):
        with self.assertRaises(AttributeError):
            self.test.hold_out = 'bar'
        self.assertEqual(self.test.hold_out, self.hold_out)

    def test_has_attribute_only_new(self):
        self.assertTrue(hasattr(self.test, 'only_new'))

    def test_type_of_attribute_only_new(self):
        self.assertIsInstance(self.test.only_new, bool)

    def test_correct_value_of_attribute_only_new(self):
        self.assertEqual(self.test.only_new, self.only_new)

    def test_cannot_set_attribte_only_new(self):
        with self.assertRaises(AttributeError):
            self.test.only_new = 'baz'
        self.assertEqual(self.test.only_new, self.only_new)

    def test_has_attribute_number_of_cases(self):
        self.assertTrue(hasattr(self.test, 'number_of_cases'))

    def test_type_of_attribute_number_of_cases(self):
        self.assertIsInstance(self.test.number_of_cases, int)

    def test_correct_value_of_attribute_number_of_cases(self):
        self.assertEqual(self.test.number_of_cases, 2)

    def test_cannot_set_attribute_set_number_of_cases(self):
        with self.assertRaises(AttributeError):
            self.test.number_of_cases = 'foz'
        self.assertEqual(self.test.number_of_cases, 2)


if __name__ == '__main__':
    ut.main()
