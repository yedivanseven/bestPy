#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log


class Benchmark():
    def __init__(self, recommender):
        self.__recommendation = recommender

    def against(self, test):
        self.__test = test
        if test.only_new and not self.__recommendation.only_new:
            self.__recommendation = self.__recommendation.pruning_old
            log.info('Resetting recommender to "pruning_old" because of'
                     ' test-data preference.')
        elif not test.only_new and self.__recommendation.only_new:
            self.__recommendation = self.__recommendation.keeping_old
            log.info('Resetting recommender to "keeping_old" because of'
                     ' test-data preference.')
        Benchmark.score = property(lambda self: self.__score())
        return self

    def __score(self):
        total = sum(len(set(self.__recommendation.for_one(user,
                            self.__test.hold_out)).intersection(items))
                    for user, items in self.__test.data.items())
        return total / self.__test.number_of_cases
