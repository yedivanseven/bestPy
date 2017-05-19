#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import unittest as ut
from ..algorithms import MostPopular, Baseline
from ..datastructures import Transactions
from .. import RecommendationBasedOn


class TestMostPopularOnlyNewIsBaseline(ut.TestCase):

    def setUp(self):
        file = './bestPy/tests/data/data50.csv'
        data = Transactions.from_csv(file)
        self.recommender = RecommendationBasedOn(data)

    def test_most_popular_only_new_returns_baseline(self):
        target = '4'
        baseline = self.recommender.using(Baseline()).pruning_old
        should_be = list(baseline.for_one(target, 4))
        algorithm = self.recommender.using(MostPopular()).pruning_old
        actually_is = list(algorithm.for_one(target, 4))
        self.assertListEqual(should_be, actually_is)


if __name__ == '__main__':
    ut.main()
