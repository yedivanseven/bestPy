#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import unittest as ut
from ....algorithms import Baseline
from ....datastructures import UserItemMatrix


class TestBaseline(ut.TestCase):

    def setUp(self):
        file = './bestPy/tests/data/data50.csv'
        self.data = UserItemMatrix.from_csv(file)
        self.baseline = Baseline()

    def test_binarize_type(self):
        log_msg = ['ERROR:root:Attempt to set "binarize" to non-boolean type.']
        err_msg = 'Attribute "binarize" must be True or False!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg):
                self.baseline.binarize = 'foo'
        self.assertEqual(log.output, log_msg)

    def test_binarize_true(self):
        self.baseline.binarize = True
        self.assertTrue(self.baseline.binarize)

    def test_binarize_false(self):
        self.baseline.binarize = False
        self.assertFalse(self.baseline.binarize)

    def test_has_data_false(self):
        self.assertFalse(self.baseline.has_data)

    def test_has_data_true(self):
        self.baseline = self.baseline.operating_on(self.data)
        self.assertTrue(self.baseline.has_data)

    def test_data_type(self):
        log_msg = ['ERROR:root:Attempt to set incompatible data type.'
                  ' Must be <UserItemMatrix>']
        err_msg = 'Data must be of type <UserItemMatrix>!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg):
                _ = self.baseline.operating_on('bar')
        self.assertEqual(log.output, log_msg)

    def test_no_attribute_for_one_after_wrong_data_type(self):
        with self.assertLogs(level=logging.ERROR):
            with self.assertRaises(TypeError):
                _ = self.baseline.operating_on('baz')
        self.assertFalse(hasattr(self.baseline, 'for_one'))

    def test_no_attribute_for_one_without_data(self):
        self.assertFalse(hasattr(self.baseline, 'for_one'))

    def test_has_attribute_for_one_with_data(self):
        self.baseline = self.baseline.operating_on(self.data)
        self.assertTrue(hasattr(self.baseline, 'for_one'))

    def test_recommendation_binarized(self):
        should_be = [1., 1., 5., 3., 2., 1., 2., 1., 1., 1., 1., 1., 1., 1.,
                     1., 1., 1., 1., 1., 1., 1., 1., 1.]
        self.baseline.binarize = True
        self.baseline = self.baseline.operating_on(self.data)
        actually_is = self.baseline.for_one().tolist()
        self.assertListEqual(should_be, actually_is)

    def test_recommendation_not_binarized(self):
        should_be = [1., 1., 6., 3., 2., 1., 2., 10., 10., 1., 1., 1., 1.,
                     1., 1., 1., 1., 1., 1., 1., 1., 1., 1.]
        self.baseline.binarize = False
        self.baseline = self.baseline.operating_on(self.data)
        actually_is = self.baseline.for_one().tolist()
        self.assertListEqual(should_be, actually_is)

    def test_binarized_recommendation_does_not_change(self):
        self.baseline.binarize = True
        self.baseline = self.baseline.operating_on(self.data)
        before = self.baseline.for_one().copy().tolist()
        recommendation = self.baseline.for_one()
        recommendation += 1
        after = self.baseline.for_one().tolist()
        self.assertListEqual(before, after)

    def test_non_binarized_recommendation_does_not_change(self):
        self.baseline.binarize = False
        self.baseline = self.baseline.operating_on(self.data)
        before = self.baseline.for_one().copy().tolist()
        recommendation = self.baseline.for_one()
        recommendation += 1
        after = self.baseline.for_one().tolist()
        self.assertListEqual(before, after)


if __name__ == '__main__':
    ut.main()