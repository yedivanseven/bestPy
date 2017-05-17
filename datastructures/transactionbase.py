# -*- coding: utf-8 -*-

from . import read


class TransactionBase():
    def __init__(self, n_rec, n_err, user_i, item_j, counts):
        self.__number_of_transactions = n_rec
        self.__number_of_corrupted_records = n_err
        self.__userIndex_of = user_i
        self.__itemIndex_of = item_j
        self.__count_buys_of = counts

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
    def userIndex_of(self):
        return self.__userIndex_of

    @property
    def itemIndex_of(self):
        return self.__itemIndex_of

    @property
    def _count_buys_of(self):
        return self.__count_buys_of
