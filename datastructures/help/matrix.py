# -*- coding: utf-8 -*-

from scipy.sparse import csc_matrix


class Matrix():
    def __init__(self, user_item_counts):
        self.__counts_users = user_item_counts
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
