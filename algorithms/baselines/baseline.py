# -*- coding: utf-8 -*-

import logging as log
from ...datastructures import Transactions


class Baseline:
    '''Baseline recommendation based only on article popularity.

    Attributes
    ----------
    binarize : bool, optional
        Whether article popularity is evaluated as number of unique buyers
        (``True``) or number of times bought (``False``). Defaults to ``True``.

    Methods
    -------
    operating_on(data) : `Baseline`
        Returns the `Baseline` instance it is called on with the `data`
        object attached to it. It then `has_data` and reveals the method ...

    for_one() : array
        Returns an array with ratings of all articles. The higher the rating,
        the more highly recommended the article with that rating's index is.

    Examples
    --------
    >>> baseline = Baseline().operating_on(data)
    >>> baseline.has_data
    True

    >>> baseline.binarize = False
    >>> baseline.for_one()
    array([ 1.,  5.,  7.,  1.,  1.])

    '''

    def __init__(self):
        self.__binarize = True
        self.__depending_on_whether_we = {True : self.__count_unique_buyers,
                                          False: self.__sum_over_all_buys}
        self.__class_prefix = '_' + self.__class__.__name__ + '__'

    @property
    def binarize(self):
        '''Count number of: times bought (``True``) or buyers (``False``).'''
        return self.__binarize

    @binarize.setter
    def binarize(self, binarize):
        self.__check_boolean_type_of(binarize)
        if binarize != self.binarize:
            self.__delete_precomputed()
        self.__binarize = binarize

    def operating_on(self, data):
        '''Set data object for the baseline algorithm to operate on.

        Parameters
        ----------
        data : `Transactions`
            Instance of `bestPy.datastructures.Transactions`.

        Returns
        -------
        The instance of `Baseline` it is called on with a `for_one()` method.

        Examples
        --------
        >>> baseline = Baseline().operating_on(data)
        >>> baseline.has_data
        True

        '''
        self.__data = self.__transactions_type_checked(data)
        self.__delete_precomputed()
        self.for_one = self.__for_one
        return self

    @property
    def has_data(self):
        return self.__has('data')

    def __for_one(self, target=None):
        '''Returns array with the popularity of all articles.

        Examples
        --------
        >>> baseline = Baseline().operating_on(data)
        >>> baseline.for_one()
        array([ 1.,  5.,  7.,  1.,  1.])

        '''
        return self.__depending_on_whether_we[self.binarize]()

    def __count_unique_buyers(self):
        if not self.__has('number_of_buyers'):
            self.__number_of_buyers = self.__data.matrix.bool_by_col.sum(0).A1
        return self.__number_of_buyers.copy()

    def __sum_over_all_buys(self):
        if not self.__has('number_of_buys'):
            self.__number_of_buys = self.__data.matrix.by_col.sum(0).A1
        return self.__number_of_buys.copy()

    def __delete_precomputed(self):
        if self.__has('number_of_buyers'):
            delattr(self, self.__class_prefix + 'number_of_buyers')
        if self.__has('number_of_buys'):
            delattr(self, self.__class_prefix + 'number_of_buys')

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
