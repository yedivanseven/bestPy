#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from numpy import diag
from scipy.sparse.linalg import svds


class NaiveSVD():
    def __init__(self):
        self.__number_of_factors = 20
        self.__binarize = True
        self.__class_prefix = '_' + self.__class__.__name__ + '__'

    @property
    def number_of_factors(self):
        return self.__number_of_factors

    @number_of_factors.setter
    def number_of_factors(self, number_of_factors):
        if self.__we_need_to_redo_the_SVD_with(number_of_factors):
            self.__delete_USV_matrices()
        self.__set(number_of_factors)

    @property
    def binarize(self):
        return self.__binarize

    @binarize.setter
    def binarize(self, binarize):
        if self.__we_need_to_redo_the_SVD_because_we(binarize):
            self.__delete_USV_matrices()
        self.__binarize = binarize

    def operating_on(self, data):
        self.__data = data
        NaiveSVD.max_number_of_factors = property(
            lambda self: self.__data.min_matrix_shape - 1
        )
        self.__reset(self.number_of_factors)
        self.for_one = self.__for_one
        if self.__has('U'):
            self.__delete_USV_matrices()
        return self

    @property
    def has_data(self):
        return self.__has('data')

    def __for_one(self, target):
        if not self.__has('U'):
            self.__compute_USV_matrices()
        return self.__U[target].dot(self.__SV)

    def __compute_USV_matrices(self):
        self.__U, s, V = svds(self.__matrix(), k=self.number_of_factors)
        self.__SV = diag(s).dot(V)

    def __delete_USV_matrices(self):
        delattr(self, self.__class_prefix + 'U')
        delattr(self, self.__class_prefix + 'SV')

    def __matrix(self):
        if self.__binarize:
            return self.__data.bool_matrix_by_row
        return self.__data.matrix_by_row

    def __we_need_to_redo_the_SVD_with(self, number_of_factors):
        return (self.__has('U') & (number_of_factors != self.number_of_factors))

    def __we_need_to_redo_the_SVD_because_we(self, binarize):
        return (self.__has('U') & (binarize != self.binarize))

    def __set(self, number_of_factors):
        if not self.has_data:
            self.__number_of_factors = number_of_factors
        else:
            self.__reset(number_of_factors)

    def __reset(self, number_of_factors):
        if number_of_factors > self.max_number_of_factors:
            logging.warning('Requested {0} latent features, but only {1} '
                            'available. Resetting to {1}.'.format(
                                number_of_factors,
                                self.max_number_of_factors
                            ))
            self.__number_of_factors = self.max_number_of_factors
        else:
            self.__number_of_factors = number_of_factors

    def __has(self, attribute):
        return hasattr(self, self.__class_prefix + attribute)
