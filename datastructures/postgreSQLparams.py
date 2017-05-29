# -*- coding: utf-8 -*-

import logging as log
from psycopg2.extensions import AsIs


class PostgreSQLparams:
    '''Holds parameters needed to retrieve transaction data from PostgreSQL.

    Attributes
    ----------
    login_db_name : str
        Name of the database.

    login_host : str
        Host that the database is running on.

    login_user : str
        Name of user with access to table in database.

    login_password : str
        Password of user.

    login : str, read only
        The current login string that will be used to log into the database.

    table : str
        Name of database table to retrieve transaction data from.

    timestamp : str
        Name of column with the timestamps of the transactions.

    userID : str
        Name of column with the customer IDs of the transactions.

    itemID : str
        Name of column with the article IDs of the transactions.

    limit : int > 0 or str 'all', optional
        How many records to retrieve from the database.
        Defaults to 100.

    '''

    def __init__(self):
        self.__login_db_name = '<dbname>'
        self.__login_host = '<host>'
        self.__login_user = '<user>'
        self.__login_password = '<password>'
        self.__table = AsIs('<table>')
        self.__timestamp = AsIs('<field with timestamp>')
        self.__userID = AsIs('<field with userID>')
        self.__itemID = AsIs('<field with itemID>')
        self.__limit = 100

    @property
    def login_db_name(self):
        return self.__login_db_name

    @login_db_name.setter
    def login_db_name(self, login_db_name):
        self.__login_db_name = self.__prepend(login_db_name, 'dbname')

    @property
    def login_host(self):
        return self.__login_host

    @login_host.setter
    def login_host(self, login_host):
        self.__login_host = self.__prepend(login_host, 'host')

    @property
    def login_user(self):
        return self.__login_user

    @login_user.setter
    def login_user(self, login_user):
        self.__login_user = self.__prepend(login_user, 'user')

    @property
    def login_password(self):
        return self.__login_password

    @login_password.setter
    def login_password(self, login_password):
        self.__login_password = self.__prepend(login_password, 'password')

    @property
    def login(self):
        '''Current state of the string used for database login (read-only).'''
        prefix = '__login'
        params = [getattr(self, attr) for attr in dir(self) if prefix in attr]
        return ' '.join(params)

    @property
    def table(self):
        return self.__table.adapted

    @table.setter
    def table(self, table):
        self.__table = AsIs(self.__convert(table, 'table'))

    @property
    def timestamp(self):
        return self.__timestamp.adapted

    @timestamp.setter
    def timestamp(self, timestamp):
        self.__timestamp = AsIs(self.__convert(timestamp, 'timestamp'))

    @property
    def userID(self):
        return self.__userID.adapted

    @userID.setter
    def userID(self, userID):
        self.__userID = AsIs(self.__convert(userID, 'userID'))

    @property
    def itemID(self):
        return self.__itemID.adapted

    @itemID.setter
    def itemID(self, itemID):
        self.__itemID = AsIs(self.__convert(itemID, 'itemID'))

    @property
    def limit(self):
        if isinstance(self.__limit, int):
            return self.__limit
        return self.__limit.adapted

    @limit.setter
    def limit(self, limit):
        no = lambda x: False
        permitted = {int: lambda i: True if i > 0 else False,
                     str: lambda s: True if s.upper() == 'ALL' else False}
        set_according_to = {int: lambda i: i,
                            str: lambda s: AsIs(s)}
        type_of = type(limit)

        if permitted.get(type_of, no)(limit):
            self.__limit = set_according_to[type_of](limit)
        else:
            log.error('Limit must be the string "all" or a positive integer!')
            raise ValueError('Limit must be "all" or a positive integer!')

    @property
    def _params(self):
        params = {'timestamp': self.__timestamp,
                     'userid': self.__userID,
                  'articleid': self.__itemID,
                      'table': self.__table,
                      'limit': self.__limit}
        return params

    @staticmethod
    def __prepend(parameter, prefix):
        if not isinstance(parameter, str):
            log.warning(prefix + ' should be a string. Trying nevertheless!')
        return prefix + "='" + str(parameter) + "'"

    @staticmethod
    def __convert(parameter, prefix):
        if not isinstance(parameter, str):
            log.warning(prefix + ' should be a string. Trying nevertheless!')
        return str(parameter)

    @property
    def _requested(self):
        return self.limit if isinstance(self.limit, int) else float('-inf')
