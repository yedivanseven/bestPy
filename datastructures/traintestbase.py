# -*- coding: utf-8 -*-

import logging as log
from . import split


class TrainTestBase():
    def __init__(self, n_trans, n_corr, last_unique, transactions):
        self.__number_of_transactions = self.__int_type_value_checked(n_trans)
        self.__number_of_corrupted_records = self.__type_range_checked(n_corr)
        self.__unique = self.__dict_type_and_empty_checked(last_unique)
        self.__transactions = self.__list_type_and_entry_checked(transactions)
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
            self.__max_hold_out = max(len(u) for u in self.__unique.values())
        return self.__max_hold_out

    def __has(self, attribute):
        return hasattr(self, self.__class_prefix + attribute)

    @staticmethod
    def __int_type_value_checked(n_trans):
        log_msg = ('Attempt to instantiate data object with number of'
                   ' transactions not a positive integer.')
        err_msg = 'Number of transactions not a positive integer!'
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

    @staticmethod
    def __dict_type_and_empty_checked(unique):
        if not isinstance(unique, dict):
            log.error('Attempt to instantiate data object with last unique'
                      ' buys not of required type <dict>.')
            raise TypeError('Last unique items bought must be of type <dict>!')
        if len(unique) < 1:
            log.error('Attempt to instantiate data object with empty <dict>'
                      ' of last unique items bought.')
            raise ValueError('Last unique items dictionary must not be empty!')
        items = next(iter(unique.values()))
        if not isinstance(items, dict):
            log.error('Attempt to instantiate data object with values in last'
                      ' unique item dictionary not of type <dict>.')
            raise TypeError('Last unique item values must be of type <dict>!')
        if len(items) < 1:
            log.error('Attempt to instantiate data object with empty <dict>'
                      ' as entry of last unique items dictionary.')
            raise ValueError('Entries of last unique items must not be empty!')
        return unique

    @staticmethod
    def __list_type_and_entry_checked(transactions):
        if not isinstance(transactions, list):
            log.error('Attempt to instantiate data object with transactions'
                      ' not of required type <list>.')
            raise TypeError('Transactions must be of type <list>!')
        if len(transactions) < 1:
            log.error('Attempt to instantiate data object with empty'
                      ' transaction list.')
            raise ValueError('Transaction list must not be empty!')
        log_msg = ('Attempt to instantiate data object with transactions'
                   ' not 3-tuples of strings.')
        err_msg = 'Transactions must be 3-tuples of strings!'
        first = transactions[0]
        if not isinstance(first, tuple):
            log.error(log_msg)
            raise TypeError(err_msg)
        if len(first) != 3:
            log.error(log_msg)
            raise TypeError(err_msg)
        if not all(isinstance(entry, str) for entry in first):
            log.error(log_msg)
            raise TypeError(err_msg)
        return transactions
