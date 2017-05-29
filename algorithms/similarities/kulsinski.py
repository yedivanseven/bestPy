# -*- coding: utf-8 -*-

from numpy import repeat


def kulsinski(data):
    '''Kulsinski similarity among articles.

    Parameters
    ----------
    data : `Transactions`
        An instance of `bestPy.datastructures.Transactions`.

    Returns
    -------
    scipy.sparse.csc_matrix
        The matrix of pairwise similarities in scipy compressed sparse
        column (CSC) format.

    '''
    smat = data.matrix.bool_by_col.T.dot(data.matrix.bool_by_col)
    diagonal = smat.diagonal()
    cols = repeat(diagonal, smat.getnnz(axis=0))
    rows = diagonal[smat.indices]
    smat.data /= (cols + rows - 2*smat.data + data.user.count)
    return smat
