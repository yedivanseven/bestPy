#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log
from numpy import argpartition
from .algorithms import default_algorithm
from .algorithms import Baseline

RETURNING = True


class RecommendationBasedOn():
    def __init__(self, data):
        self.__data = data
        self.__only_new = False
        self.__baseline = Baseline().operating_on(data)
        self.__recommendation = default_algorithm().operating_on(data)
        self.__recommendation_for = {not RETURNING: self.__cold_start,
                                         RETURNING: self.__calculated}

    def using(self, algorithm):
        self.__recommendation = algorithm.operating_on(self.__data)
        return self

    @property
    def pruning_old(self):
        self.__only_new = True
        return self

    @property
    def keeping_old(self):
        self.__only_new = False
        return self

    @property
    def is_pruned(self):
        return self.__only_new

    @property
    def baseline(self):
        return self.__baseline

    @baseline.setter
    def baseline(self, baseline):
        self.__baseline = baseline.operating_on(self.__data)

    def for_one(self, target, max_number_of_items=5):
        type_of = target in self.__data.userIndex_of.keys()
        item_scores = self.__recommendation_for[type_of](target)
        head = self.__min_of(max_number_of_items, len(item_scores))
        sorted_item_indices = argpartition(item_scores, -head)[-head:]
        return (self.__data.itemID_of[index] for index in sorted_item_indices)

    def __cold_start(self, target=None):
        log.info('Unknown target user. Defaulting to baseline recommendation.')
        return self.baseline.for_one()

    def __calculated(self, target):
        target_index = self.__data.userIndex_of[target]
        item_scores = self.__recommendation.for_one(target_index)
        if self.__only_new:
            already_bought = self.__data.matrix_by_row[target_index].indices
            item_scores[already_bought] = float('-inf')
        return item_scores

    def __min_of(self, requested, available):
        if requested > available:
            log.warning('Requested {0} recommendations but only {1} available.'
                        ' Returning all {1}.'.format(requested, available))
        return min(requested, available)
