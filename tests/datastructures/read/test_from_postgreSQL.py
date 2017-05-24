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


class TestReadFromPostgreSQL(ut.TestCase):

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
                   'WARNING:root:Requested 123 transactions from table head100'
                   ' but only 102 available. Fetched all 102.']
        with self.assertLogs(level=logging.WARNING) as log:
                _ = from_postgreSQL(db)
        self.assertEqual(log.output, log_msg)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_type_of_number_of_transactions(self):
        with self.assertLogs(level=logging.WARNING):
            n_rec, _, _, _, _ = from_postgreSQL(database())
        self.assertIsInstance(n_rec, int)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_correct_number_of_transactions(self):
        with self.assertLogs(level=logging.WARNING):
            n_rec, _, _, _, _ = from_postgreSQL(database())
        self.assertEqual(n_rec, 102)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_type_of_number_of_corrupted_records(self):
        with self.assertLogs(level=logging.WARNING):
            _, n_err, _, _, _ = from_postgreSQL(database())
        self.assertIsInstance(n_err, int)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_correct_number_of_corrupted_records(self):
        with self.assertLogs(level=logging.WARNING):
            _, n_err, _, _, _ = from_postgreSQL(database())
        self.assertEqual(n_err, 4)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_type_of_user_index(self):
        with self.assertLogs(level=logging.WARNING):
            _, _, user_i, _, _ = from_postgreSQL(database())
        self.assertIsInstance(user_i, dict)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_correct_values_in_user_index(self):
        should_be = {'11': 0, '27': 1, '29': 2, '17': 3, '1': 4, '19': 5,
                     'test0': 6, '21': 7, '10': 8, '7': 9, '30': 10, '12': 11,
                     '5': 12, '23': 13, '14': 14, '25': 15, '28': 16, '16': 17,
                     'test': 18, '32': 19, '26': 20, '13': 21, '31': 22,
                     '4': 23}
        with self.assertLogs(level=logging.WARNING):
            _, _, user_i, _, _ = from_postgreSQL(database())
        self.assertDictEqual(user_i, should_be)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_type_of_item_index(self):
        with self.assertLogs(level=logging.WARNING):
            _, _, _, item_j, _ = from_postgreSQL(database())
        self.assertIsInstance(item_j, dict)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_correct_values_in_item_index(self):
        should_be = {'LE629EL54ANHALID-345': 0, 'SA851EL90ATPALID-509': 1,
                     'NO749EL20DJRALID-2279': 2, 'SA848EL83DOYALID-2416': 3,
                     'AC016EL81LHA-7618': 4, 'WI981EL52EFNALID-2847': 5,
                     'AC016EL58BKFALID-941': 6, 'test0article': 7,
                     'AP082EL37CPUALID-1762': 8, 'MO717EL47ARKALID-452': 9,
                     'PH789EL03ATCALID-496': 10, 'AP082EL13BLYALID-986': 11,
                     'GE362EL02DCRALID-2097': 12, 'BL152EL82CRXALID-1817': 13,
                     'OL756EL65HDYALID-4834': 14, 'AD029EL42BKVALID-957': 15,
                     'DO274EL91APSALID-408': 16, 'AC016EL67BJWALID-932': 17,
                     'AP082EL01CFQALID-1498': 18, 'LE627EL19DFWALID-2180': 19,
                     'AS100EL41BOSALID-1058': 20, 'AP082EL03BMIALID-996': 21,
                     'SA848EL62IBDALID-5437': 22, 'VI962EL59EFGALID-2840': 23,
                     'testarticle': 24, 'SO888EL82CKFALID-1617': 25,
                     'CA189EL29AGOALID-170': 26, 'VI962EL69EEWALID-2830': 27,
                     'VI962EL62EFDALID-2837': 28, 'MO717EL52ARFALID-447': 29,
                     'CO228EL88FBFALID-3411': 30, 'PI794EL32ENZALID-3067': 31,
                     'OL756EL55HAMALID-4744': 32, 'AC016EL56BKHALID-943': 33,
                     'AC016EL50CPHALID-1749': 34}
        with self.assertLogs(level=logging.WARNING):
            _, _, _, item_j, _ = from_postgreSQL(database())
        self.assertDictEqual(item_j, should_be)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_type_of_user_item_counts(self):
        with self.assertLogs(level=logging.WARNING):
            _, _, _, _, counts = from_postgreSQL(database())
        self.assertIsInstance(counts, dict)

    @ut.skipIf(no_connection_to(database()),
              'Could not establish connection to test database.')
    def test_correct_values_in_user_item_counts(self):
        should_be = {(0, 0): 1, (1, 1): 1, (2, 2): 2, (3, 3): 1, (4, 4): 3,
                     (1, 5): 1, (5, 6): 1, (6, 7): 1, (7, 8): 1, (8, 9): 1,
                     (1, 10): 1, (9, 11): 1, (10, 4): 4, (11, 3): 1,
                     (12, 11): 1, (0, 3): 1, (1, 12): 1, (13, 13): 1,
                     (9, 14): 2, (1, 13): 3, (14, 2): 1, (5, 15): 1,
                     (1, 16): 1, (4, 2): 1, (9, 5): 1, (12, 13): 1, (4, 17): 1,
                     (5, 18): 1, (1, 18): 1, (15, 19): 1, (16, 8): 1,
                     (12, 3): 1, (5, 16): 1, (9, 6): 2, (9, 20): 1, (12, 8): 2,
                     (1, 3): 2, (9, 21): 1, (13, 3): 2, (1, 22): 1,
                     (17, 23): 1, (18, 24): 1, (0, 13): 1, (1, 25): 2,
                     (11, 13): 1, (3, 26): 1, (1, 27): 1, (1, 28): 1,
                     (3, 29): 1, (19, 25): 1, (20, 30): 2, (1, 30): 1,
                     (21, 31): 1, (9, 32): 10, (22, 15): 1, (0, 26): 1,
                     (4, 8): 2, (14, 3): 1, (8, 14): 1, (3, 13): 1,
                     (11, 26): 1, (9, 33): 10, (4, 3): 1, (14, 8): 1,
                     (1, 20): 1, (4, 13): 1, (12, 2): 1, (23, 34): 1}
        with self.assertLogs(level=logging.WARNING):
            _, _, _, _, counts = from_postgreSQL(database())
        self.assertDictEqual(counts, should_be)


if __name__ == '__main__':
    ut.main()
