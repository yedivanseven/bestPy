#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from operator import itemgetter
from .traintestbase import TrainTestBase, TestDataFrom, FileFrom
from .useritemmatrix import UserItemMatrix


class TrainTest(TrainTestBase):
    def __init__(self, n_rec, n_err, unique, trans):
        super().__init__(n_rec, n_err, unique, trans)
        self.__unique = self._TrainTestBase__unique
        self.__transactions = self._TrainTestBase__transactions

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
