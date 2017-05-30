# -*- coding: utf-8 -*-

from numpy import reciprocal, sqrt
from scipy.sparse import diags


def cosine_binary(data):
    """Cosine similarity among articles.

    Unlike the simple `cosine` similarity measure, the non-zero entries in the
    article vectors are all taken to be 1.0 here.


    Parameters
    ----------
    data : `Transactions`
        An instance of `bestPy.datastructures.Transactions`.

    Returns
    -------
    scipy.sparse.csc_matrix
        The matrix of pairwise similarities in scipy compressed sparse
        column (CSC) format.
    """
    norm = diags(reciprocal(sqrt(data.matrix.bool_by_col.power(2).sum(0))).A1)
    normed_user_item_matrix = data.matrix.bool_by_col.dot(norm)
    similarity_matrix = normed_user_item_matrix.T.dot(normed_user_item_matrix)
    return similarity_matrix
