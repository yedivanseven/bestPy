#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log
from collections import defaultdict


def from_csv(file, seperator=';'):
    number_of_transactions = 0
    number_of_corrupted_records = 0
    last_unique_items_of = defaultdict(lambda: defaultdict(int))
    transactions = []

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
                time = int(timestamp)
                if time > last_unique_items_of[user][item]:
                    last_unique_items_of[user][item] = time
                transactions.append((timestamp, user, item))

    return (number_of_transactions,
            number_of_corrupted_records,
            dict(last_unique_items_of),
            transactions)
