#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import unittest as ut
from ...algorithms import CollaborativeFiltering, Baseline
from ...datastructures import UserItemMatrix
from ...algorithms.similarities import default_similarity, sokalsneath

class TestCollaborativeFiltering(ut.TestCase):

    def setUp(self):
        pass

    def test(self):
        def func():
            pass
        print(type(func))
        print(callable(func))


if __name__ == '__main__':
    ut.main()
