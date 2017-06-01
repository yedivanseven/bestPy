# -*- coding: utf-8 -*-

import logging as log
from . import RecoBasedOn
from .datastructures.help import TestDataFrom


class Benchmark:
    """Benchmarks a given recommendation engine against held-out test data.

    Parameters
    ----------
    recommender : `RecoBasedOn`
        A configured instance of `bestPy.RecoBasedOn` with the training data.

    Methods
    -------
    against(test) : `Benchmark` instance it is invoked on.
        Called with a `TestDataFrom` instance as argument, it returns
        the `Benchmark` instance it is invoked on with the test data set
        accordingly and unlocks the otherwise hidden attribute `score`.

    Attributes
    ----------
    score : float
        The average number of correctly predicted purchases per customer.

    Examples
    --------
    >>> benchmark = Benchmark(recommender).against(data.test)
    >>> benchmark.score
    0.8934756

    """

    def __init__(self, recommender):
        self.__recommendation = self.__validated(recommender)

    def against(self, test):
        """Sets the test data to score the provided recommendation engine.

        Parameters
        ----------
        test : object
            A test-data object, best provided by the `test` attribute
            of a `bestPy.datastructures.TrainTest` instance.

        Returns
        -------
        The instance of `Benchmark` it is called on, now with the previously
        hidden attribute `score` enabled and the test data set accordingly.

        Examples
        --------
        >>> benchmark = Benchmark(recommender)
        >>> benchmark = benchmark.against(data.test)

        """
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
        """Returns the average number of correctly predicted buys per user."""
        total = sum(len(set(self.__recommendation.for_one(user,
                            self.__test.hold_out)).intersection(items))
                    for user, items in self.__test.data.items())
        return total / self.__test.number_of_cases

    @staticmethod
    def __validated(recommender):
        if not isinstance(recommender, RecoBasedOn):
            log.error('Attempt to instantiate with incompatible recommender.'
                      ' Must be of type <RecoBasedOn>.')
            raise TypeError('Recommender must be of type <RecoBasedOn>!')
        return recommender

    @staticmethod
    def __testdata_type_checked(data):
        if not isinstance(data, TestDataFrom):
            log.error('Attempt to set incompatible type of test data.'
                      ' Must be <TestDataFrom>.')
            raise TypeError('Test data must be of type <TestDataFrom>!')
        return data
