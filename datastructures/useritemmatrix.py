#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import unique
from scipy.sparse import csc_matrix
from .transactions import Transactions


class UserItemMatrix(Transactions):
    def __init__(self, n_buys, n_err, user_i, item_j, counts):
        super().__init__(n_buys, n_err, user_i, item_j, counts)
        self.__class_prefix = '_' + self.__class__.__name__ + '__'

    @property
    def min_matrix_shape(self):
        if not self.__has('min_matrix_shape'):
            self.__min_matrix_shape = min(self.number_of_users,
                                          self.number_of_items)
        return self.__min_matrix_shape

    @property
    def matrix_by_col(self):
        if not self.__has('matrix_by_col'):
            counts, indices = tuple(zip(*((count, user_item)
                                          for user_item, count
                                          in self._count_buys_of.items())))
            self.__matrix_by_col = csc_matrix((counts, zip(*indices)))
            self.__matrix_by_col = self.__matrix_by_col.astype(float)
        return self.__matrix_by_col

    @property
    def bool_matrix_by_col(self):
        if not self.__has('bool_matrix_by_col'):
            self.__bool_matrix_by_col = self.matrix_by_col.copy()
            self.__bool_matrix_by_col.data[:] = 1.0
        return self.__bool_matrix_by_col

    @property
    def matrix_by_row(self):
        if not self.__has('matrix_by_row'):
            self.__matrix_by_row = self.matrix_by_col.tocsr()
        return self.__matrix_by_row

    @property
    def bool_matrix_by_row(self):
        if not self.__has('bool_matrix_by_row'):
            self.__bool_matrix_by_row = self.matrix_by_row.copy()
            self.__bool_matrix_by_row.data[:] = 1.0
        return self.__bool_matrix_by_row

    def users_who_bought(self, items):
        return unique(self.matrix_by_col[:, items].indices)

    def __has(self, attribute):
        return hasattr(self, self.__class_prefix + attribute)
