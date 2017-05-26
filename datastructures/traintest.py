# -*- coding: utf-8 -*-

import logging as log
from operator import itemgetter
from .help import TestDataFrom, FileFrom
from .traintestbase import TrainTestBase
from .transactions import Transactions


class TrainTest(TrainTestBase):
    '''Transaction data split into training and test sets for benchmarking.

    Direct instantiation of this class is discouraged and, therefore,
    not documented. Use the classmethods "from_csv", "from_postgreSQL", ...
    instead and refer to the docstrings there!

    -------------------------------------------------

    Attributes
    ----------
    train : Transactions
        Instance of bestPy.datastructures.Transactions holding
        the training data. Revealed after calling the "split" method.

    test : object
        Object with test data as dictionary in its "data" attribute.
        Further attributes include the number of test cases.
        Is revealed only after calling the "split" method.

    number_of_transactions : int
        Number of transactions in the dataset before splitting.

    number_of_corrupted_records : int
        Number of corrupted records skipped when reading data.

    max_hold_out : int
        Maximum number of unique articles to hold out for testing.

    Methods
    -------
    split(hold_out, only_new)
        Splits transaction data into training and test sets, holding out
        the last "hold_out" unique articles each customer bought as test
        set. The training set depends on whether "only_new" articles should
        be recommened or also previously purchased ones. Once called, the
        data attributes "train" and "test" are revealed.

    Examples
    --------
    >>> data = TrainTest.from_csv(file)
    >>> data.split(4, True)
    >>> data.test.number_of_cases
    10475

    >>> data = TrainTest.from_postgreSQL(database)
    >>> data.split(6, False)
    >>> data.train.number_of_transactions
    345697

    '''

    def __init__(self, n_trans, n_corr, unique, transactions):
        super().__init__(n_trans, n_corr, unique, transactions)
        self.__unique = self._TrainTestBase__unique
        self.__transactions = self._TrainTestBase__transactions

    def split(self, hold_out=5, only_new=True):
        '''Split transaction data into training and test set for benchmarking.

        -----------------------

        Parameters
        ----------
        hold_out : int, optional
            How many unique articles to retain from each
            customer's purchase history for testing later.
            Defaults to 5.

        only_new : bool
            Whether only articles that a given customer has not yet
            bought will be recommended.

        Examples
        --------
        >>> data.split(4, True)

        >>> data.split(6, False)

        '''
        self.__check_boolean_type_of(only_new)
        hold_out = self.__checked_for_integer_type_and_range_of(hold_out)
        keep = {user: items
                for user, items in self.__unique.items()
                if len(items) >= hold_out}
        last_unique_items_of = {user: self.__last(unique_items)[:hold_out]
                                for user, unique_items in keep.items()}
        test = {user: self.__items_from(last_transactions)
                for user, last_transactions in last_unique_items_of.items()}
        if only_new:
            train = (';'.join((timestamp, user, item))
                     for timestamp, user, item in self.__transactions
                     if user in keep.keys()
                     and item not in test[user])
        else:
            train = (';'.join((timestamp, user, item))
                     for timestamp, user, item in self.__transactions
                     if user in keep.keys()
                     and (item, timestamp) not in last_unique_items_of[user])
        self.__test = TestDataFrom(test, hold_out, only_new)
        TrainTest.test = property(lambda obj: obj.__test)
        self.__train = Transactions.from_csv(FileFrom(train))
        TrainTest.train = property(lambda obj: obj.__train)

    @staticmethod
    def __last(unique):
        return sorted(unique.items(), key=itemgetter(1), reverse=True)

    @staticmethod
    def __items_from(last_transactions):
        return set(tuple(zip(*last_transactions))[0])

    @staticmethod
    def __check_boolean_type_of(only_new):
        if not isinstance(only_new, bool):
            log.error('Attempt to set "only_new" to non-boolean type.')
            raise TypeError('Flag "only_new" can only be True or False!')

    def __checked_for_integer_type_and_range_of(self, hold_out):
        if not isinstance(hold_out, int):
            log.error('Attempt to set "hold_out" to non-integer type.')
            raise TypeError('Parameter "hold_out" must be an integer!')
        if hold_out < 1:
            log.warning('Attempt to set hold_out < 1. Resetting to 1.')
            hold_out = 1
        if hold_out > self.max_hold_out:
            log.warning('Hold_out > meaningful maximum of {0}.'
                        ' Resetting to {0}.'.format(self.max_hold_out))
            hold_out = self.max_hold_out
        return hold_out
