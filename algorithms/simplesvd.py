#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from numpy import diag
from scipy.sparse.linalg import svds


class SimpleSVD():
    def __init__(self):
        self.__number_of_factors = 20
        self.__binarize = True

    @property
    def number_of_factors(self):
        return self.__number_of_factors

    @number_of_factors.setter
    def number_of_factors(self, number_of_factors):
        if self.__we_need_to_redo_the_SVD_with(number_of_factors):
            del self._SimpleSVD__U
            del self._SimpleSVD__SV
        self.__set(number_of_factors)

    @property
    def binarize(self):
        return self.__binarize

    @binarize.setter
    def binarize(self, binarize):
        if self.__we_need_to_redo_the_SVD_because_we(binarize):
            del self._SimpleSVD__U
            del self._SimpleSVD__SV
        self.__binarize = binarize

    def operating_on(self, data):
        self.__data = data
        SimpleSVD.max_number_of_factors = property(
            lambda self: self.__data.min_matrix_shape - 1
        )
        self.__reset(self.number_of_factors)
        self.for_one = self.__for_one
        if hasattr(self, '_SimpleSVD__U'):
            del self._SimpleSVD__U
            del self._SimpleSVD__SV
        return self

    @property
    def has_data(self):
        return hasattr(self, '_SimpleSVD__data')

    def __for_one(self, target):
        if not hasattr(self, '_SimpleSVD__U'):
            self.__compute_USV_matrices()
        return self.__U[target].dot(self.__SV)

    def __compute_USV_matrices(self):
        self.__U, s, V = svds(self.__matrix(), k=self.number_of_factors)
        self.__SV = diag(s).dot(V)

    def __matrix(self):
        if self.__binarize:
            return self.__data.bool_matrix_by_row
        return self.__data.matrix_by_row

    def __we_need_to_redo_the_SVD_with(self, number_of_factors):
        return (hasattr(self, '_SimpleSVD__U')
                & (number_of_factors != self.number_of_factors))

    def __we_need_to_redo_the_SVD_because_we(self, binarize):
        return (hasattr(self, '_SimpleSVD__U') & (binarize != self.binarize))

    def __set(self, number_of_factors):
        if self.has_data:
            self.__reset(number_of_factors)
        else:
            self.__number_of_factors = number_of_factors

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
