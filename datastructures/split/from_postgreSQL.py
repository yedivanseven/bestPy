# -*- coding: utf-8 -*-

import logging as log
import datetime as dt
from collections import defaultdict
from psycopg2 import connect, OperationalError, ProgrammingError
from ..postgreSQLparams import PostgreSQLparams


def from_postgreSQL(database):
    check_type_of(database)
    number_of_transactions = 0
    number_of_corrupted_records = 0
    transactions = []
    last_unique_items_of = defaultdict(lambda:
                           defaultdict(lambda: dt.datetime(1, 1, 1)))

    query = '''SELECT %(timestamp)s, %(userid)s, %(articleid)s
               FROM %(table)s
               LIMIT %(limit)s'''

    def process_valid_transaction(record):
        timestamp, user, item = record
        time = converted(timestamp)
        if time > last_unique_items_of[user][item]:
            last_unique_items_of[user][item] = time
        transactions.append((time.isoformat(), user, item))
        return 1

    def log_corrupted_transaction(record):
        log.warning('Transaction record {0} from database is incomplete. '
                    'Skipping.'.format(number_of_transactions + 1))
        return 0

    process = {True : process_valid_transaction,
               False: log_corrupted_transaction}

    try:
        connection = connect(database.login)
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
            finalized(last_unique_items_of),
            transactions)


def check_type_of(database):
    if not isinstance(database, PostgreSQLparams):
        log.error('Attempt to set database parameter object of incompatible'
                  ' type. Must be <PostgreSQLparams>.')
        raise TypeError('Database parameter object must be of'
                        ' type <PostgreSQLparams>!')


def converted(timestamp):
    converted = {dt.datetime: lambda time: time,
                         int: lambda time: dt.datetime.fromtimestamp(time)}
    type_of = type(timestamp)
    if type_of not in converted.keys():
        log.error('Type of timestamp field is neither integer nor timestamp!')
        raise TypeError('Timestamp field must be an integer or a timestamp!')
    return converted[type_of](timestamp)


def finalized(last_unique):
    finalized = {user: {item: time.isoformat()
                        for item, time in article.items()}
                for user, article in last_unique.items()}
    return finalized
