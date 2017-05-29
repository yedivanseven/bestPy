# -*- coding: utf-8 -*-

import logging as log


class IndexFrom:
    def __init__(self, index_of):
        self.__index_of = self.__dict_type_and_empty_checked(index_of)
        self.__class_prefix = '_' + self.__class__.__name__ + '__'

    @property
    def index_of(self):
        '''Dictionary with unique ID as key and integer index as value.'''
        return self.__index_of

    @property
    def id_of(self):
        '''Dictionary with integer index as key and unique ID as value.'''
        if not self.__has('id_of'):
            self.__id_of = {value: key
                            for key, value
                            in self.__index_of.items()}
        return self.__id_of

    @property
    def count(self):
        if not self.__has('count'):
            self.__count = len(self.index_of)
        return self.__count

    def __has(self, attribute):
        return hasattr(self, self.__class_prefix + attribute)

    @staticmethod
    def __dict_type_and_empty_checked(index_of):
        if not isinstance(index_of, dict):
            log.error('Attempt to instantiate index object with'
                      ' non-dictionary argument.')
            raise TypeError('Argument of index object must be of type <dict>!')
        if len(index_of) < 1:
            log.warning('Index instantiated with empty dictionary.')
        return index_of
