# -*- coding: utf-8 -*-

import logging as log
from . import RecommendationBasedOn
from .datastructures.help import TestDataFrom


class Benchmark:
    def __init__(self, recommender):
        self.__recommendation = self.__validated(recommender)

    def against(self, test):
        self.__test = self.__testdata_type_checked(test)
        if test.only_new and not self.__recommendation.only_new:
            self.__recommendation = self.__recommendation.pruning_old
            log.info('Resetting recommender to "pruning_old" because of'
                     ' test-data preference.')
        elif not test.only_new and self.__recommendation.only_new:
            self.__recommendation = self.__recommendation.keeping_old
            log.info('Resetting recommender to "keeping_old" because of'
                     ' test-data preference.')
        Benchmark.score = property(lambda obj: obj.__score())
        return self

    def __score(self):
        total = sum(len(set(self.__recommendation.for_one(user,
                            self.__test.hold_out)).intersection(items))
                    for user, items in self.__test.data.items())
        return total / self.__test.number_of_cases

    @staticmethod
    def __validated(recommender):
        if not isinstance(recommender, RecommendationBasedOn):
            log.error('Attempt to instantiate with incompatible recommender.'
                      ' Must be of type <RecommendationBasedOn>.')
            raise TypeError('Recommender must be of type'
                            ' <RecommendationBasedOn>!')
        return recommender

    @staticmethod
    def __testdata_type_checked(data):
        if not isinstance(data, TestDataFrom):
            log.error('Attempt to set incompatible type of test data.'
                      ' Must be <TestDataFrom>.')
            raise TypeError('Test data must be of type <TestDataFrom>!')
        return data
