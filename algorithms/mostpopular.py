# -*- coding: utf-8 -*-

import logging as log
from ..datastructures import Transactions
from .baselines import Baseline


class MostPopular:
    '''Recommendation based on a customer's personal preference.

    If only new articles are to be recommended, this is equivalent to the
    baseline recommendation, i.e., based on general article popularity.

    Attributes
    ----------
    binarize : bool, optional
        Whether article popularity for the baseline is evaluated as number of
        unique buyers (``True``) or number of times bought (``False``).
        Defaults to ``True``.

    Methods
    -------
    operating_on(data) : `MostPopular`
        Returns the `MostPopular` instance it is called on with the `data`
        object attached to it. It then `has_data` and reveals the method ...

    for_one(target) : array
        Returns an array with ratings of all articles for the customer with
        the internal integer index `target`. The higher the rating,
        the more highly recommended the article is for customer `target`.

    Examples
    --------
    >>> ratings = MostPopular().operating_on(data)
    >>> ratings.has_data
    True

    >>> customer = 245
    >>> ratings.binarize = True
    >>> ratings.for_one(customer)
    array([ 0.16129032,  0.09677419,  ...,  0.06451613])


    '''

    def __init__(self):
        self.__baseline = Baseline()
        self.__class_prefix = '_' + self.__class__.__name__ + '__'

    @property
    def binarize(self):
        '''Count number of: times bought (``True``) or buyers (``False``).'''
        return self.__baseline.binarize

    @binarize.setter
    def binarize(self, binarize):
        self.__check_boolean_type_of(binarize)
        if binarize != self.binarize:
            self.__delete_precomputed()
        self.__baseline.binarize = binarize

    def operating_on(self, data):
        '''Set data object for the algorithm to operate on.

        Parameters
        ----------
        data : `Transactions`
            Instance of `bestPy.datastructures.Transactions`.

        Returns
        -------
        The instance of `MostPopular` it is called on.

        Examples
        --------
        >>> algorithm = MostPopular().operating_on(data)
        >>> algorithm.has_data
        True

        '''
        self.__data = self.__transactions_type_checked(data)
        self.__baseline = self.__baseline.operating_on(data)
        self.__delete_precomputed()
        self.for_one = self.__for_one
        return self

    @property
    def has_data(self):
        return self.__has('data')

    def __for_one(self, target):
        '''Make an actual recommendation for the target customer.

        Parameters
        ----------
        target : int
            Internally used integer index of the target customer.

        Returns
        -------
        array : float
            Suitability ratings of all items for the target customer.

        Examples
        --------
        >>> ratings = MostPopular().operating_on(data)
        >>> customer = 245
        >>> ratings.for_one(customer)
        array([ 0.16129032,  0.09677419,  ..., 0.06451613])

        '''
        target_agnostic = self.__precomputed()
        target_specific = self.__data.matrix.by_row[target]
        target_agnostic[target_specific.indices] = target_specific.data
        return target_agnostic

    def __precomputed(self):
        if not self.__has('scaled_baseline'):
            depending_on = {True : self.__data.number_of_userItem_pairs,
                            False: self.__data.number_of_transactions}
            self.__scaled_baseline = (self.__baseline.for_one() /
                                      depending_on[self.binarize])
        return self.__scaled_baseline.copy()

    def __delete_precomputed(self):
        if self.__has('scaled_baseline'):
            delattr(self, self.__class_prefix + 'scaled_baseline')

    def __has(self, attribute):
        return hasattr(self, self.__class_prefix + attribute)

    @staticmethod
    def __check_boolean_type_of(binarize):
        if not isinstance(binarize, bool):
            log.error('Attempt to set "binarize" to non-boolean type.')
            raise TypeError('Attribute "binarize" must be True or False!')

    @staticmethod
    def __transactions_type_checked(data):
        if not isinstance(data, Transactions):
            log.error('Attempt to set incompatible data type.'
                      ' Must be <Transactions>.')
            raise TypeError('Data must be of type <Transactions>!')
        return data
