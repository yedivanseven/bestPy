#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
from ....datastructures.help import TestDataFrom


class TestTestDataFrom(ut.TestCase):

    def setUp(self):
        self.data = {'12': {'SA848EL83DOYALID-2416', 'BL152EL82CRXALID-1817'},
                      '7': {'AC016EL56BKHALID-943', 'OL756EL55HAMALID-4744'}}
        self.hold_out = 2
        self.only_new = False
        self.test = TestDataFrom(self.data, self.hold_out, self.only_new)

    def test_data(self):
        self.assertDictEqual(self.test.data, self.data)

    def test_set_data(self):
        with self.assertRaises(AttributeError):
            self.test.data = 'foo'
        self.assertDictEqual(self.test.data, self.data)

    def test_hold_out(self):
        self.assertEqual(self.test.hold_out, self.hold_out)

    def test_set_hold_out(self):
        with self.assertRaises(AttributeError):
            self.test.hold_out = 'bar'
        self.assertEqual(self.test.hold_out, self.hold_out)

    def test_only_new(self):
        self.assertEqual(self.test.only_new, self.only_new)

    def test_set_only_new(self):
        with self.assertRaises(AttributeError):
            self.test.only_new = 'baz'
        self.assertEqual(self.test.only_new, self.only_new)

    def test_number_of_cases(self):
        self.assertEqual(self.test.number_of_cases, 2)

    def test_set_number_of_cases(self):
        with self.assertRaises(AttributeError):
            self.test.number_of_cases = 'foz'
        self.assertEqual(self.test.number_of_cases, 2)


if __name__ == '__main__':
    ut.main()
