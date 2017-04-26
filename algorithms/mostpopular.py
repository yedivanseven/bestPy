#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .baselines import Baseline


class MostPopular():
    def __init__(self):
        self.__baseline = Baseline()
        self.__baseline.binarize = True
        self.__depending_on = {True : self.__unique_buys,
                               False: self.__transactions}
        self.__class_prefix = '_' + self.__class__.__name__ + '__'

    @property
    def binarize(self):
        return self.__baseline.binarize

    @binarize.setter
    def binarize(self, binarize):
        if binarize != self.binarize:
            self.__delete_precomputed()
        self.__baseline.binarize = binarize

    def operating_on(self, data):
        self.__data = data
        self.__baseline = self.__baseline.operating_on(data)
        self.__delete_precomputed()
        self.for_one = self.__for_one
        return self

    @property
    def has_data(self):
        return self.__has('data')

    def __for_one(self, target):
        target_agnostic = self.__precomputed()
        target_specific = self.__data.matrix_by_row[target]
        target_agnostic[target_specific.indices] = target_specific.data
        return target_agnostic

    def __delete_precomputed(self):
        if self.__has('scaled_baseline'):
            delattr(self, self.__class_prefix + 'scaled_baseline')

    def __precomputed(self):
        if not self.__has('scaled_baseline'):
            self.__scaled_baseline = self.__depending_on[self.binarize]()
        return self.__scaled_baseline.copy()

    def __has(self, attribute):
        return hasattr(self, self.__class_prefix + attribute)

    def __unique_buys(self):
        return self.__baseline.for_one() / len(self.__data._count_buys_of)

    def __transactions(self):
        return self.__basline.for_one() / self.__data.number_of_transactions
