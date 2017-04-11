#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def russelrao(data):
    similarity_matrix = data.bool_matrix_by_col.T.dot(data.bool_matrix_by_col)
    similarity_matrix.data /= data.number_of_users
    return similarity_matrix
