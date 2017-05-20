#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import unittest as ut
from ...logger import write_log_to


class TestLogger(ut.TestCase):

    def test_raises_error_on_wring_filename_type(self):
        err_msg = 'Filename must be a string!'
        with self.assertRaises(TypeError, msg=err_msg) as err:
            write_log_to(12.3)
        self.assertEqual(err.msg, err_msg)

    def test_raises_error_on_non_numeric_logging_level(self):
        err_msg = ('Logging level must be an integer between 10 (= DEBUG)'
                   ' and 50 (= CRITICAL)!')
        with self.assertRaises(TypeError, msg=err_msg) as err:
            write_log_to('file', 'level')
        self.assertEqual(err.msg, err_msg)

    def test_raises_error_on_numeric_logging_level_too_large(self):
        err_msg = ('Logging level must be an integer between 10 (= DEBUG)'
                   ' and 50 (= CRITICAL)!')
        with self.assertRaises(ValueError, msg=err_msg) as err:
            write_log_to('file', 76)
        self.assertEqual(err.msg, err_msg)

    def test_raises_error_on_numeric_logging_level_too_small(self):
        err_msg = ('Logging level must be an integer between 10 (= DEBUG)'
                   ' and 50 (= CRITICAL)!')
        with self.assertRaises(ValueError, msg=err_msg) as err:
            write_log_to('file', -3)
        self.assertEqual(err.msg, err_msg)


if __name__ == '__main__':
    ut.main()
