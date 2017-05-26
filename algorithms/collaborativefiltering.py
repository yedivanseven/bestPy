# -*- coding: utf-8 -*-

import logging as log
from .similarities import default_similarity, all_similarities
from .baselines import default_baseline
from ..datastructures import Transactions


class CollaborativeFiltering():
    def __init__(self):
        self.__binarize = True
        self.__similarity = default_similarity
        self.__baseline = default_baseline()
        self.__class_prefix = '_' + self.__class__.__name__ + '__'

    @property
    def binarize(self):
        return self.__binarize

    @binarize.setter
    def binarize(self, binarize):
        self.__binarize = self.__boolean_type_checked(binarize)

    @property
    def similarity(self):
        return self.__similarity.__name__

    @similarity.setter
    def similarity(self, similarity):
        similarity = self.__permitted(similarity)
        if similarity != self.__similarity:
            self.__delete_sim_mat()
        self.__similarity = similarity

    @property
    def baseline(self):
        return self.__baseline.__class__.__name__

    @baseline.setter
    def baseline(self, baseline):
        self.__baseline = self.__base_attribute_checked(baseline)
        if self.has_data:
            self.__baseline = self.__baseline.operating_on(self.__data)
            self.__baseline = self.__data_attribute_checked(self.__baseline)

    def operating_on(self, data):
        self.__data = self.__transactions_type_checked(data)
        self.__baseline = self.__baseline.operating_on(data)
        self.__baseline = self.__data_attribute_checked(self.__baseline)
        self.__delete_sim_mat()
        self.for_one = self.__for_one
        return self

    @property
    def has_data(self):
        return self.__has('data')

    def __for_one(self, target):
        if self.__no_one_else_bought_items_bought_by(target):
            log.info('Uncomparable user with ID {}. Returning baseline'
                     ' recommendation.'.format(self.__data.user.id_of[target]))
            return self.__baseline.for_one()
        history_vector = self.__data.matrix.by_row[target]
        if self.binarize:
            history_vector.data[:] = 1.0
        return history_vector.dot(self.__similarity_matrix()).A[0]

    def __similarity_matrix(self):
        if not self.__has('sim_mat'):
            self.__sim_mat = self.__similarity(self.__data)
        return self.__sim_mat

    def __delete_sim_mat(self):
        if self.__has('sim_mat'):
            delattr(self, self.__class_prefix + 'sim_mat')

    def __no_one_else_bought_items_bought_by(self, target):
        items_bought_by_target = self.__data.matrix.by_row[target].indices
        return self.__data.users_who_bought(items_bought_by_target).size == 1

    def __has(self, attribute):
        return hasattr(self, self.__class_prefix + attribute)

    @staticmethod
    def __permitted(similarity):
        if not similarity in all_similarities:
            log.error('Attempt to set unrecognized similarity.')
            raise TypeError('Unrecognized similarity! See "all_similarities"'
                            ' from the similarities module for your choices.')
        return similarity

    @staticmethod
    def __boolean_type_checked(binarize):
        if not isinstance(binarize, bool):
            log.error('Attempt to set "binarize" to non-boolean type.')
            raise TypeError('Attribute "binarize" must be True or False!')
        return binarize

    @staticmethod
    def __transactions_type_checked(data):
        if not isinstance(data, Transactions):
            log.error('Attempt to set incompatible data type.'
                      ' Must be <Transactions>.')
            raise TypeError('Data must be of type <Transactions>!')
        return data

    @staticmethod
    def __base_attribute_checked(baseline):
        if not hasattr(baseline, 'operating_on'):
            log.error('Attempt to set baseline object lacking mandatory'
                      ' "operating_on()" method.')
            raise AttributeError('Baseline lacks "operating_on()" method!')
        if not callable(baseline.operating_on):
            log.error('The "operating_on()" method of the baseline object'
                      ' is not callable.')
            raise TypeError('Operating_on() method of baseline not callable!')
        if not hasattr(baseline, 'has_data'):
            log.error('Attempt to set baseline object lacking mandatory'
                      ' "has_data" attribute.')
            raise AttributeError('Baseline lacks "has_data" attribute!')
        return baseline

    @staticmethod
    def __data_attribute_checked(baseline):
        if not baseline.has_data:
            log.error("Baseline object's 'has_data' attribute returned False"
                      " after attaching data.")
            raise ValueError('Cannot attach data to baseline object!')
        if not hasattr(baseline, 'for_one'):
            log.error('Attempt to set baseline object lacking mandatory'
                      ' "for_one()" method.')
            raise AttributeError('Baseline lacks "for_one()" method!')
        if not callable(baseline.for_one):
            log.error('The "for_one()" method of the baseline object'
                      ' is not callable.')
            raise TypeError('"for_one()" method of baseline not callable!')
        return baseline
