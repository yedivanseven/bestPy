#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import unique
from scipy.sparse import csc_matrix
from .transactions import Transactions


class UserItemMatrix(Transactions):

    @property
    def number_of_users(self):
        if not hasattr(self, '_UserItemMatrix__number_of_users'):
            self.__number_of_users = len(self.userIndex_of)
        return self.__number_of_users

    @property
    def userID_of(self):
        if not hasattr(self, '_UserItemMatrix__userID_of'):
            self.__userID_of = {
                index: user for user, index in self.userIndex_of.items()
            }
        return self.__userID_of

    @property
    def itemID_of(self):
        if not hasattr(self, '_UserItemMatrix__itemID_of'):
            self.__itemID_of = {
                index: item for item, index in self.itemIndex_of.items()
            }
        return self.__itemID_of

    @property
    def matrix_by_col(self):
        if not hasattr(self, '_UserItemMatrix__matrix_by_col'):
            counts, indices = tuple(zip(
                *((count, user_item) for user_item, count
                                      in self.count_buys_of.items()
                 )
            ))
            self.__matrix_by_col = csc_matrix((counts, zip(*indices))
                                              ).astype(float)
        return self.__matrix_by_col

    @property
    def bool_matrix_by_col(self):
        if not hasattr(self, '_UserItemMatrix__bool_matrix_by_col'):
            self.__bool_matrix_by_col = self.matrix_by_col.copy()
            self.__bool_matrix_by_col.data[:] = 1.0
        return self.__bool_matrix_by_col

    @property
    def matrix_by_row(self):
        if not hasattr(self, '_UserItemMatrix__matrix_by_row'):
            self.__matrix_by_row = self.matrix_by_col.tocsr()
        return self.__matrix_by_row

    @property
    def bool_matrix_by_row(self):
        if not hasattr(self, '_UserItemMatrix__bool_matrix_by_row'):
            self.__bool_matrix_by_row = self.matrix_by_row.copy()
            self.__bool_matrix_by_row.data[:] = 1.0
        return self.__bool_matrix_by_row

    @property
    def baseline(self):
        if not hasattr(self, '_UserItemMatrix__baseline'):
            self.__baseline = self.matrix_by_col.getnnz(0)
        return self.__baseline

    def users_who_bought(self, items):
        return unique(self.matrix_by_col[:, items].indices)
