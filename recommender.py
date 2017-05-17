# -*- coding: utf-8 -*-

import logging as log
from numpy import argpartition
from .algorithms import default_algorithm
from .algorithms import default_baseline
from .datastructures import UserItemMatrix

RETURNING = True


class RecommendationBasedOn():
    def __init__(self, data):
        self.__data = self.__type_checked(data)
        self.__only_new = True
        self.__baseline = default_baseline().operating_on(data)
        self.__recommendation = default_algorithm().operating_on(data)
        self.__recommendation_for = {not RETURNING: self.__cold_start,
                                         RETURNING: self.__calculated}

    def using(self, algorithm):
        self.__check_base_attributes_of(algorithm)
        self.__recommendation = algorithm.operating_on(self.__data)
        self.__check_data_attributes_of(algorithm)
        return self

    @property
    def algorithm(self):
        return self.__recommendation.__class__.__name__

    @property
    def pruning_old(self):
        self.__only_new = True
        return self

    @property
    def keeping_old(self):
        self.__only_new = False
        return self

    @property
    def only_new(self):
        return self.__only_new

    @property
    def baseline(self):
        return self.__baseline.__class__.__name__

    @baseline.setter
    def baseline(self, baseline):
        self.__check_base_attributes_of(baseline)
        self.__baseline = baseline.operating_on(self.__data)
        self.__check_data_attributes_of(baseline)

    def for_one(self, target, max_number_of_items=5):
        head = self.__type_and_range_checked(max_number_of_items)
        type_of = target in self.__data.userIndex_of.keys()
        item_scores = self.__recommendation_for[type_of](target)
        sorted_item_indices = argpartition(item_scores, -head)[-head:]
        return (self.__data.itemID_of[index] for index in sorted_item_indices)

    def __cold_start(self, target=None):
        log.info('Unknown target user. Defaulting to baseline recommendation.')
        return self.__baseline.for_one()

    def __calculated(self, target):
        target_index = self.__data.userIndex_of[target]
        item_scores = self.__recommendation.for_one(target_index)
        if self.__only_new:
            already_bought = self.__data.matrix_by_row[target_index].indices
            item_scores[already_bought] = float('-inf')
        return item_scores

    def __type_checked(self, data):
        if not isinstance(data, UserItemMatrix):
            log.error('Attempt to instantiate with incompatible data type.'
                      ' Must be <UserItemMatrix>.')
            raise TypeError('Data must be of type <UserItemMatrix>!')
        return data

    def __check_base_attributes_of(self, algorithm):
        if not hasattr(algorithm, 'operating_on'):
            log.error('Attempt to set object lacking mandatory'
                      ' "operating_on()" method.')
            raise AttributeError('Object lacks "operating_on()" method!')
        if not callable(algorithm.operating_on):
            log.error('The "operating_on()" method of this object'
                      ' is not callable.')
            raise TypeError('"operating_on()" method of object not callable!')
        if not hasattr(algorithm, 'has_data'):
            log.error('Attempt to set object lacking mandatory'
                      ' "has_data" attribute.')
            raise AttributeError('Object lacks "has_data" attribute!')

    def __check_data_attributes_of(self, algorithm):
        if not algorithm.has_data:
            log.error("Object's 'has_data' attribute returned False"
                      " after attaching data.")
            raise ValueError('Cannot attach data to object!')
        if not hasattr(algorithm, 'for_one'):
            log.error('Attempt to set object lacking mandatory'
                      ' "for_one()" method.')
            raise AttributeError('Object lacks "for_one()" method!')
        if not callable(algorithm.for_one):
            log.error('The "for_one()" method of this object'
                      ' is not callable.')
            raise TypeError('"for_one()" method of object not callable!')

    def __type_and_range_checked(self, requested):
        if not isinstance(requested, int):
            log.error('Requested number of recommendations is not an integer.')
            raise TypeError('Requested number of recommendations must be'
                             ' a positive integer!')
        if requested < 1:
            log.error('Requested number of recommendations < 1.')
            raise ValueError('Requested number of recommendations must be'
                             ' a positive integer!')
        available = self.__data.number_of_items
        if requested > available:
            log.warning('Requested {0} recommendations but only {1} available.'
                        ' Returning all {1}.'.format(requested, available))
            requested = available
        return requested
