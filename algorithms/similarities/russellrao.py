# -*- coding: utf-8 -*-


def russellrao(data):
    '''Russell-Rao similarity among articles.

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
    similarity_matrix = data.matrix.bool_by_col.T.dot(data.matrix.bool_by_col)
    similarity_matrix.data /= data.user.count
    return similarity_matrix
