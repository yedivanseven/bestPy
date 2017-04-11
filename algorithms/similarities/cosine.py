#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import reciprocal, sqrt
from scipy.sparse import diags


def cosine(data):
    norm = diags(reciprocal(sqrt(data.matrix_by_col.power(2).sum(0))).A1)
    normed_user_item_matrix = data.matrix_by_col.dot(norm)
    similarity_matrix = normed_user_item_matrix.T.dot(normed_user_item_matrix)
    return similarity_matrix
