#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class MostPopular():
    def __init__(self):
        self.__binarize = True
        self.__class_prefix = '_' + self.__class__.__name__ + '__'

    @property
    def binarize(self):
        return self.__binarize

    @binarize.setter
    def binarize(self, binarize):
        if binarize != self.binarize:
            self.__delete_precomputed()
        self.__binarize = binarize

    def operating_on(self, data):
        self.__data = data
        self.__delete_precomputed()
        self.for_one = self.__for_one
        return self

    @property
    def has_data(self):
        return self.__has('data')

    def __for_one(self, target):
        target_agnostic = self.__target_agnostic()
        target_specific = self.__data.matrix_by_row[target]
        target_agnostic[target_specific.indices] = target_specific.data
        return target_agnostic

    def __target_agnostic(self):
        if self.binarize:
            return self.__count()
        return self.__sum()

    def __delete_precomputed(self):
        if self.__has('unique_buyers'):
            delattr(self, self.__class_prefix + 'unique_buyers')
        if self.__has('number_of_buys'):
            delattr(self, self.__class_prefix + 'number_of_buys')

    def __has(self, attribute):
        return hasattr(self, self.__class_prefix + attribute)

    def __count(self):
        if not self.__has('unique_buyers'):
            self.__unique_buyers = (self.__data.baseline /
                                    len(self.__data._count_buys_of))
        return self.__unique_buyers.copy()

    def __sum(self):
        if not self.__has('number_of_buys'):
            self.__number_of_buys = (self.__data.matrix_by_col.sum(0).A1 /
                                     self.__data.number_of_transactions)
        return self.__number_of_buys.copy()
