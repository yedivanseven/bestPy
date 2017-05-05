#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scipy.sparse import csc_matrix


class Data():
    def __init__(self, data):
        self.matrix_by_col = csc_matrix(data).astype(float)
        self.bool_matrix_by_col = self.matrix_by_col.copy()
        self.bool_matrix_by_col.data[:] = 1.0
        self.number_of_users = data.shape[0]
