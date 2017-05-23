#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import logging
from psycopg2 import connect, OperationalError, ProgrammingError
from ....datastructures import PostgreSQLparams
from ....datastructures.read import from_postgreSQL

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


class TestFromPostgreSQL(ut.TestCase):

    def test_cannot_connect_to_database(self):
        db = database()
        db.login_host = 'non_existent'
        log_msg = ["ERROR:root:Failed connecting to dbname='pythontest'"
                   " @host='non_existent'."]
        err_msg = 'Connect to database failed. Check settings!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(OperationalError, msg=err_msg) as err:
                _ = from_postgreSQL(db)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to database.')
    def test(self):
        pass


if __name__ == '__main__':
    ut.main()
