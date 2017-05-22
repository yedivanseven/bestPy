# -*- coding: utf-8 -*-

import logging as log


class TestDataFrom():
    def __init__(self, data, hold_out, only_new):
        self.__data = self.__dict_type_and_structure_checked(data)
        self.__hold_out = self.__int_type_and_value_checked(hold_out)
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

    def __dict_type_and_structure_checked(self, data):
        if not isinstance(data, dict):
            log.error('Attempt to set non-dictionary type as test data.')
            raise TypeError('Test data must be of type <dict>!')
        if len(data) < 1:
            log.warning('Test data object instantiated with empty dictionary.')
        else:
            value = next(iter(data.values()))
            if not isinstance(value, set):
                log.error('Attempt to initialize test-data object from'
                          ' dictionary with values not of type <set>.')
                raise TypeError('Test data values must be of type <set>!')
            if len(value) < 1:
                log.error('Attempt to initialize test-data object from'
                          ' dictionary with empty set as values.')
                raise ValueError('Test data values must not be empty sets!')
        return data

    def __int_type_and_value_checked(self, hold_out):
        if not isinstance(hold_out, int):
            log.error('Attempt to set non-integer type as "hold_out".')
            raise TypeError('"hold_out" must be of type <int>!')
        what_it_should_be = len(next(iter(self.__data.values())))
        if hold_out != what_it_should_be:
            log.error('Attempt to set argument "hold_out" to value other than'
                      ' the number of held-out items.')
            raise ValueError('"hold_out" differs from the number of'
                             ' held-out items!')
        return hold_out

    def __bool_type_checked(self, only_new):
        if not isinstance(only_new, bool):
            log.error('Attempt to set non-boolean type as "only_new".')
            raise TypeError('"only_new" must be of type <bool>!')
        return only_new
