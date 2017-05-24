#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import logging
from psycopg2 import connect, OperationalError, ProgrammingError
from ....datastructures import PostgreSQLparams
from ....datastructures.split import from_postgreSQL

def database():
    database = PostgreSQLparams()
    database.login_db_name = 'pythontest'
    database.login_host = 'localhost'
    database.login_user = 'test'
    database.login_password = 'test123'
    database.table = 'head100'
    database.timestamp = 'timestamp'
    database.itemID = 'articleid'
    database.userID = 'userid'
    database.limit = 'all'
    return database

def no_connection_to(database):
    try:
        connection = connect(database.login)
    except OperationalError:
        return True
    return False


class TestSplitFromPostgreSQL(ut.TestCase):

    def test_error_on_wrong_databse_object_type(self):
        log_msg = ['ERROR:root:Attempt to set database parameter object of'
                   ' incompatible type. Must be <PostgreSQLparams>.']
        err_msg = ('Database parameter object must be of'
                   ' type <PostgreSQLparams>!')
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = from_postgreSQL('foo')
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_cannot_connect_to_database_with_wrong_db_name(self):
        db = database()
        db.login_db_name = 'wrong'
        log_msg = ["ERROR:root:Failed connecting to dbname='wrong'"
                   " @host='localhost'."]
        err_msg = 'Connect to database failed. Check settings!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(OperationalError, msg=err_msg) as err:
                _ = from_postgreSQL(db)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_cannot_connect_to_database_with_wrong_host(self):
        db = database()
        db.login_host = 'wrong'
        log_msg = ["ERROR:root:Failed connecting to dbname='pythontest'"
                   " @host='wrong'."]
        err_msg = 'Connect to database failed. Check settings!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(OperationalError, msg=err_msg) as err:
                _ = from_postgreSQL(db)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_cannot_connect_to_database_with_wrong_user(self):
        db = database()
        db.login_user = 'wrong'
        log_msg = ["ERROR:root:Failed connecting to dbname='pythontest'"
                   " @host='localhost'."]
        err_msg = 'Connect to database failed. Check settings!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(OperationalError, msg=err_msg) as err:
                _ = from_postgreSQL(db)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_cannot_connect_to_database_with_wrong_pwd(self):
        db = database()
        db.login_password = 'wrong'
        log_msg = ["ERROR:root:Failed connecting to dbname='pythontest'"
                   " @host='localhost'."]
        err_msg = 'Connect to database failed. Check settings!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(OperationalError, msg=err_msg) as err:
                _ = from_postgreSQL(db)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_error_on_wrong_table_name(self):
        db = database()
        db.table = 'wrong'
        log_msg = ['ERROR:root:Failed to execute SQL query.'
                   ' Check your parameters!']
        err_msg = 'SQL query failed. Check your parameters!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ProgrammingError, msg=err_msg) as err:
                _ = from_postgreSQL(db)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_error_on_wrong_timestamp_column_name(self):
        db = database()
        db.timestamp = 'wrong'
        log_msg = ['ERROR:root:Failed to execute SQL query.'
                   ' Check your parameters!']
        err_msg = 'SQL query failed. Check your parameters!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ProgrammingError, msg=err_msg) as err:
                _ = from_postgreSQL(db)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_error_on_wrong_item_column_name(self):
        db = database()
        db.itemID = 'wrong'
        log_msg = ['ERROR:root:Failed to execute SQL query.'
                   ' Check your parameters!']
        err_msg = 'SQL query failed. Check your parameters!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ProgrammingError, msg=err_msg) as err:
                _ = from_postgreSQL(db)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_error_on_wrong_user_column_name(self):
        db = database()
        db.userID = 'wrong'
        log_msg = ['ERROR:root:Failed to execute SQL query.'
                   ' Check your parameters!']
        err_msg = 'SQL query failed. Check your parameters!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(ProgrammingError, msg=err_msg) as err:
                _ = from_postgreSQL(db)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_warning_on_incomplete_records(self):
        log_msg = ['WARNING:root:Incomplete record returned from database.'
                   ' Skipping.',
                   'WARNING:root:Incomplete record returned from database.'
                   ' Skipping.',
                   'WARNING:root:Incomplete record returned from database.'
                   ' Skipping.',
                   'WARNING:root:Incomplete record returned from database.'
                   ' Skipping.',
                   'WARNING:root:Incomplete record returned from database.'
                   ' Skipping.',
                   'WARNING:root:Incomplete record returned from database.'
                   ' Skipping.']
        with self.assertLogs(level=logging.WARNING) as log:
            _ = from_postgreSQL(database())
        self.assertEqual(log.output, log_msg)


if __name__ == '__main__':
    ut.main()
