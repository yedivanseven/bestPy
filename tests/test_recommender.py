#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import unittest as ut
from ..algorithms import default_algorithm, default_baseline
from ..datastructures import UserItemMatrix
from .. import RecommendationBasedOn


class TestRecommenderInitialization(ut.TestCase):

    def test_logs_and_raises_error_with_wrong_data_type(self):
        data = 12.3
        log_msg = ['ERROR:root:Attempt to instantiate with incompatible data'
                  ' type. Must be <UserItemMatrix>']
        err_msg = 'Data must be of type <UserItemMatrix>!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg):
                _ = RecommendationBasedOn(data)
        self.assertEqual(log.output, log_msg)


class TestRecommender(ut.TestCase):

    def setUp(self):
        file = './bestPy/tests/data/data50.csv'
        self.data = UserItemMatrix.from_csv(file)
        self.algorithm = default_algorithm()
        self.recommender = RecommendationBasedOn(self.data)

    def test_has_method_using(self):
        self.assertTrue(hasattr(self.recommender, 'using'))

    def test_method_using_is_callable(self):
        self.assertTrue(callable(self.recommender.using))

    def test_error_on_algo_without_using_method(self):
        algorithm = 'foo'
        log_msg = ['ERROR:root:Attempt to set object lacking mandatory'
                   ' "operating_on()" method.']
        err_msg = 'Object lacks "operating_on()" method!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(AttributeError, msg=err_msg):
                _ = self.recommender.using(algorithm)
        self.assertEqual(log.output, log_msg)

    def test_error_on_algo_with_using_method_not_callable(self):
        class MockUp():
            @property
            def operating_on(self):
                pass
        algorithm = MockUp()
        log_msg = ['ERROR:root:The "operating_on()" method of this object'
                   ' is not callable.']
        err_msg = 'Operating_on() method of object not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg):
                _ = self.recommender.using(algorithm)
        self.assertEqual(log.output, log_msg)

    def test_has_attribute_pruning_old(self):
        self.assertTrue(hasattr(self.recommender, 'pruning_old'))

    def test_has_attribute_keeping_old(self):
        self.assertTrue(hasattr(self.recommender, 'keeping_old'))

    def test_has_attribute_only_new(self):
        self.assertTrue(hasattr(self.recommender, 'only_new'))

    def test_pruning_old(self):
        recommendation = self.recommender.pruning_old
        self.assertTrue(recommendation.only_new)

    def test_keeping_old(self):
        recommendation = self.recommender.keeping_old
        self.assertFalse(recommendation.only_new)

    def test_pruning_old_return_type(self):
        recommendation = self.recommender.pruning_old
        self.assertIsInstance(recommendation, RecommendationBasedOn)

    def test_keeping_old_return_type(self):
        recommendation = self.recommender.keeping_old
        self.assertIsInstance(recommendation, RecommendationBasedOn)

    def test_has_attribute_baseline(self):
        self.assertTrue(hasattr(self.recommender, 'baseline'))

    # continue testing the setting of a baseline

if __name__ == '__main__':
    ut.main()
