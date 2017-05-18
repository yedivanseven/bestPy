# -*- coding: utf-8 -*-

import logging as log


class TestDataFrom():
    def __init__(self, data, hold_out, only_new):
        self.__data = self.__dict_type_checked(data)
        self.__hold_out = self.__int_type_checked(hold_out)
        self.__only_new = self.__bool_type_checked(only_new)
        self.__class_prefix = '_' + self.__class__.__name__ + '__'

    @property
    def data(self):
        return self.__data

    @property
    def hold_out(self):
        return self.__hold_out

    @property
    def only_new(self):
        return self.__only_new

    @property
    def number_of_cases(self):
        if not self.__has('number_of_cases'):
            self.__number_of_cases = len(self.__data)
        return self.__number_of_cases

    def __has(self, attribute):
        return hasattr(self, self.__class_prefix + attribute)

    def __dict_type_checked(self, data):
        if not isinstance(data, dict):
            log.error('Attempt to set non-dictionary type as test data.')
            raise TypeError('Test data must be of type <dict>!')
        return data

    def __int_type_checked(self, hold_out):
        if not isinstance(hold_out, int):
            log.error('Attempt to set non-integer type as "hold_out".')
            raise TypeError('"hold_out" must be of type <int>!')
        return hold_out

    def __bool_type_checked(self, only_new):
        if not isinstance(only_new, bool):
            log.error('Attempt to set non-boolean type as "only_new".')
            raise TypeError('"only_new" must be of type <bool>!')
        return only_new
