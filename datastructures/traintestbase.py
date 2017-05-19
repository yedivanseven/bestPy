# -*- coding: utf-8 -*-

import logging as log
from . import split


class TrainTestBase():
    def __init__(self, n_rec, n_err, last_unique, transactions):
        self.__number_of_transactions = self.__int_type_value_checked(n_rec)
        self.__number_of_corrupted_records = self.__type_range_checked(n_err)
        self.__unique = last_unique
        self.__transactions = transactions
        self.__class_prefix = '_' + self.__class__.__name__ + '__'

    @classmethod
    def from_csv(cls, file, separator=';', fmt=None):
        return cls(*split.from_csv(file, separator=separator, fmt=fmt))

    @classmethod
    def from_postgreSQL(cls, database):
        return cls(*split.from_postgreSQL(database))

    @property
    def number_of_transactions(self):
        return self.__number_of_transactions

    @property
    def number_of_corrupted_records(self):
        return self.__number_of_corrupted_records

    @property
    def max_hold_out(self):
        if not self.__has('max_hold_out'):
            self.__max_hold_out =  max(len(u) for u in self.__unique.values())
        return self.__max_hold_out

    def __has(self, attribute):
        return hasattr(self, self.__class_prefix + attribute)

    def __int_type_value_checked(self, n_rec):
        log_msg = ('Attempt to instantiate data object with number of'
                   ' transactions not a positive integer.')
        err_msg = 'Number of transactions not a positive integer!'
        if not isinstance(n_rec, int):
            log.error(log_msg)
            raise TypeError(err_msg)
        if n_rec < 1:
            log.error(log_msg)
            raise ValueError(err_msg)
        return n_rec

    def __type_range_checked(self, n_err):
        log_msg = ('Attempt to instantiate data object with number of'
                   ' corrupted records not an integer >= 0.')
        err_msg = 'Number of corrupted records not an integer >= 0!'
        if not isinstance(n_err, int):
            log.error(log_msg)
            raise TypeError(err_msg)
        if n_err < 0:
            log.error(log_msg)
            raise ValueError(err_msg)
        return n_err
