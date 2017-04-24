#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Benchmark():
    def __init__(self, recommender):
        self.__recommendation = recommender

    def against(self, test):
        self.__test = test
        if test.only_new:
            self.__recommendation = self.__recommendation.pruning_old
        else:
            self.__recommendation = self.__recommendation.keeping_old
        Benchmark.score = property(lambda self: self.__score())
        return self

    def __score(self):
        total = sum(len(set(self.__recommendation.for_one(user,
                            self.__test.hold_out)).intersection(items))
                    for user, items in self.__test.data.items())
        return total / self.__test.number_of_cases
