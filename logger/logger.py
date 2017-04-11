#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging


def write_log_to(file):
    color = '\033[33m[{0}]\033[34m{1}\033[0m|\033[32m{2}\033[0m: {3}'
    log_entry_format = color.format('%(levelname)-8s',
                                    '%(module)-11s',
                                    '%(funcName)-12s',
                                    '%(message)s')
    logging.basicConfig(filename=file,
                        filemode='w',
                        level=logging.INFO,
                        format=log_entry_format)
