#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import logging
from ....datastructures.help import FileFrom


class TestFileFrom(ut.TestCase):

    def setUp(self):
        str_generator = (str(i) for i in range(11))
        int_generator = (i for i in range(2))
        self.str_stream = FileFrom(str_generator)
        self.int_stream = FileFrom(int_generator)
        self.no_stream = FileFrom(12.3)

    def test_read_like_file_str_works(self):
        should_be = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        actual = []
        with self.str_stream as file:
            for line in file:
                actual.append(line)
        self.assertListEqual(should_be, actual)

    def test_read_like_file_int_fails(self):
        log_msg = ['ERROR:root:Line read from file-like object is not a'
                   ' string. Was it created from a string iterator?']
        err_msg = 'Line read from file-like object is not a string!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                with self.int_stream as file:
                    for line in file:
                        _ = line
        self.assertListEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_readline_like_file_fails(self):
        log_msg = ['ERROR:root:Failed to read line from file-like object.'
                   ' Was it created from an iterator?']
        err_msg = 'Object was not created from an iterator!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                with self.no_stream as file:
                    for line in file:
                        _ = line
        self.assertListEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)


if __name__ == '__main__':
    ut.main()
