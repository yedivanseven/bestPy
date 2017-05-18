# -*- coding: utf-8 -*-

import logging as log
from ..datastructures import UserItemMatrix
from .baselines import Baseline


class MostPopular():
    def __init__(self):
        self.__baseline = Baseline()
        self.__class_prefix = '_' + self.__class__.__name__ + '__'

    @property
    def binarize(self):
        return self.__baseline.binarize

    @binarize.setter
    def binarize(self, binarize):
        self.__check_bool_type_of(binarize)
        if binarize != self.binarize:
            self.__delete_precomputed()
        self.__baseline.binarize = binarize

    def operating_on(self, data):
        self.__data = self.__type_checked(data)
        self.__baseline = self.__baseline.operating_on(data)
        self.__delete_precomputed()
        self.for_one = self.__for_one
        return self

    @property
    def has_data(self):
        return self.__has('data')

    def __for_one(self, target):
        target_agnostic = self.__precomputed()
        target_specific = self.__data.matrix.by_row[target]
        target_agnostic[target_specific.indices] = target_specific.data
        return target_agnostic

    def __precomputed(self):
        if not self.__has('scaled_baseline'):
            depending_on_whether_we = {True : self.__unique_buys,
                                       False: self.__transactions}
            self.__scaled_baseline = depending_on_whether_we[self.binarize]()
        return self.__scaled_baseline.copy()

    def __unique_buys(self):
        return self.__baseline.for_one() / self.__data.number_of_userItem_pairs

    def __transactions(self):
        return self.__baseline.for_one() / self.__data.number_of_transactions

    def __delete_precomputed(self):
        if self.__has('scaled_baseline'):
            delattr(self, self.__class_prefix + 'scaled_baseline')

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
