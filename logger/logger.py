#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging


def write_log_to(file, log_level=30):
    color = '\033[33m[{0}]\033[34m{1}\033[0m|\033[32m{2}\033[0m: {3}'
    log_entry_format = color.format('%(levelname)-8s',
                                    '%(module)-15s',
                                    '%(funcName)-15s',
                                    '%(message)s')
    logging.basicConfig(filename=file,
                        filemode='w',
                        level=log_level,
                        format=log_entry_format)
