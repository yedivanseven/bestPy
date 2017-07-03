# -*- coding: utf-8 -*-

import logging as log
from operator import itemgetter
from ..auxiliary import TestDataFrom, FileFrom
from .traintestbase import TrainTestBase
from ..transactions import Transactions


class TrainTest(TrainTestBase):
    """Transaction data split into training and test sets for benchmarking.

    Direct instantiation of this class is discouraged and, therefore,
    not documented. Use the classmethods `from_csv()`, `from_postgreSQL()`, ...
    instead and refer to the docstrings there!

    Attributes
    ----------
    train : `Transactions`
        Instance of `bestPy.datastructures.Transactions` holding
        the training data. Revealed after calling the `split` method.

    test : object
        Object with test data as dictionary in its `data` attribute, revealed
        only after calling the `split()` method.

    number_of_transactions : int
        Number of transactions in the dataset before splitting.

    number_of_corrupted_records : int
        Number of corrupted records skipped when reading data.

    max_hold_out : int
        Maximum number of unique articles that can be held out for testing.

    Methods
    -------
    split(hold_out, only_new)
        Splits transaction data. The last `hold_out` unique articles each
        customer bought (up to a maximum of `max_hold_out`) are held out as
        test set. The training set depends on whether `only_new` articles
        should be recommened or also previously purchased ones. Once called,
        the data attributes `train` and `test` are revealed.

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

    """

    def __init__(self, n_trans, n_corr, unique, transactions):
        super().__setattr__('_TrainTest__is_split', False)
        super().__init__(n_trans, n_corr, unique, transactions)
        self.__unique = self._TrainTestBase__unique
        self.__transactions = self._TrainTestBase__transactions

    def __setattr__(self, name, value):
        """Makes attributes 'test' and 'train' read-only once we are split."""
        read_only_attributes = ('test', 'train')
        if self.__is_split and (name in read_only_attributes):
            raise AttributeError("can't set attribute")
        super().__setattr__(name, value)

    def split(self, hold_out=5, only_new=True):
        """Split transaction data into training and test set for benchmarking.

        Parameters
        ----------
        hold_out : int, optional
            How many unique articles to retain from each customer's purchase
            history for testing later. Default is 5 and maximum value is
            attribute `max_hold_out`.

        only_new : bool
            Whether only articles that a given customer has not yet bought
            will be recommended.

        Examples
        --------
        >>> data.split(4, True)

        >>> data.split(6, False)

        """
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
        self.__is_split = False
        self.test = TestDataFrom(test, hold_out, only_new)
        self.test.__doc__ = TrainTest.__test_docstring
        self.train = Transactions.from_csv(FileFrom(train))
        self.train.__doc__ = TrainTest.__train_docstring
        self.__is_split = True

    @staticmethod
    def __last(unique):
        """Sort dict by value time and return list of (item, time) tuples."""
        return sorted(unique.items(), key=itemgetter(1), reverse=True)

    @staticmethod
    def __items_from(last_transactions):
        """Get set of items from list of (item, timestamp) tuples."""
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

    __test_docstring = """Test data to benchmark algorithms and baselines.

                       Attributes
                       ----------
                       data : dict
                           Test data as dictionary with customer IDs as keys
                           and set of `hold-out` article IDs as values.

                       hold_out : int
                           Number of articles in test set for each customer.

                       only_new : bool
                           Whether `only_new` articles are recommended.

                       number_of_cases : int
                           Number of users in the test data set.

                       """
    __train_docstring = """Training data of type `Transactions`.

                        See also
                        --------
                        Documentation of `bestPy.datastructures.Transactions`

                        """
