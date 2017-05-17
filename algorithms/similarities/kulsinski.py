# -*- coding: utf-8 -*-

from numpy import repeat


def kulsinski(data):
    smat = data.bool_matrix_by_col.T.dot(data.bool_matrix_by_col)
    diagonal = smat.diagonal()
    cols = repeat(diagonal, smat.getnnz(axis=0))
    rows = diagonal[smat.indices]
    smat.data /= (cols + rows - 2*smat.data + data.number_of_users)
    return smat
