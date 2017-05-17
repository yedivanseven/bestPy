# -*- coding: utf-8 -*-

import logging as log
from io import TextIOBase
from . import split


class TrainTestBase():
    def __init__(self, n_rec, n_err, unique, trans):
        self.__number_of_transactions = n_rec
        self.__number_of_corrupted_records = n_err
        self.__unique = unique
        self.__transactions = trans
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
