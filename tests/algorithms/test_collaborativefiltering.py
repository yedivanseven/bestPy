#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import unittest as ut
from ...algorithms import CollaborativeFiltering, Baseline
from ...datastructures import UserItemMatrix
from ...algorithms.similarities import default_similarity, sokalsneath

class TestCollaborativeFiltering(ut.TestCase):

    def setUp(self):
        file = './bestPy/tests/data/data50.csv'
        self.data = UserItemMatrix.from_csv(file)
        self.algorithm = CollaborativeFiltering()

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

    def test_has_data_false(self):
        self.assertFalse(self.algorithm.has_data)

    def test_has_data_true(self):
        self.algorithm = self.algorithm.operating_on(self.data)
        self.assertTrue(self.algorithm.has_data)

    def test_cannot_set_attribute_has_data_without_data(self):
        with self.assertRaises(AttributeError):
            self.algorithm.has_data = 'bar'
        self.assertFalse(self.algorithm.has_data)

    def test_cannot_set_attribute_has_data_with_data(self):
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
        self.algorithm = self.algorithm.operating_on(self.data)
        self.assertTrue(hasattr(self.algorithm, 'for_one'))



if __name__ == '__main__':
    ut.main()
