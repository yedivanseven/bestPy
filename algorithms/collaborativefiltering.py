# -*- coding: utf-8 -*-

import logging as log
from .similarities import default_similarity, all_similarities
from .baselines import default_baseline
from ..datastructures import Transactions


class CollaborativeFiltering:
    '''Collaborative filtering based on article-article similarity.

    Attributes
    ----------
    binarize : bool, optional
        Whether a customer's purchase history should be reduced to whether or
        not an article as bought (``True``), or whether the number of times
        articles were bought should count (``False``). Defaults to ``True``.

    similarity : function, optional
        Takes data object of type `bestPy.datastructures.Transactions` as
        argument and returns similarity matrix in scipy compressed sparse
        column (CSC) format. Defaults to `kulsinski`.

    baseline : object, object
        Fall-back algorithm needed for customers that only bought articles
        no one else bought. Defaults to `bestPy.algorithms.Baseline`.

    Methods
    -------
    operating_on(data) : `CollaborativeFiltering`
        Returns the `CollaborativeFiltering` instance it is called on with
        the `data` object attached. It then `has_data` and reveals method ...

    for_one(target) : array
        Returns an array with ratings of all articles for the customer with
        the internal integer index `target`. The higher the rating,
        the more highly recommended the article is for customer `target`.

    Examples
    --------
    >>> ratings = CollaborativeFiltering().operating_on(data)
    >>> ratings.has_data
    True

    >>> ratings.similarity
    'kulsinksi'

    >>> ratings.baseline
    'Baseline'

    >>> customer = 245
    >>> ratings.binarize = True
    >>> ratings.for_one(customer)
    array([ 0.16129032,  0.09677419, ...., 0.06451613])

    '''

    def __init__(self):
        self.__binarize = True
        self.__similarity = default_similarity
        self.__baseline = default_baseline()
        self.__class_prefix = '_' + self.__class__.__name__ + '__'

    @property
    def binarize(self):
        '''Count number of: times bought (``True``) or buyers (``False``).'''
        return self.__binarize

    @binarize.setter
    def binarize(self, binarize):
        self.__binarize = self.__boolean_type_checked(binarize)

    @property
    def similarity(self):
        '''Measure used to compute the similarity between articles.'''
        return self.__similarity.__name__

    @similarity.setter
    def similarity(self, similarity):
        similarity = self.__permitted(similarity)
        if similarity != self.__similarity:
            self.__delete_sim_mat()
        self.__similarity = similarity

    @property
    def baseline(self):
        '''Baseline algorithm used for uncomparable customers.'''
        return self.__baseline.__class__.__name__

    @baseline.setter
    def baseline(self, baseline):
        self.__baseline = self.__base_attribute_checked(baseline)
        if self.has_data:
            self.__baseline = self.__baseline.operating_on(self.__data)
            self.__baseline = self.__data_attribute_checked(self.__baseline)

    def operating_on(self, data):
        '''Set data object for the algorithm to operate on.

        Parameters
        ----------
        data : `Transactions`
            Instance of `bestPy.datastructures.Transactions`.

        Returns
        -------
        The instance of `CollaborativeFiltering` it is called on, now with the
        previously hidden `for_one()` method enabled.

        Examples
        --------
        >>> algorithm = CollaborativeFiltering().operating_on(data)
        >>> algorithm.has_data
        True

        '''
        self.__data = self.__transactions_type_checked(data)
        self.__baseline = self.__baseline.operating_on(data)
        self.__baseline = self.__data_attribute_checked(self.__baseline)
        self.__delete_sim_mat()
        self.__depending_on_whether_we = {True: self.__data.matrix.bool_by_row,
                                          False: self.__data.matrix.by_row}
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
        >>> ratings = CollaborativeFiltering().operating_on(data)
        >>> customer = 245
        >>> ratings.for_one(customer)
        array([ 0.16129032,  0.09677419, ...., 0.06451613])

        '''
        if self.__no_one_else_bought_items_bought_by(target):
            log.info('Uncomparable user with ID {}. Returning baseline'
                     ' recommendation.'.format(self.__data.user.id_of[target]))
            return self.__baseline.for_one()
        history_vector = self.__depending_on_whether_we[self.binarize][target]
        return history_vector.dot(self.__similarity_matrix()).A[0]

    def __similarity_matrix(self):
        if not self.__has('sim_mat'):
            self.__sim_mat = self.__similarity(self.__data)
        return self.__sim_mat

    def __delete_sim_mat(self):
        if self.__has('sim_mat'):
            delattr(self, self.__class_prefix + 'sim_mat')

    def __no_one_else_bought_items_bought_by(self, target):
        items_bought_by_target = self.__data.matrix.by_row[target].indices
        return self.__data._users_who_bought(items_bought_by_target).size == 1

    def __has(self, attribute):
        return hasattr(self, self.__class_prefix + attribute)

    @staticmethod
    def __permitted(similarity):
        if similarity not in all_similarities:
            log.error('Attempt to set unrecognized similarity.')
            raise TypeError('Unrecognized similarity! See "all_similarities"'
                            ' from the similarities module for your choices.')
        return similarity

    @staticmethod
    def __boolean_type_checked(binarize):
        if not isinstance(binarize, bool):
            log.error('Attempt to set "binarize" to non-boolean type.')
            raise TypeError('Attribute "binarize" must be True or False!')
        return binarize

    @staticmethod
    def __transactions_type_checked(data):
        if not isinstance(data, Transactions):
            log.error('Attempt to set incompatible data type.'
                      ' Must be <Transactions>.')
            raise TypeError('Data must be of type <Transactions>!')
        return data

    @staticmethod
    def __base_attribute_checked(baseline):
        '''Check methods and attributes of baseline before data is attached.'''
        if not hasattr(baseline, 'operating_on'):
            log.error('Attempt to set baseline object lacking mandatory'
                      ' "operating_on()" method.')
            raise AttributeError('Baseline lacks "operating_on()" method!')
        if not callable(baseline.operating_on):
            log.error('The "operating_on()" method of the baseline object'
                      ' is not callable.')
            raise TypeError('Operating_on() method of baseline not callable!')
        if not hasattr(baseline, 'has_data'):
            log.error('Attempt to set baseline object lacking mandatory'
                      ' "has_data" attribute.')
            raise AttributeError('Baseline lacks "has_data" attribute!')
        return baseline

    @staticmethod
    def __data_attribute_checked(baseline):
        '''Check methods and attirbutes of baseline after data is attached.'''
        if not baseline.has_data:
            log.error("Baseline object's 'has_data' attribute returned False"
                      " after attaching data.")
            raise ValueError('Cannot attach data to baseline object!')
        if not hasattr(baseline, 'for_one'):
            log.error('Attempt to set baseline object lacking mandatory'
                      ' "for_one()" method.')
            raise AttributeError('Baseline lacks "for_one()" method!')
        if not callable(baseline.for_one):
            log.error('The "for_one()" method of the baseline object'
                      ' is not callable.')
            raise TypeError('"for_one()" method of baseline not callable!')
        return baseline
