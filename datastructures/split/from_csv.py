#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log
import datetime as dt
from collections import defaultdict


def from_csv(file, seperator=';', fmt=None):
    number_of_transactions = 0
    number_of_corrupted_records = 0
    transactions = []
    last_unique_items_of = defaultdict(lambda:
                           defaultdict(lambda: dt.datetime(1, 1, 1)))

    with open(file) as stream:
        for transaction in stream:
            try:
                timestamp, user, item = transaction.rstrip().split(seperator)
            except ValueError:
                log.warning('Could not interpret transaction on line {0}. '
                            'Skipping.'.format(number_of_transactions + 1))
                number_of_corrupted_records += 1
            else:
                number_of_transactions += 1
                time = formatted_with(fmt)(timestamp)
                if time > last_unique_items_of[user][item]:
                    last_unique_items_of[user][item] = time
                transactions.append((time.isoformat(), user, item))

    return (number_of_transactions,
            number_of_corrupted_records,
            dict(last_unique_items_of),
            transactions)


def formatted_with(fmt=None):
    def fromstring(timestamp):
        return dt.datetime.strptime(timestamp, fmt)
    def fromstamp(timestamp):
        return dt.datetime.fromtimestamp(int(timestamp))
    return fromstring if fmt else fromstamp
