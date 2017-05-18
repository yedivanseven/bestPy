#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import logging
import scipy.sparse as scpsp
from ....datastructures.help import Matrix


class TestIndex(ut.TestCase):

    def setUp(self):
        self.counts = {(0, 0): 1,
                       (1, 1): 1,
                       (1, 2): 1,
                       (2, 3): 1,
                       (3, 4): 9,
                       (3, 5): 8}
        self.matrix = Matrix(self.counts)

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
