# -*- coding: utf-8 -*-

import logging as log


def write_log_to(file, log_level=30):
    '''Initialize the logging functionality of bestPy.

    Parameters
    ----------
    file : str
        Path to and name of the logfile to be written.

    log_level : int, optional
        Minimum level of events to log. Defaults to 30.
        Permitted values are 10 (DEBUG), 20 (INFO),
        30 (WARNING), 40 (ERROR), and 50 (CRITICAL).

    Examples
    --------
    >>> write_log_to('/path/to/my/logfile.txt', 20)

    '''
    check_string_type_of(file)
    check_numeric_type_and_range_of(log_level)
    color = '\033[33m[{0}]\033[0m: {1} (\033[34m{2}\033[0m|\033[32m{3}\033[0m)'
    log_entry_format = color.format('%(levelname)-8s',
                                    '%(message)s',
                                    '%(module)s',
                                    '%(funcName)s')
    log.basicConfig(filename=file,
                    filemode='w',
                    level=round(log_level, -1),
                    format=log_entry_format)


def check_string_type_of(file):
    if not isinstance(file, str):
        raise TypeError('Filename must be a string!')


def check_numeric_type_and_range_of(level):
    error_message = ('Logging level must be an integer between 10 (= DEBUG)'
                     ' and 50 (= CRITICAL)!')
    if not isinstance(level, int) or isinstance(level, float):
        raise TypeError(error_message)
    if (level < 6) or (level > 54):
        raise ValueError(error_message)
