#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import logging
from psycopg2.extensions import AsIs
from ...datastructures import PostgreSQLparams


class TestPostGreSqlParams(ut.TestCase):

    def setUp(self):
        self.database = PostgreSQLparams()

    def test_db_name_right(self):
        self.database.login_db_name = 'foo'
        self.assertEqual(self.database.login_db_name, "dbname='foo'")

    def test_db_name_wrong(self):
        with self.assertLogs(level=logging.WARNING):
            self.database.login_db_name = 12.3
        self.assertEqual(self.database.login_db_name, "dbname='12.3'")

    def test_db_name_warn(self):
        log_msg = ['WARNING:root:dbname should be a string.'
                   ' Trying nevertheless!']
        with self.assertLogs(level=logging.WARNING) as log:
            self.database.login_db_name = 12.3
        self.assertListEqual(log.output, log_msg)

    def test_host_right(self):
        self.database.login_host = 'bar'
        self.assertEqual(self.database.login_host, "host='bar'")

    def test_host_wrong(self):
        with self.assertLogs(level=logging.WARNING):
            self.database.login_host = 45.6
        self.assertEqual(self.database.login_host, "host='45.6'")

    def test_host_warn(self):
        log_msg = ['WARNING:root:host should be a string.'
                   ' Trying nevertheless!']
        with self.assertLogs(level=logging.WARNING) as log:
            self.database.login_host = 45.6
        self.assertListEqual(log.output, log_msg)

    def test_user_right(self):
        self.database.login_user = 'john'
        self.assertEqual(self.database.login_user, "user='john'")

    def test_user_wrong(self):
        with self.assertLogs(level=logging.WARNING):
            self.database.login_user = 78.9
        self.assertEqual(self.database.login_user, "user='78.9'")

    def test_user_warn(self):
        log_msg = ['WARNING:root:user should be a string.'
                   ' Trying nevertheless!']
        with self.assertLogs(level=logging.WARNING) as log:
            self.database.login_user = 78.9
        self.assertListEqual(log.output, log_msg)

    def test_password_right(self):
        self.database.login_password = 'doe'
        self.assertEqual(self.database.login_password, "password='doe'")

    def test_password_wrong(self):
        with self.assertLogs(level=logging.WARNING):
            self.database.login_password = 12.3
        self.assertEqual(self.database.login_password, "password='12.3'")

    def test_password_warn(self):
        log_msg = ['WARNING:root:password should be a string.'
                   ' Trying nevertheless!']
        with self.assertLogs(level=logging.WARNING) as log:
            self.database.login_password = 12.3
        self.assertListEqual(log.output, log_msg)

    def test_login_assembly(self):
        self.database.login_db_name = 'foo'
        self.database.login_host = 'bar'
        self.database.login_user = 'john'
        self.database.login_password = 'doe'
        should_be = "dbname='foo' host='bar' password='doe' user='john'"
        self.assertEqual(self.database.login, should_be)

    def test_cannot_set_login(self):
        with self.assertRaises(AttributeError):
            self.database.login = 45.6

    def test_table_right(self):
        self.database.table = 'foo'
        self.assertEqual(self.database.table, 'foo')

    def test_table_wrong(self):
        with self.assertLogs(level=logging.WARNING):
            self.database.table = 12.3
        self.assertEqual(self.database.table, '12.3')

    def test_table_warn(self):
        log_msg = ['WARNING:root:table should be a string.'
                   ' Trying nevertheless!']
        with self.assertLogs(level=logging.WARNING) as log:
            self.database.table = 12.3
        self.assertListEqual(log.output, log_msg)

    def test_table_params(self):
        with self.assertLogs(level=logging.WARNING):
            self.database.table = 12.3
        self.assertEqual(self.database._params['table'].adapted, '12.3')

    def test_timestamp_right(self):
        self.database.timestamp = 'bar'
        self.assertEqual(self.database.timestamp, 'bar')

    def test_timestamp_wrong(self):
        with self.assertLogs(level=logging.WARNING):
            self.database.timestamp = 45.6
        self.assertEqual(self.database.timestamp, '45.6')

    def test_timestamp_warn(self):
        log_msg = ['WARNING:root:timestamp should be a string.'
                   ' Trying nevertheless!']
        with self.assertLogs(level=logging.WARNING) as log:
            self.database.timestamp = 45.6
        self.assertListEqual(log.output, log_msg)

    def test_timestamp_params(self):
        with self.assertLogs(level=logging.WARNING):
            self.database.timestamp = 45.6
        self.assertEqual(self.database._params['timestamp'].adapted, '45.6')

    def test_userID_right(self):
        self.database.userID = 'john'
        self.assertEqual(self.database.userID, 'john')

    def test_userID_wrong(self):
        with self.assertLogs(level=logging.WARNING):
            self.database.userID = 78.9
        self.assertEqual(self.database.userID, '78.9')

    def test_userID_warn(self):
        log_msg = ['WARNING:root:userID should be a string.'
                   ' Trying nevertheless!']
        with self.assertLogs(level=logging.WARNING) as log:
            self.database.userID = 78.9
        self.assertListEqual(log.output, log_msg)

    def test_userID_params(self):
        with self.assertLogs(level=logging.WARNING):
            self.database.userID = 78.9
        self.assertEqual(self.database._params['userid'].adapted, '78.9')

    def test_itemID_right(self):
        self.database.itemID = 'doe'
        self.assertEqual(self.database.itemID, 'doe')

    def test_itemID_wrong(self):
        with self.assertLogs(level=logging.WARNING):
            self.database.itemID = 12.3
        self.assertEqual(self.database.itemID, '12.3')

    def test_itemID_warn(self):
        log_msg = ['WARNING:root:itemID should be a string.'
                   ' Trying nevertheless!']
        with self.assertLogs(level=logging.WARNING) as log:
            self.database.itemID = 12.3
        self.assertListEqual(log.output, log_msg)

    def test_itemID_params(self):
        with self.assertLogs(level=logging.WARNING):
            self.database.itemID = 12.3
        self.assertEqual(self.database._params['articleid'].adapted, '12.3')

    def test_limit_int(self):
        self.database.limit = 200
        self.assertEqual(self.database.limit, 200)

    def test_limit_int_params(self):
        self.database.limit = 200
        self.assertEqual(self.database._params['limit'], 200)

    def test_limit_all(self):
        self.database.limit = 'All'
        self.assertEqual(self.database.limit, 'All')

    def test_limit_all_params(self):
        self.database.limit = 'All'
        self.assertEqual(self.database._params['limit'].adapted, 'All')

    def test_limit_negative(self):
        log_msg = ['ERROR:root:Limit must be the string "all" or a'
                   ' positive integer!']
        err_msg = 'Limit must be "all" or a positive integer!'
        with self.assertLogs(level=logging.WARNING) as log:
            with self.assertRaises(ValueError, msg=err_msg) as err:
                self.database.limit = -100
        self.assertListEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_limit_float(self):
        log_msg = ['ERROR:root:Limit must be the string "all" or a'
                   ' positive integer!']
        err_msg = 'Limit must be "all" or a positive integer!'
        with self.assertLogs(level=logging.WARNING) as log:
            with self.assertRaises(ValueError, msg=err_msg) as err:
                self.database.limit = 12.3
        self.assertListEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_limit_not_all(self):
        log_msg = ['ERROR:root:Limit must be the string "all" or a'
                   ' positive integer!']
        err_msg = 'Limit must be "all" or a positive integer!'
        with self.assertLogs(level=logging.WARNING) as log:
            with self.assertRaises(ValueError, msg=err_msg) as err:
                self.database.limit = 'foo'
        self.assertListEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    def test_cannot_set_params(self):
        with self.assertRaises(AttributeError):
            self.database._params = 78.9

    def test_requested_int(self):
        self.database.limit = 123
        self.assertEqual(self.database._requested, 123)

    def test_requested_all(self):
        self.database.limit = 'all'
        self.assertEqual(self.database._requested, float('-inf'))

    def test_cannot_set_requested(self):
        with self.assertRaises(AttributeError):
            self.database._requested = 'foo'


if __name__ == '__main__':
    ut.main()
