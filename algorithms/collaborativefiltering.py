#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log
from .similarities import default_similarity


class CollaborativeFiltering():
    def __init__(self):
        self.__similarity = default_similarity
        self.__binarize = True
        self.__class_prefix = '_' + self.__class__.__name__ + '__'

    @property
    def similarity(self):
        return self.__similarity

    @similarity.setter
    def similarity(self, similarity):
        if self.__we_need_to_recompute_the_matrix_of(similarity):
            self.__delete_sim_mat()
        self.__similarity = similarity

    @property
    def binarize(self):
        return self.__binarize

    @binarize.setter
    def binarize(self, binarize):
        self.__binarize = binarize

    def operating_on(self, data):
        self.__data = data
        self.for_one = self.__for_one
        if self.__has('sim_mat'):
            self.__delete_sim_mat()
        return self

    @property
    def has_data(self):
        return self.__has('data')

    def __for_one(self, target):
        if self.__no_one_else_bought_items_bought_by(target):
            log.info('Uncomparable user. Returning baseline recommendation.')
            return self.__data.baseline

        history_vector = self.__data.matrix_by_row[target]
        if self.binarize:
            history_vector.data[:] = 1.0
        return history_vector.dot(self.__similarity_matrix()).A[0]

    def __similarity_matrix(self):
        if not self.__has('sim_mat'):
            self.__sim_mat = self.similarity(self.__data)
        return self.__sim_mat

    def __delete_sim_mat(self):
        delattr(self, self.__class_prefix + 'sim_mat')

    def __no_one_else_bought_items_bought_by(self, target):
        items_bought_by_target = self.__data.matrix_by_row[target].indices
        return self.__data.users_who_bought(items_bought_by_target).size == 1

    def __we_need_to_recompute_the_matrix_of(self, similarity):
        return (self.__has('sim_mat') and (similarity != self.__similarity))

    def __has(self, attribute):
        return hasattr(self, self.__class_prefix + attribute)
