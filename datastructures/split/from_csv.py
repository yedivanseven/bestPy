#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log
import datetime as dt
from collections import defaultdict


def from_csv(file, seperator=';', fmt=None):
    format_of = fmt
    number_of_transactions = 0
    number_of_corrupted_records = 0
    transactions = []
    last_unique_items_of = defaultdict(lambda:
                           defaultdict(lambda: dt.datetime(1, 1, 1)))

    def process_transaction_time():
        try:
            time = depending_on(format_of)(timestamp)
        except (ValueError, OverflowError):
            line = number_of_transactions + number_of_corrupted_records + 1
            log.warning('Could not interpret timestamp on line {0}. '
                        'Skipping.'.format(line))
            return 0
        if time > last_unique_items_of[user][item]:
            last_unique_items_of[user][item] = time
        transactions.append((time.isoformat(), user, item))
        return 1

    def log_corrupted_transaction():
        line = number_of_transactions + number_of_corrupted_records + 1
        log.warning('Transaction on line {0} contains empty fields. '
                    'Skipping.'.format(line))
        return 0

    process = {True : process_transaction_time,
               False: log_corrupted_transaction}

    with open(file) as stream:
        for transaction in stream:
            try:
                timestamp, user, item = transaction.rstrip().split(seperator)
            except ValueError:
                number_of_corrupted_records += 1
                line = number_of_transactions + number_of_corrupted_records
                log.warning('Could not interpret transaction on line {0}. '
                            'Skipping.'.format(line))
            else:
                complete_record = all((timestamp, user, item))
                success = process[complete_record]()
                number_of_transactions += success
                number_of_corrupted_records += 1 - success

    return (number_of_transactions,
            number_of_corrupted_records,
            dict(last_unique_items_of),
            transactions)


def depending_on(fmt=None):

    def fromstring(timestamp):
        try:
            time = dt.datetime.strptime(timestamp, fmt)
        except ValueError:
            log.warning('Failed to read timestamp. Check that it adheres to '
                        'the given format "{0}".'.format(fmt))
            raise ValueError
        return time

    def fromstamp(timestamp):
        try:
            time = int(timestamp)
        except ValueError:
            log.warning('Failed to convert UNIX epoch timestamp to integer.')
            raise ValueError
        try:
            converted = dt.datetime.fromtimestamp(time)
        except OverflowError:
            log.warning('Integer is not a valid UNIX epoch timestamp.')
            raise OverflowError
        return converted

    return fromstring if fmt else fromstamp
