#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import logging
from ....datastructures.help import IndexFrom


class TestInstatiateIndex(ut.TestCase):

    def test_error_on_wrong_argument_type(self):
        log_msg = ['ERROR:root:Attempt to instantiate index object with'
                   ' non-dictionary argument.']
        err_msg = 'Argument of index object must be of type <dict>!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = IndexFrom('foo')
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_warning_on_empty_dictionary_as_argument(self):
        log_msg = ['WARNING:root:Index instantiated with empty dictionary.']
        with self.assertLogs(level=logging.WARNING) as log:
            _ = IndexFrom({})
        self.assertEqual(log.output, log_msg)


class TestIndexFrom(ut.TestCase):

    def setUp(self):
        self.dictionary = {'AC016EL50CPHALID-1749': 0,
                           'CA189EL29AGOALID-170' : 1,
                           'LE629EL54ANHALID-345' : 2,
                           'OL756EL65HDYALID-4834': 3,
                           'OL756EL55HAMALID-4744': 4,
                           'AC016EL56BKHALID-943' : 5}
        self.invertdict = {0: 'AC016EL50CPHALID-1749',
                           1: 'CA189EL29AGOALID-170',
                           2: 'LE629EL54ANHALID-345',
                           3: 'OL756EL65HDYALID-4834',
                           4: 'OL756EL55HAMALID-4744',
                           5: 'AC016EL56BKHALID-943'}
        self.index = IndexFrom(self.dictionary)

    def test_has_attribute_index_of(self):
        self.assertTrue(hasattr(self.index, 'index_of'))

    def test_cannot_set_attribute_index_of(self):
        with self.assertRaises(AttributeError):
            self.index.index_of = 12.3
        self.assertDictEqual(self.index.index_of, self.dictionary)

    def test_type_of_attribute_index_of(self):
        self.assertIsInstance(self.index.index_of, dict)

    def test_correct_values_in_index_of(self):
        self.assertDictEqual(self.index.index_of, self.dictionary)

    def test_has_attribute_id_of(self):
        self.assertTrue(hasattr(self.index, 'id_of'))

    def test_cannot_set_attribute_id_of(self):
        with self.assertRaises(AttributeError):
            self.index.id_of = 'foo'
        self.assertDictEqual(self.index.id_of, self.invertdict)

    def test_type_of_attribute_id_of(self):
        self.assertIsInstance(self.index.id_of, dict)

    def test_correct_values_in_id_of(self):
        self.assertDictEqual(self.index.id_of, self.invertdict)

    def test_has_attribute_count(self):
        self.assertTrue(hasattr(self.index, 'count'))

    def test_cannot_set_attribute_count(self):
        with self.assertRaises(AttributeError):
            self.index.count = {'foo': 1}
        self.assertEqual(self.index.count, 6)

    def test_type_of_attribute_count(self):
        self.assertIsInstance(self.index.count, int)

    def test_correct_values_in_count(self):
        self.assertEqual(self.index.count, 6)


if __name__ == '__main__':
    ut.main()
