# -*- coding: utf-8 -*-


def russellrao(data):
    similarity_matrix = data.matrix.bool_by_col.T.dot(data.matrix.bool_by_col)
    similarity_matrix.data /= data.user.count
    return similarity_matrix
