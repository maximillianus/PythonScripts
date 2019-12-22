import unittest

import logging

from pylogger import Logger

class Test(unittest.TestCase):

    def test_stream(self):
        pylogger = Logger(name='test_stream_logger', level=logging.DEBUG, stdout=True)
        pylogger.debug('This is DEBUG test')
        pylogger.info('This is INFO test')
        pylogger.warning('This is WARNING test')
        pylogger.error('This is ERROR test')
        pylogger.critical('This is CRITICAL test')
    
    def test_file(self):
        pylogger = Logger(name='test_file_logger', level=logging.DEBUG, stdout=False, file=True)
        pylogger.debug('This is DEBUG test')
        pylogger.info('This is INFO test')
        pylogger.warning('This is WARNING test')
        pylogger.error('This is ERROR test')
        pylogger.critical('This is CRITICAL test')
    
    def test_rotating_file(self):
        pylogger = Logger(name='test_rotating_file_logger', level=logging.DEBUG, stdout=False, rotating_file=True)
        pylogger.debug('This is DEBUG test')
        pylogger.info('This is INFO test')
        pylogger.warning('This is WARNING test')
        pylogger.error('This is ERROR test')
        pylogger.critical('This is CRITICAL test')

    def test_timed_rotating_file(self):
        pylogger = Logger(name='test_timed_rotating_file_logger', level=logging.DEBUG, stdout=False, timed_rotating_file=True)
        pylogger.debug('This is DEBUG test')
        pylogger.info('This is INFO test')
        pylogger.warning('This is WARNING test')
        pylogger.error('This is ERROR test')
        pylogger.critical('This is CRITICAL test')


if __name__ == "__main__":
    unittest.main()