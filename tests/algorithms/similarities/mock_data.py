# -*- coding: utf-8 -*-

from scipy.sparse import csc_matrix


class Matrix():
    pass

class Index():
    pass

class Data():
    def __init__(self, data):
        self.matrix = Matrix()
        self.user = Index()
        self.matrix.by_col = csc_matrix(data).astype(float)
        self.matrix.bool_by_col = self.matrix.by_col.copy()
        self.matrix.bool_by_col.data[:] = 1.0
        self.user.count = data.shape[0]
