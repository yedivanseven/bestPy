# -*- coding: utf-8 -*-

import logging as log
from numpy import diag
from scipy.sparse.linalg import svds
from ..datastructures import Transactions


class TruncatedSVD:
    """Recommendation based on a truncated SVD of the customer-article matrix.

    Attributes
    ----------
    binarize : bool, optional
        Whether the entries in the customer-article matrix should be reduced
        to the number of unique buyers (``True``) or remain number of times
        bought (``False``). Defaults to ``True``.

    number_of_factors : integer, optional
        Number of latent variables thought to charaterize both the customers
        and the articles. Defaults to 20.

    max_number_of_factors : integer
        Maximum value that `number_of_factors` can be set to. Depends on the
        data and is, therefore, not availabel before calling ...

    Methods
    -------
    operating_on(data) : `TruncatedSVD`
        Returns the `TruncatedSVD` instance it is called on with the `data`
        object attached to it. It then `has_data` and reveals the method ...

    for_one(target) : array
        Returns an array with ratings of all articles for the customer with
        the internal integer index `target`. The higher the rating,
        the more highly recommended the article is for the `target` customer.

    Examples
    --------
    >>> ratings = TruncatedSVD().operating_on(data)
    >>> ratings.has_data
    True

    >>> ratings.max_number_of_factors
    278

    >>> ratings.number_of_factors = 30
    >>> ratings.binarize = False
    >>> customer = 245
    >>> ratings.for_one(customer)
    array([ 0.16129032,  0.09677419, ...., 0.06451613])

    """

    def __init__(self):
        self.__binarize = True
        self.__number_of_factors = 20
        self.__class_prefix = '_' + self.__class__.__name__ + '__'

    @property
    def binarize(self):
        """Count number of: times bought (``True``) or buyers (``False``)."""
        return self.__binarize

    @binarize.setter
    def binarize(self, binarize):
        self.__check_boolean_type_of(binarize)
        if binarize != self.binarize:
            self.__delete_USV_matrices()
        self.__binarize = binarize

    @property
    def number_of_factors(self):
        """Number of latent variables characterizing cutomers and articles."""
        return self.__number_of_factors

    @number_of_factors.setter
    def number_of_factors(self, number_of_factors):
        self.__check_integer_type_and_range_of(number_of_factors)
        previous_number_of_factors = self.number_of_factors
        self.__set(number_of_factors)
        if self.number_of_factors != previous_number_of_factors:
            self.__delete_USV_matrices()

    def operating_on(self, data):
        """Set data object for the algorithm to operate on.

        Parameters
        ----------
        data : `Transactions`
            Instance of `bestPy.datastructures.Transactions`.

        Returns
        -------
        The instance of `TruncatedSVD` it is called on, now with the
        previously hidden `for_one()` method enabled an the data attached.

        Examples
        --------
        >>> algorithm = TruncatedSVD().operating_on(data)
        >>> algorithm.has_data
        True

        >>> algorithm.max_number_of_factors
        278

        """
        self.__data = self.__transactions_type_checked(data)
        new_property = property(lambda obj: obj.__data.matrix.min_shape - 1)
        doc = """Maximum number of latent variables supported by the data."""
        TruncatedSVD.max_number_of_factors = new_property
        TruncatedSVD.max_number_of_factors.__doc__ = doc
        self.__reset(self.number_of_factors)
        self.__delete_USV_matrices()
        self.for_one = self.__for_one
        return self

    @property
    def has_data(self):
        return self.__has('data')

    def __for_one(self, target):
        """Make an actual recommendation for the target customer.

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
        >>> ratings = TruncatedSVD().operating_on(data)
        >>> ratings.number_of_factors = 30
        >>> customer = 245
        >>> ratings.for_one(customer)
        array([ 0.16129032,  0.09677419, ...., 0.06451613])

        """
        if not self.__has('U'):
            self.__compute_USV_matrices()
        return self.__U[target].dot(self.__SV)

    def __compute_USV_matrices(self):
        self.__U, s, V = svds(self.__matrix(), k=self.number_of_factors)
        self.__SV = diag(s).dot(V)

    def __delete_USV_matrices(self):
        if self.__has('U'):
            delattr(self, self.__class_prefix + 'U')
        if self.__has('SV'):
            delattr(self, self.__class_prefix + 'SV')

    def __matrix(self):
        if self.__binarize:
            return self.__data.matrix.bool_by_row
        return self.__data.matrix.by_row

    def __set(self, number_of_factors):
        if not self.has_data:
            self.__number_of_factors = number_of_factors
        else:
            self.__reset(number_of_factors)

    def __reset(self, n_factors):
        if n_factors > self.max_number_of_factors:
            msg = ('Requested {0} latent features, but only {1} available.'
                   ' Resetting to {1}.')
            log.warning(msg.format(n_factors, self.max_number_of_factors))
            self.__number_of_factors = self.max_number_of_factors
        else:
            self.__number_of_factors = n_factors

    def __has(self, attribute):
        return hasattr(self, self.__class_prefix + attribute)

    @staticmethod
    def __check_integer_type_and_range_of(number_of_factors):
        error_message = '"number_of_factors" must be a positive integer!'
        if not isinstance(number_of_factors, int):
            log.error('Attempt to set number_of_factors to non-integer type.')
            raise TypeError(error_message)
        if number_of_factors < 1:
            log.error('Attempt to set number_of_factors to value < 1.')
            raise ValueError(error_message)

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
