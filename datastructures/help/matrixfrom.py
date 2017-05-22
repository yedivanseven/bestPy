# -*- coding: utf-8 -*-

import logging as log
from scipy.sparse import csc_matrix


class MatrixFrom():
    def __init__(self, user_item_counts):
        self.__counts_users = self.__validated(user_item_counts)
        self.__class_prefix = '_' + self.__class__.__name__ + '__'

    @property
    def by_col(self):
        if not self.__has('by_col'):
            counts, indices = tuple(zip(*((count, user_item)
                                          for user_item, count
                                          in self.__counts_users.items())))
            self.__by_col = csc_matrix((counts, zip(*indices)))
            self.__by_col = self.__by_col.astype(float)
        return self.__by_col

    @property
    def bool_by_col(self):
        if not self.__has('bool_by_col'):
            self.__bool_by_col = self.by_col.copy()
            self.__bool_by_col.data[:] = 1.0
        return self.__bool_by_col

    @property
    def by_row(self):
        if not self.__has('by_row'):
            self.__by_row = self.by_col.tocsr()
        return self.__by_row

    @property
    def bool_by_row(self):
        if not self.__has('bool_by_row'):
            self.__bool_by_row = self.by_row.copy()
            self.__bool_by_row.data[:] = 1.0
        return self.__bool_by_row

    @property
    def min_shape(self):
        if not self.__has('min_shape'):
            self.__min_shape = min(self.by_col.shape)
        return self.__min_shape

    def __has(self, attribute):
        return hasattr(self, self.__class_prefix + attribute)

    def __validated(self, user_item_counts):
        if not isinstance(user_item_counts, dict):
            log.error('Attempt to instantiate matrix object with'
                      ' non-dictionary argument.')
            raise TypeError('Argument of matrix object must be <dict>!')
        if len(user_item_counts) < 1:
            log.warning('Matrix instantiated with empty dictionary.')
        else:
            key_log = ('Attempt to instantiate matrix object from dictionary'
                      ' with keys not 2-tuple of integer >= 0.')
            key_err = 'Keys of dictionary must be 2-tuple of integer >= 0!'
            val_log = ('Attempt to create matrix object from dictionary'
                       'with values not positive integers.')
            val_err = 'Values of dictionary must be positive integers!'
            key, val = next(iter(user_item_counts.items()))
            if not isinstance(key, tuple) or (len(key) != 2):
                log.error(key_log)
                raise TypeError(key_err)
            if not all(isinstance(number, int) for number in key):
                log.error(key_log)
                raise TypeError(key_err)
            if any(number < 0 for number in key):
                log.error(key_log)
                raise ValueError(key_err)
            if not isinstance(val, int):
                log.error(val_log)
                raise TypeError(val_err)
            if val < 1:
                log.error(val_log)
                raise ValueError(val_err)
        return user_item_counts
