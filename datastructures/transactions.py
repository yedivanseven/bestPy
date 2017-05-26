# -*- coding: utf-8 -*-

import logging as log
from numpy import unique
from . import read
from .help import IndexFrom, MatrixFrom


class Transactions:
    def __init__(self, n_trans, n_corr, user_i, item_j, counts):
        self.__number_of_transactions = self.__int_type_value_checked(n_trans)
        self.__number_of_corrupted_records = self.__type_range_checked(n_corr)
        self.__user = IndexFrom(user_i)
        self.__item = IndexFrom(item_j)
        self.__matrix = MatrixFrom(counts)
        self.__number_of_userItem_pairs = len(counts)
        self.__check_data_for_consistency()

    @classmethod
    def from_csv(cls, file, separator=';'):
        return cls(*read.from_csv(file, separator=separator))

    @classmethod
    def from_postgreSQL(cls, database):
        return cls(*read.from_postgreSQL(database))

    @property
    def number_of_transactions(self):
        return self.__number_of_transactions

    @property
    def number_of_corrupted_records(self):
        return self.__number_of_corrupted_records

    @property
    def number_of_userItem_pairs(self):
        return self.__number_of_userItem_pairs

    @property
    def user(self):
        return self.__user

    @property
    def item(self):
        return self.__item

    @property
    def matrix(self):
        return self.__matrix

    def users_who_bought(self, items):
        return unique(self.matrix.by_col[:, items].indices)

    @staticmethod
    def __int_type_value_checked(n_trans):
        log_msg = ('Attempt to instantiate data object with number of'
                   ' valid transactions not a positive integer.')
        err_msg = 'Number of valid transactions not a positive integer!'
        if not isinstance(n_trans, int):
            log.error(log_msg)
            raise TypeError(err_msg)
        if n_trans < 1:
            log.error(log_msg)
            raise ValueError(err_msg)
        return n_trans

    @staticmethod
    def __type_range_checked(n_corr):
        log_msg = ('Attempt to instantiate data object with number of'
                   ' corrupted records not an integer >= 0.')
        err_msg = 'Number of corrupted records not an integer >= 0!'
        if not isinstance(n_corr, int):
            log.error(log_msg)
            raise TypeError(err_msg)
        if n_corr < 0:
            log.error(log_msg)
            raise ValueError(err_msg)
        return n_corr

    def __check_data_for_consistency(self):
        if (self.user.count, self.item.count) != self.matrix.by_col.shape:
            log.error('Attempt to instantiate data object with number of'
                      ' customers/articles incompatible with matrix shape.')
            raise ValueError('Number of users/items incompatible with'
                             ' matrix shape!')
        if self.number_of_transactions != self.matrix.by_col.sum().sum():
            log.error('Attempt to instantiate data object with number of'
                      ' transactions incompatible with matrix values.')
            raise ValueError('Number of transactions incompatible with values'
                             ' in matrix!')
        if self.number_of_userItem_pairs != self.matrix.by_col.getnnz():
            log.error('Attempt to instantiate data object with number of'
                      ' user/item pairs incompatible with matrix values.')
            raise ValueError('Number of user/item pairs incompatible with'
                             'values in matrix!')
