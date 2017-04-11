#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from numpy import diag
from scipy.sparse.linalg import svds


class SimpleSVD():
    def __init__(self):
        self.__number_of_features = 20
        self.__binarize = True

    @property
    def number_of_features(self):
        return self.__number_of_features

    @number_of_features.setter
    def number_of_features(self, number_of_features):
        if self.__we_need_to_redo_the_SVD_with(number_of_features):
            del self._SimpleSVD__U
            del self._SimpleSVD__SV
        self.__number_of_features = number_of_features

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
        self.__check()
        self.__U, s, V = svds(self.__matrix(), k=self.number_of_features)
        self.__SV = diag(s).dot(V)

    def __matrix(self):
        if self.__binarize:
            return self.__data.bool_matrix_by_row
        return self.__data.matrix_by_row

    def __we_need_to_redo_the_SVD_with(self, number_of_features):
        return (hasattr(self, '_SimpleSVD__U')
                & (self.__number_of_features != number_of_features))

    def __check(self):
        if self.number_of_features >= self.__data.min_matrix_shape:
            logging.warning('Requested {0} latent features, but only {1} '
                            'available. Resetting to {1}.'.format(
                                self.number_of_features,
                                self.__data.min_matrix_shape - 1
                            ))
            self.number_of_features = self.__data.min_matrix_shape - 1

    def __we_need_to_redo_the_SVD_because_we(self, binarize):
        return (hasattr(self, '_SimpleSVD__U') & (self.__binarize != binarize))
