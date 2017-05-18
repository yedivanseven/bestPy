# -*- coding: utf-8 -*-

import logging as log
from ...datastructures import UserItemMatrix


class Baseline():
    def __init__(self):
        self.__binarize = True
        self.__depending_on_whether_we = {True : self.__count_unique_buyers,
                                          False: self.__sum_over_all_buys}
        self.__class_prefix = '_' + self.__class__.__name__ + '__'

    @property
    def binarize(self):
        return self.__binarize

    @binarize.setter
    def binarize(self, binarize):
        self.__check_bool_type_of(binarize)
        if binarize != self.binarize:
            self.__delete_precomputed()
        self.__binarize = binarize

    def operating_on(self, data):
        self.__data = self.__type_checked(data)
        self.__delete_precomputed()
        self.for_one = self.__for_one
        return self

    @property
    def has_data(self):
        return self.__has('data')

    def __for_one(self, target=None):
        return self.__depending_on_whether_we[self.binarize]()

    def __count_unique_buyers(self):
        if not self.__has('number_of_buyers'):
            self.__number_of_buyers = self.__data.matrix.bool_by_col.sum(0).A1
        return self.__number_of_buyers.copy()

    def __sum_over_all_buys(self):
        if not self.__has('number_of_buys'):
            self.__number_of_buys = self.__data.matrix.by_col.sum(0).A1
        return self.__number_of_buys.copy()

    def __delete_precomputed(self):
        if self.__has('number_of_buyers'):
            delattr(self, self.__class_prefix + 'number_of_buyers')
        if self.__has('number_of_buys'):
            delattr(self, self.__class_prefix + 'number_of_buys')

    def __check_bool_type_of(self, binarize):
        if not isinstance(binarize, bool):
            log.error('Attempt to set "binarize" to non-boolean type.')
            raise TypeError('Attribute "binarize" must be True or False!')

    def __type_checked(self, data):
        if not isinstance(data, UserItemMatrix):
            log.error('Attempt to set incompatible data type.'
                      ' Must be <UserItemMatrix>.')
            raise TypeError('Data must be of type <UserItemMatrix>!')
        return data

    def __has(self, attribute):
        return hasattr(self, self.__class_prefix + attribute)
