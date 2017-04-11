#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from numpy import argpartition
from .algorithms import default

RETURNING = True


class RecommendationBasedOn():
    def __init__(self, data):
        self.__data = data
        self.__only_new = False
        self.__recommendation = default().operating_on(data)
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

    def _baseline(self, max_number_of_items=5):
        head = self.__min_of(max_number_of_items, len(self.__data.baseline))
        sorted_item_indices = argpartition(self.__data.baseline, -head)[-head:]
        return (self.__data.itemID_of[index] for index in sorted_item_indices)

    def for_one(self, target, max_number_of_items=5):
        type_of = target in self.__data.userIndex_of.keys()
        item_scores = self.__recommendation_for[type_of](target)
        head = self.__min_of(max_number_of_items, len(item_scores))
        sorted_item_indices = argpartition(item_scores, -head)[-head:]
        return (self.__data.itemID_of[index] for index in sorted_item_indices)

    def __cold_start(self, target=None):
        logging.warning('Unknown target user. '
                        'Defaulting to baseline recommendation.')
        return self.__data.baseline

    def __calculated(self, target):
        target_index = self.__data.userIndex_of[target]
        item_scores = self.__recommendation.for_one(target_index)
        if self.__only_new:
            already_bought = self.__data.matrix_by_row[target_index].indices
            item_scores[already_bought] = -2
        return item_scores

    def __min_of(self, requested, available):
        if requested > available:
            logging.warning('Requested {0} recommendations, but only {1} '
                            'available.'.format(requested, available))
        return min(requested, available)


if __name__ == '__main__':
    from logger import write_log_to
    from datastructures import UserItemMatrix
    from algorithms import CollaborativeFiltering
    write_log_to('./recolog.txt')
    data = UserItemMatrix.from_csv('./data/head100.csv')
    algo = CollaborativeFiltering()
    recommendation = RecommendationBasedOn(data).using(algo).pruning_old
    print('baseline ...')
    top_five = recommendation._baseline(6)
    for item in top_five:
        print(item)
    print('... and for user')
    top_five = recommendation.for_one('11')
    for item in top_five:
        print(item)
