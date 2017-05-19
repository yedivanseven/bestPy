#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import unittest as ut
from ...algorithms import CollaborativeFiltering, Baseline, default_baseline
from ...datastructures import Transactions
from ...algorithms.similarities import default_similarity, sokalsneath

class TestCollaborativeFiltering(ut.TestCase):

    def setUp(self):
        file = './bestPy/tests/data/data50.csv'
        self.data = Transactions.from_csv(file)
        self.algorithm = CollaborativeFiltering()

    def test_has_attribute_binarize(self):
        self.assertTrue(hasattr(self.algorithm, 'binarize'))

    def test_binarize_type(self):
        log_msg = ['ERROR:root:Attempt to set "binarize" to non-boolean type.']
        err_msg = 'Attribute "binarize" must be True or False!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg):
                self.algorithm.binarize = 'foo'
        self.assertEqual(log.output, log_msg)

    def test_binarize_true(self):
        self.algorithm.binarize = True
        self.assertTrue(self.algorithm.binarize)

    def test_binarize_false(self):
        self.algorithm.binarize = False
        self.assertFalse(self.algorithm.binarize)

    def test_has_attribute_operating_on(self):
        self.assertTrue(hasattr(self.algorithm, 'operating_on'))

    def test_attribute_operating_on_is_callable(self):
        self.assertTrue(callable(self.algorithm.operating_on))

    def test_has_attribute_has_data(self):
        self.assertTrue(hasattr(self.algorithm, 'has_data'))

    def test_has_data_false(self):
        self.assertFalse(self.algorithm.has_data)

    def test_has_data_true(self):
        self.algorithm = self.algorithm.operating_on(self.data)
        self.assertTrue(self.algorithm.has_data)

    def test_cannot_set_attribute_has_data_without_data(self):
        with self.assertRaises(AttributeError):
            self.algorithm.has_data = 'bar'
        self.assertFalse(self.algorithm.has_data)

    def test_cannot_set_attribute_has_data_with_data(self):
        self.algorithm = self.algorithm.operating_on(self.data)
        with self.assertRaises(AttributeError):
            self.algorithm.has_data = 'baz'
        self.assertTrue(self.algorithm.has_data)

    def test_data_type(self):
        log_msg = ['ERROR:root:Attempt to set incompatible data type.'
                  ' Must be <Transactions>.']
        err_msg = 'Data must be of type <Transactions>!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg):
                _ = self.algorithm.operating_on('foz')
        self.assertEqual(log.output, log_msg)

    def test_no_attribute_for_one_after_wrong_data_type(self):
        with self.assertLogs(level=logging.ERROR):
            with self.assertRaises(TypeError):
                _ = self.algorithm.operating_on('john')
        self.assertFalse(hasattr(self.algorithm, 'for_one'))

    def test_no_attribute_for_one_without_data(self):
        self.assertFalse(hasattr(self.algorithm, 'for_one'))

    def test_has_attribute_for_one_with_data(self):
        self.algorithm = self.algorithm.operating_on(self.data)
        self.assertTrue(hasattr(self.algorithm, 'for_one'))

    def test_has_default_baseline(self):
        should_be = default_baseline().__class__.__name__
        self.assertEqual(self.algorithm.baseline, should_be)

    def test_set_baseline_without_data(self):
        should_be = CollaborativeFiltering().__class__.__name__
        self.algorithm.baseline = CollaborativeFiltering()
        self.assertEqual(self.algorithm.baseline, should_be)

    def test_set_baseline_with_data(self):
        should_be = CollaborativeFiltering().__class__.__name__
        self.algorithm = self.algorithm.operating_on(self.data)
        self.algorithm.baseline = CollaborativeFiltering()
        self.assertEqual(self.algorithm.baseline, should_be)

    def test_baseline_no_operating_on_method(self):
        class MockUp():
            pass
        log_msg = ['ERROR:root:Attempt to set baseline object lacking'
                   ' mandatory "operating_on()" method.']
        err_msg = 'Baseline lacks "operating_on()" method!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(AttributeError, msg=err_msg):
                self.algorithm.baseline = MockUp()
        self.assertEqual(log.output, log_msg)

    def test_baseline_operating_on_method_not_callable(self):
        class MockUp():
            pass
        baseline = MockUp()
        baseline.operating_on = 'foo'
        log_msg = ['ERROR:root:The "operating_on()" method of the baseline'
                   ' object is not callable.']
        err_msg = 'Operating_on() method of baseline not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg):
                self.algorithm.baseline = baseline
        self.assertEqual(log.output, log_msg)

    def test_baseline_has_no_has_data_attrribute(self):
        class MockUp():
            def operating_on(self, data):
                return self
        baseline = MockUp()
        log_msg = ['ERROR:root:Attempt to set baseline object lacking'
                   ' mandatory "has_data" attribute.']
        err_msg = 'Baseline lacks "has_data" attribute!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(AttributeError, msg=err_msg):
                self.algorithm.baseline = baseline
        self.assertEqual(log.output, log_msg)

    def test_data_not_attached_to_baseline(self):
        class MockUp():
            @property
            def has_data(self):
                return False
            def operating_on(self, data):
                return self
        self.algorithm.baseline = MockUp()
        log_msg = ["ERROR:root:Baseline object's 'has_data' attribute returned"
                   " False after attaching data."]
        err_msg = 'Cannot attach data to baseline object!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ValueError, msg=err_msg):
                self.algorithm = self.algorithm.operating_on(self.data)
        self.assertEqual(log.output, log_msg)

    def test_baseline_has_no_for_one_method(self):
        class MockUp():
            @property
            def has_data(self):
                return True
            def operating_on(self, data):
                return self
        self.algorithm.baseline = MockUp()
        log_msg = ['ERROR:root:Attempt to set baseline object lacking'
                   ' mandatory "for_one()" method.']
        err_msg = 'Baseline lacks "for_one()" method!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(AttributeError, msg=err_msg):
                self.algorithm = self.algorithm.operating_on(self.data)
        self.assertEqual(log.output, log_msg)

    def test_baseline_for_one_method_is_not_callable(self):
        class MockUp():
            @property
            def has_data(self):
                return True
            def operating_on(self, data):
                return self
        baseline = MockUp()
        baseline.for_one = 'bar'
        self.algorithm.baseline = baseline
        log_msg = ['ERROR:root:The "for_one()" method of the baseline object'
                   ' is not callable.']
        err_msg = '"for_one()" method of baseline not callable!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg):
                self.algorithm = self.algorithm.operating_on(self.data)
        self.assertEqual(log.output, log_msg)

    def test_has_default_similarity(self):
        should_be = default_similarity.__name__
        self.assertEqual(self.algorithm.similarity, should_be)

    def test_set_permitted_similarity(self):
        self.algorithm.similarity = sokalsneath
        self.assertEqual(self.algorithm.similarity, 'sokalsneath')

    def test_set_forbidden_similarity(self):
        def dice(data):
            pass
        log_msg = ['ERROR:root:Attempt to set unrecognized similarity.']
        err_msg = ('Unrecognized similarity! See "all_similarities"' +
                   ' from the similarities module for your choices.')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg):
                self.algorithm.similarity = dice
        self.assertEqual(log.output, log_msg)

    def test_binarized_recommendation_does_not_change(self):
        target = 5
        self.algorithm.binarize = True
        self.algorithm = self.algorithm.operating_on(self.data)
        before = self.algorithm.for_one(target).copy().tolist()
        recommendation = self.algorithm.for_one(target)
        recommendation += 1
        after = self.algorithm.for_one(target).tolist()
        self.assertListEqual(before, after)

    def test_non_binarized_recommendation_does_not_change(self):
        target = 5
        self.algorithm.binarize = False
        self.algorithm = self.algorithm.operating_on(self.data)
        before = self.algorithm.for_one(target).copy().tolist()
        recommendation = self.algorithm.for_one(target)
        recommendation += 1
        after = self.algorithm.for_one(target).tolist()
        self.assertListEqual(before, after)

    def test_binarized_data_does_not_change(self):
        target = 5
        before_col = self.data.matrix.by_col.copy().todense().tolist()
        before_row = self.data.matrix.by_row.copy().todense().tolist()
        before_boolcol = self.data.matrix.bool_by_col.copy().todense().tolist()
        before_boolrow = self.data.matrix.bool_by_row.copy().todense().tolist()
        self.algorithm.binarize = True
        self.algorithm = self.algorithm.operating_on(self.data)
        recommendation = self.algorithm.for_one(target)
        recommendation += 1
        after_col = self.data.matrix.by_col.copy().todense().tolist()
        after_row = self.data.matrix.by_row.copy().todense().tolist()
        after_boolcol = self.data.matrix.bool_by_col.copy().todense().tolist()
        after_boolrow = self.data.matrix.bool_by_row.copy().todense().tolist()
        self.assertListEqual(before_col, after_col)
        self.assertListEqual(before_row, after_row)
        self.assertListEqual(before_boolcol, after_boolcol)
        self.assertListEqual(before_boolrow, after_boolrow)

    def test_non_binarized_data_does_not_change(self):
        target = 5
        before_col = self.data.matrix.by_col.copy().todense().tolist()
        before_row = self.data.matrix.by_row.copy().todense().tolist()
        before_boolcol = self.data.matrix.bool_by_col.copy().todense().tolist()
        before_boolrow = self.data.matrix.bool_by_row.copy().todense().tolist()
        self.algorithm.binarize = False
        self.algorithm = self.algorithm.operating_on(self.data)
        recommendation = self.algorithm.for_one(target)
        recommendation += 1
        after_col = self.data.matrix.by_col.copy().todense().tolist()
        after_row = self.data.matrix.by_row.copy().todense().tolist()
        after_boolcol = self.data.matrix.bool_by_col.copy().todense().tolist()
        after_boolrow = self.data.matrix.bool_by_row.copy().todense().tolist()
        self.assertListEqual(before_col, after_col)
        self.assertListEqual(before_row, after_row)
        self.assertListEqual(before_boolcol, after_boolcol)
        self.assertListEqual(before_boolrow, after_boolrow)

    def test_default_recommendation_non_binarized(self):
        target = 5
        self.algorithm = self.algorithm.operating_on(self.data)
        self.algorithm.binarize = False
        history_vector = self.data.matrix.by_row[target]
        similarity_matrix = default_similarity(self.data)
        should_be = history_vector.dot(similarity_matrix).A[0].tolist()
        actually_is = self.algorithm.for_one(target).tolist()
        self.assertListEqual(should_be, actually_is)

    def test_default_recommendation_binarized(self):
        target = 5
        self.algorithm = self.algorithm.operating_on(self.data)
        self.algorithm.binarize = True
        history_vector = self.data.matrix.by_row[target]
        history_vector.data[:] = 1.0
        similarity_matrix = default_similarity(self.data)
        should_be = history_vector.dot(similarity_matrix).A[0].tolist()
        actually_is = self.algorithm.for_one(target).tolist()
        self.assertListEqual(should_be, actually_is)

    def test_explicit_recommendation_non_binarized(self):
        target = 5
        should_be = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9.0, 24.333333333333336,
                     24.333333333333336, 0.0, 0.0, 0.3333333333333333, 0.0,
                     0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 24.333333333333336,
                     24.333333333333336, 24.333333333333336,
                     24.333333333333336]
        self.algorithm = self.algorithm.operating_on(self.data)
        self.algorithm.binarize = False
        self.algorithm.similarity = sokalsneath
        actually_is = self.algorithm.for_one(target).tolist()
        self.assertListEqual(should_be, actually_is)

    def test_explicit_recommendation_binarized(self):
        target = 5
        should_be = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 6.333333333333333,
                     6.333333333333333, 0.0, 0.0, 0.3333333333333333, 0.0,
                     0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.333333333333333,
                     6.333333333333333, 6.333333333333333, 6.333333333333333]
        self.algorithm = self.algorithm.operating_on(self.data)
        self.algorithm.binarize = True
        self.algorithm.similarity = sokalsneath
        actually_is = self.algorithm.for_one(target).tolist()
        self.assertListEqual(should_be, actually_is)

    def test_logs_uncomparable_user_and_returns_default_baseline(self):
        target = 6
        file = './bestPy/tests/data/data50.csv'
        data = Transactions.from_csv(file)
        log_msg = ['INFO:root:Uncomparable user with ID 13. Returning baseline'
                   ' recommendation.']
        self.algorithm = self.algorithm.operating_on(data)
        should_be = default_baseline().operating_on(data).for_one().tolist()
        with self.assertLogs(level=logging.INFO) as log:
            actually_is = self.algorithm.for_one(target).tolist()
        self.assertEqual(log.output, log_msg)
        self.assertListEqual(should_be, actually_is)

    def test_logs_uncomparable_user_and_returns_explicit_baseline(self):
        target = 6
        file = './bestPy/tests/data/data50.csv'
        data = Transactions.from_csv(file)
        log_msg = ['INFO:root:Uncomparable user with ID 13. Returning baseline'
                   ' recommendation.']
        self.algorithm = self.algorithm.operating_on(data)
        self.algorithm.baseline = Baseline()
        should_be = Baseline().operating_on(data).for_one().tolist()
        with self.assertLogs(level=logging.INFO) as log:
            actually_is = self.algorithm.for_one(target).tolist()
        self.assertEqual(log.output, log_msg)
        self.assertListEqual(should_be, actually_is)

    def test_data_is_passed_on_to_baseline_before(self):
        target = 6
        should_be = Baseline().operating_on(self.data).for_one().tolist()
        file = './bestPy/tests/data/data25semicolon.csv'
        with self.assertLogs(level=logging.WARNING):
            data = Transactions.from_csv(file)
        baseline = Baseline().operating_on(data)
        self.algorithm.baseline = baseline
        self.algorithm = self.algorithm.operating_on(self.data)
        with self.assertLogs(level=logging.INFO):
            actually_is = self.algorithm.for_one(target).tolist()
        self.assertListEqual(should_be, actually_is)

    def test_data_is_passed_on_to_baseline_after(self):
        target = 6
        should_be = Baseline().operating_on(self.data).for_one().tolist()
        file = './bestPy/tests/data/data25semicolon.csv'
        with self.assertLogs(level=logging.WARNING):
            data = Transactions.from_csv(file)
        baseline = Baseline().operating_on(data)
        self.algorithm = self.algorithm.operating_on(self.data)
        self.algorithm.baseline = baseline
        with self.assertLogs(level=logging.INFO):
            actually_is = self.algorithm.for_one(target).tolist()
        self.assertListEqual(should_be, actually_is)

    def test_length_of_recommendation_equals_number_of_items(self):
        target = 5
        should_be = self.data.item.count
        self.algorithm = self.algorithm.operating_on(self.data)
        actually_is = len(self.algorithm.for_one(target))
        self.assertEqual(should_be, actually_is)


if __name__ == '__main__':
    ut.main()
