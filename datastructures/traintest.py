#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from io import TextIOBase
from operator import itemgetter
from . import split
from .useritemmatrix import UserItemMatrix


class TrainTest():
    def __init__(self, n_rec, n_err, unique, trans):
        self.__number_of_transactions = n_rec
        self.__number_of_corrupted_records = n_err
        self.__unique = unique
        self.__transactions = trans

    @classmethod
    def from_csv(cls, file):
        return cls(*split.from_csv(file))

    @property
    def number_of_transactions(self):
        return self.__number_of_transactions

    @property
    def number_of_corrupted_records(self):
        return self.__number_of_corrupted_records

    def split(self, hold_out=5, only_new=True):
        keep = {user: items
                for user, items in self.__unique.items()
                if len(items) >= hold_out}
        last_unique = {user: self.__last(unique)[:hold_out]
                       for user, unique in keep.items()}
        test = {user: self.__items_from(last_transactions)
                for user, last_transactions in last_unique.items()}
        if only_new:
            train = (';'.join((timestamp, user, item))
                     for timestamp, user, item in self.__transactions
                     if user in keep.keys()
                     and item not in test[user])
        else:
            train = (';'.join((timestamp, user, item))
                     for timestamp, user, item in self.__transactions
                     if user in keep.keys()
                     and (timestamp, item) not in last_unique[user])
        self.__test = TestDataFrom(test, hold_out, only_new)
        TrainTest.test = property(lambda self: self.__test)
        self.__train = UserItemMatrix.from_csv(FileFrom(train))
        TrainTest.train = property(lambda self: self.__train)

    def __last(self, unique):
        return sorted(unique.items(), key=itemgetter(1), reverse=True)

    def __items_from(self, last):
        return set(tuple(zip(*last))[0])


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
        line = next(self.__generator)
        return line
