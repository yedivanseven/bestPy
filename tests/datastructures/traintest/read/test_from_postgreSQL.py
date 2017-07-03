#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest as ut
import logging
from psycopg2 import connect, OperationalError, ProgrammingError
from .....datastructures import PostgreSQLparams
from .....datastructures.traintest.read import from_postgreSQL

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

    def test_error_on_wrong_database_object_type(self):
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

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_logging_and_reset_of_limit_when_too_large(self):
        db = database()
        db.limit = 123
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
                   ' Skipping.',
                   'WARNING:root:Requested 123 transactions from table head100'
                   ' but only 100 available. Fetched all 100.']
        with self.assertLogs(level=logging.WARNING) as log:
                _ = from_postgreSQL(db)
        self.assertEqual(log.output, log_msg)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_error_on_timestamp_field_neither_integer_nor_timestamp(self):
        db = database()
        db.table = 'time_type_test'
        log_msg = ['ERROR:root:Type of timestamp field is neither integer'
                   ' nor timestamp.']
        err_msg = 'Timestamp field must be an integer or a timestamp!'
        with self.assertLogs(level=logging.ERROR) as log:
            with self.assertRaises(TypeError, msg=err_msg) as err:
                _ = from_postgreSQL(db)
        self.assertEqual(log.output, log_msg)
        self.assertEqual(err.msg, err_msg)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_timestamp_field_is_read_and_converted_correctly(self):
        db = database()
        db.table = 'data25timestamp'
        should_be = ('2012-03-06T23:26:35', '2012-03-09T16:18:02',
                     '2012-03-09T16:18:02', '2012-03-09T16:18:52',
                     '2012-03-09T16:19:01', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14')
        with self.assertLogs(level=logging.WARNING):
            _, _, _, transactions = from_postgreSQL(db)
        actually_is = list(zip(*transactions))[0]
        self.assertTupleEqual(actually_is, should_be)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_unix_epoch_field_is_read_and_converted_correctly(self):
        db = database()
        db.table = 'head25'
        should_be = ('2012-03-06T23:26:35', '2012-03-06T23:53:45',
                     '2012-03-09T16:18:02', '2012-03-09T16:18:02',
                     '2012-03-09T16:18:33', '2012-03-09T16:18:52',
                     '2012-03-09T16:19:01', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14', '2012-03-09T16:20:14',
                     '2012-03-09T16:20:14')
        _, _, _, transactions = from_postgreSQL(db)
        actually_is = list(zip(*transactions))[0]
        self.assertTupleEqual(actually_is, should_be)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_int_type_of_number_of_transactions(self):
        db = database()
        db.table = 'data25timestamp'
        with self.assertLogs(level=logging.WARNING):
            n_rec, _, _, _ = from_postgreSQL(db)
        self.assertIsInstance(n_rec, int)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_correct_number_of_transactions(self):
        db = database()
        db.table = 'data25timestamp'
        with self.assertLogs(level=logging.WARNING):
            n_rec, _, _, _ = from_postgreSQL(db)
        self.assertEqual(n_rec, 21)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_int_type_of_number_of_corrupted_records(self):
        db = database()
        db.table = 'data25timestamp'
        with self.assertLogs(level=logging.WARNING):
            _, n_err, _, _ = from_postgreSQL(db)
        self.assertIsInstance(n_err, int)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_correct_number_of_corrupted_records(self):
        db = database()
        db.table = 'data25timestamp'
        with self.assertLogs(level=logging.WARNING):
            _, n_err, _, _ = from_postgreSQL(db)
        self.assertEqual(n_err, 1)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_dict_type_of_last_unique_items(self):
        pass

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_correct_values_in_last_unique_items(self):
        db = database()
        db.table = 'data25timestamp'
        with self.assertLogs(level=logging.WARNING):
            _, _, last_unique, _ = from_postgreSQL(db)
        self.assertIsInstance(last_unique, dict)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_list_type_of_transactions(self):
        db = database()
        db.table = 'data25timestamp'
        should_be = {'4' : {'AC016EL50CPHALID-1749': '2012-03-06T23:26:35'},
                     '12': {'SA848EL83DOYALID-2416': '2012-03-09T16:18:02',
                            'BL152EL82CRXALID-1817': '2012-03-09T16:18:02'},
                     '11': {'LE629EL54ANHALID-345': '2012-03-09T16:18:52'},
                     '10': {'OL756EL65HDYALID-4834': '2012-03-09T16:19:01'},
                     '7' : {'OL756EL55HAMALID-4744': '2012-03-09T16:20:14',
                            'AC016EL56BKHALID-943': '2012-03-09T16:20:14'}}
        with self.assertLogs(level=logging.WARNING):
            _, _, last_unique, _ = from_postgreSQL(db)
        self.assertDictEqual(last_unique, should_be)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_correct_values_transactions(self):
        db = database()
        db.table = 'data25timestamp'
        should_be = [('2012-03-06T23:26:35', '4', 'AC016EL50CPHALID-1749'),
                     ('2012-03-09T16:18:02', '12', 'SA848EL83DOYALID-2416'),
                     ('2012-03-09T16:18:02', '12', 'BL152EL82CRXALID-1817'),
                     ('2012-03-09T16:18:52', '11', 'LE629EL54ANHALID-345'),
                     ('2012-03-09T16:19:01', '10', 'OL756EL65HDYALID-4834'),
                     ('2012-03-09T16:20:14', '7', 'OL756EL55HAMALID-4744'),
                     ('2012-03-09T16:20:14', '7', 'OL756EL55HAMALID-4744'),
                     ('2012-03-09T16:20:14', '7', 'OL756EL55HAMALID-4744'),
                     ('2012-03-09T16:20:14', '7', 'OL756EL55HAMALID-4744'),
                     ('2012-03-09T16:20:14', '7', 'OL756EL55HAMALID-4744'),
                     ('2012-03-09T16:20:14', '7', 'OL756EL55HAMALID-4744'),
                     ('2012-03-09T16:20:14', '7', 'OL756EL55HAMALID-4744'),
                     ('2012-03-09T16:20:14', '7', 'OL756EL55HAMALID-4744'),
                     ('2012-03-09T16:20:14', '7', 'AC016EL56BKHALID-943'),
                     ('2012-03-09T16:20:14', '7', 'AC016EL56BKHALID-943'),
                     ('2012-03-09T16:20:14', '7', 'AC016EL56BKHALID-943'),
                     ('2012-03-09T16:20:14', '7', 'AC016EL56BKHALID-943'),
                     ('2012-03-09T16:20:14', '7', 'AC016EL56BKHALID-943'),
                     ('2012-03-09T16:20:14', '7', 'AC016EL56BKHALID-943'),
                     ('2012-03-09T16:20:14', '7', 'AC016EL56BKHALID-943'),
                     ('2012-03-09T16:20:14', '7', 'AC016EL56BKHALID-943')]
        with self.assertLogs(level=logging.WARNING):
            _, _, _, transactions = from_postgreSQL(db)
        self.assertListEqual(transactions, should_be)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_number_of_transactions_equals_length_transaction_list(self):
        with self.assertLogs(level=logging.WARNING):
            n_rec, _, _, transactions = from_postgreSQL(database())
        self.assertEqual(n_rec, len(transactions))


if __name__ == '__main__':
    ut.main()
