#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import unittest as ut
from ...algorithms import CollaborativeFiltering, Baseline, default_baseline
from ...datastructures import UserItemMatrix
from ...algorithms.similarities import default_similarity, sokalsneath

class TestCollaborativeFiltering(ut.TestCase):

    def setUp(self):
        file = './bestPy/tests/data/data50.csv'
        self.data = UserItemMatrix.from_csv(file)
        self.algorithm = CollaborativeFiltering()

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
                  ' Must be <UserItemMatrix>']
        err_msg = 'Data must be of type <UserItemMatrix>!'
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
        self.assertIsInstance(self.algorithm.baseline, default_baseline)

    def test_set_baseline_without_data(self):
        self.algorithm.baseline = Baseline()
        self.assertIsInstance(self.algorithm.baseline, Baseline)

    def test_set_baseline_with_data(self):
        self.algorithm.baseline = Baseline()
        self.algorithm = self.algorithm.operating_on(self.data)
        self.assertTrue(hasattr(self.algorithm.baseline, 'for_one'))

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
        self.assertTrue(self.algorithm.similarity is default_similarity)

    def test_set_permitted_similarity(self):
        self.algorithm.similarity = sokalsneath
        self.assertTrue(self.algorithm.similarity is sokalsneath)

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

    def test_recommendation_binarized(self):
        target = 3
        self.algorithm = self.algorithm.operating_on(self.data)
        recommendation = self.algorithm.for_one(target)
        print(recommendation)


if __name__ == '__main__':
    ut.main()