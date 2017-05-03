#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import logging
import scipy
from ...datastructures import UserItemMatrix


class TestUserItemMatrix(ut.TestCase):

    def setUp(self):
        file = './bestPy/tests/data/data25comma.csv'
        with self.assertLogs(level=logging.WARNING):
            self.data = UserItemMatrix.from_csv(file, ',')

    def test_min_matrix_shape(self):
        self.assertEqual(self.data.min_matrix_shape, 4)

    def test_set_min_matrix_shape(self):
        with self.assertRaises(AttributeError):
            self.data.min_matrix_shape = 123
        self.assertEqual(self.data.min_matrix_shape, 4)

    def test_matrix_by_col_types(self):
        self.assertIsInstance(self.data.matrix_by_col,
                              scipy.sparse.csc.csc_matrix)

    def test_matrix_by_col_values(self):
        should_be = [[1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 9.0, 8.0]]
        self.assertListEqual(self.data.matrix_by_col.toarray().tolist(),
                             should_be)

    def test_set_matrix_by_col(self):
        should_be = [[1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 9.0, 8.0]]
        with self.assertRaises(AttributeError):
            self.data.matrix_by_col = 'foo'
        self.assertListEqual(self.data.matrix_by_col.toarray().tolist(),
                             should_be)

    def test_bool_matrix_by_col_type(self):
        self.assertIsInstance(self.data.bool_matrix_by_col,
                              scipy.sparse.csc.csc_matrix)

    def test_bool_matrix_by_col_values(self):
        should_be = [[1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 1.0, 1.0]]
        self.assertListEqual(self.data.bool_matrix_by_col.toarray().tolist(),
                             should_be)

    def test_set_bool_matrix_by_col(self):
        should_be = [[1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 1.0, 1.0]]
        with self.assertRaises(AttributeError):
            self.data.bool_matrix_by_col = 'bar'
        self.assertListEqual(self.data.bool_matrix_by_col.toarray().tolist(),
                             should_be)

    def test_matrix_by_row_types(self):
        self.assertIsInstance(self.data.matrix_by_row,
                              scipy.sparse.csr.csr_matrix)

    def test_matrix_by_row_values(self):
        should_be = [[1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 9.0, 8.0]]
        self.assertListEqual(self.data.matrix_by_row.toarray().tolist(),
                             should_be)

    def test_set_matrix_by_row(self):
        should_be = [[1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 9.0, 8.0]]
        with self.assertRaises(AttributeError):
            self.data.matrix_by_col = 'baz'
        self.assertListEqual(self.data.matrix_by_row.toarray().tolist(),
                             should_be)

    def test_bool_matrix_by_row_type(self):
        self.assertIsInstance(self.data.bool_matrix_by_row,
                              scipy.sparse.csr.csr_matrix)

    def test_bool_matrix_by_row_values(self):
        should_be = [[1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 1.0, 1.0]]
        self.assertListEqual(self.data.bool_matrix_by_row.toarray().tolist(),
                             should_be)

    def test_set_bool_matrix_by_row(self):
        should_be = [[1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 1.0, 1.0]]
        with self.assertRaises(AttributeError):
            self.data.bool_matrix_by_row = 'foz'
        self.assertListEqual(self.data.bool_matrix_by_row.toarray().tolist(),
                             should_be)

    def test_users_who_bought(self):
        should_be = [[0], [1], [1], [2], [3], [3]]
        actual = [self.data.users_who_bought(i).tolist() for i in range(6)]
        self.assertListEqual(should_be, actual)


if __name__ == '__main__':
    ut.main()
