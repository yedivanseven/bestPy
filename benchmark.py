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
        Benchmark.baseline = property(lambda self: self.__baseline())
        Benchmark.score = property(lambda self: self.__score())
        return self

    def __baseline(self):
        baseline = set(self.__recommendation._baseline(self.__test.hold_out))
        total = sum(len(baseline.intersection(items))
                    for items in self.__test.data.values())
        self.__baseline = total / self.__test.number_of_cases
        return self.__baseline

    def __score(self):
        total = sum(len(set(self.__recommendation.for_one(user,
                            self.__test.hold_out)).intersection(items))
                    for user, items in self.__test.data.items())
        return total / self.__test.number_of_cases
