# -*- coding: utf-8 -*-

import logging as log
from numpy import argpartition
from .algorithms import default_algorithm
from .algorithms import default_baseline
from .datastructures import Transactions

RETURNING = True


class RecoBasedOn:
    """Merges data and algorithm into an engine to make actual recommendations.

    Parameters
    ----------
    data : object
        A data instance of type `bestPy.datastructures.Transactions`.

    Attributes
    ----------
    algorithm : str, optional
        The name of the algorithm used to make recommendations.
        Defaults to `bestPy.algorithms.CollaborativeFiltering`.

    pruning_old : `RecoBasedOn`
        The instance of `RecoBasedOn` it is called on, now set to recommend
        only articles that a given customer has not bought before.

    keeping_old : `RecoBasedOn`
        The instance of `RecoBasedOn` it is called on, now set to recommend
        also articles that a given customer has bought before.

    only_new : bool
        Whether the recommendations include articles that
        a given customer has bought before or not.

    baseline : object, optional
        Algorithm object to provide a cold-start recommendation for
        unknown customers. Defaults to `bestPy.algorithms.Baseline`.

    Methods
    -------
    using(algorithm) : `RecoBasedOn`
        Called with a recommendation-algorithm object as argument, it
        returns the instance of `RecoBasedOn` it is called on, with
        the recommendation algorithm set accordingly.

    for_one(target, max_number_of_items) : generator
        Returns a generator of up to `max_number_of_items article` IDs,
        which are the recommendations for the customer with ID `target`.

    Examples
    --------
    >>> reco = RecoBasedOn(data).using(algorithm).pruning_old
    >>> top_two = reco.for_one(customer, 2)
    >>> for article in top_two:
    >>>     print(article)
    'bestPyHoodieMedium'
    'bestPyBaseCap'

    """

    def __init__(self, data):
        self.__data = self.__transactions_type_checked(data)
        self.__only_new = True
        self.__baseline = default_baseline().operating_on(data)
        self.__recommendation = default_algorithm().operating_on(data)
        self.__recommendation_for = {not RETURNING: self.__cold_start,
                                         RETURNING: self.__calculated}

    def using(self, algorithm):
        """Sets the algorithm object to compute recommendations.

        Parameters
        ----------
        algorithm : object, optional
            An algorithm object to provide actual recommendations.
            Defaults to `bestPy.algorithms.CollaborativeFiltering`.

        Returns
        -------
        The `RecoBasedOn` instance it is called on with the
        recommendation algorithm set accordingly.

        Examples
        --------
        >>> recommendation = RecoBasedOn(data).pruning_old
        >>> recommendation = recommendation.using(algorithm)

        """
        self.__check_base_attributes_of(algorithm)
        self.__recommendation = algorithm.operating_on(self.__data)
        self.__check_data_attributes_of(algorithm)
        return self

    @property
    def algorithm(self):
        return self.__recommendation.__class__.__name__

    @property
    def pruning_old(self):
        self.__only_new = True
        return self

    @property
    def keeping_old(self):
        self.__only_new = False
        return self

    @property
    def only_new(self):
        return self.__only_new

    @property
    def baseline(self):
        return self.__baseline.__class__.__name__

    @baseline.setter
    def baseline(self, baseline):
        self.__check_base_attributes_of(baseline)
        self.__baseline = baseline.operating_on(self.__data)
        self.__check_data_attributes_of(baseline)

    def for_one(self, target, max_number_of_items=5):
        """Provides the actual recommendations.

        Parameters
        ----------
        target : object
            ID of the customer to provide a recommendation for.

        max_number_of_items : int, optional
            The number of recommendations to provide. If fewer
            than that are available, only the available number
            will be returned. Defaults to 5.

        Returns
        -------
        recommendations : generator
            A generator for up to `max_number_of_items` article IDs
            that are the recommendations for the specified customer.

        Examples
        --------
        >>> reco = RecoBasedOn(data).using(algorithm).keeping_old
        >>> top_two = reco.for_one(customer, 2)
        >>> for article in top_two:
        >>>     print(article)
        'bestPyHoodieMedium'
        'bestPyBaseCap'

        """
        head = self.__integer_type_and_range_checked(max_number_of_items)
        type_of = target in self.__data.user.index_of.keys()
        item_scores = self.__recommendation_for[type_of](target)
        sorted_item_indices = argpartition(item_scores, -head)[-head:]
        return (self.__data.item.id_of[index] for index in sorted_item_indices)

    def __cold_start(self, target=None):
        log.info('Unknown target user. Defaulting to baseline recommendation.')
        try:
            cold_start_recommendation = self.__baseline.for_one()
        except TypeError:
            log.error('Failed to call the "for_one()" method of the'
                      ' baseline algorithm without argument "target".')
            raise TypeError('Choose a baseline algorithm whose "for_one()"'
                            ' method is callable without argument "target"!')
        return cold_start_recommendation

    def __calculated(self, target):
        target_index = self.__data.user.index_of[target]
        item_scores = self.__recommendation.for_one(target_index)
        if self.__only_new:
            already_bought = self.__data.matrix.by_row[target_index].indices
            item_scores[already_bought] = float('-inf')
        return item_scores

    @staticmethod
    def __transactions_type_checked(data):
        if not isinstance(data, Transactions):
            log.error('Attempt to instantiate with incompatible data type.'
                      ' Must be <Transactions>.')
            raise TypeError('Data must be of type <Transactions>!')
        return data

    @staticmethod
    def __check_base_attributes_of(algorithm):
        """Check methods of algorithm and baseline before they get data."""
        if not hasattr(algorithm, 'operating_on'):
            log.error('Attempt to set object lacking mandatory'
                      ' "operating_on()" method.')
            raise AttributeError('Object lacks "operating_on()" method!')
        if not callable(algorithm.operating_on):
            log.error('The "operating_on()" method of this object'
                      ' is not callable.')
            raise TypeError('"operating_on()" method of object not callable!')
        if not hasattr(algorithm, 'has_data'):
            log.error('Attempt to set object lacking mandatory'
                      ' "has_data" attribute.')
            raise AttributeError('Object lacks "has_data" attribute!')

    @staticmethod
    def __check_data_attributes_of(algorithm):
        """Check methods of algorithm and baseline after they got data."""
        if not algorithm.has_data:
            log.error("Object's 'has_data' attribute returned False"
                      " after attaching data.")
            raise ValueError('Cannot attach data to object!')
        if not hasattr(algorithm, 'for_one'):
            log.error('Attempt to set object lacking mandatory'
                      ' "for_one()" method.')
            raise AttributeError('Object lacks "for_one()" method!')
        if not callable(algorithm.for_one):
            log.error('Attempt to set object with a "for_one()" method'
                      ' that is not callable.')
            raise TypeError('"for_one()" method of object not callable!')

    def __integer_type_and_range_checked(self, requested):
        if not isinstance(requested, int):
            log.error('Requested number of recommendations is not an integer.')
            raise TypeError('Requested number of recommendations must be'
                            ' a positive integer!')
        if requested < 1:
            log.error('Requested number of recommendations < 1.')
            raise ValueError('Requested number of recommendations must be'
                             ' a positive integer!')
        available = self.__data.item.count
        if requested > available:
            log.warning('Requested {0} recommendations but only {1} available.'
                        ' Returning all {1}.'.format(requested, available))
            requested = available
        return requested
