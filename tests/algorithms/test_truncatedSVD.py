#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import unittest as ut
from numpy import array, allclose
from ...algorithms import TruncatedSVD
from ...datastructures import UserItemMatrix


class TestCollaborativeFiltering(ut.TestCase):

    def setUp(self):
        file = './bestPy/tests/data/data50.csv'
        self.data = UserItemMatrix.from_csv(file)
        self.algorithm = TruncatedSVD()

    def test_has_attribute_binarize(self):
        self.assertTrue(hasattr(self.algorithm, 'binarize'))

    def test_binarize_type(self):
        log_msg = ['ERROR:root:Attempt to set "binarize" to non-boolean type.']
        err_msg = 'Attribute "binarize" must be True or False!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg):
                self.algorithm.binarize = 'foo'
        self.assertEqual(log.output, log_msg)

    def test_binarize_true(self):
        self.algorithm.binarize = True
        self.assertTrue(self.algorithm.binarize)

    def test_binarize_false(self):
        self.algorithm.binarize = False
        self.assertFalse(self.algorithm.binarize)

    def test_has_attribute_number_of_factors(self):
        self.assertTrue(hasattr(self.algorithm, 'number_of_factors'))

    def test_default_number_of_factors(self):
        self.assertEqual(self.algorithm.number_of_factors, 20)

    def test_set_allowed_number_of_factors_without_data(self):
        self.algorithm.number_of_factors = 15
        self.assertEqual(self.algorithm.number_of_factors, 15)

    def test_set_number_of_factors_to_wrong_type(self):
        log_msg = ['ERROR:root:Attempt to set number_of_factors to'
                   ' non-integer type.']
        err_msg = '"number_of_factors" must be a positive integer!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg):
                self.algorithm.number_of_factors = 'bar'
        self.assertEqual(log.output, log_msg)

    def test_set_number_of_factors_to_negative_value(self):
        log_msg = ['ERROR:root:Attempt to set number_of_factors to'
                   ' value < 1.']
        err_msg = '"number_of_factors" must be a positive integer!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ValueError, msg=err_msg):
                self.algorithm.number_of_factors = -3
        self.assertEqual(log.output, log_msg)

    def test_has_attribute_operating_on(self):
        self.assertTrue(hasattr(self.algorithm, 'operating_on'))

    def test_attribute_operating_on_is_callable(self):
        self.assertTrue(callable(self.algorithm.operating_on))

    def test_gets_correct_attribute_max_number_of_factors_with_data(self):
        self.algorithm.number_of_factors = 8
        self.algorithm = self.algorithm.operating_on(self.data)
        self.assertTrue(hasattr(self.algorithm, 'max_number_of_factors'))
        self.assertEqual(self.algorithm.max_number_of_factors, 11)

    def test_logs_warning_and_resets_default_number_of_factors_with_data(self):
        log_msg = ['WARNING:root:Requested 20 latent features, but only 11'
                   ' available. Resetting to 11.']
        with self.assertLogs(level=logging.WARNING) as log:
            self.algorithm = self.algorithm.operating_on(self.data)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(self.algorithm.number_of_factors, 11)

    def test_logs_warning_and_resets_set_number_of_factors_with_data(self):
        self.algorithm.number_of_factors = 27
        log_msg = ['WARNING:root:Requested 27 latent features, but only 11'
                   ' available. Resetting to 11.']
        with self.assertLogs(level=logging.WARNING) as log:
            self.algorithm = self.algorithm.operating_on(self.data)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(self.algorithm.number_of_factors, 11)

    def test_logs_warning_and_resets_number_of_factors_if_too_many(self):
        self.algorithm.number_of_factors = 7
        self.algorithm = self.algorithm.operating_on(self.data)
        log_msg = ['WARNING:root:Requested 36 latent features, but only 11'
                   ' available. Resetting to 11.']
        with self.assertLogs(level=logging.WARNING) as log:
            self.algorithm.number_of_factors = 36
        self.assertEqual(log.output, log_msg)
        self.assertEqual(self.algorithm.number_of_factors, 11)

    def test_has_attribute_has_data(self):
        self.assertTrue(hasattr(self.algorithm, 'has_data'))

    def test_has_data_false(self):
        self.assertFalse(self.algorithm.has_data)

    def test_has_data_true(self):
        self.algorithm.number_of_factors = 9
        self.algorithm = self.algorithm.operating_on(self.data)
        self.assertTrue(self.algorithm.has_data)

    def test_cannot_set_attribute_has_data_without_data(self):
        with self.assertRaises(AttributeError):
            self.algorithm.has_data = 'bar'
        self.assertFalse(self.algorithm.has_data)

    def test_cannot_set_attribute_has_data_with_data(self):
        self.algorithm.number_of_factors = 9
        self.algorithm = self.algorithm.operating_on(self.data)
        with self.assertRaises(AttributeError):
            self.algorithm.has_data = 'baz'
        self.assertTrue(self.algorithm.has_data)

    def test_data_type(self):
        log_msg = ['ERROR:root:Attempt to set incompatible data type.'
                  ' Must be <UserItemMatrix>']
        err_msg = 'Data must be of type <UserItemMatrix>!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg):
                _ = self.algorithm.operating_on('foz')
        self.assertEqual(log.output, log_msg)

    def test_no_attribute_for_one_after_wrong_data_type(self):
        with self.assertLogs(level=logging.ERROR):
            with self.assertRaises(TypeError):
                _ = self.algorithm.operating_on('john')
        self.assertFalse(hasattr(self.algorithm, 'for_one'))

    def test_no_attribute_for_one_without_data(self):
        self.assertFalse(hasattr(self.algorithm, 'for_one'))

    def test_has_attribute_for_one_with_data(self):
        self.algorithm.number_of_factors = 9
        self.algorithm = self.algorithm.operating_on(self.data)
        self.assertTrue(hasattr(self.algorithm, 'for_one'))

    def test_binarized_recommendation_does_not_change(self):
        target = 5
        self.algorithm.binarize = True
        self.algorithm.number_of_factors = 4
        self.algorithm = self.algorithm.operating_on(self.data)
        before = self.algorithm.for_one(target).copy().tolist()
        recommendation = self.algorithm.for_one(target)
        recommendation += 1
        after = self.algorithm.for_one(target).tolist()
        self.assertListEqual(before, after)

    def test_non_binarized_recommendation_does_not_change(self):
        target = 5
        self.algorithm.binarize = False
        self.algorithm.number_of_factors = 4
        self.algorithm = self.algorithm.operating_on(self.data)
        before = self.algorithm.for_one(target).copy().tolist()
        recommendation = self.algorithm.for_one(target)
        recommendation += 1
        after = self.algorithm.for_one(target).tolist()
        self.assertListEqual(before, after)

    def test_binarized_data_does_not_change(self):
        target = 5
        before_col = self.data.matrix_by_col.copy().todense().tolist()
        before_row = self.data.matrix_by_row.copy().todense().tolist()
        before_boolcol = self.data.bool_matrix_by_col.copy().todense().tolist()
        before_boolrow = self.data.bool_matrix_by_row.copy().todense().tolist()
        self.algorithm.binarize = True
        self.algorithm.number_of_factors = 4
        self.algorithm = self.algorithm.operating_on(self.data)
        recommendation = self.algorithm.for_one(target)
        recommendation += 1
        after_col = self.data.matrix_by_col.copy().todense().tolist()
        after_row = self.data.matrix_by_row.copy().todense().tolist()
        after_boolcol = self.data.bool_matrix_by_col.copy().todense().tolist()
        after_boolrow = self.data.bool_matrix_by_row.copy().todense().tolist()
        self.assertListEqual(before_col, after_col)
        self.assertListEqual(before_row, after_row)
        self.assertListEqual(before_boolcol, after_boolcol)
        self.assertListEqual(before_boolrow, after_boolrow)

    def test_non_binarized_data_does_not_change(self):
        target = 5
        before_col = self.data.matrix_by_col.copy().todense().tolist()
        before_row = self.data.matrix_by_row.copy().todense().tolist()
        before_boolcol = self.data.bool_matrix_by_col.copy().todense().tolist()
        before_boolrow = self.data.bool_matrix_by_row.copy().todense().tolist()
        self.algorithm.binarize = False
        self.algorithm.number_of_factors = 4
        self.algorithm = self.algorithm.operating_on(self.data)
        recommendation = self.algorithm.for_one(target)
        recommendation += 1
        after_col = self.data.matrix_by_col.copy().todense().tolist()
        after_row = self.data.matrix_by_row.copy().todense().tolist()
        after_boolcol = self.data.bool_matrix_by_col.copy().todense().tolist()
        after_boolrow = self.data.bool_matrix_by_row.copy().todense().tolist()
        self.assertListEqual(before_col, after_col)
        self.assertListEqual(before_row, after_row)
        self.assertListEqual(before_boolcol, after_boolcol)
        self.assertListEqual(before_boolrow, after_boolrow)

    def test_recommendation_non_binarized(self):
        target = 1
        should_be = array([-3.71779941e-17,  1.12137650e-01,  9.01851352e-01,
                            4.63025802e-01,  3.39422048e-01,  1.69711024e-01,
                           -1.45263575e-17, -2.84841847e-17, -2.84841847e-17,
                           -9.29449854e-17,  2.32362463e-17, -1.16779390e-17,
                            1.69711024e-01,  4.64724927e-17, -9.29449854e-17,
                            1.12137650e-01,  1.12137650e-01,  4.64724927e-17,
                            4.64724927e-17, -2.84841847e-18, -2.84841847e-18,
                           -2.84841847e-18, -2.84841847e-18])
        self.algorithm.binarize = False
        self.algorithm.number_of_factors = 2
        self.algorithm = self.algorithm.operating_on(self.data)
        actually_is = self.algorithm.for_one(target)
        self.assertTrue(allclose(should_be, actually_is))

    def test_recommendation_binarized(self):
        target = 1
        should_be = array([ 9.32360549e-18,  1.12841097e-01,  7.13607215e-01,
                            5.24231676e-01,  3.91473337e-01,  1.95736668e-01,
                            2.78329185e-16,  2.38779085e-16,  2.38779085e-16,
                           -9.32360549e-18, -4.66180274e-18,  3.95500995e-17,
                            1.95736668e-01,  3.03017178e-17,  6.13589243e-33,
                            1.12841097e-01,  1.12841097e-01,  3.03017178e-17,
                            3.03017178e-17,  2.38779085e-16,  2.38779085e-16,
                            2.38779085e-16,  2.38779085e-16])
        self.algorithm.binarize = True
        self.algorithm.number_of_factors = 2
        self.algorithm = self.algorithm.operating_on(self.data)
        actually_is = self.algorithm.for_one(target)
        self.assertTrue(allclose(should_be, actually_is))


if __name__ == '__main__':
    ut.main()
