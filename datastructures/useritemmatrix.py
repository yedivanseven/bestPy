# -*- coding: utf-8 -*-

from numpy import unique
from . import read
from .help import IndexFrom, MatrixFrom


class UserItemMatrix():
    def __init__(self, n_rec, n_err, user_i, item_j, counts):
        self.__number_of_transactions = n_rec
        self.__number_of_corrupted_records = n_err
        self.__number_of_userItem_pairs = len(counts)
        self.__user = IndexFrom(user_i)
        self.__item = IndexFrom(item_j)
        self.__matrix = MatrixFrom(counts)

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
