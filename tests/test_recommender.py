#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import unittest as ut
from ..algorithms import default_algorithm, default_baseline, TruncatedSVD
from ..datastructures import UserItemMatrix
from .. import RecommendationBasedOn


class TestRecommenderInitialization(ut.TestCase):

    def test_logs_and_raises_error_with_wrong_data_type(self):
        data = 12.3
        log_msg = ['ERROR:root:Attempt to instantiate with incompatible data'
                  ' type. Must be <UserItemMatrix>.']
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

    def test_error_on_algo_without_operating_on_method(self):
        algorithm = 'foo'
        log_msg = ['ERROR:root:Attempt to set object lacking mandatory'
                   ' "operating_on()" method.']
        err_msg = 'Object lacks "operating_on()" method!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(AttributeError, msg=err_msg):
                _ = self.recommender.using(algorithm)
        self.assertEqual(log.output, log_msg)

    def test_error_on_algorithm_with_operating_method_not_callable(self):
        class MockUp():
            pass
        algorithm = MockUp()
        algorithm.operating_on = 'bar'
        log_msg = ['ERROR:root:The "operating_on()" method of this object'
                   ' is not callable.']
        err_msg = '"operating_on()" method of object not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg):
                _ = self.recommender.using(algorithm)
        self.assertEqual(log.output, log_msg)

    def test_error_on_algorithm_without_has_data_attribute(self):
        class MockUp():
            def operating_on(self, data):
                return self
        algorithm = MockUp()
        log_msg = ['ERROR:root:Attempt to set object lacking mandatory'
                   ' "has_data" attribute.']
        err_msg = 'Object lacks "has_data" attribute!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(AttributeError, msg=err_msg):
                _ = self.recommender.using(algorithm)
        self.assertEqual(log.output, log_msg)

    def test_error_on_data_not_attachable_to_algorithm(self):
        class MockUp():
            @property
            def has_data(self):
                return False
            def operating_on(self, data):
                return self
        algorithm = MockUp()
        log_msg = ["ERROR:root:Object's 'has_data' attribute returned False"
                   " after attaching data."]
        err_msg = 'Cannot attach data to object!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ValueError, msg=err_msg):
                _ = self.recommender.using(algorithm)
        self.assertEqual(log.output, log_msg)

    def test_error_on_algorithm_has_no_for_one_method(self):
        class MockUp():
            @property
            def has_data(self):
                return True
            def operating_on(self, data):
                return self
        algorithm = MockUp()
        log_msg = ['ERROR:root:Attempt to set object lacking mandatory'
                   ' "for_one()" method.']
        err_msg = 'Object lacks "for_one()" method!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(AttributeError, msg=err_msg):
                _ = self.recommender.using(algorithm)
        self.assertEqual(log.output, log_msg)

    def test_error_on_algorithm_for_one_method_is_not_callable(self):
        class MockUp():
            @property
            def has_data(self):
                return True
            def operating_on(self, data):
                return self
        algorithm = MockUp()
        algorithm.for_one = 'baz'
        log_msg = ['ERROR:root:The "for_one()" method of this object'
                   ' is not callable.']
        err_msg = '"for_one()" method of object not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg):
                _ = self.recommender.using(algorithm)
        self.assertEqual(log.output, log_msg)

    def test_has_attribute_algorithm(self):
        self.assertTrue(hasattr(self.recommender, 'algorithm'))

    def test_algorithm_is_default(self):
        should_be = default_algorithm().__class__.__name__
        self.assertEqual(self.recommender.algorithm, should_be)

    def test_cannot_set_attribute_algorithm(self):
        should_be = default_algorithm().__class__.__name__
        with self.assertRaises(AttributeError):
            self.recommender.algorithm = 45.6
        self.assertEqual(self.recommender.algorithm, should_be)

    def test_setting_legitimate_algorithm_works(self):
        algorithm = TruncatedSVD()
        algorithm.number_of_factors = 3
        should_be = algorithm.__class__.__name__
        recommender = self.recommender.using(algorithm)
        self.assertEqual(self.recommender.algorithm, should_be)

    def test_has_attribute_pruning_old(self):
        self.assertTrue(hasattr(self.recommender, 'pruning_old'))

    def test_has_attribute_keeping_old(self):
        self.assertTrue(hasattr(self.recommender, 'keeping_old'))

    def test_has_attribute_only_new(self):
        self.assertTrue(hasattr(self.recommender, 'only_new'))

    def test_cannot_set_attribute_only_new(self):
        before = self.recommender.only_new
        with self.assertRaises(AttributeError):
            self.recommender.only_new = 78.9
        after = self.recommender.only_new
        self.assertEqual(before, after)

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

    def test_cannot_set_attribute_pruning_old(self):
        before = self.recommender.only_new
        with self.assertRaises(AttributeError):
            self.recommender.pruning_old = 'foo'
        recommendation = self.recommender.pruning_old
        after = self.recommender.only_new
        self.assertIsInstance(recommendation, RecommendationBasedOn)
        self.assertEqual(before, after)

    def test_cannot_set_attribute_keeping_old(self):
        before = not self.recommender.only_new
        with self.assertRaises(AttributeError):
            self.recommender.keeping_old = 'bar'
        recommendation = self.recommender.keeping_old
        after = self.recommender.only_new
        self.assertIsInstance(recommendation, RecommendationBasedOn)
        self.assertEqual(before, after)

    def test_has_attribute_baseline(self):
        self.assertTrue(hasattr(self.recommender, 'baseline'))

    def test_has_default_baseline(self):
        should_be = default_baseline().__class__.__name__
        self.assertEqual(should_be, self.recommender.baseline)

    def test_error_on_baseline_without_operating_on_method(self):
        baseline = 'foo'
        log_msg = ['ERROR:root:Attempt to set object lacking mandatory'
                   ' "operating_on()" method.']
        err_msg = 'Object lacks "operating_on()" method!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(AttributeError, msg=err_msg):
                self.recommender.baseline = baseline
        self.assertEqual(log.output, log_msg)

    def test_error_on_baseline_with_operating_method_not_callable(self):
        class MockUp():
            pass
        baseline = MockUp()
        baseline.operating_on = 'bar'
        log_msg = ['ERROR:root:The "operating_on()" method of this object'
                   ' is not callable.']
        err_msg = '"operating_on()" method of object not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg):
                self.recommender.baseline = baseline
        self.assertEqual(log.output, log_msg)

    def test_error_on_baseline_without_has_data_attribute(self):
        class MockUp():
            def operating_on(self, data):
                return self
        baseline = MockUp()
        log_msg = ['ERROR:root:Attempt to set object lacking mandatory'
                   ' "has_data" attribute.']
        err_msg = 'Object lacks "has_data" attribute!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(AttributeError, msg=err_msg):
                self.recommender.baseline = baseline
        self.assertEqual(log.output, log_msg)

    def test_error_on_data_not_attachable_to_baseline(self):
        class MockUp():
            @property
            def has_data(self):
                return False
            def operating_on(self, data):
                return self
        baseline = MockUp()
        log_msg = ["ERROR:root:Object's 'has_data' attribute returned False"
                   " after attaching data."]
        err_msg = 'Cannot attach data to object!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ValueError, msg=err_msg):
                self.recommender.baseline = baseline
        self.assertEqual(log.output, log_msg)

    def test_error_on_baseline_has_no_for_one_method(self):
        class MockUp():
            @property
            def has_data(self):
                return True
            def operating_on(self, data):
                return self
        baseline = MockUp()
        log_msg = ['ERROR:root:Attempt to set object lacking mandatory'
                   ' "for_one()" method.']
        err_msg = 'Object lacks "for_one()" method!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(AttributeError, msg=err_msg):
                self.recommender.baseline = baseline
        self.assertEqual(log.output, log_msg)

    def test_error_on_baseline_for_one_method_is_not_callable(self):
        class MockUp():
            @property
            def has_data(self):
                return True
            def operating_on(self, data):
                return self
        baseline = MockUp()
        baseline.for_one = 'baz'
        log_msg = ['ERROR:root:The "for_one()" method of this object'
                   ' is not callable.']
        err_msg = '"for_one()" method of object not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg):
                self.recommender.baseline = baseline
        self.assertEqual(log.output, log_msg)

    def test_setting_legitimate_baseline_works(self):
        baseline = TruncatedSVD()
        baseline.number_of_factors = 3
        should_be = baseline.__class__.__name__
        self.recommender.baseline = baseline
        self.assertEqual(self.recommender.baseline, should_be)

    def test_data_is_passed_on_to_baseline(self):
        file = './bestPy/tests/data/data25semicolon.csv'
        with self.assertLogs(level=logging.WARNING):
            data = UserItemMatrix.from_csv(file)
        baseline = default_baseline().operating_on(data)
        self.recommender.baseline = baseline
        should_be = self.data.item.count
        actually_is = len(list(self.recommender.for_one(1, 23)))
        self.assertEqual(should_be, actually_is)

    def test_has_method_for_one(self):
        self.assertTrue(hasattr(self.recommender, 'for_one'))

    def test_method_for_one_is_callable(self):
        self.assertTrue(callable(self.recommender.for_one))

    def test_number_of_recommendations(self):
        target = '4'
        top_hits = self.recommender.for_one(target, 4)
        self.assertEqual(len(list(top_hits)), 4)

    def test_logs_warning_and_resets_on_too_many_recommendations(self):
        target = '4'
        log_msg = ['WARNING:root:Requested 25 recommendations but only 23'
                   ' available. Returning all 23.']
        with self.assertLogs(level = logging.WARNING) as log:
            top_hits = self.recommender.for_one(target, 25)
        self.assertEqual(len(list(top_hits)), 23)
        self.assertEqual(log.output, log_msg)

    def test_error_on_too_few_recommendations(self):
        target = '4'
        log_msg = ['ERROR:root:Requested number of recommendations < 1.']
        err_msg = ('Requested number of recommendations must be' +
                   ' a positive integer!')
        with self.assertLogs(level = logging.ERROR) as log:
            with self.assertRaises(ValueError, msg=err_msg):
                _ = self.recommender.for_one(target, 0)
        self.assertEqual(log.output, log_msg)

    def test_error_on_wrong_recommendation_number_type(self):
        target = '4'
        log_msg = ['ERROR:root:Requested number of recommendations is not'
                   ' an integer.']
        err_msg = ('Requested number of recommendations must be' +
                   ' a positive integer!')
        with self.assertLogs(level = logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg):
                _ = self.recommender.for_one(target, 23.5)
        self.assertEqual(log.output, log_msg)

    def test_logs_warning_on_unknown_user(self):
        target = 'john doe'
        log_msg = ['INFO:root:Unknown target user. Defaulting to baseline'
                   ' recommendation.']
        with self.assertLogs(level=logging.INFO) as log:
            top_hits = self.recommender.for_one(target)
        self.assertEqual(log.output, log_msg)

    def test_recommendation_for_unknown_user_is_baseline(self):
        target = 'john doe'
        should_be = ['CA189EL29AGOALID-170', 'BL152EL82CRXALID-1817',
                     'SA848EL83DOYALID-2416', 'OL756EL65HDYALID-4834']
        self.recommender = self.recommender.pruning_old
        with self.assertLogs(level=logging.INFO):
            actually_is = list(self.recommender.for_one(target, 4))
        self.assertListEqual(actually_is, should_be)
        self.recommender = self.recommender.keeping_old
        with self.assertLogs(level=logging.INFO):
            actually_is = list(self.recommender.for_one(target, 4))
        self.assertListEqual(actually_is, should_be)

    def test_recommendation_for_known_user_is_algorithm(self):
        target = '7'
        self.recommender = self.recommender.pruning_old
        should_be = ['PI794EL32ENZALID-3067', 'AC016EL67BJWALID-932',
                     'VI962EL59EFGALID-2840', 'MO717EL47ARKALID-452']
        actually_is = list(self.recommender.for_one(target, 4))
        self.assertListEqual(actually_is, should_be)

    def test_recommendation_keeping_old_known_user(self):
        target = '7'
        self.recommender = self.recommender.keeping_old
        should_be = ['AC016EL56BKHALID-943', 'OL756EL55HAMALID-4744',
                     'OL756EL65HDYALID-4834', 'AC016EL58BKFALID-941']
        actually_is = list(self.recommender.for_one(target, 4))
        self.assertListEqual(actually_is, should_be)

    def test_data_is_passed_on_to_algorithm(self):
        file = './bestPy/tests/data/data25semicolon.csv'
        with self.assertLogs(level=logging.WARNING):
            data = UserItemMatrix.from_csv(file)
        algorithm = default_algorithm().operating_on(data)
        recommender = self.recommender.using(algorithm)
        should_be = self.data.item.count
        actually_is = len(list(recommender.for_one(1, 23)))
        self.assertEqual(should_be, actually_is)


if __name__ == '__main__':
    ut.main()
