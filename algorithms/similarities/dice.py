# -*- coding: utf-8 -*-

from numpy import repeat


def dice(data):
    similarity_matrix = data.matrix.bool_by_col.T.dot(data.matrix.bool_by_col)
    diagonal = similarity_matrix.diagonal()
    cols = repeat(diagonal, similarity_matrix.getnnz(axis=0))
    rows = diagonal[similarity_matrix.indices]
    similarity_matrix.data /= (cols + rows)/2
    return similarity_matrix
