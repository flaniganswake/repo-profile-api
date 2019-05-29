""" Utility functions for the API
    flaniganswake@protonmail.com """
import logging


def init_logging(_app: 'app', logfile: str)-> 'logger':
    ''' initialize logging '''
    _logger = logging.getLogger(_app)
    _logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    _logger.addHandler(fh)
    _logger.addHandler(ch)
    return _logger
