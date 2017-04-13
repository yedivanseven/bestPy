#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from collections import defaultdict
import psycopg2 as pg
from psycopg2.extensions import AsIs
from psycopg2 import OperationalError, ProgrammingError


class PostgreSQLparams():
    def __init__(self):
        self.__login_db_name = '<dbname>'
        self.__login_host = '<host>'
        self.__login_user = '<user>'
        self.__login_password = '<password>'
        self.__table = AsIs('<table>')
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
        prefix = '_login'
        params = [getattr(self, a) for a in dir(self) if prefix in a]
        return ' '.join(params)

    @property
    def table(self):
        return self.__table

    @table.setter
    def table(self, table):
        self.__table = AsIs(str(table))

    @property
    def userID(self):
        return self.__userID

    @userID.setter
    def userID(self, userID):
        self.__userID = AsIs(str(userID))

    @property
    def itemID(self):
        return self.__itemID

    @itemID.setter
    def itemID(self, itemID):
        self.__itemID = AsIs(str(itemID))


    @property
    def limit(self):
        return self.__limit

    @limit.setter
    def limit(self, limit):
        if isinstance(limit, int):
            self.__limit = limit
        else:
            self.__limit = AsIs(str(limit))

    @property
    def params(self):
        params = {   'userid': self.userID,
                  'articleid': self.itemID,
                      'table': self.table,
                      'limit': self.limit}
        return params

    def __prepend(self, parameter, prefix=''):
        if isinstance(parameter, str):
            return prefix + "='" + parameter + "'"
        logging.warning(prefix + ' must be a string!')
        return '<' + prefix + '>'


def from_postgreSQL(database):
    number_of_transactions = 0
    number_of_corrupted_entries = 0
    userIndex_of = defaultdict(lambda: len(userIndex_of))
    itemIndex_of = defaultdict(lambda: len(itemIndex_of))
    count_buys_of = defaultdict(int)

    query = '''SELECT %(userid)s, %(articleid)s, COUNT(*) as count
               FROM %(table)s
               GROUP BY %(userid)s, %(articleid)s
               LIMIT %(limit)s'''

    try:
        connection = pg.connect(database.login)
    except OperationalError:
        logging.error('Failed connecting to {}'.format(database.login_db_name))
        raise OperationalError
    else:
        with connection.cursor() as cursor:
            try:
                cursor.execute(query, database.params)
            except ProgrammingError:
                logging.error('Failed to execute SQL query. Check user input!')
                raise ProgrammingError
            else:
                for entry in cursor:
                    user, item, count = entry
                    count_buys_of[(userIndex_of[user],
                                   itemIndex_of[item])] = count
                    number_of_transactions = cursor.rownumber
            finally:
                connection.close()

    return (number_of_transactions,
            number_of_corrupted_entries,
            dict(userIndex_of),
            dict(itemIndex_of),
            dict(count_buys_of))
