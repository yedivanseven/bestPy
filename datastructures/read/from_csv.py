#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from collections import defaultdict

def from_csv(file):
    number_of_transactions = 0
    number_of_corrupted_entries = 0
    userIndex_of = defaultdict(lambda: len(userIndex_of))
    itemIndex_of = defaultdict(lambda: len(itemIndex_of))
    count_buys_of = defaultdict(int)

    with open(file) as stream:
        for transaction in stream:
            try:
                _, user, item = transaction.rstrip().split(sep=";")
            except ValueError:
                logging.warning('Could not interpret transaction on line {0}. '
                                'Skipping.'.format(number_of_transactions + 1))
                number_of_corrupted_entries += 1
            else:
                number_of_transactions += 1
                count_buys_of[(userIndex_of[user], itemIndex_of[item])] += 1

    return (number_of_transactions,
            number_of_corrupted_entries,
            dict(userIndex_of),
            dict(itemIndex_of),
            dict(count_buys_of))
