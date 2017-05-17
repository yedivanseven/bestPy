# -*- coding: utf-8 -*-

import logging as log
from collections import defaultdict
from psycopg2 import connect, OperationalError, ProgrammingError


def from_postgreSQL(database):
    number_of_transactions = 0
    number_of_corrupted_records = 0
    userIndex_of = defaultdict(lambda: len(userIndex_of))
    itemIndex_of = defaultdict(lambda: len(itemIndex_of))
    count_buys_of = defaultdict(int)

    query = '''SELECT %(userid)s, %(articleid)s, COUNT(*) as count
               FROM (SELECT %(userid)s, %(articleid)s
                     FROM %(table)s
                     LIMIT %(limit)s) AS head
               GROUP BY %(userid)s, %(articleid)s'''

    def process_valid_transaction(record):
        user, item, count = record
        count_buys_of[(userIndex_of[user], itemIndex_of[item])] = count
        return 0

    def log_corrupted_transaction(record):
        log.warning('Incomplete record returned from database. Skipping.')
        return 1

    problems_with = {True : process_valid_transaction,
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
                number_of_corrupted_records += problems_with[complete](record)
        finally:
            connection.close()

    number_of_transactions = sum(count_buys_of.values())
    compare(number_of_transactions, database)

    return (number_of_transactions,
            number_of_corrupted_records,
            dict(userIndex_of),
            dict(itemIndex_of),
            dict(count_buys_of))


def compare(available, database):
    if available < database._requested:
        log.warning('Requested {0} transactions from table {1} but only {2} '
                    'available. Fetched all {2}.'.format(database.limit,
                                                         database.table,
                                                         available))
        log.info('Resetting limit to the maximum of {}.'.format(available))
        database.limit = available
