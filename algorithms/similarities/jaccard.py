# -*- coding: utf-8 -*-

from numpy import repeat


def jaccard(data):
    similarity_matrix = data.matrix.bool_by_col.T.dot(data.matrix.bool_by_col)
    diagonal = similarity_matrix.diagonal()
    cols = repeat(diagonal, similarity_matrix.getnnz(axis=0))
    rows = diagonal[similarity_matrix.indices]
    similarity_matrix.data /= (cols + rows - similarity_matrix.data)
    return similarity_matrix
