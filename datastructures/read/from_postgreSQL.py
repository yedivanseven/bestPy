#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from collections import defaultdict
import psycopg2 as pg

class PostgreSQLparams():
    def __init__(self):
        self.__name = '<database>'
        self.__host = '<host>'
        self.__user = '<user>'
        self.__password = '<password>'
        self.table = '<table>'
        self.userID_field = '<field with userID>'
        self.articleID_field = '<field with articleID>'

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, db_name):
        self.__database = "dbname='" + str(db_name) + "'"

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, host_name):
        self.__host = "host='" + str(host_name) + "'"

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, user_name):
        self.__user = "user='" + str(user_name) + "'"

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = "password='" + str(password) + "'"

    @property
    def login(self):
        prefix = '_' + self.__class__.__name__
        params = [getattr(self, a) for a in dir(self) if a.startswith(prefix)]
        return ' '.join(params)

def from_postgreSQL(database):

    with pg.connect(database.login) as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM {}'.format(database.table))
            for row in cursor.fetchall():
                print(row)


    return (number_of_transactions,
            number_of_corrupted_entries,
            dict(userIndex_of),
            dict(itemIndex_of),
            dict(count_buys_of))
