#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log
from collections import defaultdict
import psycopg2 as pg
from psycopg2 import OperationalError, ProgrammingError


def from_postgreSQL(database):
    number_of_transactions = 0
    number_of_corrupted_records = 0
    last_unique_items_of = defaultdict(lambda: defaultdict(int))
    transactions = []

    query = '''SELECT %(timestamp)s, %(userid)s, %(articleid)s
               FROM %(table)s
               LIMIT %(limit)s'''

    def process_valid_transaction(record):
        timestamp, user, item = record
        if timestamp > last_unique_items_of[user][item]:
            last_unique_items_of[user][item] = timestamp
        transactions.append((str(timestamp), user, item))
        return 1

    def log_corrupted_transaction(record):
        log.warning('Transaction record {0} from database is incomplete. '
                    'Skipping.'.format(number_of_transactions + 1))
        return 0

    process = {True : process_valid_transaction,
               False: log_corrupted_transaction}

    try:
        connection = pg.connect(database.login)
    except OperationalError:
        log.error('Failed connecting to {}.'.format(database.login_db_name))
        raise OperationalError('Connect to database failed. Check settings!')

    with connection.cursor() as cursor:
        try:
            cursor.execute(query, database._params)
        except ProgrammingError:
            log.error('Failed to execute SQL query. Check your parameters!')
            raise ProgrammingError('SQL query failed. Check your parameters!')
        else:
            for record in cursor:
                complete = all(record)
                success = process[complete](record)
                number_of_transactions += success
                number_of_corrupted_records += 1 - success
        finally:
            connection.close()

    return (number_of_transactions,
            number_of_corrupted_records,
            dict(last_unique_items_of),
            transactions)
