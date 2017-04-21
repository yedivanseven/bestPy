#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .transactionbase import TransactionBase


class Transactions(TransactionBase):

    @property
    def number_of_users(self):
        if not self.__has('number_of_users'):
            self.__number_of_users = len(self.userIndex_of)
        return self.__number_of_users

    @property
    def number_of_items(self):
        if not self.__has('number_of_items'):
            self.__number_of_items = len(self.itemIndex_of)
        return self.__number_of_items

    @property
    def userID_of(self):
        if not self.__has('userID_of'):
            self.__userID_of = {index: user
                                for user, index
                                in self.userIndex_of.items()}
        return self.__userID_of

    @property
    def itemID_of(self):
        if not self.__has('itemID_of'):
            self.__itemID_of = {index: item
                                for item, index
                                in self.itemIndex_of.items()}
        return self.__itemID_of

    def __has(self, attribute):
        class_prefix = '_' + self.__class__.__name__ + '__'
        return hasattr(self, class_prefix + attribute)
