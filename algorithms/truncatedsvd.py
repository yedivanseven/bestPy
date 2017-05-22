# -*- coding: utf-8 -*-

import logging as log
from numpy import diag
from scipy.sparse.linalg import svds
from ..datastructures import Transactions


class TruncatedSVD():
    def __init__(self):
        self.__binarize = True
        self.__number_of_factors = 20
        self.__class_prefix = '_' + self.__class__.__name__ + '__'

    @property
    def binarize(self):
        return self.__binarize

    @binarize.setter
    def binarize(self, binarize):
        self.__check_bool_type_of(binarize)
        if binarize != self.binarize:
            self.__delete_USV_matrices()
        self.__binarize = binarize

    @property
    def number_of_factors(self):
        return self.__number_of_factors

    @number_of_factors.setter
    def number_of_factors(self, number_of_factors):
        self.__check_integer_type_and_range_of(number_of_factors)
        previous_number_of_factors = self.number_of_factors
        self.__set(number_of_factors)
        if self.number_of_factors != previous_number_of_factors:
            self.__delete_USV_matrices()

    def operating_on(self, data):
        self.__data = self.__type_checked(data)
        TruncatedSVD.max_number_of_factors = property(
            lambda self: self.__data.matrix.min_shape - 1
        )
        self.__reset(self.number_of_factors)
        self.__delete_USV_matrices()
        self.for_one = self.__for_one
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
        if self.__has('U'):
            delattr(self, self.__class_prefix + 'U')
        if self.__has('SV'):
            delattr(self, self.__class_prefix + 'SV')

    def __matrix(self):
        if self.__binarize:
            return self.__data.matrix.bool_by_row
        return self.__data.matrix.by_row

    def __set(self, number_of_factors):
        if not self.has_data:
            self.__number_of_factors = number_of_factors
        else:
            self.__reset(number_of_factors)

    def __reset(self, number_of_factors):
        if number_of_factors > self.max_number_of_factors:
            log.warning('Requested {0} latent features, but only {1}'
                        ' available. Resetting to {1}.'.format(
                            number_of_factors,
                            self.max_number_of_factors
                        ))
            self.__number_of_factors = self.max_number_of_factors
        else:
            self.__number_of_factors = number_of_factors

    def __has(self, attribute):
        return hasattr(self, self.__class_prefix + attribute)

    def __check_integer_type_and_range_of(self, number_of_factors):
        error_message = '"number_of_factors" must be a positive integer!'
        if not isinstance(number_of_factors, int):
            log.error('Attempt to set number_of_factors to non-integer type.')
            raise TypeError(error_message)
        if number_of_factors < 1:
            log.error('Attempt to set number_of_factors to value < 1.')
            raise ValueError(error_message)

    def __check_bool_type_of(self, binarize):
        if not isinstance(binarize, bool):
            log.error('Attempt to set "binarize" to non-boolean type.')
            raise TypeError('Attribute "binarize" must be True or False!')

    def __type_checked(self, data):
        if not isinstance(data, Transactions):
            log.error('Attempt to set incompatible data type.'
                      ' Must be <Transactions>.')
            raise TypeError('Data must be of type <Transactions>!')
        return data
