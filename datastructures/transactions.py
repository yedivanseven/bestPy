#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import read


class Transactions():
    def __init__(self, n_buys, n_err, user_i, item_j, counts):
        self.__number_of_transactions = n_buys
        self.__number_of_corrupted_entries = n_err
        self.__userIndex_of = user_i
        self.__itemIndex_of = item_j
        self.__count_buys_of = counts

    @classmethod
    def from_csv(cls, file):
        return cls(*read.from_csv(file))

    @property
    def number_of_transactions(self):
        return self.__number_of_transactions

    @property
    def number_of_corrupted_entries(self):
        return self.__number_of_corrupted_entries

    @property
    def userIndex_of(self):
        return self.__userIndex_of

    @property
    def itemIndex_of(self):
        return self.__itemIndex_of

    @property
    def count_buys_of(self):
        return self.__count_buys_of
