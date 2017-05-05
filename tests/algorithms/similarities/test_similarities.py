#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import numpy as np
import scipy.spatial.distance as spd
from .mock_data import Data
from ....algorithms.similarities import cosine_binary, cosine, dice, jaccard
from ....algorithms.similarities import kulsinski, russellrao, sokalsneath

MATRIX = np.array([[1, 0, 3, 5, 0, 2],
                   [0, 1, 2, 0, 4, 1],
                   [3, 4, 0, 0, 1, 1],
                   [5, 0, 1, 2, 3, 0],
                   [2, 0, 4, 2, 0, 0],
                   [0, 7, 0, 1, 2, 5],
                   [4, 2, 5, 3, 5, 4]])
BOOL_MATRIX = MATRIX.astype(bool).astype(float)


class TestSimilarities(ut.TestCase):

    def setUp(self):
        self.data = Data(MATRIX)

    def test_cosine(self):
        should_be = spd.squareform(spd.pdist(MATRIX.T, spd.cosine))
        actually_is = (1 - cosine(self.data).toarray())
        self.assertTrue(np.allclose(should_be, actually_is))

    def test_cosine_binary(self):
        should_be = spd.squareform(spd.pdist(BOOL_MATRIX.T, spd.cosine))
        actually_is = (1 - cosine_binary(self.data).toarray())
        self.assertTrue(np.allclose(should_be, actually_is))

    def test_dice(self):
        should_be = spd.squareform(spd.pdist(BOOL_MATRIX.T, spd.dice))
        actually_is = (1 - dice(self.data).toarray())
        self.assertTrue(np.allclose(should_be, actually_is))

    def test_jaccard(self):
        should_be = spd.squareform(spd.pdist(BOOL_MATRIX.T, spd.jaccard))
        actually_is = (1 - jaccard(self.data).toarray())
        self.assertTrue(np.allclose(should_be, actually_is))

    def test_kulsinski(self):
        n_items = MATRIX.shape[1]
        should_be = np.zeros((n_items, n_items))
        for i in range(n_items):
            for j in range(n_items):
                should_be[i, j] = spd.kulsinski(BOOL_MATRIX.T[i],
                                                BOOL_MATRIX.T[j])
        actually_is = (1 - kulsinski(self.data).toarray())
        self.assertTrue(np.allclose(should_be, actually_is))

    def test_russellrao(self):
        n_items = MATRIX.shape[1]
        should_be = np.zeros((n_items, n_items))
        for i in range(n_items):
            for j in range(n_items):
                should_be[i, j] = spd.russellrao(BOOL_MATRIX.T[i],
                                                 BOOL_MATRIX.T[j])
        actually_is = (1 - russellrao(self.data).toarray())
        self.assertTrue(np.allclose(should_be, actually_is))

    def test_sokalsneath(self):
        should_be = spd.squareform(spd.pdist(BOOL_MATRIX.T, spd.sokalsneath))
        actually_is = (1 - sokalsneath(self.data).toarray())
        self.assertTrue(np.allclose(should_be, actually_is))


if __name__ == '__main__':
    ut.main()
