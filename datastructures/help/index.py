# -*- coding: utf-8 -*-


class Index():
    def __init__(self, index_of):
        self.__index_of = index_of
        self.__class_prefix = '_' + self.__class__.__name__ + '__'

    @property
    def index_of(self):
        return self.__index_of

    @property
    def ID_of(self):
        if not self.__has('ID_of'):
            self.__ID_of = {value: key
                            for key, value
                            in self.__index_of.items()}
        return self.__ID_of

    @property
    def count(self):
        if not self.__has('count'):
            self.__count = len(self.index_of)
        return self.__count

    def __has(self, attribute):
        return hasattr(self, self.__class_prefix + attribute)
