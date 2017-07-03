#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import logging
import scipy.sparse as scpsp
from ....datastructures.auxiliary import MatrixFrom


class TestInstatiateMatrix(ut.TestCase):

    def test_error_on_wrong_argument_type(self):
        log_msg = ['ERROR:root:Attempt to instantiate matrix object with'
                   ' non-dictionary argument.']
        err_msg = 'Argument of matrix object must be <dict>!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = MatrixFrom('foo')
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_warning_on_empty_dictionary_as_argument(self):
        log_msg = ['WARNING:root:Matrix instantiated with empty dictionary.']
        with self.assertLogs(level=logging.WARNING) as log:
            _ = MatrixFrom({})
        self.assertEqual(log.output, log_msg)

    def test_error_on_key_not_of_type_tuple(self):
        log_msg = ['ERROR:root:Attempt to instantiate matrix object from'
                   ' dictionary with keys not 2-tuple of integer >= 0.']
        err_msg = 'Keys of dictionary must be 2-tuple of integer >= 0!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = MatrixFrom({'foo': 1})
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_key_tuple_too_long(self):
        log_msg = ['ERROR:root:Attempt to instantiate matrix object from'
                   ' dictionary with keys not 2-tuple of integer >= 0.']
        err_msg = 'Keys of dictionary must be 2-tuple of integer >= 0!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = MatrixFrom({(1, 2, 3): 1})
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_key_tuple_too_short(self):
        log_msg = ['ERROR:root:Attempt to instantiate matrix object from'
                   ' dictionary with keys not 2-tuple of integer >= 0.']
        err_msg = 'Keys of dictionary must be 2-tuple of integer >= 0!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = MatrixFrom({(1,): 1})
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_first_element_in_key_not_integer(self):
        log_msg = ['ERROR:root:Attempt to instantiate matrix object from'
                   ' dictionary with keys not 2-tuple of integer >= 0.']
        err_msg = 'Keys of dictionary must be 2-tuple of integer >= 0!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = MatrixFrom({(1.0, 1): 1})
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_second_element_in_key_not_integer(self):
        log_msg = ['ERROR:root:Attempt to instantiate matrix object from'
                   ' dictionary with keys not 2-tuple of integer >= 0.']
        err_msg = 'Keys of dictionary must be 2-tuple of integer >= 0!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = MatrixFrom({(1, 'bar'): 1})
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_first_element_in_key_negative(self):
        log_msg = ['ERROR:root:Attempt to instantiate matrix object from'
                   ' dictionary with keys not 2-tuple of integer >= 0.']
        err_msg = 'Keys of dictionary must be 2-tuple of integer >= 0!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ValueError, msg=err_msg) as err:
                _ = MatrixFrom({(-1, 0): 2})
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_second_element_in_key_negative(self):
        log_msg = ['ERROR:root:Attempt to instantiate matrix object from'
                   ' dictionary with keys not 2-tuple of integer >= 0.']
        err_msg = 'Keys of dictionary must be 2-tuple of integer >= 0!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ValueError, msg=err_msg) as err:
                _ = MatrixFrom({(1, -3): 4})
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_wrong_type_of_value(self):
        log_msg = ['ERROR:root:Attempt to create matrix object from dictionary'
                   'with values not positive integers.']
        err_msg = 'Values of dictionary must be positive integers!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = MatrixFrom({(1, 1): 'baz'})
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_error_on_non_positive_value(self):
        log_msg = ['ERROR:root:Attempt to create matrix object from dictionary'
                   'with values not positive integers.']
        err_msg = 'Values of dictionary must be positive integers!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ValueError, msg=err_msg) as err:
                _ = MatrixFrom({(1, 1): 0})
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

class TestMatrixFrom(ut.TestCase):

    def setUp(self):
        self.counts = {(0, 0): 1,
                       (1, 1): 1,
                       (1, 2): 1,
                       (2, 3): 1,
                       (3, 4): 9,
                       (3, 5): 8}
        self.matrix = MatrixFrom(self.counts)

    def test_has_attribute_by_col(self):
        self.assertTrue(hasattr(self.matrix, 'by_col'))

    def test_cannot_set_attribute_by_col(self):
        with self.assertRaises(AttributeError):
            self.matrix.by_col = 12.3

    def test_type_of_attribute_by_col(self):
        self.assertIsInstance(self.matrix.by_col, scpsp.csc.csc_matrix)

    def test_correct_values_in_attribute_by_col(self):
        should_be = [[1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 9.0, 8.0]]
        actually_is = self.matrix.by_col.toarray().tolist()
        self.assertListEqual(should_be, actually_is)

    def test_has_attribute_bool_by_col(self):
        self.assertTrue(hasattr(self.matrix, 'bool_by_col'))

    def test_cannot_set_attribute_bool_by_col(self):
        with self.assertRaises(AttributeError):
            self.matrix.bool_by_col = 'foo'

    def test_type_of_attribute_bool_by_col(self):
        self.assertIsInstance(self.matrix.bool_by_col, scpsp.csc.csc_matrix)

    def test_correct_values_in_attribute_bool_by_col(self):
        should_be = [[1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 1.0, 1.0]]
        actually_is = self.matrix.bool_by_col.toarray().tolist()
        self.assertListEqual(should_be, actually_is)

    def test_has_attribute_by_row(self):
        self.assertTrue(hasattr(self.matrix, 'by_row'))

    def test_cannot_set_attribute_by_row(self):
        with self.assertRaises(AttributeError):
            self.matrix.by_row = 45.6

    def test_type_of_attribute_by_row(self):
        self.assertIsInstance(self.matrix.by_row, scpsp.csr.csr_matrix)

    def test_correct_values_in_attribute_by_row(self):
        should_be = [[1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 9.0, 8.0]]
        actually_is = self.matrix.by_row.toarray().tolist()
        self.assertListEqual(should_be, actually_is)

    def test_has_attribute_bool_by_row(self):
        self.assertTrue(hasattr(self.matrix, 'bool_by_row'))

    def test_cannot_set_attribute_bool_by_row(self):
        with self.assertRaises(AttributeError):
            self.matrix.bool_by_row = 'bar'

    def test_type_of_attribute_bool_by_row(self):
        self.assertIsInstance(self.matrix.bool_by_row, scpsp.csr.csr_matrix)

    def test_correct_values_in_attribute_bool_by_row(self):
        should_be = [[1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 1.0, 1.0]]
        actually_is = self.matrix.bool_by_row.toarray().tolist()
        self.assertListEqual(should_be, actually_is)

    def test_has_attribute_min_shape(self):
        self.assertTrue(hasattr(self.matrix, 'min_shape'))

    def test_cannot_set_attribute_min_shape(self):
        with self.assertRaises(AttributeError):
            self.matrix.min_shape = {'bar': 34}

    def test_type_of_attribute_min_shape(self):
        self.assertIsInstance(self.matrix.min_shape, int)

    def test_correct_values_in_attribute_min_shape(self):
        self.assertEqual(self.matrix.min_shape, 4)


if __name__ == '__main__':
    ut.main()
