#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import repeat


def sokalsneath(data):
    similarity_matrix = data.bool_matrix_by_col.T.dot(data.bool_matrix_by_col)
    diagonal = similarity_matrix.diagonal()
    cols = repeat(diagonal, similarity_matrix.getnnz(axis=0))
    rows = diagonal[similarity_matrix.indices]
    similarity_matrix.data /= (2*(cols + rows) - 3*similarity_matrix.data)
    return similarity_matrix
