#!/usr/bin/env python3
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
            self.__max_hold_out =  max(len(d) for d in self.__unique.values())
        return self.__max_hold_out

    def __has(self, attribute):
        return hasattr(self, self.__class_prefix + attribute)


class TestDataFrom():
    def __init__(self, data, hold_out, only_new):
        self.__data = data
        self.__hold_out = hold_out
        self.__only_new = only_new
        self.__class_prefix = '_' + self.__class__.__name__ + '__'

    @property
    def data(self):
        return self.__data

    @property
    def hold_out(self):
        return self.__hold_out

    @property
    def only_new(self):
        return self.__only_new

    @property
    def number_of_cases(self):
        if not self.__has('number_of_cases'):
            self.__number_of_cases = len(self.__data)
        return self.__number_of_cases

    def __has(self, attribute):
        return hasattr(self, self.__class_prefix + attribute)


class FileFrom(TextIOBase):
    def __init__(self, generator):
        self.__generator = generator

    def readline(self):
        try:
            line = next(self.__generator)
        except TypeError:
            log.error('Failed to read line from file-like object.'
                      ' Was it created from an iterator?')
            raise TypeError('Object was not created from an iterator!')
        try:
            assert(type(line) == str)
        except AssertionError:
            log.error('Line read from file-like object is not a string.'
                      ' Was it created from a string iterator?')
            raise TypeError('Line read from file-like object is not a string!')
        return line
