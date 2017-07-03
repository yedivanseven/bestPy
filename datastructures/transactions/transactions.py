# -*- coding: utf-8 -*-

import logging as log
from numpy import unique
from . import read
from ..auxiliary import IndexFrom, MatrixFrom


class Transactions:
    """Read and hold transaction data from a number of sources.

    Direct instantiation of this class is discouraged and, therefore,
    not documented. Use the classmethods `from_csv`, `from_postgreSQL`, ...
    instead and refer to the docstrings there!

    Attributes
    ----------
    number_of_transactions : int
        Number of transactions in the dataset.

    number_of_corrupted_records : int
        Number of corrupted records skipped when reading data.

    number_of_userItem_pairs : int
        Number of times any article has been bought by a unique user.

    user : object
        Provides dictionary attributes to translate between
        the unqiue customer ID in the data and the internally
        used (integer) customer index.

    item : object
        Provides dictionary attributes to translate between
        the unique article ID in the data and the internally
        used (integer) article index.

    matrix : object
        Holds transaction data as customer-article matrix with the
        former as rows, the latter as columns, and the number of
        times a customer has bought an article as entries.

    Examples
    --------
    >>> data = Transactions.from_csv(file)
    >>> data.number_of_transactions
    205830

    >>> data = Transactions.from_postgreSQL(database)
    >>> data.user.index_of['first customer']
    0

    >>> data.item.id_of[1]
    'second article'

    """

    def __init__(self, n_trans, n_corr, user_i, item_j, counts):
        self.__number_of_transactions = self.__int_type_value_checked(n_trans)
        self.__number_of_corrupted_records = self.__type_range_checked(n_corr)
        self.__user = IndexFrom(user_i)
        self.__item = IndexFrom(item_j)
        self.__matrix = MatrixFrom(counts)
        self.__number_of_userItem_pairs = len(counts)
        self.__check_data_for_consistency()

    @classmethod
    def from_csv(cls, file, separator=';'):
        """Read transaction data from a CSV file.

        Parameters
        ----------
        file : str
            Path to and name of CSV file holding transaction data
            in three columns: timestamp, customer ID, article ID.

        separator : str, optional
            Delimiter character between entries on each line in the file.
            Defaults to ';'.

        Returns
        -------
        Instance of `Transactions` holding the data.

        Examples
        --------
        >>> file = '/path/to/my/file.csv'
        >>> data = Transactions.from_csv(file, '|')

        """
        return cls(*read.from_csv(file, separator=separator))

    @classmethod
    def from_postgreSQL(cls, database):
        """Read transaction data from a PostgreSQL database.

        Parameters
        ----------
        database : `PostgreSQLparams`
            Configured instance of `bestPy.datastructures.PostgreSQLparams`.

        Returns
        -------
        Instance of `Transactions` holding the data.

        Examples
        --------
        >>> data = Transactions.from_postgreSQL(database)

        """
        return cls(*read.from_postgreSQL(database))

    @property
    def number_of_transactions(self):
        return self.__number_of_transactions

    @property
    def number_of_corrupted_records(self):
        return self.__number_of_corrupted_records

    @property
    def number_of_userItem_pairs(self):
        return self.__number_of_userItem_pairs

    @property
    def user(self):
        """Convert between unique customer ID and internal integer index."""
        return self.__user

    @property
    def item(self):
        """Convert between unique article ID and internal integer index."""
        return self.__item

    @property
    def matrix(self):
        """Customer-article matrix in various `scipy.sparse` formats."""
        return self.__matrix

    def _users_who_bought(self, items):
        """Array of customer indices who bought array of article indices"""
        return unique(self.matrix.by_col[:, items].indices)

    @staticmethod
    def __int_type_value_checked(n_trans):
        log_msg = ('Attempt to instantiate data object with number of'
                   ' valid transactions not a positive integer.')
        err_msg = 'Number of valid transactions not a positive integer!'
        if not isinstance(n_trans, int):
            log.error(log_msg)
            raise TypeError(err_msg)
        if n_trans < 1:
            log.error(log_msg)
            raise ValueError(err_msg)
        return n_trans

    @staticmethod
    def __type_range_checked(n_corr):
        log_msg = ('Attempt to instantiate data object with number of'
                   ' corrupted records not an integer >= 0.')
        err_msg = 'Number of corrupted records not an integer >= 0!'
        if not isinstance(n_corr, int):
            log.error(log_msg)
            raise TypeError(err_msg)
        if n_corr < 0:
            log.error(log_msg)
            raise ValueError(err_msg)
        return n_corr

    def __check_data_for_consistency(self):
        if (self.user.count, self.item.count) != self.matrix.by_col.shape:
            log.error('Attempt to instantiate data object with number of'
                      ' customers/articles incompatible with matrix shape.')
            raise ValueError('Number of users/items incompatible with'
                             ' matrix shape!')
        if self.number_of_transactions != self.matrix.by_col.sum().sum():
            log.error('Attempt to instantiate data object with number of'
                      ' transactions incompatible with matrix values.')
            raise ValueError('Number of transactions incompatible with values'
                             ' in matrix!')
        if self.number_of_userItem_pairs != self.matrix.by_col.getnnz():
            log.error('Attempt to instantiate data object with number of'
                      ' user/item pairs incompatible with matrix values.')
            raise ValueError('Number of user/item pairs incompatible with'
                             'values in matrix!')
