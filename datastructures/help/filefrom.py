# -*- coding: utf-8 -*-

import logging as log
from io import TextIOBase


class FileFrom(TextIOBase):
    def __init__(self, generator):
        self.__generator = generator

    def readline(self):
        try:
            line = next(self.__generator)
        except TypeError:
            log.error('Failed to read line from file-like object.'
                      ' Was it created from an iterator?')
            raise TypeError('Object was not created from an iterator!')
        try:
            assert(type(line) == str)
        except AssertionError:
            log.error('Line read from file-like object is not a string.'
                      ' Was it created from a string iterator?')
            raise TypeError('Line read from file-like object is not a string!')
        return line
