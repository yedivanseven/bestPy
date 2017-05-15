#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log
from .similarities import default_similarity
from .baselines import default_baseline
from ..datastructures import UserItemMatrix


class CollaborativeFiltering():
    def __init__(self):
        self.__similarity = default_similarity
        self.__baseline = default_baseline()
        self.__binarize = True
        self.__class_prefix = '_' + self.__class__.__name__ + '__'

    @property
    def similarity(self):
        return self.__similarity

    @similarity.setter
    def similarity(self, similarity):
        if similarity != self.similarity:
            self.__delete_sim_mat()
        self.__similarity = similarity

    @property
    def binarize(self):
        return self.__binarize

    @binarize.setter
    def binarize(self, binarize):
        self.__binarize = self.__bool_type_checked(binarize)

    def operating_on(self, data):
        self.__data = self.__type_checked(data)
        self.__baseline = self.__baseline.operating_on(data)
        self.__delete_sim_mat()
        self.for_one = self.__for_one
        return self

    @property
    def baseline(self):
        return self.__baseline

    @baseline.setter
    def baseline(self, baseline):
        self.__baseline = self.__attribute_checked(baseline)
        if self.has_data:
            self.__baseline = self.__baseline.operating_on(self.__data)
            self.__baseline = self.__attribute_checked(self.__baseline)

    @property
    def has_data(self):
        return self.__has('data')

    def __for_one(self, target):
        if self.__no_one_else_bought_items_bought_by(target):
            log.info('Uncomparable user. Returning baseline recommendation.')
            return self.baseline.for_one()
        history_vector = self.__data.matrix_by_row[target]
        if self.binarize:
            history_vector.data[:] = 1.0
        return history_vector.dot(self.__similarity_matrix()).A[0]

    def __similarity_matrix(self):
        if not self.__has('sim_mat'):
            self.__sim_mat = self.similarity(self.__data)
        return self.__sim_mat

    def __delete_sim_mat(self):
        if self.__has('sim_mat'):
            delattr(self, self.__class_prefix + 'sim_mat')

    def __no_one_else_bought_items_bought_by(self, target):
        items_bought_by_target = self.__data.matrix_by_row[target].indices
        return self.__data.users_who_bought(items_bought_by_target).size == 1

    def __bool_type_checked(self, binarize):
        if not isinstance(binarize, bool):
            log.error('Attempt to set "binarize" to non-boolean type.')
            raise TypeError('Attribute "binarize" must be True or False!')
        return binarize

    def __type_checked(self, data):
        if not isinstance(data, UserItemMatrix):
            log.error('Attempt to set incompatible data type.'
                      ' Must be <UserItemMatrix>')
            raise TypeError('Data must be of type <UserItemMatrix>!')
        return data

    def __attribute_checked(self, baseline):
        if not hasattr(baseline, 'operating_on'):
            log.error('Attempt to set baseline object lacking mandatory'
                      ' "operating_on" method.')
            raise AttributeError('Baseline lacks "operating_on" method!')
        if not callable(baseline.operating_on):
            log.error('The "operating_on" method of the baseline object'
                      ' is not callable.')
            raise TypeError('Operating_on method of baseline not callable!')
        if not hasattr(baseline, 'has_data'):
            log.error('Attempt to set baseline object lacking mandatory'
                      ' "has_data" attribute.')
            raise AttributeError('Baseline lacks "has_data" attribute!')
        if baseline.has_data:
            if not hasattr(baseline, 'for_one'):
                log.error('Attempt to set baseline object lacking mandatory'
                          ' "for_one" method.')
                raise AttributeError('Baseline lacks "for_one" method!')
            if not callable(baseline.operating_on):
                log.error('The "for_one" method of the baseline object'
                          ' is not callable.')
                raise TypeError('For_one method of baseline not callable!')
        return baseline

    def __has(self, attribute):
        return hasattr(self, self.__class_prefix + attribute)
