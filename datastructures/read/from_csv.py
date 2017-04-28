#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging as log
from collections import defaultdict


def from_csv(file, seperator=';'):
    number_of_transactions = 0
    number_of_corrupted_records = 0
    userIndex_of = defaultdict(lambda: len(userIndex_of))
    itemIndex_of = defaultdict(lambda: len(itemIndex_of))
    count_buys_of = defaultdict(int)

    def process_valid_transaction():
        count_buys_of[(userIndex_of[user], itemIndex_of[item])] += 1
        return 1

    def log_corrupted_transaction():
        line = number_of_transactions + number_of_corrupted_records + 1
        log.warning('Transaction on line {0} contains empty fields. '
                    'Skipping.'.format(line))
        return 0

    check_for = {True : process_valid_transaction,
                 False: log_corrupted_transaction}

    stream = open(file) if isinstance(file, str) else file
    with stream:
        for transaction in stream:
            try:
                _, user, item = transaction.rstrip().split(seperator)
            except ValueError:
                number_of_corrupted_records += 1
                line = number_of_transactions + number_of_corrupted_records
                log.warning('Could not interpret transaction on line {0}. '
                            'Skipping.'.format(line))
            else:
                completeness = all((user, item))
                success = check_for[completeness]()
                number_of_transactions += success
                number_of_corrupted_records += 1 - success

    return (number_of_transactions,
            number_of_corrupted_records,
            dict(userIndex_of),
            dict(itemIndex_of),
            dict(count_buys_of))
